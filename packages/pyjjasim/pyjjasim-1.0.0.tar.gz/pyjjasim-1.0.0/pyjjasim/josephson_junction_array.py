from __future__ import annotations
import numpy as np
import scipy
import scipy.sparse
import scipy.sparse.linalg
from scipy.sparse import coo_matrix
import scipy.spatial

__all__ = ["Array", "Solver", "SquareArray", "HoneycombArray", "TriangularArray"]

# requirements
# - fix single compoent and non-planar check error
# - add nodes/junctions makes no sense...
# - check/debug all physical quantities
# - dynamic compute broadcasting slicing
# - documentation
# - unit testing
# - publish


# nice to haves
# - optimize IpJ and IpJL time dependence
# - lattices
# - periodic lattices
# - 3D
# - voltage bias
# - bare resistors, capacitors and inductors?
# - GPU
#   * Multigrid
#   * single/double precision
#   * phase build-up rounding correction

class NotSingleComponentError(Exception):
    pass

class NotPlanarError(Exception):
    pass

class Array:
    """Construct a Josephson Junction Array (JJA). A JJA is an electric circuit that can include
    Josephson junctions, passive components, current sources and batteries. The network is required
    to be planar and single component.

    Defined with nodes and junctions, where the junctions represent three elements in series: a battery,
    an inductor (optionally coupled to other junctions) and the third element is a resistor, capacitor
    and josephson junction in parallel. To omit a component; set it's value to zero.

    A last requirement is that if any inductor is present; all junctions must include an inductor.

    Parameters
    ----------
    x, y:                               Node coordinates                        float (Nn,) arrays
    node1, node2:                       Junction nodes                          int (Nj,) arrays
    min_distance=1E-10:                 minimum node distance                   float
    external_current_basis=None:        proportion of external current          float (Nn,) array
                                        injected per node (+ sign means in)     or None
    critical_current_factors=1:         critical current factors of junctions   float (Nj,) array
                                                                                or scalar
    resistance_factors=1:               resistance factors of junctions         positive float (Nj,) array
                                                                                or scalar
    capacitance_factors=1:              capacitance factors of junctions        positive float (Nj,) array
                                                                                or scalar
    beta_C=0:                           beta_C parameter                        positive float
    beta_L=0:                           beta_L parameter                        positive float
    ignore_current_conservation=False:  no error if external_current_basis      bool
                                        does not add up to zero
    matrix_format="csc":                Format of sparse problem matrices       "csr" or "csc"

    Returns
    -------
    array: Array object with methods:
     - CONSTRUCTION METHODS:
         * add_nodes(x, y, current_base=None)
         * remove_nodes(nodes_to_remove)
         * add_junctions(node1, node2, critical_current_factors=1, resistance_factors=1, capacitance_factors=1)
         * remove_junctions(junctions_to_remove)
     - NODE METHODS:
         * get_node_coordinates()
         * node_count(), Nn()
         * get_external_current_basis()
         * set_external_current_basis(basis)
     - JUNCTION METHODS:
         * junction_count(), Nj()
         * get_external_current_basis()
         * set_external_current_basis(Ibase)
         * get_junction(node1, node2, check_if_exists=True, return_is_aligned=True)
         * get_critical_current_factors(), Ic()
         * get_resistance_factors(), R()
         * get_capacitance_factors()
         * C()
         * set_critical_current_factors(Ic)
         * set_resistance_factors(R)
         * set_capacitance_factors(C)
     - FACE METHODS:
         * face_count, Np
         * get_faces
         * get_face_common_junction(path1, path2, check_if_exists=True, return_sign=True):
         * locate_faces(x, y)
         * get_face_areas, areas
         * get_face_centroids, centroids
     - ARRAY METHODS:
         * approximate_inductance(junc_L=1, junc_M=0, max_dist=0)
         * get_junction_inductance_matrix, L
         * set_junction_inductance_matrix(junction_inductance_matrix)
         * get_beta_C
         * get_beta_L
         * set_beta_C(beta_C)
         * set_beta_L(beta_L)
         * has_capacitance
         * has_inductance
         * get_cut_matrix(omit_last_node=False)
         * get_cycle_matrix(omit_last_node=False)
     - VISUALIZE METHODS:
         * plot(show_nodes=True, show_node_ids=True, node_labels=None, show_junctions=True,
                show_junction_directions=True, show_junction_ids=True, junction_labels=None,
                show_paths=True, show_path_directions=True, show_path_ids=True, path_labels=None, figsize=None)

    Notes
    -----
    * Coordinates are assumed normalized with some scale factor a0. Similarly, Resistance with R0, capacitance
      with C0 and all currents with I0 (fluxes are "naturally" normalized with the flux quantum Phi0,
      inductances with mu0 * a0, and voltages with I0 * R0). The set a0, R0, C0, I0 can be chosen freely
      to match the desired real-world situation.
    * Arrays can be constructed using the add/remove_nodes/junctions methods, but every time it is called,
      a new array is created and all faces and matrices are re-computed. This means adding nodes one-by-one
      will be very slow. It is faster to add multiple nodes in one function call.

    """

    def __init__(self, x, y, node1, node2, min_distance=1E-10, external_current_basis=None,
                 critical_current_factors=1, resistance_factors=1, capacitance_factors=1,
                 beta_C=0, beta_L=0, ignore_current_conservation=False, matrix_format="csc"):
        self.matrix_format = matrix_format
        self.x = np.array(x, dtype=np.double).flatten()
        self.y = np.array(y, dtype=np.double).flatten()
        if len(self.x) != len(self.y):
            raise ValueError("x and y must be same length")
        if self.node_count() > 2 ** 31:
            raise ValueError("max node count exceeded")
        self.current_base = None
        self.nodes_permute = None
        self.ignore_current_conservation = ignore_current_conservation
        self.set_external_current_basis(external_current_basis)
        self.min_distance = min_distance
        self.nodes_tree = scipy.spatial.KDTree(np.stack((self.x, self.y), axis=1))
        if len(self.nodes_tree.query_pairs(self.min_distance)) > 0:
            raise ValueError("Duplicate points (two distinct points cannot be closer than min_distance)")
        self.cut_reduced_square = None
        self.cut_matrix_reduced = None
        self.cut_matrix = None
        self.cut_square = None
        self.cut_matrix_reduced_transposed = None
        self.cut_matrix_transposed = None
        self.node1 = np.array(node1, dtype=int).flatten()
        self.node2 = np.array(node2, dtype=int).flatten()
        if len(self.node1) != len(self.node2):
            raise ValueError("node1 and node2 must be of equal length")
        if np.any((self.node1 < 0) | (self.node2 < 0) |(self.node1 >= self.node_count()) |(self.node1 >= self.node_count())):
            raise ValueError("junctions refer to non-existing nodes.")
        self.resistance_factors = None
        self.capacitance_factors = None
        self.critical_current_factors=None
        self.set_resistance_factors(resistance_factors)
        self.set_critical_current_factors(critical_current_factors)
        self.set_capacitance_factors(capacitance_factors)
        self.junc_hash = None
        self.hash_idx = None
        self._set_junction_hash()
        self._permute_nodes_lexsort()
        self._assign_cut_matrix()
        if not self._single_connected_component_check():
            raise NotSingleComponentError("Array is not a single component.")
        self.path_nodes, self.outer_paths, self.areas, self.centroid_x, self.centroid_y = \
            Array._construct_faces(self.x, self.y, self.node1, self.node2)
        self.path_lengths = np.array([len(n) for n in self.path_nodes], dtype=int)
        self.reorder_ids = self._reorder_paths()
        self.path1, self.path2, self.path1_sign, self.path_hash, self.path_hash_idx = self._assign_path_map()
        self.locator = None
        self.faces_permute = None
        self.cycle_matrix = self._get_cycle_matrix(matrix_format)
        self.cycle_matrix_transposed = None
        self.cycle_square = None
        if not self._circuit_rank_test():
            raise ValueError("Circuit rank criteria is not met. ")
        if not self._is_orthogonal_check():
            raise ValueError("Cut space and cycle space are not orthogonal.")
        self.current_base_J = None
        self.current_base_total = None
        self.beta_C = beta_C
        self.beta_L = beta_L
        self.junction_inductance_matrix = None
        self.inductance_is_diagonal = True
        self.approximate_inductance(1, 0, 0)
        self.solver = Solver(self)

    def add_nodes(self, x, y, current_base=None):
        """ Add nodes to array.

        """
        x = np.array(x, dtype=np.double).flatten()
        if current_base is None:
            current_base = np.zeros(len(x), dtype=np.double)
        else:
            current_base = np.array(current_base, dtype=np.double).flatten()
        new_x = np.append(self.x, x)
        new_y = np.append(self.y, np.array(y, dtype=np.double).flatten())
        new_current_basis = np.append(self.current_base, current_base)
        return Array(new_x, new_y, self.node1, self.node2, min_distance=self.min_distance,
                     external_current_basis=new_current_basis,
                     critical_current_factors=self.critical_current_factors,
                     resistance_factors=self.resistance_factors,
                     capacitance_factors=self.capacitance_factors,
                     beta_C=self.beta_C, beta_L=self.beta_L,
                     ignore_current_conservation=self.ignore_current_conservation,
                     matrix_format=self.matrix_format)

    def remove_nodes(self, nodes_to_remove):
        """ Remove nodes from array.
        in:  nodes_to_remove    int array in range(node_count)  or  (Nn,) mask
        out: new_array          Array
        """
        nodes_to_remove = np.array(nodes_to_remove).flatten()
        if not isinstance(nodes_to_remove.dtype, (bool, np.bool)):
            try:
                node_remove_mask = np.zeros(self.node_count(), dtype=bool)
                node_remove_mask[nodes_to_remove] = True
            except:
                raise ValueError("Invalid store_time_steps; must be None, mask, slice or index array")
        else:
            node_remove_mask = nodes_to_remove
        new_x = self.x[~node_remove_mask]
        new_y = self.y[~node_remove_mask]
        new_current_basis = self.current_base[~node_remove_mask]
        junc_remove_mask, new_node_id = self._junction_remove_mask(self.node1, self.node2, node_remove_mask)
        new_node1 = new_node_id[self.node1][~junc_remove_mask]
        new_node2 = new_node_id[self.node2][~junc_remove_mask]
        new_Ic = self.critical_current_factors if self.critical_current_factors.size == 1 \
            else self.critical_current_factors[~junc_remove_mask]
        new_R = self.resistance_factors if self.resistance_factors.size == 1 \
            else self.resistance_factors[~junc_remove_mask]
        new_C = self.capacitance_factors if self.capacitance_factors.size == 1 \
            else self.capacitance_factors[~junc_remove_mask]
        return Array(new_x, new_y, new_node1, new_node2, min_distance=self.min_distance,
                     external_current_basis=new_current_basis, critical_current_factors=new_Ic,
                     resistance_factors=new_R, capacitance_factors=new_C,
                     beta_C=self.beta_C, beta_L=self.beta_L,
                     ignore_current_conservation=self.ignore_current_conservation,
                     matrix_format=self.matrix_format)

    def add_junctions(self, node1, node2, critical_current_factors=1.0,
                      resistance_factors=1.0, capacitance_factors=1.0):
        """ Add junctions to array.
        in:  node1, node2                         int arrays in range(node_count)
             critical_current_factors=1.0:        float (Nj_new,) array  or  scalar
             resistance_factors=1.0:              positive float (Nj_new,) array  or  scalar
             capacitance_factors=1.0:             positive float (Nj_new,) array  or  scalar
        out: new_array                            Array
        """
        new_node1 = np.append(self.node1, np.array(node1, dtype=int).flatten())
        new_node2 = np.append(self.node2, np.array(node2, dtype=int).flatten())
        N1, N2 = self.junction_count(), len(new_node1)
        new_Ic = self._append_quantities(self.critical_current_factors, critical_current_factors, N1, N2)
        new_R = self._append_quantities(self.resistance_factors, resistance_factors, N1, N2)
        new_C = self._append_quantities(self.capacitance_factors, capacitance_factors, N1, N2)
        return Array(self.x, self.y, new_node1, new_node2, min_distance=self.min_distance,
                     external_current_basis=self.current_base, critical_current_factors=new_Ic,
                     resistance_factors=new_R, capacitance_factors=new_C,
                     beta_C=self.beta_C, beta_L=self.beta_L,
                     ignore_current_conservation=self.ignore_current_conservation,
                     matrix_format=self.matrix_format)

    def remove_junctions(self, junctions_to_remove):
        """ Remove junctions from array.
        in:  junctions_to_remove    int array in range(junction_count)  or  (Nj,) mask
        out: new_array              Array
        """
        if not isinstance(junctions_to_remove.dtype, (bool, np.bool)):
            try:
                junction_mask = np.zeros(self.junction_count(), dtype=bool)
                junction_mask[junctions_to_remove] = True
            except:
                raise ValueError("Invalid store_time_steps; must be None, mask, slice or index array")
        else:
            junction_mask = junctions_to_remove
        new_node1 = self.node1[~junction_mask]
        new_node2 = self.node2[~junction_mask]
        new_Ic = self.critical_current_factors[~junction_mask]
        new_R = self.resistance_factors[~junction_mask]
        new_C = self.capacitance_factors[~junction_mask]
        return Array(self.x, self.y, new_node1, new_node2, min_distance=self.min_distance,
                     external_current_basis=self.current_base, critical_current_factors=new_Ic,
                     resistance_factors=new_R, capacitance_factors=new_C,
                     beta_C=self.beta_C, beta_L=self.beta_L,
                     ignore_current_conservation=self.ignore_current_conservation,
                     matrix_format=self.matrix_format)

    def get_node_coordinates(self):
        """ Get node coordinates x and y
        out: x      (Nn,) float array
             y      (Nn,) float array
        """
        return self.x, self.y

    def node_count(self):
        return self.Nn()

    def Nnr(self):
        # reduced node count; returns node_count - 1
        return self.Nn() - 1

    def get_external_current_basis(self):
        # return the "external current basis", which is an instruction in which nodes external
        # current has to be injected and ejected and in what proportion.
        # out:  external_current_basis      (node_count,) float array which sums to 0.0
        return self.current_base

    def set_external_current_basis(self, Ibase):
        # Sets the "external current basis", which is an instruction in which nodes external
        # current has to be injected and ejected and in what proportion.
        # in:  external_current_basis       (node_count,) float array which sums to 0.0
        # out: self
        if Ibase is None:
            self.current_base = np.zeros(self.node_count(), dtype=np.double)
        else:
            self.current_base = np.array(Ibase, dtype=np.double).flatten()
        if len(self.current_base) != self.node_count():
            raise ValueError("current base must be of array of length Nn (or None)")
        if not self.ignore_current_conservation:
            if np.abs(np.mean(self.current_base)) > 1E-10:
                raise ValueError("current base entries must add up to 0 (conservation of current)")
        if self.nodes_permute is not None:
            self.current_base_reordered = self.current_base[self.nodes_permute]
        self.current_base_J = None
        self.current_base_total = None
        return self

    def get_junction(self, node1, node2, check_if_exists=True, return_is_aligned=True):
        """ Checks if node junctions (node1[i], node2[i]) exist in array, and returns the corresponding
            junction_ids.
        in:  node1, node2               int arrays in range(node_count)
             check_if_exists=True       raise error if junction (node1[i], node2[i]) is not in array
             return_is_aligned=True     if True, is_aligned is also returned.
        out: junction_ids               int array in range(junction_count) or -1
             is_aligned
        Notes:
          * Optionally also return if the queried junctions are "aligned" with corresponding
            junctions in array, meaning node1,2 corresponds to self.node1,2 respectively, and not reversed.
          * For queries that do not exist; either an error is raised is check_if_exists=True, otherwise
            junction_ids is -1 for non-existing queries.
        """
        node1, node2 = np.array(node1, dtype=int), np.array(node2, dtype=int)
        nmin, nmax = np.minimum(node1, node2).astype(np.int64), np.maximum(node1, node2).astype(np.int64)
        Nn_p = np.array(self.node_count(), dtype=np.int64)
        junction_ids = self.hash_idx[np.searchsorted(self.junc_hash, nmin + nmax * Nn_p)]
        if check_if_exists:
            Array._assert_junction_id_exists(junction_ids, self.node1, self.node2, node1, node2)
        if return_is_aligned:
            return junction_ids, node1 == self.node1[junction_ids]
        else:
            return junction_ids

    def get_critical_current_factors(self):
        # out: (junction_count,) float array of scalar
        return self.Ic()

    def get_resistance_factors(self):
        # out: (junction_count,) positive float array of scalar
        return self.R()

    def get_capacitance_factors(self):
        # out: (junction_count,) positive float array of scalar
        return self.C()

    def set_critical_current_factors(self, Ic):
        # in: (junction_count,) positive float array of scalar
        self.critical_current_factors = self._prepare_junction_quantity(
            Ic, self.junction_count(), x_name="Ic", criterion=lambda s: s<=0,
            crit_error=" must be positive")
        return self

    def set_resistance_factors(self, R):
        # in: (junction_count,) positive float array of scalar
        self.resistance_factors = self._prepare_junction_quantity(
            R, self.junction_count(), x_name="R", criterion=lambda s: s <= 0,
            crit_error=" must be positive")
        return self

    def set_capacitance_factors(self, C):
        # in: (junction_count,) positive float array of scalar
        self.capacitance_factors = self._prepare_junction_quantity(
            C, self.junction_count(), x_name="C", criterion=lambda s: s < 0,
            crit_error=" must be positive or 0")
        return self

    def C(self) -> np.ndarray:
        # returns self.get_beta_C() * self.get_capacitance_factors()
        return self.beta_C * self.capacitance_factors

    def junction_count(self):
        return self.Nj()

    def face_count(self):
        return self.Np()

    def get_faces(self):
        # Returns a list of faces. Each face is a 1d array containing node_ids.
        return np.array([p for stacked_p in self.path_nodes for p in stacked_p.T if len(p) > 0], dtype=object)[self.reorder_ids].tolist()

    def get_face_areas(self):
        # Returns unsigned area of each face in array.
        # out: areas            (face_count,) positive float array
        return self.areas

    def get_face_centroids(self):
        # Returns centroid face_x, face_y of each face in array.
        # out: face_x, face_y   (face_count,) float array
        return self.centroids()

    def get_face_common_junction(self, face1, face2, check_if_exists=True, return_sign=True):
        """ Get the common junction of a pair of faces, if it exists.
        in:  face1, face2               int arrays in range(face_count)
             check_if_exists=True       raise error if junction (face1[i], face2[i]) is not in array
             return_is_aligned=True     if True, is_aligned is also returned.
        out: junction_ids               int array in range(junction_count) or -1
             is_aligned
        Notes:
          * Optionally also return if the queried junctions are "aligned" with corresponding
            junctions in array, meaning face1,2 corresponds to self.face1,2 respectively, and not reversed.
          * For queries that do not exist; either an error is raised is check_if_exists=True, otherwise
            junction_ids is -1 for non-existing queries.
        """
        face1, face2 = np.array(face1, dtype=int), np.array(face2, dtype=int)
        pmin, pmax = np.minimum(face1, face2).astype(np.int64), np.maximum(face1, face2).astype(np.int64)
        phash = pmax + pmin * np.array(self.face_count(), dtype=np.int64)
        idx = self.path_hash_idx[np.searchsorted(self.path_hash, phash)]
        if check_if_exists:
            Array._assert_junction_id_exists(idx, self.path1, self.path2, face1, face2)
        if return_sign:
            return idx, (-1 + 2 * (face1 == self.path1[idx]).astype(np.double)) * self.path1_sign[idx]
        else:
            return idx

    def locate_faces(self, x, y):
        """ Get faces whose centroids are closest to queried (x,y) coordinate pairs.
        in:  x, y               float arrays of shape (N,)
        out: face_ids           int array in range(face_count) of shape (N,)
        """
        if self.locator is None:
            self.locator = scipy.spatial.KDTree(np.stack((self.centroid_x, self.centroid_y), axis=-1))
        _, faces = self.locator.query(np.stack(np.broadcast_arrays(x, y), axis=-1), k=1)
        return faces

    def approximate_inductance(self, junc_L=1, junc_M=0, max_dist=0):
        """ Sets self and mutual junction inductance according to the formula:
            - self:     L = junc_L * l
            - mutual:   M_12 = junc_M * l_1 * l_2 * cos(alpha_12) / distance_12

        These are assigned to the sparse self.junction_inductance_matrix, where only junction_pairs
        (i, j) are included with distance_ij < max_dist.

        Here L is the self inductance and M_12 are the mutual inductance between junction 1 and
        2 in units of L0 = mu0 * a. Furthermore:

            l, l1, l2    dimensionless junction lengths
            alpha_12     angle between junction 1 and junction 2
            distance_12  dimensionless distance between centres of junction 1 and junction 2

        Note that these properties refer to dimensionless coordinates as specified on the nodes-
        coo of self. Actual coordinates are scaled by a free to choose factor a.

        The mutual inductance is a crude approximation of Neumann's formula for two wire segments.
        One can alternatively set the junction-inductance-matrix manually using
        set_junction_inductance_matrix().

        The JJA equations are non-dimensionalized using beta_L =  2pi L0 * I0 / Phi0 where
        again L0 is mu0 * a. Beta_L has to be assigned consistently to account for real units,
        meaning  that a * array_coordinates must match real coordinates, I0 * Ic_factor must
        match real Ic and junction_inductance_matrix * mu0 * a must match real inductances.

        These inductances are junction-inductances, not path-inductances. Note for example that
        only junction-self-inductance leads to both a path self inductance equal to the sum of
        its junction-self inductances and a nearest-neighbour mutual inductance between paths
        based on the self-inductance of their common junction.

        """

        self.junction_inductance_matrix = None
        self.inductance_is_diagonal = junc_M == 0 or max_dist == 0
        i, j = np.arange(self.Nj(), dtype=int), np.arange(self.Nj(), dtype=int)
        data = self._junction_lengths() * junc_L
        if not self.inductance_is_diagonal:
            tree = scipy.spatial.KDTree(np.stack(self._junction_centers(), axis=-1))
            pairs = tree.query_pairs(max_dist, 2, output_type='ndarray')
            i, j = np.append(i, pairs[:, 0]), np.append(j, pairs[:, 1])
            i, j = np.append(i, pairs[:, 1]), np.append(j, pairs[:, 0])
            inner = self._junction_inner(*pairs.T)
            distance = self._junction_distance(*pairs.T)
            mutual = junc_M * inner / distance
            data = np.append(data, mutual)
            data = np.append(data, mutual)
        self.junction_inductance_matrix = scipy.sparse.coo_matrix((data, (i, j)), shape=(self.Nj(), self.Nj())).tocsr()
        return self

    def get_junction_inductance_matrix(self):
        # return matrix whose entry (r, c) is the magnetic coupling between wire r and wire c.
        # out: (junction_count, junction_count) sparse symmetric float matrix
        return self.junction_inductance_matrix

    def set_junction_inductance_matrix(self, junction_inductance_matrix):
        # in: (junction_count, junction_count) sparse symmetric float matrix
        self.junction_inductance_matrix = junction_inductance_matrix
        if not self.junction_inductance_matrix.shape == (self.Nj(), self.Nj()):
            raise ValueError("junction inductance matrix must be square matrix with junction_count rows")
        if not _is_symmetric(self.junction_inductance_matrix):
            raise ValueError("junction inductance matrix must be symmetric")
        self.inductance_is_diagonal = _is_diagonal(self.junction_inductance_matrix)
        return self

    def L(self):
        # returns beta_L * junction_inductance_matrix
        return self.beta_L * self.junction_inductance_matrix

    def __str__(self):
        return "x: \n" + str(self.x) +"y: \n" + str(self.y) + \
               "\nnode1: \n" + str(self.node1) + "\nnode2: \n" + str(self.node2)

    def get_beta_C(self):
        # damping parameter (=2 * pi * I0 * (R0 ** 2) * C0 / Phi0)
        return self.beta_C

    def get_beta_L(self):
        # screening parameter (=2 * pi * L0 * I0 / Phi0 = 2 * pi * mu0 * a0 * I0 / Phi0)
        return self.beta_L

    def set_beta_C(self, beta_C):
        # damping parameter (=2 * pi * I0 * (R0 ** 2) * C0 / Phi0)
        self.beta_C = beta_C

    def set_beta_L(self, beta_L):
        # screening parameter (=2 * pi * L0 * I0 / Phi0 = 2 * pi * mu0 * a0 * I0 / Phi0)
        self.beta_L = beta_L

    def has_capacitance(self):
        # returns True if the damping parameter, beta_C, is positive. In this case, the time-evolution
        # differential equation becomes second-order.
        return self.beta_C != 0

    def has_inductance(self):
        # returns True if the screening parameter, beta_L, is positive. This determines which algorithms
        # are used for computations.
        return self.beta_L != 0

    def get_cut_matrix(self):
        """
        returns the "cut-matrix" (abbreviated M in this code), which is a node_count by junction_count matrix.
        Its transpose is  the incidence matrix, node1 of a junction is -1 and node2 is -1 (abbreviated MT).
        Its rows span the cut-space (which is orthogonal to the cycle space). The cut-space has a span of
        node_count - 1, so one might want to use omit_last_node=True to match the span.
        out: (node_count, junction_count) sparse matrix      if  omit_last_node=False
             (node_count - 1, junction_count) sparse matrix  if  omit_last_node=True
        Important: The row number does nót correspond with node_idx, because the nodes are permuted internally.
        """
        return _apply_matrix_format(self.cut_matrix.to_coo()[self.nodes_permute, :], self.matrix_format)

    def get_cycle_matrix(self):
        """
        returns the "cycle-matrix" (abbreviated A in this code), which is a face_count by junction_count matrix.
        It is +1 if traversing a face counter-clockwise passes through a junction in its direction, and -1
        otherwise. Its rows span the cycle-space (which is orthogonal to the cut space). The cut-space has a
        span equal to face_count = junction_count - node_count + 1.
        out: (face_count, junction_count) sparse matrix
        """
        return self.cycle_matrix

    def plot(self, show_nodes=True, show_node_ids=True,
             node_labels=None, show_junctions=True, show_junction_directions=True,
             show_junction_ids=True, junction_labels=None,
             show_paths=True, show_path_directions=True,
             show_path_ids=True, path_labels=None, figsize=None):
        """
        Visualize array nodes, junctions and faces; and their respective indices.
        For full documentation, see: ArrayVisualize.CircuitPlot
        """
        from array_visualize import CircuitPlot

        cr = CircuitPlot(self, show_nodes=show_nodes, show_node_ids=show_node_ids,
                         node_labels=node_labels, show_junctions=show_junctions,
                         show_junction_directions=show_junction_directions,
                         show_junction_ids=show_junction_ids, junction_labels=junction_labels,
                         show_paths=show_paths, show_path_directions=show_path_directions,
                         show_path_ids=show_path_ids, path_labels=path_labels, figsize=figsize)
        return cr.show()

    # abbreviations and aliases
    def Nn(self):   # alias for node_count
        return len(self.x)

    def Nj(self):   # alias for get_junction_count()
        return len(self.node1)

    def Ic(self) -> np.ndarray:     # alias for get_critical_current_factors
        return self.critical_current_factors

    def R(self) -> np.ndarray:      # alias for get_resistance_factors
        return self.resistance_factors

    def centroids(self):
        return self.centroid_x, self.centroid_y

    def Np(self):
        return np.sum([p.shape[1] for p in self.path_nodes])

    def A(self):  # alias for get_cycle_matrix()
        return self.cycle_matrix

    def AT(self):   # equal to A().T
        if self.cycle_matrix_transposed is None:
            self.cycle_matrix_transposed = self.cycle_matrix.T
        return self.cycle_matrix_transposed

    def Asq(self):  # equal to A() @ A().T
        if self.cycle_square is None:
            self.cycle_square = self.cycle_matrix @ self.cycle_matrix.T  # (Np, Np)
        return self.cycle_square

    def Mr(self):   # equal to get_cut_matrix(omit_last_node=True)
        return self.cut_matrix_reduced

    def M(self):
        # equal to get_cut_matrix(omit_last_node=False)[self.node_permute, :] (nodes reordered internally)
        return self.cut_matrix

    def MT(self):   # equal M().T
        if self.cut_matrix_transposed is None:
            self.cut_matrix_transposed = self.cut_matrix.T
        return self.cut_matrix_transposed

    def MrT(self):  # equal Mr().T
        if self.cut_matrix_reduced_transposed is None:
            self.cut_matrix_reduced_transposed = self.cut_matrix_reduced.T
        return self.cut_matrix_reduced_transposed

    def Mrsq(self): # equal Mr() @ Mr().T
        if self.cut_reduced_square is None:
            if self.cut_matrix_reduced_transposed is None:
                self.cut_reduced_square = self.cut_matrix_reduced @ self.cut_matrix_reduced.T
            else:
                self.cut_reduced_square = self.cut_matrix_reduced @ self.cut_matrix_reduced_transposed
        return self.cut_reduced_square

    def Msq(self):  # equal M() @ M().T
        if self.cut_square is None:
            if self.cut_matrix_transposed is None:
                self.cut_square = self.cut_matrix @ self.cut_matrix.T
            else:
                self.cut_square = self.cut_matrix @ self.cut_matrix_transposed
        return self.cut_square

    def _permute_nodes(self, nodes_permute):
        # in: nodes_permute (Nn,) int array.
        # sets permute_nodes property. This affects the matrices and current base (which must be
        # re-computed), but not the node order the user sees.
        self.nodes_permute = nodes_permute
        self._assign_cut_matrix()
        self.current_base_reordered = self.current_base[nodes_permute]

    def _permute_nodes_lexsort(self):
        # sets permute_nodes property based on the lex-sort of the node-coordinates; effectively sorting
        # them. This is the default node-ordering (and generally creates cut-square-matrices on which LU is fast).
        self._permute_nodes(np.lexsort(self.get_node_coordinates()))

    def _all_same_junction_self_L(self):
        # if true; all junctions have the same self inductance, and no mutual inductance
        if self.inductance_is_diagonal:
            diag = self.junction_inductance_matrix.diagonal()
            return np.allclose(diag, diag[0])
        return False

    def _set_junction_hash(self):
        # internal: create hash structure to find junctions from nodes
        nmin = np.minimum(self.node1, self.node2).astype(np.int64)
        nmax = np.maximum(self.node1, self.node2).astype(np.int64)
        Nn_p = np.array(self.node_count(), dtype=np.int64)
        self.junc_hash, self.hash_idx = np.unique(nmin + nmax * Nn_p, return_index=True)
        if len(self.junc_hash) < self.junction_count():
            raise ValueError("contains duplicate junctions or self-loops")

    def _Ibase_reduced(self) -> np.ndarray:
        # _Ibase() but last node removed
        return self._Ibase()[:-1]

    def _Ibase(self) -> np.ndarray:
        # internal call to external_current_basis. Its output is the output of
        # get_external_current_basis() and afterwards permuted with nodes_permute.
        if self.current_base_reordered is None:
            return self.current_base
        else:
            return self.current_base_reordered

    def _assign_cut_matrix(self):
        self.cut_square = None
        self.cut_matrix_reduced_transposed = None
        self.cut_matrix_transposed = None
        if self.cut_matrix_reduced is None or self.cut_matrix is None:
            Nj, Nn = self.junction_count(), self.node_count()
            row = np.concatenate((self.node1, self.node2))
            col = np.concatenate((np.arange(Nj), np.arange(Nj)))
            data = np.concatenate((np.ones(Nj), -np.ones(Nj)))
            if self.nodes_permute is not None:
                inv_reorder = np.argsort(self.nodes_permute)
                row = inv_reorder[row]
            self.cut_matrix = coo_matrix((data, (row, col)), shape=(Nn, Nj))
            self.cut_matrix = _apply_matrix_format(self.cut_matrix, self.matrix_format)
            mask = row != (Nn - 1)
            self.cut_matrix_reduced = coo_matrix((data[mask], (row[mask], col[mask])), shape=(Nn - 1, Nj))
            self.cut_matrix_reduced = _apply_matrix_format(self.cut_matrix_reduced, self.matrix_format)
            return self.cut_matrix, self.cut_matrix_reduced

    def _get_cycle_matrix(self, matrix_format):
        Np, Nj = self.face_count(), self.junction_count()
        mask1 = self.path1 >= 0
        mask2 = self.path2 >= 0
        p = np.concatenate((self.path1[mask1], self.path2[mask2]))
        j = np.concatenate((np.flatnonzero(mask1), np.flatnonzero(mask2)))
        sgns = np.concatenate((-self.path1_sign[mask1], self.path1_sign[mask2]))
        cycle_matrix = coo_matrix((sgns, (p, j)), shape=(Np, Nj))
        return _apply_matrix_format(cycle_matrix, matrix_format)

    def _check_inductance_in_array(self):
        L = self.junction_inductance_matrix
        if scipy.sparse.issparse(L):
            if scipy.sparse.csgraph.structural_rank(self.A() @ L @ self.AT()) < self.Np():
                raise ValueError("A@L@A.T rank smaller than Np so not invertible. "
                                 "Likely some paths have no self-inductance, while others do, "
                                 "which can be done in principle but is not supported ")

    def _is_orthogonal_check(self):
        return (self.M() @ self.AT()).sum() == 0

    def _single_connected_component_check(self):
        return scipy.sparse.csgraph.connected_components(self.Msq(), return_labels=False) == 1

    def _circuit_rank_test(self):
        return (self.Nn() + self.Np()) == (self.Nj() + 1)

    def _IbaseJ(self) -> np.ndarray:
        if self.current_base_J is None:
            self.current_base_J = (self.MrT() @ scipy.sparse.linalg.spsolve(self.Mrsq(), self._Ibase()[:-1]))
        return self.current_base_J

    def _Ibase_total(self):
        if self.current_base_total is None:
            self.current_base_total = np.sum(self._Ibase()[self._Ibase() > 0])
        return self.current_base_total

    @staticmethod
    def _compress_array(x):
        x = np.array(x)
        if x.size == 1:
            return x
        elif np.allclose(x, x[0]):
            return x[0]
        else:
            return x

    @staticmethod
    def _assert_junction_id_exists(idx, self_elem1, self_elem2, elem1, elem2):
        if not np.all(((self_elem1[idx] == elem1) & (self_elem2[idx] == elem2)) |
                      ((self_elem1[idx] == elem2) & (self_elem2[idx] == elem1))):
            raise ValueError("(some of) queried junctions do not exist")

    @staticmethod
    def _append_quantities(x1, x2, N1, N2):
        x1, x2 = Array._compress_array(x1), Array._compress_array(x2)
        if x1.size == 1 and x2.size==1:
            return x1 if x1 == x2 else np.append(np.ones(N1, x1.dtype) * x1, np.ones(N2, x2.dtype) * x2)
        if x1.size == 1:
            x1 = np.ones(N1, x1.dtype) * x1
        if x2.size==1:
            x2 = np.ones(N1, x2.dtype) * x2
        return np.append(x1, x2)

    @staticmethod
    def _prepare_junction_quantity(x, Nj, x_name="x", criterion=lambda s: s <= 0, crit_error=" must be positive"):
        x = np.array(x, dtype=np.double)
        if scipy.sparse.issparse(x):
            if _is_sparse_diag(x):
                x = x.diagonal()
            else:
                raise ValueError(x_name + " must be scalar, array of len(Nj) or sparse diagonal matrix of size Nj")
        else:
            x = np.array(x, dtype=np.double).flatten()
        if not (len(x) == 1 or len(x) == Nj):
            raise ValueError(x_name + " must be scalar or array of length Nj")
        if np.any(criterion(x)):
            raise ValueError(x_name + crit_error)
        return x

    def _junction_centers(self):
        x, y = self.get_node_coordinates()
        return 0.5 * (x[self.node1] + x[self.node2]),  0.5 * (y[self.node1] + y[self.node2])

    def _junction_lengths(self):
        x, y = self.get_node_coordinates()
        return np.sqrt((x[self.node2] - x[self.node1]) ** 2 + (y[self.node2] - y[self.node1]) ** 2)

    def _junction_inner(self, ids1, ids2):
        x, y = self.get_node_coordinates()
        x_n1_j1, y_n1_j1 = x[self.node1[ids1]], y[self.node1[ids1]]
        x_n2_j1, y_n2_j1 = x[self.node2[ids1]], y[self.node2[ids1]]
        x_n1_j2, y_n1_j2 = x[self.node1[ids2]], y[self.node1[ids2]]
        x_n2_j2, y_n2_j2 = x[self.node2[ids2]], y[self.node2[ids2]]
        return (x_n2_j1 - x_n1_j1) * (x_n2_j2 - x_n1_j2) + (y_n2_j1 - y_n1_j1) * (y_n2_j2 - y_n1_j2)

    def _junction_distance(self, ids1, ids2):
        x, y = self._junction_centers()
        return np.sqrt((x[ids2] - x[ids1]) ** 2 + (y[ids2] - y[ids1]) ** 2)

    def _get_path_junctions(self, return_aligned=True):
        if not return_aligned:
            return [self.get_junction(p, np.roll(p, -1, axis=0), return_is_aligned=False) for p in self.path_nodes]
        else:
            juncs, is_aligned = [], []
            for p in self.path_nodes:
                j, is_al = self.get_junction(p, np.roll(p, -1, axis=0), return_is_aligned=True)
                juncs += [j]
                is_aligned += [is_al]
            return juncs, is_aligned

    def _reorder_paths(self):
        reorder_ids = np.lexsort(self.centroids())
        self.areas = self.areas[reorder_ids]
        self.centroid_x = self.centroid_x[reorder_ids]
        self.centroid_y = self.centroid_y[reorder_ids]
        return reorder_ids

    def _assign_path_map(self):
        j, is_al = self._get_path_junctions(return_aligned=True)
        Nj = self.junction_count()
        p_counts = [p.shape[1] for p in self.path_nodes]
        p_counts_cum = np.cumsum(p_counts) - p_counts
        inv_p_reorder = np.argsort(self.reorder_ids)
        p_ids = [c + np.ones((p.shape[0], 1), dtype=int) * np.arange(p.shape[1], dtype=int) for c, p in zip(p_counts_cum, self.path_nodes)]
        j = np.concatenate([p.flatten() for p in j])
        p_ids = inv_p_reorder[np.concatenate([p.flatten() for p in p_ids])]
        j_sgns = np.concatenate([(2 * p.astype(int) - 1).flatten() for p in is_al])
        idx = np.argsort(j)
        j, p_ids, j_sgns = j[idx], p_ids[idx], j_sgns[idx]
        j_p, j_idx, j_cnt = np.unique(j, return_index=True, return_counts=True)
        j_full_cnt = np.zeros(Nj, dtype=np.int64)
        j_full_cnt[j_p] = j_cnt
        if np.any(j_cnt> 2):
            raise NotPlanarError("array not planar")
        p1_idx = (np.cumsum(j_cnt) - j_cnt)
        p1 = -np.ones(Nj, dtype=np.int32)
        p1[j_p] = p_ids[p1_idx]
        p2 = -np.ones(Nj, dtype=np.int32)
        out_signs = np.zeros(Nj, dtype=np.int32)
        out_signs[j_p] = -j_sgns[p1_idx]
        p2[j_full_cnt==2] = p_ids[j_idx[j_cnt==2] + 1]
        pmin, pmax = np.minimum(p1, p2).astype(np.int64), np.maximum(p1, p2).astype(np.int64)
        path_hash = (pmax.astype(np.int64)) + (pmin.astype(np.int64)) * np.array(self.face_count(), dtype=np.int64)
        path_hash_idx = np.argsort(path_hash)
        return p1, p2, out_signs, path_hash[path_hash_idx], path_hash_idx

    @staticmethod
    def _construct_faces(x, y, node1, node2, robust=True):

        def make_cycle_structure(x, y, node1, node2):
            # makes "cycle" structure, which is a function (n1, n2) -> e. The idea
            # is that coming from node1, passing through neighbour node2, if one makes
            # the sharpest possible turn left in the network, e is the edge you end up on.
            # output:
            # n1, n2    (2 * Nj,) arrays     list of all edges in both directions (sorted by n1)
            # next_idx  (2 * Nj,) arrays     index in (n1, n2) of next edge
            x, y = np.array(x, dtype=np.double).flatten(), np.array(y, dtype=np.double).flatten()
            n1, n2 = np.append(node1, node2), np.append(node2, node1)
            n1_sort_arg = np.lexsort((n2, n1))
            n1, n2 = n1[n1_sort_arg], n2[n1_sort_arg]
            cum_degree_count = np.append(np.flatnonzero(np.diff(np.append([0], n1))), [len(n1)])
            degree_count = np.diff(np.append([0], cum_degree_count))
            n21_map = np.argsort(np.lexsort((n1, n2)))
            angle = np.arctan2(y[n2] - y[n1], x[n2] - x[n1])
            angle_arg_sort = np.argsort(2 * np.pi * n1 + angle)
            n2 = n2[angle_arg_sort]
            n21_map = np.argsort(angle_arg_sort)[n21_map[angle_arg_sort]]
            n1_index = np.repeat(cum_degree_count - degree_count, degree_count)
            roll_map = ((np.arange(len(n1), dtype=int) - n1_index - 1) % np.repeat(degree_count, degree_count) + n1_index)
            next_idx = roll_map[n21_map]
            return n1, n2, next_idx

        n1, n2, next_idx = make_cycle_structure(x, y, node1, node2)

        if robust:
            edge_ids = np.arange(len(n1), dtype=int)
        else:
            edge_ids = np.flatnonzero(n2 > n1)

        paths = -np.ones((3, len(edge_ids)), dtype=int)
        paths[0, :] = n1[edge_ids]
        path_lengths = np.ones(len(edge_ids), dtype=int)
        max_path_length = 1
        out_paths, out_path_lengths = [], []
        next_node = n2[edge_ids]

        def move_terminated_paths_to_output(paths, path_lengths, out_paths, out_path_lengths, edge_ids, next_node):
            # terminated paths that have looped back to the first node are removed from the loop and stored
            # in out_paths as a new page.
            is_terminated = next_node == paths[0, :]
            if np.any(is_terminated):
                out_path_lengths += [path_lengths[is_terminated]]
                out_paths += [paths[:np.max(out_path_lengths[-1]), is_terminated]]
                paths = paths[:, ~is_terminated]
                path_lengths = path_lengths[~is_terminated]
                edge_ids = edge_ids[~is_terminated]
                next_node = next_node[~is_terminated]
            return paths, path_lengths, out_paths, out_path_lengths, edge_ids, next_node

        def erase_to_previous_occurance(paths, path_lengths, next_node):
            in_path_idx, path_idx = np.nonzero(paths == next_node[None, :])
            if len(in_path_idx) > 0:
                range_lengths = path_lengths[path_idx] - in_path_idx
                all_path_ids = np.repeat(path_idx, range_lengths)
                all_in_path_ids = np.arange(len(all_path_ids)) - np.repeat(range_lengths.cumsum() - range_lengths - in_path_idx, range_lengths)
                path_lengths[path_idx] = in_path_idx
                paths[all_in_path_ids, all_path_ids] = -1
            return paths, path_lengths

        # iteration doing counter-clockwise walks through the graphs starting from each junction
        while len(edge_ids) > 0:
            paths, path_lengths, out_paths, out_path_lengths, edge_ids, next_node = move_terminated_paths_to_output(
                paths, path_lengths, out_paths, out_path_lengths, edge_ids, next_node)
            paths, path_lengths = erase_to_previous_occurance(paths, path_lengths, next_node)
            if paths.shape[0] == (max_path_length + 1):
                paths = np.append(paths, -np.ones(paths.shape, dtype=int), axis=0)
            paths[path_lengths, np.arange(len(edge_ids))] = next_node
            path_lengths += 1
            max_path_length += 1
            edge_ids = next_idx[edge_ids]
            next_node = n2[edge_ids]

        def rearrange_paths(paths, path_lengths):
            # rearrange path structure such that the paths in any page are the same length.
            # in:
            #  paths         list of P pages, where each page paths[i] is (..., path_count[i]) array
            #  path_lengths  list of P arrays, where each array is (path_count[i],) array equal to the path lengths
            # out:
            #  out_paths         list of P' pages, where each page out_paths[i] is (path_length[i], new_path_count[i]) array
            #  out_path_lengths  (P',) int array
            out_path_lengths, path_length_counts = np.unique(np.concatenate(path_lengths), return_counts=True)
            lengths_index = -np.ones(out_path_lengths[-1] + 1, dtype=int)
            lengths_index[out_path_lengths] = np.arange(len(out_path_lengths))
            out_paths = [np.zeros((l, c), dtype=int) for l, c in zip(out_path_lengths, path_length_counts)]
            current_out_path_index = np.zeros(len(out_path_lengths), dtype=int)
            for path_page, path_length_page in zip(paths, path_lengths):
                page_path_unique_lengths, page_path_length_counts = np.unique(path_length_page, return_counts=True)
                for length, count in zip(page_path_unique_lengths, page_path_length_counts):
                    index = lengths_index[length]
                    p_index = current_out_path_index[index]
                    out_paths[index][:, p_index:(p_index + count)] = path_page[:length, path_length_page == length]
                    current_out_path_index[index] += count
            return out_paths, out_path_lengths

        out_paths, _ = rearrange_paths(out_paths, out_path_lengths)

        def get_areas(paths, x, y):
            areas = np.zeros(np.sum([p.shape[1] for p in paths]), dtype=np.double)
            i = 0
            for p in paths:
                xp, yp = x[p], y[p]
                areas[i:(i + p.shape[1])] = 0.5 * np.sum((xp * np.roll(yp, 1, axis=0) - np.roll(xp, 1, axis=0) * yp), axis=0)
                i += p.shape[1]
            return areas

        def get_centroids(paths, nx, ny):
            path_count = np.sum([p.shape[1] for p in paths])
            centroid_x = np.zeros(path_count, dtype=np.double)
            centroid_y = np.zeros(path_count, dtype=np.double)
            i = 0
            for p in paths:
                x, y = nx[p], ny[p]
                xp, yp = np.roll(x, 1, axis=0), np.roll(y, 1, axis=0)
                xy = x * yp - xp * y
                six_times_area = 3.0 * np.sum(xy, axis=0)
                p_slice = slice(i, i + p.shape[1])
                centroid_x[p_slice] = np.sum((x + xp) * xy, axis=0) / six_times_area
                centroid_y[p_slice] = np.sum((y + yp) * xy, axis=0) / six_times_area
                i += p.shape[1]
            return centroid_x, centroid_y

        def select_from_pages(paths, mask):
            split_stacked = np.split(mask, np.cumsum([p.shape[1] for p in paths]))
            return [p[:, m] for m, p in zip(split_stacked, paths)]

        def remove_duplicate_paths(paths):
            out_paths, i, idxs = [], 0, []
            for p in paths:
                i_new = i + p.shape[1]
                if p.shape[1] > 0:
                    rows, col = np.ogrid[:p.shape[0], :p.shape[1]]
                    p = p[(rows + np.argmin(p, axis=0)) % p.shape[0], col]
                    p, idx = np.unique(p, axis=1, return_index=True)
                    idxs += [idx + i]
                    out_paths += [p]
                i = i_new
            return out_paths, np.concatenate(tuple(idxs))

        areas = -get_areas(out_paths, x, y)
        boundary_paths = select_from_pages(out_paths, areas < 0)
        boundary_paths, _ = remove_duplicate_paths(boundary_paths)
        out_paths = select_from_pages(out_paths, areas > 0)
        out_paths, ind = remove_duplicate_paths(out_paths)
        cx, cy = get_centroids(out_paths, x, y)

        def check_panarity(paths, Nn):
            # Mac Lane's planarity criterion
            n1 = np.concatenate([p.flatten() for p in paths]).astype(np.int64)
            n2 = np.concatenate([np.roll(p, -1, axis=0).flatten() for p in paths]).astype(np.int64)
            _, cnts = np.unique(np.minimum(n1 + Nn * n2, n2 + Nn * n1), return_counts=True)
            if np.any(cnts > 2):
                raise NotPlanarError("Edge contained more than two times in cycle basis")

        check_panarity(out_paths, len(x))
        return out_paths, boundary_paths, areas[areas > 0][ind], cx, cy

    @staticmethod
    def _junction_remove_mask(nodes1, nodes2, node_remove_mask):
        node_remove_mask = node_remove_mask.copy().astype(int)
        remove_nodes = np.flatnonzero(node_remove_mask)
        new_node_id = np.arange(node_remove_mask.size, dtype=int) - (np.cumsum(node_remove_mask) - node_remove_mask)
        junc_remove_mask = (np.isin(nodes1, remove_nodes) | np.isin(nodes2, remove_nodes))
        return junc_remove_mask, new_node_id


def _apply_matrix_format(matrix, matrix_format):
    if matrix_format == "coo":
        return matrix.tocoo()
    if matrix_format == "csr":
        return matrix.tocsr()
    elif matrix_format == "csc":
        return matrix.tocsc()
    elif matrix_format == "dense":
        return matrix.todense()
    raise ValueError("invalid matrix format")

def _is_sparse_diag(A):
    if scipy.sparse.issparse(A):
        return A.nnz == scipy.sparse.diags(A.diagonal()).nnz
    return False

def _is_diagonal(A):
    if scipy.sparse.isspmatrix(A):
        return _is_sparse_diag(A)
    else:
        return np.count_nonzero(A - np.diag(np.diagonal(A)))

def _is_sparse_symmetric(A):
    if scipy.sparse.issparse(A):
        return (A - A.T).nnz == 0
    return False

def _is_symmetric(A):
    if scipy.sparse.isspmatrix(A):
        return _is_sparse_symmetric(A)
    else:
        return np.all(A == A.T)


class Solver:

    def __init__(self, array):
        self.array = array
        self.Msq_factorized = None
        self.Asq_factorized = None
        self.MsqS_factorized = None
        self.AsqS_factorized = None
        self.LsqS_factorized = None
        self.p_shape = None

    def pack(self, b):
        # reshape (p_shape, Nx) to (Nx, :) (suitable for matrix multiplication or solve)
        self.p_shape = b.shape[:-1]
        if len(b.shape) == 1:
            return b.flatten()[:, None]
        return b.reshape(-1, b.shape[-1]).T

    def unpack(self, b):
        # reshape (Nx, :) back to (p_shape, Nx)
        if self.p_shape == ():
            return b.flatten()
        return b.T.reshape(*self.p_shape, -1)

    def dot(self, A, b: np.ndarray, p=True, u=True):
        # p and u are pack/unpack respectively
        if p and u:
            return self.unpack(A @ self.pack(b))
        if p:
            return A @ self.pack(b)
        if u:
            return self.unpack(A @ b)
        return A @ b

    def A_dot(self, b, p=True, u=True):
        return self.dot(self.array.A(), b, p=p, u=u)

    def AT_dot(self, b, p=True, u=True):
        return self.dot(self.array.AT(), b, p=p, u=u)

    def M_dot(self, b, p=True, u=True):
        return self.dot(self.array.Mr(), b, p=p, u=u)

    def MT_dot(self, b, p=True, u=True):
        return self.dot(self.array.MrT(), b, p=p, u=u)

    def L_dot(self, b, p=True, u=True):
        if not self.array.inductance_is_diagonal:
            return self.dot(self.array.junction_inductance_matrix, self.array.beta_L * b, p=p, u=u)
        if self.array._all_same_junction_self_L():
            out = self.array.beta_L * self.array.junction_inductance_matrix[0, 0] * b
        else:
            if p:
                out = self.array.beta_L * self.array.junction_inductance_matrix.diagonal() * b
            else:
                out = self.array.beta_L * self.array.junction_inductance_matrix.diagonal()[:, None] * b
        if p and not u:
            return self.pack(out)
        if u and not p:
            return self.unpack(out)
        return out

    def A_solve(self, b):
        """
        Solves the equation: A @ x = b (where A = cycle_matrix).
        If b is integral (contain only integers), the output array x will also be integral.

        input:  b (..., Np)
        output: x (..., Nj)

        Notes:
            - The equation is underdetermined, so the solution x is not unique.

        Use cases:
            - Used for changing phase zones (theta, z) -> (theta', z').
              Here theta' = theta + 2 * pi * Z where A @ Z = z' - z. Crucially, Z must
              be integral to ensure theta keeps obeying Kirchhoff's current rule.
            - Used for projecting theta onto cycle space; theta' = theta - g so that A @ theta'= 0.
              Then A @ g = 2 * pi * (z - areas * f)
        """

        b = np.array(b)
        b_shape = list(b.shape)
        b = b.reshape(-1, self.array.Np())
        boundary_path = self.array.outer_paths[-1][:, 0].flatten()
        cur, predecessor = scipy.sparse.csgraph.depth_first_order(self.array.Asq(), boundary_path[0])
        prev = predecessor[cur]
        prev[0] = -1
        juncs, sgns = self.array.get_face_common_junction(prev, cur)
        for i in reversed(range(self.array.Np())):
            if prev[i] >= 0:
                b[:, prev[i]] += b[:, cur[i]]
        x = np.zeros((b.shape[0], self.array.Nj()), dtype=b.dtype)
        x[:, juncs] = b[:, cur] * sgns
        b_shape[-1] = self.array.Nj()
        return -x.reshape(tuple(b_shape))

    def get_Msq_solver(self):
        if self.Msq_factorized is None:
            self.Msq_factorized = scipy.sparse.linalg.factorized(self.array.Mrsq())
        return self.Msq_factorized

    def get_Asq_solver(self):
        if self.Asq_factorized is None:
            self.Asq_factorized = scipy.sparse.linalg.factorized(self.array.Asq())
        return self.Asq_factorized

    def get_M_sandwich(self, sandwich, full=False):
        # compute M @ diag(sandwich) @ MT
        sandwich = np.array(sandwich, dtype=np.double).flatten()
        if sandwich.size == 1:
            if full:
                return self.array.Msq() * sandwich.item()
            else:
                return self.array.Mrsq() * sandwich.item()
        else:
            if len(sandwich) != self.array.Nj():
                raise ValueError("sandwich must be of size 1 or Nj")
            if full:
                return self.array.M() @ self.array.MT().multiply(sandwich[:, None])
            else:
                return self.array.Mr() @ self.array.MrT().multiply(sandwich[:, None])

    def get_A_sandwich(self, sandwich):
        # compute A @ diag(sandwich) @ AT
        sandwich = np.array(sandwich, dtype=np.double).flatten()
        if sandwich.size == 1:
            return self.array.Asq() * sandwich.item()
        else:
            if len(sandwich) != self.array.Nj():
                raise ValueError("sandwich must be of size 1 or Nj")
            return self.array.A() @ self.array.AT().multiply(sandwich[:, None])

    def get_L_sandwich(self, sandwich_a=1, sandwich_b=0):
        # compute A @ (L @ diag(sandwich_a) + diag(sandwich_b)) @ AT
        sandwich_a = np.array(sandwich_a, dtype=np.double)
        sandwich_b = np.array(sandwich_b, dtype=np.double)

        # if is constant
        if self.array._all_same_junction_self_L() and sandwich_a.size == 1 and sandwich_b.size == 1:
            return self.array.Asq() * (sandwich_a * self.array.beta_L * self.array.junction_inductance_matrix[0, 0] + sandwich_b).item()

        # if is matrix:
        if not self.array.inductance_is_diagonal:
            e = np.ones(self.array.Nj(), dtype=np.double)
            L = (self.array.junction_inductance_matrix  @ scipy.sparse.diags(self.array.beta_L * e * sandwich_a)) + scipy.sparse.diags(e * sandwich_b)
            return self.array.A() @ L @ self.array.AT()

        # is vector:
        vector = sandwich_a * self.array.beta_L * self.array.junction_inductance_matrix.diagonal() + sandwich_b
        return self.array.A() @ self.array.AT().multiply(vector[:, None])

    def get_M_sandwich_solver(self, sandwich, force_factorize=False, as_linear_operator=False):
        if (self.MsqS_factorized is None) or force_factorize:
            self.MsqS_factorized = scipy.sparse.linalg.factorized(self.get_M_sandwich(sandwich))
        if as_linear_operator:
            Nn = self.array.Nnr()
            return scipy.sparse.linalg.LinearOperator((Nn, Nn), matvec=self.MsqS_factorized)
        else:
            return self.MsqS_factorized

    def get_A_sandwich_solver(self, sandwich, force_factorize=False, as_linear_operator=False):
        if (self.AsqS_factorized is None) or force_factorize:
            self.AsqS_factorized = scipy.sparse.linalg.factorized(self.get_A_sandwich(sandwich))
        if as_linear_operator:
            Np = self.array.Np()
            return scipy.sparse.linalg.LinearOperator((Np, Np), matvec=self.AsqS_factorized)
        else:
            return self.AsqS_factorized

    def get_L_sandwich_solver(self, sandwich_a=1, sandwich_b=0, force_factorize=False, as_linear_operator=False):
        if (self.LsqS_factorized is None) or force_factorize:
            self.LsqS_factorized = scipy.sparse.linalg.factorized(self.get_L_sandwich(sandwich_a, sandwich_b))
        if as_linear_operator:
            Np = self.array.Np()
            return scipy.sparse.linalg.LinearOperator((Np, Np), matvec=self.LsqS_factorized)
        else:
            return self.LsqS_factorized


class SquareArray(Array):

    def __init__(self, count_x, count_y, x_scale=1.0, y_scale=1.0, current_direction="x", matrix_format="csc",
                 beta_L=0, beta_C=0):
        x, y = SquareArray.get_xy(count_x, count_y, x_scale=x_scale, y_scale=y_scale)
        I_base = SquareArray.get_Ibase(count_x, count_y, current_direction=current_direction)
        nodes1, nodes2 = SquareArray.get_node12(count_x, count_y)
        super().__init__(x, y, nodes1, nodes2, external_current_basis=I_base,
                         matrix_format=matrix_format, beta_L=beta_L, beta_C=beta_C)

    @staticmethod
    def get_xy(count_x, count_y, x_scale=1.0, y_scale=1.0):
        y, x = np.mgrid[0:count_y, 0:count_x]
        return x_scale * x, y_scale * y

    @staticmethod
    def get_node12(count_x, count_y):
        idx = np.arange(count_x * count_y).reshape(count_y, count_x)
        nodes1 = np.concatenate((idx[:, 0:-1].flatten(), idx[0:-1, :].flatten()))
        nodes2 = np.concatenate((idx[:, 1:].flatten(), idx[1:, :].flatten()))
        return nodes1, nodes2

    @staticmethod
    def get_Ibase(count_x, count_y, current_direction="x"):
        if current_direction == "x":
            if count_x < 2:
                raise ValueError("count_x must be at least 2")
            I_base = np.array([1] + [0] * (count_x - 2) + [-1]) * np.ones((count_y, 1))
        elif current_direction == "y":
            if count_y < 2:
                raise ValueError("count_y must be at least 2")
            I_base = np.array([1] + [0] * (count_y - 2) + [-1])[:, None] * np.ones(count_x)
        else:
            raise ValueError("Invalid current direction. Choose 'x' or 'y'.")
        return I_base

class HoneycombArray(Array):

    def __init__(self, count_x, count_y, x_scale=1.0, y_scale=1.0, current_direction="x", matrix_format="csc",
                 beta_L=0, beta_C=0):
        x, y = HoneycombArray.get_xy(count_x, count_y, x_scale=x_scale, y_scale=y_scale)
        I_base = HoneycombArray.get_Ibase(count_x, count_y, current_direction=current_direction)
        nodes1, nodes2, remove_nodes = HoneycombArray.get_node12(count_x, count_y)
        node_remove_mask = np.zeros(x.size, dtype=bool)
        node_remove_mask[remove_nodes] = True
        junc_remove_mask, new_node_id = self._junction_remove_mask(nodes1, nodes2, node_remove_mask)
        x = np.delete(x, remove_nodes)
        y = np.delete(y, remove_nodes)
        I_base = np.delete(I_base, remove_nodes)
        nodes1 = new_node_id[nodes1][~junc_remove_mask]
        nodes2 = new_node_id[nodes2][~junc_remove_mask]
        super().__init__(x, y, nodes1, nodes2, external_current_basis=I_base,
                         matrix_format=matrix_format, beta_L=beta_L, beta_C=beta_C)

    @staticmethod
    def get_xy(count_x, count_y, x_scale=1.0, y_scale=1.0):
        y, x = np.mgrid[0:count_y, 0:count_x]
        x1, y1 = 3.0 * x, np.sqrt(3.0) * y
        nodes_x = np.concatenate((x1, x1 + 0.5, x1 + 1.5, x1 + 2), axis=0)
        nodes_y = np.concatenate((y1, y1 + np.sqrt(0.75), y1 + np.sqrt(0.75), y1), axis=0)
        return x_scale * nodes_x, y_scale * nodes_y

    @staticmethod
    def get_node12(count_x, count_y):
        s = count_x * count_y
        idx = np.arange(count_x * count_y).reshape(count_y, count_x)
        nodes1 = (idx,   idx[:-1, :]+s, idx+s,   idx[:-1, :]+2*s, idx+2*s, idx[:, :-1]+3*s)
        nodes2 = (idx+s, idx[1:, :],    idx+2*s, idx[1:, :]+3*s,  idx+3*s, idx[:, 1:])
        nodes1 = np.concatenate(tuple([n1.flatten() for n1 in nodes1]))
        nodes2 = np.concatenate(tuple([n2.flatten() for n2 in nodes2]))
        remove_nodes = [0, idx[0, -1] + 3 * s]
        return nodes1, nodes2, remove_nodes

    @staticmethod
    def get_Ibase(count_x, count_y, current_direction="x"):
        y, x = np.mgrid[0:count_y, 0:count_x]
        z = np.zeros((count_y, count_x), dtype=int)
        if current_direction == 'x':
            I_base = np.concatenate((x==0, z, z, -(x==(count_x-1)).astype(int)), axis=0)
        elif current_direction == 'y':
            I_base = np.concatenate(((y==0).astype(int), -(y==(count_y-1)).astype(int),
                                     -(y==(count_y-1)).astype(int), (y==0).astype(int)), axis=0)
            I_base[count_y, 0] = 1
            I_base[2 * count_y, -1] = 1
        else:
            raise ValueError("Invalid current direction. Choose 'x' or 'y'.")
        return I_base

class TriangularArray(Array):

    def __init__(self, count_x, count_y, x_scale=1.0, y_scale=1.0, current_direction='x', matrix_format="csc",
                 beta_L=0, beta_C=0):
        x, y = TriangularArray.get_xy(count_x, count_y, x_scale=x_scale, y_scale=y_scale)
        I_base = TriangularArray.get_Ibase(count_x, count_y, current_direction=current_direction)
        nodes1, nodes2 = TriangularArray.get_node12(count_x, count_y)
        super().__init__(x, y, nodes1, nodes2, external_current_basis=I_base,
                         matrix_format=matrix_format, beta_L=beta_L, beta_C=beta_C)


    @staticmethod
    def get_xy(count_x, count_y, x_scale=1.0, y_scale=1.0):
        y, x = np.mgrid[0:count_y, 0:count_x]
        x1, y1 = x, np.sqrt(3.0) * y
        nodes_x = np.concatenate((x1, x1 + 0.5), axis=0)
        nodes_y = np.concatenate((y1, y1 + np.sqrt(0.75)), axis=0)
        return x_scale * nodes_x, y_scale * nodes_y

    @staticmethod
    def get_Ibase(count_x, count_y, current_direction="x"):
        y, x = np.mgrid[0:count_y, 0:count_x]
        if current_direction == 'x':
            I_base = np.concatenate((x==0, -(x==(count_x-1)).astype(int)), axis=0)
        elif current_direction == 'y':
            I_base = np.concatenate((y==0, -(y==(count_y-1)).astype(int)), axis=0)
        else:
            raise ValueError("Invalid current direction. Choose 'x' or 'y'.")
        return I_base

    @staticmethod
    def get_node12(count_x, count_y):
        idx = np.arange(count_x * count_y).reshape(count_y, count_x)
        s = count_x * count_y
        nodes1 = (idx,   idx[:, :-1], idx[:-1, :]+s, idx[:-1, :-1]+s, idx[:, :-1]+s, idx[:, 1:])
        nodes2 = (idx+s, idx[:, 1:],  idx[1:, :],    idx[1:, 1:],     idx[:, 1:]+s,  idx[:, :-1]+s)
        nodes1 = np.concatenate(tuple([n1.flatten() for n1 in nodes1]))
        nodes2 = np.concatenate(tuple([n2.flatten() for n2 in nodes2]))
        return nodes1, nodes2
