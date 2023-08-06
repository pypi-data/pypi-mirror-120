from __future__ import annotations

from josephson_junction_array import Array
import numpy as np
import scipy.linalg
import scipy.sparse.linalg

from static_problem import DefaultCurrentPhaseRelation

from static_problem import StaticConfiguration, StaticProblem
from stencil_derivative import stencil_derivative


__all__ = ["InitialCondition", "DefaultIntialCondition",
           "ZeroIntialCondition", "RandomInitialCondition",
           "DynamicProblem", "DynamicConfiguration"]


class InitialCondition:

    def generate(self, problem) -> StaticConfiguration:
        pass

    def _get_problem(self, problem: StaticProblem | DynamicProblem) -> StaticProblem:
        if isinstance(problem, DynamicProblem):
            return problem.get_static_problem(time_step=0)
        if isinstance(problem, StaticProblem):
            return problem.copy()
        raise ValueError("invalid problem")


class DefaultIntialCondition(InitialCondition):

    def generate(self, problem: StaticProblem | DynamicProblem) -> StaticConfiguration:
        return self._get_problem(problem).approximate(algorithm=1)


class ZeroIntialCondition(InitialCondition):


    def generate(self, problem: StaticProblem | DynamicProblem) -> StaticConfiguration:
        theta = np.zeros(problem.shape() + (problem.array.Nj(),), dtype=np.double)
        return StaticConfiguration(self._get_problem(problem), theta)


class RandomInitialCondition(InitialCondition):

    def __init__(self, amplitude=10):
        self.amplitude = amplitude

    def generate(self, problem: StaticProblem | DynamicProblem) -> StaticConfiguration:
        theta = self.amplitude * np.random.randn(*(problem.shape() + (problem.array.Nj(),)))
        return StaticConfiguration(self._get_problem(problem), theta)


class DynamicProblem:
    """
    Define multiple dynamic JJA problems problems with varying parameters.

    All problems are computed in one call, which is generally much faster than
    computing individual problems consecutively.

    Use self.compute(...) to obtain a DynamicConfiguration object containing the
    resulting time evolution.

    One can specify various parameters:

    Physical parameters:       symbol  default
     - time_step               dt      0.05
     - time_step_count         Nt      100
     - current_phase_relation  cp      DefaultCurrentPhaseRelation()

    Problem space parameters: symbol  default    shape
     - external_current        Iext    0.0        (..., Nt or 1)
     - frustration             f       0.0        (..., Np or 1)
     - phase_zone              z       0          (..., Np or 1)
     - temperature             T       0.0        (..., Nj or 1, Nt or 1)
     - batteries               B       0.0        (..., Nj or 1, Nt or 1)

    The variable ... shapes form the "problem space" and must be numpy-broadcast-compatible.
    The pr_shape can be found with self.shape() and its dimension count ndim=self.ndim()

    So the shape of the problem space is:
    pr_shape = np.broadcast_shapes(Iext.shape, f.shape[:-1], z.shape[:-1], T.shape[:-1])

    Store parameters:     default   type
     - store_time_steps   None      None or anything that can index an (Nt,) array  (None -> all points)
     - store_theta        True
     - store_voltage      True
     - store_current      True

    Algorithm parameters:
     - voltage_scheme

    """

    def __init__(self, array: Array, time_step=0.05, time_step_count=100,
                 current_phase_relation=DefaultCurrentPhaseRelation(),
                 external_current=0.0, frustration=0.0, phase_zone=0,
                 temperature=0.0, batteries=0.0, store_time_steps=None,
                 store_theta=True, store_voltage=True, store_current=True,
                 voltage_scheme="forward"):
        self.array = array
        self.time_step = time_step
        self.time_step_count = time_step_count
        self.current_phase_relation = current_phase_relation
        self.external_current = np.atleast_1d(np.array(external_current, dtype=np.double))
        self.frustration = np.atleast_1d(np.array(frustration, dtype=np.double))
        self.phase_zone = np.atleast_1d(np.array(phase_zone, dtype=int))
        self.temperature = np.atleast_2d(np.array(temperature, dtype=np.double))
        self.batteries = np.atleast_2d(np.array(batteries, dtype=np.double))
        self.store_time_steps = store_time_steps
        if self.store_time_steps is None:
            self.store_time_steps = np.ones(self.Nt(), dtype=bool)
        if not isinstance(self.store_time_steps.dtype, (bool, np.bool)):
            try:
                self.store_time_steps = np.zeros(self.Nt(), dtype=bool)
                self.store_time_steps[store_time_steps] = True
            except:
                raise ValueError("Invalid store_time_steps; must be None, mask, slice or index array")
        self.store_theta = store_theta
        self.store_voltage = store_voltage
        self.store_current = store_current
        self.voltage_scheme = self._set_voltage_scheme(voltage_scheme)
        self.prepared_Ip = None
        self.prepared_IpJ = None
        self.prepared_df = None
        self.prepared_g = None

    def _set_voltage_scheme(self, voltage_scheme):
        if voltage_scheme in ("forward", None):
            return [0, -1, 1]
        if voltage_scheme == "central":
            return [-0.5, 0, 0.5]
        if voltage_scheme == "backward":
            return [-1, 1, 0]
        return voltage_scheme

    def get_static_problem(self, time_step=0) -> StaticProblem:
        return StaticProblem(self.array, external_current=self.external_current[..., time_step],
                             frustration=self.frustration, phase_zone=self.phase_zone,
                             target_vortex_configuration=self.phase_zone,
                             current_phase_relation=self.current_phase_relation)

    def to_gpu(self):
        pass

    def shape(self):
        return np.broadcast_shapes(self.external_current.shape[:-1], self.frustration.shape[:-1],
                                   self.phase_zone.shape[:-1], self.phase_zone.shape[:-1],
                                   self.temperature.shape[:-2])

    def ndim(self):
        return len(self.shape())

    def __getitem__(self, item):
        # I_sh = self.external_current.shape
        # f_sh = self.frustration.shape
        # z_sh = self.phase_zone.shape
        # T_sh = self.temperature.shape
        # B_sh = self.batteries.shape
        # shape = np.broadcast_shapes(I_sh[:-1], f_sh[:-1], z_sh[:-1], T_sh[:-2], B_sh[:-2])
        # numpy_broadcast_object = NumpyIndex(shape)[item]
        # keys = numpy_broadcast_object.multi_shape((I_sh[:-1], f_sh[:-1], z_sh[:-1], T_sh[:-2], B_sh[:-2]))
        # s = (slice(None),)
        # return DynamicProblem(self.array, time_step=self.time_step, time_step_count=self.time_step_count,
        #                       current_phase_relation=self.current_phase_relation,
        #                       external_current=self.external_current[keys[0] + s],
        #                       frustration=self.frustration[keys[1] + s],
        #                       phase_zone=self.phase_zone[keys[2] + s],
        #                       temperature=self.temperature[keys[3] + s + s],
        #                       batteries=self.batteries[keys[4] + s + s],
        #                       store_time_steps=self.store_time_steps, store_theta=self.store_theta,
        #                       store_current=self.store_current, store_voltage=self.store_voltage,
        #                       voltage_scheme=self.voltage_scheme)

        if not isinstance(item, tuple):
            item = (item,)
        Nj = np.max([self.temperature.shape[-2], self.batteries.shape[-2]])
        Np = np.max([self.frustration.shape[-1], self.phase_zone.shape[-1]])
        Nt = np.max([self.external_current.shape[-1], self.temperature.shape[-1], self.batteries.shape[-1]])
        self.external_current = np.broadcast_to(self.external_current, self.shape() + (Nt,))
        self.frustration = np.broadcast_to(self.frustration, self.shape() + (Np,))
        self.phase_zone = np.broadcast_to(self.phase_zone, self.shape() + (Np,))
        self.temperature = np.broadcast_to(self.temperature, self.shape()+ (Nj, Nt))
        self.batteries = np.broadcast_to(self.batteries, self.shape() + (Nj, Nt))
        s = (slice(None),)
        return DynamicProblem(self.array, time_step=self.time_step, time_step_count=self.time_step_count,
                              current_phase_relation=self.current_phase_relation,
                              external_current=self.external_current[item + s],
                              frustration=self.frustration[item + s],
                              phase_zone=self.phase_zone[item + s],
                              temperature=self.temperature[item + s + s],
                              batteries=self.batteries[item + s + s],
                              store_time_steps=self.store_time_steps, store_theta=self.store_theta,
                              store_current=self.store_current, store_voltage=self.store_voltage,
                              voltage_scheme=self.voltage_scheme)

    def get_array(self) -> Array:
        return self.array

    def Nt(self):
        return self.time_step_count

    def NtO(self):
        return np.asscalar(np.sum(self.store_time_steps))

    def dt(self):
        return self.time_step

    def Iext(self, time_step) -> np.ndarray:
        if self.external_current.shape[-1] > 1:
            return self.external_current[..., time_step]
        return self.external_current[..., 0]

    def f(self) -> np.ndarray:
        return self.frustration

    def z(self) -> np.ndarray:
        return self.phase_zone

    def T(self, time_step):
        if self.temperature.shape[-1] > 1:
            return self.temperature[..., time_step]
        return self.temperature[..., 0]

    def B(self, time_step):
        if self.batteries.shape[-1] > 1:
            return self.batteries[..., time_step]
        return self.batteries[..., 0]

    def cp(self, Ic, theta):
        return self.current_phase_relation.eval(Ic, theta)

    def dcp(self, Ic, theta):
        return self.current_phase_relation.d_eval(Ic, theta)

    def icp(self, Ic, theta):
        return self.current_phase_relation.i_eval(Ic, theta)

    def Ip(self, time_step):
        if self.external_current.shape[-1] > 1:
            return self.array._Ibase_reduced() * self.Iext(time_step)[..., None]
        else:
            if self.prepared_Ip is None:
                self.prepared_Ip = self.array._Ibase_reduced() * self.Iext(time_step)[..., None]
            return self.prepared_Ip

    def IpJ(self, time_step):
        if self.external_current.shape[-1] > 1:
            return self.array._IbaseJ() * self.Iext(time_step)[..., None]
        else:
            if self.prepared_IpJ is None:
                self.prepared_IpJ = self.array._IbaseJ() * self.Iext(time_step)[..., None]
            return self.prepared_IpJ

    def df(self):
        if self.prepared_df is None:
            self.prepared_df = 2 * np.pi * (self.z() - self.array.areas * self.f())
        return self.prepared_df

    def g(self):
        if self.prepared_g is None:
            s = self.array.solver
            Asq_solver = s.get_Asq_solver()
            self.prepared_g = 2 * np.pi * s.AT_dot(Asq_solver(s.pack(self.z() - self.array.areas * self.f())), p=False)
        return self.prepared_g

    def compute(self, step0_init: StaticConfiguration | InitialCondition = None,
                step1_init: StaticConfiguration | InitialCondition = None,
                rounding_flux_drift_correction=False) -> DynamicConfiguration:
        """
        Compute time evolution on an Josephson Array.

        Requires an initial configuration; step0_init. Must be None, InitialCondition or
        StaticConfiguration. If None; it is set to ZeroInitialCondition()

        If the array has capacitance, requires a second initial configuration; step1_init. If
        this is set to None, it will be assigned the value of step0_init.

        Algorithm is 0 or 1, only applies if there is no inductance.

        If there is no inductance and algorithm=0; the initial condition must obey A(th-g) = 0.
        If this is not obeyed, it is automatically projected to obey the constraint. Due to numerical
        rounding, it will slowly drift away from this condition. Use rounding_flux_drift_correction=True
        to apply projection every 100 timesteps.

        """
        algorithm = 0       #

        if step0_init is None:
            step0_init = ZeroIntialCondition()
        if isinstance(step0_init, InitialCondition):
            step0_init = step0_init.generate(self)
        if self.array.has_capacitance():
            if step1_init is None:
                step1_init = step0_init
            if isinstance(step1_init, InitialCondition):
                step1_init = step1_init.generate(self)
            if self.array.has_inductance():
                th, V, I = _dynamic_compute_inductance_capacitance(self, step0_init, step1_init)
            else:
                if algorithm == 0:
                    th, V, I = _static_compute_no_inductance_capacitance_0(self, step0_init, step1_init,
                                                                           rounding_flux_drift_correction)
                elif algorithm == 1:
                    th, V, I = _static_compute_no_inductance_capacitance_1(self, step0_init, step1_init)
                else:
                    raise ValueError("invalid algorithm")
        else:
            if self.array.has_inductance():
                th, V, I = _dynamic_compute_inductance_no_capacitance(self, step0_init)
            else:
                if algorithm == 0:
                    th, V, I = _static_compute_no_inductance_no_capacitance_0(self, step0_init,
                                                                              rounding_flux_drift_correction)
                elif algorithm == 1:
                    th, V, I = _static_compute_no_inductance_no_capacitance_1(self, step0_init)
                else:
                    raise ValueError("invalid algorithm")

        return DynamicConfiguration(self, th, V, I)

    def __str__(self):
        return "dynamic problem: " + self.shape().__str__() + \
               "\n\ttime: " + self.time_step_count.__str__() + " steps of " + self.time_step.__str__() + \
               "\n\texternal current: " + self.external_current.shape.__str__() + \
               "\n\tfrustration: " + self.frustration.shape.__str__() + \
               "\n\ttemperature: " + self.temperature.shape.__str__() + \
               "\n\tphase zone: " + self.phase_zone.shape.__str__() + \
               "\n\tcurrent-phase relation: " + self.current_phase_relation.__str__()


class DynamicConfiguration:
    """
    Represents an array (of shape pr_shape) of configurations of a Josephson
    array. It is defined by a problem, array and any of the quantities
    theta, current and voltage. These must be of shape (*problem.shape(), Nj, NtO).

    One can query several properties of the array configurations:

     (property)                           (symbol)           (needs)    (shape)
     - phases                             phi                th         (pr_shape, Nn, NtO)
     - gauge_invariant_phase_difference   theta                         (pr_shape, Nj, NtO)
     - vortex_configuration               n                  th         (pr_shape, Nj, NtO)
     - junction_current                   I                             (pr_shape, Nj, NtO)
     - path_current                       J                  I          (pr_shape, Np, NtO)
                                          flux               I          (pr_shape, Nn, NtO)
                                          V                             (pr_shape, Nj, NtO)
                                          U                  V          (pr_shape, Nn, NtO)
                                          V_array            V          (pr_shape, NtO)
     - josephson_energy                   EJ                 th         (pr_shape, Nj, NtO)
     - magnetic_energy                    EM                 I          (pr_shape, Nj, NtO)
                                          EC                 V          (pr_shape, Nj, NtO)
     - total_energy                       Etot               th,(I),(V) (pr_shape, Nj, NtO)
                                          I_thermal          th         (pr_shape, Nj, NtO)
                                          J_thermal          th         (pr_shape, Np, NtO)
                                          flux_thermal       th         (pr_shape, Np, NtO)
                                          V_thermal          th         (pr_shape, Nj, NtO)
                                          V_junc_thermal     th         (pr_shape, Nj, NtO)
                                          U_thermal          th         (pr_shape, Nn, NtO)
                                          V_array_thermal    th         (pr_shape, NtO)
                                          EJ_thermal         th         (pr_shape, Nj, NtO)
                                          EM_thermal         th         (pr_shape, Nj, NtO)
                                          EC_thermal         th         (pr_shape, Nj, NtO)

    A property query is done with te command .get_[symbol]()

    DynamicProblems only store theta, current and voltage data at specified timepoints,
    other queried properties must be calculated from that. The above table shows which
    quantities need to be stored to be able to query a certain property. (parenthesis
    mean quantities may be needed).

    Thermal quantities are based only on theta, and represent "thermal averages", in the
    sense that derivatives are computed on theta over the data at the queried timepoints
    (nót the stored timepoints). This naturally smooths the quantity, which filters the
    thermal noise present at finite temperatures.

    """

    def __init__(self, problem: DynamicProblem, theta=None, voltage=None,
                 current=None):
        self.problem = problem
        self.theta = theta
        self.voltage = voltage
        self.current = current

    def shape(self):
        return self.problem.shape()

    def array(self) -> Array:
        return self.problem.array

    def select_static_configuration(self, time_step) -> StaticConfiguration:
        if self.theta is None:
            raise ValueError("Theta not stored; cannot select static configuration.")
        problem = StaticProblem(self.array(), external_current=self.problem.external_current[..., time_step],
                                frustration=self.problem.frustration,
                                phase_zone=self.problem.phase_zone,
                                target_vortex_configuration=self.get_n(time_step),
                                current_phase_relation=self.problem.current_phase_relation)
        return StaticConfiguration(problem, self.theta[..., time_step])

    def _get_time_points(self, time_points_in):
        time_points_mask = time_points_in
        if time_points_mask is None:
            time_points_mask = self.problem.store_time_steps
        if not hasattr(time_points_mask, "dtype"):
            time_points_mask = np.array(time_points_mask)
        if not (time_points_mask.dtype in (bool, np.bool)):
            try:
                time_points_mask = np.zeros(self.problem.Nt(), dtype=bool)
                time_points_mask[time_points_in] = True
            except:
                raise ValueError("Invalid time_points; must be None, mask, slice or index array")
        # if time_points_mask is None:
        #     return np.arange(self.problem.NtO()), self.problem.NtO(), np.flatnonzero(self.problem.store_time_steps)
        if not np.all(self.problem.store_time_steps[time_points_mask]):
            raise ValueError("selected time_points that are not stored during computation")
        time_points = np.flatnonzero(time_points_mask)
        time_points_idx = (np.cumsum(self.problem.store_time_steps) - self.problem.store_time_steps)[time_points_mask]
        return time_points_idx, len(time_points), time_points

    def raise_prop_error(self, has_prop, quantity, missing_quantity):
        if has_prop:
            raise ValueError("cannot determine " + quantity + "; configuration needs " + missing_quantity + " property")

    # theta-based quantities
    def get_phi(self, select_time_points=None) -> np.ndarray:
        s = self.array().solver
        Msq_solver = s.get_Msq_solver()
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.theta is None, "phi", "theta")
        phi = np.zeros(self.problem.shape() + (self.array().Nnr(), Nt), dtype=np.double)
        for i, tp in enumerate(time_points_idx):
            phi[..., i] = s.unpack(Msq_solver(s.M_dot(self.theta[..., tp], u=False)))
        return phi

    def get_theta(self, select_time_points=None) -> np.ndarray:
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.theta is None, "theta", "theta")
        return self.theta[..., time_points_idx]

    def get_n(self, select_time_points=None) -> np.ndarray:
        s = self.array().solver
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.theta is None, "n", "theta")
        n = np.zeros(self.problem.shape() + (self.array().Np(), Nt), dtype=int)
        for i, tp in enumerate(time_points_idx):
            n[..., i] = self.problem.z() - s.A_dot(np.round(self.theta[..., tp] / (2 * np.pi))).astype(int)
        return n

    def get_EJ(self, select_time_points=None) -> np.ndarray:
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.theta is None, "EJ", "theta")
        EJ = np.zeros(self.problem.shape() + (self.array().Nj(), Nt), dtype=np.double)
        for i, tp in enumerate(time_points_idx):
            EJ[..., i] = self.problem.icp(self.array().Ic(), self.theta[..., tp])
        return EJ

    def get_I_thermal(self, select_time_points=None, first_derivative_stencil=(-1, 1),
                      second_derivative_stencil=(-1, 0, 1)):
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        t = time_points * self.problem.dt()
        V_thermal = self.get_V_junc_thermal(select_time_points, derivative_stencil=first_derivative_stencil)
        I_thermal = self.problem.cp(self.array().Ic()[..., None], self.theta[..., time_points_idx])
        I_thermal += V_thermal / self.array().R()[..., None]
        if self.array().has_capacitance():
            C = self.array().C()
            ddV = stencil_derivative(t, self.theta[..., time_points_idx], second_derivative_stencil, order=2)
            I_thermal += ddV * C[..., None]
        return I_thermal

    def get_J_thermal(self, select_time_points=None):
        s = self.array().solver
        Asq_solver = s.get_Asq_solver()
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.theta is None, "J_thermal", "theta")
        J_thermal = np.zeros(self.problem.shape() + (self.array().Np(), Nt), dtype=np.double)
        I_thermal = self.get_I_thermal(select_time_points)
        for i, tp in enumerate(time_points_idx):
            J_thermal[..., i] = s.unpack(Asq_solver(s.A_dot(I_thermal[..., i], u=False)))
        return J_thermal

    def get_flux_thermal(self, select_time_points=None) -> np.ndarray:
        s = self.array().solver
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.theta is None, "flux_thermal", "theta")
        if self.array().has_inductance():
            flux_thermal = np.zeros(self.problem.shape() + (self.array().Np(), Nt), dtype=np.double)
            I_thermal = self.get_I_thermal(select_time_points)
            for i, tp in enumerate(time_points_idx):
                flux_thermal[..., i] = s.A_dot(s.L_dot(I_thermal[..., i], u=False), p=False) / (2 * np.pi)
            return flux_thermal
        else:
            return np.zeros(self.problem.shape() + (self.array().Np(), Nt), dtype=np.double)

    def get_EM_thermal(self, select_time_points=None) -> np.ndarray:
        s = self.array().solver
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        if self.array().has_inductance():
            EM_thermal = np.zeros(self.problem.shape() + (self.array().Nj(), Nt), dtype=np.double)
            I_thermal = self.get_I_thermal(select_time_points)
            for i, tp in enumerate(time_points_idx):
                EM_thermal[..., i] = 0.5 * s.L_dot(I_thermal[..., i] ** 2)
            return EM_thermal
        else:
            return np.zeros(self.problem.shape() + (self.array().Nj(), Nt), dtype=np.double)

    def get_EC_thermal(self, select_time_points=None):
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        if self.array().has_capacitance():
            EC_thermal = np.zeros(self.problem.shape() + (self.array().Nj(), Nt), dtype=np.double)
            V_thermal = self.get_V_thermal(select_time_points)
            for i, tp in enumerate(time_points_idx):
                EC_thermal[..., i] = 0.5 * self.array().C() * V_thermal[..., i] ** 2
            return EC_thermal
        else:
            return np.zeros(self.problem.shape() + (self.array().Nj(), Nt), dtype=np.double)

    def get_V_thermal(self, select_time_points=None, first_derivative_stencil=(-1, 1),
                      second_derivative_stencil=(-1, 0, 1)) -> np.ndarray:
        s = self.array().solver
        V_thermal = self.get_V_junc_thermal(select_time_points, derivative_stencil=first_derivative_stencil)
        if self.array().has_inductance():
            time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
            t = time_points * self.problem.dt()
            I_thermal = self.get_I_thermal(select_time_points, first_derivative_stencil=first_derivative_stencil,
                                           second_derivative_stencil=second_derivative_stencil)
            I_thermal = stencil_derivative(t, I_thermal, stencil=first_derivative_stencil, order=1)
            for i, tp in enumerate(time_points_idx):
                V_thermal[..., i] += s.L_dot(I_thermal[..., i]) + self.problem.B(tp)
        return V_thermal

    def get_V_junc_thermal(self, select_time_points=None, derivative_stencil=(-1, 1)) -> np.ndarray:
        self.raise_prop_error(self.theta is None, "V_junc_thermal", "theta")
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        t = time_points * self.problem.dt()
        return stencil_derivative(t, self.theta[..., time_points_idx], derivative_stencil, order=1)

    def get_U_thermal(self, select_time_points=None):
        s = self.array().solver
        Msq_solver = s.get_Msq_solver()
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.theta is None, "U_thermal", "theta")
        U_thermal = np.zeros(self.problem.shape() + (self.array().Nnr(), Nt), dtype=np.double)
        V_thermal = self.get_V_thermal(select_time_points)
        for i, tp in enumerate(time_points_idx):
            U_thermal[..., i] = s.unpack(Msq_solver(s.M_dot(V_thermal[..., i], u=False)))
        return U_thermal

    def get_V_array_thermal(self, select_time_points=None):
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.theta is None, "V_array_thermal", "theta")
        V_array_thermal = np.zeros(self.problem.shape() + (Nt,), dtype=np.double)
        V_thermal = self.get_V_thermal(select_time_points)
        for i, tp in enumerate(time_points_idx):
            V_array_thermal[..., i] = np.mean(self.array()._IbaseJ() * V_thermal[..., i], axis=-1)/ np.mean(self.array()._IbaseJ())
            # / self.array().Ibase_total()
        return V_array_thermal

    def get_V_array_time_interval(self, start_fraction=0.0, end_fraction=1.0):
        tp = np.flatnonzero(self.problem.store_time_steps)
        p1 = tp[np.argmin(np.abs(tp - start_fraction * self.problem.Nt()))]
        p2 = tp[np.argmin(np.abs(tp - 0.5 * (start_fraction + end_fraction) * self.problem.Nt()))]
        p3 = tp[np.argmin(np.abs(tp - end_fraction * self.problem.Nt()))]
        V = self.get_V_array_thermal(select_time_points=[p1, p2, p3])
        return V[..., 1]

    # I-based quantities
    def get_I(self, select_time_points=None) -> np.ndarray:
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.current is None, "I", "current")
        return self.current[..., time_points_idx]

    def get_J(self, select_time_points=None) -> np.ndarray:
        s = self.array().solver
        Asq_solver = s.get_Asq_solver()
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.current is None, "J", "current")
        J = np.zeros(self.problem.shape() + (self.array().Np(), Nt), dtype=np.double)
        for i, tp in enumerate(time_points_idx):
            J[..., i] = s.unpack(Asq_solver(s.A_dot(self.current[..., tp], u=False)))
        return J

    def get_flux(self, select_time_points=None) -> np.ndarray:
        s = self.array().solver
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        if self.array().has_inductance():
            self.raise_prop_error(self.current is None, "flux", "current")
            flux = np.zeros(self.problem.shape() + (self.array().Np(), Nt), dtype=np.double)
            for i, tp in enumerate(time_points_idx):
                flux[..., i] = s.A_dot(s.L_dot(self.current[..., tp], u=False), p=False) / (2 * np.pi)
            return flux
        else:
            return np.zeros(self.problem.shape() + (self.array().Np(), Nt), dtype=np.double)

    def get_EM(self, select_time_points=None) -> np.ndarray:
        s = self.array().solver
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        if self.array().has_inductance():
            self.raise_prop_error(self.current is None, "EM", "current")
            EM = np.zeros(self.problem.shape() + (self.array().Nj(), Nt), dtype=np.double)
            for i, tp in enumerate(time_points_idx):
                EM[..., i] = 0.5 * s.L_dot(self.current[..., tp] ** 2)
            return EM
        else:
            return np.zeros(self.problem.shape() + (self.array().Nj(), Nt), dtype=np.double)

    # V-based quantities
    def get_V(self, select_time_points=None):
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.voltage is None, "V", "voltage")
        return self.voltage[..., time_points_idx]

    def get_U(self, select_time_points=None):
        s = self.array().solver
        Msq_solver = s.get_Msq_solver()
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.voltage is None, "U", "voltage")
        U = np.zeros(self.problem.shape() + (self.array().Nnr(), Nt), dtype=np.double)
        for i, tp in enumerate(time_points_idx):
            U[..., i] = s.unpack(Msq_solver(s.M_dot(self.voltage[..., tp], u=False)))
        return U

    def get_V_array(self, select_time_points=None):
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        self.raise_prop_error(self.voltage is None, "V_array", "voltage")
        V_array = np.zeros(self.problem.shape() + (Nt,), dtype=np.double)
        for i, tp in enumerate(time_points_idx):
            V_array[..., i] = np.mean(self.array()._IbaseJ() * self.voltage[..., tp], axis=-1)/ np.mean(self.array().IbaseJ())
        return V_array

    def get_Etot_thermal(self, select_time_points=None) -> np.ndarray:
        return self.get_EJ(select_time_points) + self.get_EM_thermal(select_time_points) + \
               self.get_EC_thermal(select_time_points)

    def get_EC(self, select_time_points=None):
        time_points_idx, Nt, time_points = self._get_time_points(select_time_points)
        if self.array().has_capacitance():
            self.raise_prop_error(self.voltage is None, "EC", "voltage")
            EC = np.zeros(self.problem.shape() + (self.array().Nj(), Nt), dtype=np.double)
            for i, tp in enumerate(time_points_idx):
                EC[..., i] = 0.5 * self.array().C() * self.voltage[..., tp] ** 2
            return EC
        else:
            return np.zeros(self.problem.shape() + (self.array().Nj(), Nt), dtype=np.double)

    def get_Etot(self, select_time_points=None) -> np.ndarray:
        return self.get_EJ(select_time_points) + self.get_EM(select_time_points) + self.get_EC(select_time_points)

    # winding rules
    def obeys_winding_rules(self, path_tol=1E-5):
        return self.get_error_winding_rules() < path_tol

    def get_error_winding_rules(self) -> np.ndarray:
        # TODO implemented already for static configurations?
        s = self.array().solver
        df = 2.0 * np.pi * (self.problem.z() - self.problem.f() * self.array().areas)
        error = np.zeros(self.problem.shape() + (self.problem.NtO(),), dtype=np.double)
        if self.array().has_inductance():
            I = self.get_I()
            for i in range(self.problem.NtO()):
                x = self.theta[..., i] + s.L_dot(I[..., i])
                ref = np.max([0.2 * np.sqrt(self.array().Np()), scipy.linalg.norm(x, axis=-1), scipy.linalg.norm(df, axis=-1)])
                error[..., i] = scipy.linalg.norm(s.A_dot(x) - df, axis=-1) / ref
        else:
            for i in range(self.problem.NtO()):
                ref = np.max([0.2 * np.sqrt(self.array().Np()), scipy.linalg.norm(self.theta[..., i], axis=-1), scipy.linalg.norm(df, axis=-1)])
                error[..., i] = scipy.linalg.norm(s.A_dot(self.theta[..., i]) - df, axis=-1) / ref
        return error

    def project_onto_winding_rules(self):
        # TODO implemented already for static configurations?
        # maps th -> th + Dth after which winding rules are satisfied.
        # Dth = -AT*((A*AT)\(A*th - df)) where df = 2*pi*(z-area.*f)
        s = self.array().solver
        Asq_solver = s.get_Asq_solver()
        df = 2.0 * np.pi * s.pack(self.problem.z() - self.problem.f() * self.array().areas)
        for i in range(self.problem.NtO()):
            self.theta[..., i] -= s.AT_dot(Asq_solver(s.A_dot(self.theta[..., i], u=False) - df), p=False)

    def plot(self, time_point=0, show_vortices=True, vortex_diameter=0.25, vortex_color=(0, 0, 0),
                 anti_vortex_color=(0.8, 0.1, 0.2), vortex_alpha=1, show_grid=True, grid_width=1,
                 grid_color=(0.3, 0.5, 0.9), grid_alpha=0.5, show_colorbar=True, show_arrows=True,
                 arrow_quantity="I", arrow_width=0.005, arrow_scale=1, arrow_headwidth=3, arrow_headlength=5,
                 arrow_headaxislength=4.5, arrow_minshaft=1, arrow_minlength=1, arrow_color=(0.2, 0.4, 0.7),
                 arrow_alpha=1, show_nodes=True, node_diameter=0.2,
                 node_face_color=(1,1,1), node_edge_color=(0, 0, 0), node_alpha=1, show_node_quantity=False,
                 node_quantity="phase", node_quantity_cmap=None, node_quantity_clim=(0, 1), node_quantity_alpha=1,
                 node_quantity_logarithmic_colors=False, show_path_quantity=False, path_quantity="n",
                 path_quantity_cmap=None, path_quantity_clim=(0, 1), path_quantity_alpha=1,
                 path_quantity_logarithmic_colors=False, figsize=None, title="", **kwargs):

        from array_visualize import ArrayPlot

        return ArrayPlot(self, time_point=time_point, show_vortices = show_vortices, vortex_diameter = vortex_diameter,
                         vortex_color = vortex_color, anti_vortex_color = anti_vortex_color,
                         vortex_alpha = vortex_alpha, show_grid = show_grid, grid_width = grid_width,
                         grid_color = grid_color, grid_alpha = grid_alpha, show_colorbar=show_colorbar,
                         show_arrows = show_arrows,
                         arrow_quantity = arrow_quantity, arrow_width = arrow_width, arrow_scale = arrow_scale,
                         arrow_headwidth = arrow_headwidth, arrow_headlength = arrow_headlength,
                         arrow_headaxislength = arrow_headaxislength, arrow_minshaft = arrow_minshaft,
                         arrow_minlength = arrow_minlength, arrow_color = arrow_color,
                         arrow_alpha = arrow_alpha, show_nodes = show_nodes, node_diameter = node_diameter,
                         node_face_color = node_face_color, node_edge_color = node_edge_color,
                         node_alpha = node_alpha, show_node_quantity = show_node_quantity,
                         node_quantity = node_quantity, node_quantity_cmap = node_quantity_cmap,
                         node_quantity_clim = node_quantity_clim, node_quantity_alpha = node_quantity_alpha,
                         node_quantity_logarithmic_colors=node_quantity_logarithmic_colors,
                         show_path_quantity = show_path_quantity, path_quantity = path_quantity,
                         path_quantity_cmap = path_quantity_cmap, path_quantity_clim = path_quantity_clim,
                         path_quantity_alpha = path_quantity_alpha,
                         path_quantity_logarithmic_colors=path_quantity_logarithmic_colors,
                         figsize = figsize, title=title, **kwargs).make()


    def animate(self, time_points=None, show_vortices=True,
                 vortex_diameter=0.25, vortex_color=(0, 0, 0), anti_vortex_color=(0.8, 0.1, 0.2),
                 vortex_alpha=1, show_grid=True, grid_width=1,
                 grid_color=(0.3, 0.5, 0.9), grid_alpha=0.5, show_colorbar=True, show_arrows=True, arrow_quantity="I",
                 arrow_width=0.005, arrow_scale=1, arrow_headwidth=3, arrow_headlength=5,
                 arrow_headaxislength=4.5, arrow_minshaft=1, arrow_minlength=1, arrow_color=(0.2, 0.4, 0.7),
                 arrow_alpha=1, show_nodes=True, node_diameter=0.2,
                 node_face_color=(1,1,1), node_edge_color=(0, 0, 0), node_alpha=1, show_node_quantity=False,
                 node_quantity="phase", node_quantity_cmap=None, node_quantity_clim=(0, 1), node_quantity_alpha=1,
                 node_quantity_logarithmic_colors=False,
                 show_path_quantity=False, path_quantity="n", path_quantity_cmap=None,
                 path_quantity_clim=(0, 1), path_quantity_alpha=1,
                 path_quantity_logarithmic_colors=False, figsize=None,
                 animate_interval=5, title=""):

        from array_visualize import ArrayMovie

        return ArrayMovie(self, time_points=time_points, show_vortices=show_vortices,
                          vortex_diameter=vortex_diameter, vortex_color=vortex_color,
                          anti_vortex_color=anti_vortex_color, vortex_alpha=vortex_alpha,
                          show_grid = show_grid, grid_width = grid_width,
                          grid_color = grid_color, grid_alpha = grid_alpha,
                          show_colorbar=show_colorbar, show_arrows = show_arrows,
                          arrow_quantity = arrow_quantity, arrow_width = arrow_width, arrow_scale = arrow_scale,
                          arrow_headwidth = arrow_headwidth, arrow_headlength = arrow_headlength,
                          arrow_headaxislength = arrow_headaxislength, arrow_minshaft = arrow_minshaft,
                          arrow_minlength = arrow_minlength, arrow_color = arrow_color,
                          arrow_alpha = arrow_alpha, show_nodes = show_nodes, node_diameter = node_diameter,
                          node_face_color = node_face_color, node_edge_color = node_edge_color,
                          node_alpha = node_alpha, show_node_quantity = show_node_quantity,
                          node_quantity = node_quantity, node_quantity_cmap = node_quantity_cmap,
                          node_quantity_clim = node_quantity_clim, node_quantity_alpha = node_quantity_alpha,
                          node_quantity_logarithmic_colors=node_quantity_logarithmic_colors,
                          show_path_quantity = show_path_quantity, path_quantity = path_quantity,
                          path_quantity_cmap = path_quantity_cmap, path_quantity_clim = path_quantity_clim,
                          path_quantity_alpha = path_quantity_alpha,
                          path_quantity_logarithmic_colors=path_quantity_logarithmic_colors,
                          figsize = figsize, animate_interval=animate_interval, title=title).show()


    def __str__(self):
        return "dynamic configuration: (" + ("th" + self.theta.shape.__str__() + ", ") * (self.theta is not None) + \
               ("I" + self.current.shape.__str__() + ", ") * (self.current is not None) + \
               ("V" + self.voltage.shape.__str__()) * (self.current is not None) + ")" + \
               "\nproblem: " + self.problem.__str__() + \
               "\narray: " + self.array().__str__()

def _initialize_output(prob: DynamicProblem, Nj, NtO):
    theta_out = np.zeros(prob.shape() + (Nj, NtO), dtype=np.double) if prob.store_theta else None
    V_out = np.zeros(prob.shape() + (Nj, NtO), dtype=np.double) if prob.store_theta else None
    I_out = np.zeros(prob.shape() + (Nj, NtO), dtype=np.double) if prob.store_theta else None
    return theta_out, V_out, I_out


def _static_compute_no_inductance_no_capacitance_0(prob: DynamicProblem,
                                                   step0_config: StaticConfiguration,
                                                   rounding_flux_drift_correction=True):
    array = prob.array
    Nj_shape = prob.shape() + (array.Nj(),)
    theta_out, V_out, I_out = _initialize_output(prob, array.Nj(), prob.NtO())
    time_step_list = (np.cumsum(prob.store_time_steps) - prob.store_time_steps).astype(int)
    s = array.solver
    R = array.R()
    Asq_solver = s.get_Asq_solver()
    AsqR_solver = s.get_A_sandwich_solver(R)
    Ic = array.Ic()
    dt = prob.dt()
    g = prob.g()
    theta_next = step0_config.theta
    fluc_prefactor = np.sqrt(2.0 / dt / R)

    if np.max(np.mean(np.abs(s.A_dot(theta_next - g)), axis=-1)) > 1E-6:
        print("warning: initial condition does not obey winding rules. A Projection is done fix this.")
        theta_next -= s.AT_dot(Asq_solver(s.A_dot(theta_next - g, u=False)), p=False)
    for i in range(prob.Nt()):
        theta = theta_next
        if rounding_flux_drift_correction and (i % 100) == 0:
            theta -= s.AT_dot(Asq_solver(s.A_dot(theta - g, u=False)), p=False)
        fluctuations = fluc_prefactor * np.random.randn(*Nj_shape) * np.sqrt(prob.T(i))
        y = prob.cp(Ic, theta) + fluctuations - prob.IpJ(i)
        theta_next = s.AT_dot(AsqR_solver(s.A_dot(R * y, u=False)), p=False)
        theta_next = theta - dt * R * (y - theta_next) + dt * prob.B(i)
        if prob.store_time_steps[i]:
            if prob.store_theta:
                theta_out[..., time_step_list[i]] = theta_next
            if prob.store_voltage:
                V_out[..., time_step_list[i]] = (theta_next - theta) / dt
            if prob.store_current:
                I_out[..., time_step_list[i]] = y + prob.IpJ(i) + (theta_next - theta) / dt / R
    return theta_out, V_out, I_out


def _dynamic_compute_inductance_no_capacitance(prob: DynamicProblem, step0_config: StaticConfiguration):
    array = prob.array
    s = array.solver
    R = array.R()
    Ic = array.Ic()
    dt = prob.dt()
    L_solver = s.get_L_sandwich_solver()
    theta_next = step0_config.theta
    Nj_shape = prob.shape() + (array.Nj(),)
    fluc_prefactor = np.sqrt(2.0 / dt / R)
    g = prob.g()
    IpJ = prob.IpJ(0)
    IpLJ = s.L_dot(IpJ)
    theta_out, V_out, I_out = _initialize_output(prob, array.Nj(), prob.NtO())
    time_step_list = (np.cumsum(prob.store_time_steps) - prob.store_time_steps).astype(int)
    for i in range(prob.Nt()):
        theta = theta_next
        if prob.external_current.shape[-1] > 1:
            IpJ = prob.IpJ(i)
            IpLJ = s.L_dot(IpJ)
        fluctuations = fluc_prefactor * np.random.randn(*Nj_shape) * np.sqrt(prob.T(i))
        y = prob.cp(Ic, theta) + fluctuations
        theta_next = s.AT_dot(L_solver(s.A_dot(g - theta - IpLJ, u=False)), p=False)
        theta_next = theta - prob.dt() * R * (y - IpJ - theta_next) + dt * prob.B(i)
        if prob.store_time_steps[i]:
            k = time_step_list[i]
            if prob.store_theta:
                theta_out[..., k] = theta_next
            if prob.store_voltage:
                V_out[..., k] = _compute_inductance_voltage(prob, i, (theta_next - theta) / dt)
            if prob.store_current:
                I_out[..., k] = y + (theta_next - theta) / dt / R
    return theta_out, V_out, I_out


def _static_compute_no_inductance_capacitance_0(prob: DynamicProblem,
                                                step0_config: StaticConfiguration,
                                                step1_config: StaticConfiguration,
                                                rounding_flux_drift_correction=True):
    array = prob.array
    s = array.solver
    R = array.R()
    C = array.C()
    Ic = array.Ic()
    dt = prob.dt()
    Asq_solver = s.get_Asq_solver()

    scheme = prob.voltage_scheme
    theta = step0_config.theta.copy()
    theta_next = step1_config.theta.copy()
    g = prob.g()
    if np.max(np.mean(np.abs(s.A_dot(theta - g)), axis=-1)) > 1E-6:
        print("warning: initial condition 0 does not obey winding rules. A Projection is done fix this.")
        theta -= s.AT_dot(Asq_solver(s.A_dot(theta - g, u=False)), p=False)

    if np.max(np.mean(np.abs(s.A_dot(theta_next - g)), axis=-1)) > 1E-6:
        print("warning: initial condition 1 does not obey winding rules. A Projection is done fix this.")
        theta_next -= s.AT_dot(Asq_solver(s.A_dot(theta_next - g, u=False)), p=False)
    Nj_shape = prob.shape() + (array.Nj(),)
    fluc_prefactor = np.sqrt(2.0 / dt / R)

    Cprev = C / (dt ** 2) + scheme[0] / (dt * R)
    C0 = -2.0 * C / (dt ** 2) + scheme[1] / (dt * R)
    Cnext = C / (dt ** 2) + scheme[2] / (dt * R)
    AsqC_solver = s.get_A_sandwich_solver(1.0 / Cnext)

    theta_out, V_out, I_out = _initialize_output(prob, array.Nj(), prob.NtO())
    time_step_list = (np.cumsum(prob.store_time_steps) - prob.store_time_steps).astype(int)
    for i in range(prob.Nt()):
        theta_prev = theta.copy()
        theta = theta_next.copy()
        if rounding_flux_drift_correction and (i % 100) == 0:
            theta -= s.AT_dot(Asq_solver(s.A_dot(theta - g, u=False)), p=False)
        fluctuations = fluc_prefactor * np.random.randn(*Nj_shape) * np.sqrt(prob.T(i))
        y = prob.cp(Ic, theta) + fluctuations - prob.IpJ(i) + Cprev * theta_prev + C0 * theta
        theta_next = (s.AT_dot(AsqC_solver(s.A_dot(y / Cnext + g, u=False)), p=False) - y) / Cnext + dt * prob.B(i)
        if prob.store_time_steps[i]:
            k = time_step_list[i]
            if prob.store_theta:
                theta_out[..., k] = theta_next
            if prob.store_voltage:
                V_out[..., k] = (scheme[0] * theta_prev + scheme[1] * theta + scheme[2] * theta_next) / dt
            if prob.store_current:
                I_out[..., k] = y + prob.IpJ(i) + Cnext * theta_next
    return theta_out, V_out, I_out


def _dynamic_compute_inductance_capacitance(prob: DynamicProblem,
                                            step0_config: StaticConfiguration,
                                            step1_config: StaticConfiguration):
    array = prob.array
    s = array.solver
    R = array.R()
    C = array.C()
    Ic = array.Ic()
    dt = prob.dt()
    g = prob.g()
    scheme = prob.voltage_scheme
    theta = step0_config.theta
    theta_next = step1_config.theta
    Nj_shape = prob.shape() + (array.Nj(),)
    fluc_prefactor = np.sqrt(2.0 / dt / R)
    L_solver = s.get_L_sandwich_solver()

    Cprev = C / (dt ** 2) + scheme[0] / (dt * R)
    C0 = -2.0 * C / (dt ** 2) + scheme[1] / (dt * R)
    Cnext = C / (dt ** 2) + scheme[2] / (dt * R)

    IpJ = prob.IpJ(0)
    IpLJ = s.L_dot(IpJ)
    theta_out, V_out, I_out = _initialize_output(prob, array.Nj(), prob.NtO())
    time_step_list = (np.cumsum(prob.store_time_steps) - prob.store_time_steps).astype(int)
    for i in range(prob.Nt()):
        theta_prev = theta
        theta = theta_next
        if prob.external_current.shape[-1] > 1:
            IpJ = prob.IpJ(i)
            IpLJ = s.L_dot(IpJ)
        fluctuations = fluc_prefactor * np.random.randn(*Nj_shape) * np.sqrt(prob.T(i))
        y = prob.cp(Ic, theta) + fluctuations - IpJ + Cprev * theta_prev + C0 * theta
        theta_next = (s.AT_dot(L_solver(s.A_dot(g - theta - IpLJ, u=False)), p=False) - y) / Cnext + dt * prob.B(i)
        if prob.store_time_steps[i]:
            k = time_step_list[i]
            if prob.store_theta:
                theta_out[..., k] = theta_next
            if prob.store_voltage:
                V_out[..., k] = _compute_inductance_voltage(prob, i, (scheme[0] * theta_prev + scheme[1] * theta +
                                                                      scheme[2] * theta_next) / dt)
            if prob.store_current:
                I_out[..., k] = y + prob.IpJ(i) + Cnext * theta_next
    return theta_out, V_out, I_out


def _compute_inductance_voltage(prob, i, theta_dot):
    array = prob.array
    s = array.solver
    dt = prob.dt()
    L_solver = s.get_L_sandwich_solver()
    if prob.external_current.shape[-1] > 1:
        if i == 0:
            theta_dot += s.L_dot(prob.IpJ(1) - prob.IpJ(0)) / dt
        elif i == (prob.Nt() - 1):
            theta_dot += s.L_dot(prob.IpJ(-1) - prob.IpJ(-2)) / dt
        else:
            theta_dot += s.L_dot(prob.IpJ(i + 1) - prob.IpJ(i - 1)) / (2.0 * dt)
    return theta_dot - s.L_dot(s.AT_dot(L_solver(s.A_dot(theta_dot, u=False)), u=False, p=False), p=False)


# Not officially supported alternative algorithms (for no-inductance case)
def _static_compute_no_inductance_no_capacitance_1(prob: DynamicProblem, step0_config: StaticConfiguration):
    array = prob.array
    Nj_shape = prob.shape() + (array.Nj(),)
    theta_out, V_out, I_out = _initialize_output(prob, array.Nj(), prob.NtO())
    time_step_list = (np.cumsum(prob.store_time_steps) - prob.store_time_steps).astype(int)

    s = array.solver
    R = array.R()
    Ic = array.Ic()
    dt = prob.dt()
    Msq_solver = s.get_Msq_solver()
    MsqR_solver = s.get_M_sandwich_solver(1.0 / R)

    phi_next = Msq_solver(s.M_dot(step0_config.theta, u=False))

    fluc_prefactor = np.sqrt(2.0 / dt / R)
    for i in range(prob.Nt()):
        phi = phi_next
        fluctuations = fluc_prefactor * np.random.randn(*Nj_shape) * np.sqrt(prob.T(i))
        y = prob.cp(Ic, s.MT_dot(phi, p=False)) + fluctuations - prob.IpJ(i)
        phi_next = phi + dt * MsqR_solver(s.M_dot(y, u=False))
        if prob.store_time_steps[i]:
            if prob.store_theta:
                theta_out[..., time_step_list[i]] = s.MT_dot(phi_next, p=False)
            if prob.store_voltage:
                V_out[..., time_step_list[i]] = s.MT_dot(phi_next - phi, p=False) / dt
            if prob.store_current:
                I_out[..., time_step_list[i]] = y + prob.IpJ(i) + s.MT_dot(phi_next - phi, p=False) / dt / R
    return theta_out, V_out, I_out


def _static_compute_no_inductance_capacitance_1(prob: DynamicProblem,
                                                step0_config: StaticConfiguration,
                                                step1_config: StaticConfiguration):
    array = prob.array
    s = array.solver
    R = array.R()
    C = array.C()
    Ic = array.Ic()
    dt = prob.dt()

    Msq_solver = s.get_Msq_solver()

    scheme = prob.voltage_scheme
    phi = Msq_solver(s.MT_dot(step0_config.theta, u=False))
    phi_next = Msq_solver(s.M_dot(step1_config.theta, u=False))
    Nj_shape = prob.shape() + (array.Nj(),)
    fluc_prefactor = np.sqrt(2.0 / dt / R)
    Cprev = C / (dt ** 2) + scheme[0] / (dt * R)
    C0 = -2.0 * C / (dt ** 2) + scheme[1] / (dt * R)
    Cnext = C / (dt ** 2) + scheme[2] / (dt * R)
    MsqC_solver = s.get_M_sandwich_solver(1 / Cnext)

    MsqA, MsqB = s.get_M_sandwich(Cprev), s.get_M_sandwich().get_M_sandwich(C0)

    theta_out, V_out, I_out = _initialize_output(prob, array.Nj(), prob.NtO())
    time_step_list = (np.cumsum(prob.store_time_steps) - prob.store_time_steps).astype(int)
    for i in range(prob.Nt()):
        phi_prev = phi
        phi = phi_next
        fluctuations = fluc_prefactor * np.random.randn(*Nj_shape) * np.sqrt(prob.T(i))
        y = prob.cp(Ic, s.MT_dot(phi, p=False)) + fluctuations - prob.IpJ(i)
        phi_next = phi + dt * MsqC_solver(s.M_dot(y, u=False) - s.dot(MsqA, phi_prev, p=False, u=False) -
                                          s.dot(MsqB, phi, p=False, u=False))
        if prob.store_time_steps[i]:
            k = time_step_list[i]
            if prob.store_theta:
                theta_out[..., k] = s.MT_dot(phi_next, p=False)
            if prob.store_voltage or prob.store_current:
                U = s.unpack(scheme[0] * phi_prev + scheme[1] * phi + scheme[2] * phi_next) / prob.dt()
            if prob.store_voltage:
                V_out[..., k] = s.MT_dot(U)
            if prob.store_current:
                dU = (phi_prev - 2.0 * phi + phi_next) / (dt ** 2)
                I_out[..., k] = y + prob.IpJ(i) + s.MT_dot(U / R + C * dU)
    return theta_out, V_out, I_out


