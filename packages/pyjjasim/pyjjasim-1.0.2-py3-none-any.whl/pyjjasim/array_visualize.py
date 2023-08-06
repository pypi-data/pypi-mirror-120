from __future__ import annotations

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import Normalize, LogNorm
import matplotlib.animation as animation
import matplotlib.cm as cm
matplotlib.use("TkAgg")

from josephson_junction_array import Array
from static_problem import StaticConfiguration
from dynamic_problem import DynamicConfiguration

__all__ = ["CircuitPlot", "ArrayPlot", "ArrayMovie"]

class CircuitPlot:

    def __init__(self, array: Array, show_nodes=True, show_node_ids=True,
                 node_labels=None, show_junctions=True, show_junction_directions=True,
                 show_junction_ids=True, junction_labels=None,
                 show_paths=True, show_path_directions=True,
                 show_path_ids=True, path_labels=None, figsize=None):
        self.array = array
        self.show_nodes = show_nodes
        self.show_node_ids = show_node_ids
        self.node_labels = node_labels
        self.show_junctions = show_junctions
        self.show_junction_directions = show_junction_directions
        self.show_junction_ids = show_junction_ids
        self.junction_labels = junction_labels
        self.show_paths = show_paths
        self.show_path_directions = show_path_directions
        self.show_path_ids = show_path_ids
        self.path_labels = path_labels
        self.figsize = figsize if figsize is not None else [6.4, 4.8]

    def show(self):
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        x, y = self.array.get_node_coordinates()
        x1, y1 = x[self.array.node1], y[self.array.node1]
        x2, y2 = x[self.array.node2], y[self.array.node2]
        xc, yc = self.array.centroids()
        pn = self.array.get_faces()
        I = 0.9
        xq = x1 + 0.5 * (1 - I) * (x2 - x1)
        yq = y1 + 0.5 * (1 - I) * (y2 - y1)
        dxq = I * (x2 - x1)
        dyq = I * (y2 - y1)
        if self.show_junction_directions:
            self.ax.quiver(xq, yq, dxq, dyq, color=[0.3,0.5,0.9], facecolor=[0.3,0.5,0.9], alpha=0.5, angles='xy', scale=1, scale_units='xy')
        if self.show_junction_ids:
            for i, (xn, yn) in enumerate(zip(0.5 * (x1 + x2), 0.5 * (y1 + y2))):
                if self.junction_labels is None:
                    self.ax.annotate(i.__str__(), (xn, yn), color=[0.3,0.5,0.9], ha='center', va='center')
                else:
                    self.ax.annotate(self.junction_labels[i].__str__(), (xn, yn), color=[0.3, 0.5, 0.9], ha='center', va='center')
        if self.show_node_ids:
            for i, (xn, yn) in enumerate(zip(x, y)):
                if self.node_labels is None:
                    self.ax.annotate(i.__str__(), (xn, yn))
                else:
                    self.ax.annotate(self.node_labels[i].__str__(), (xn, yn))
        if self.show_nodes:
            self.ax.plot([x], [y], color=[0,0,0], marker="o", markerfacecolor=[1,1,1])
            self.ax.plot([x[self.array.current_base > 0]], [y[self.array.current_base > 0]], color=[0, 0, 0], marker="o", markerfacecolor=[0, 0, 0])
            self.ax.plot([x[self.array.current_base < 0]], [y[self.array.current_base < 0]], color=[1, 0, 0], marker="o", markerfacecolor=[1, 0, 0])

        if self.show_paths:
            for i, (xcn, ycn, n) in enumerate(zip(xc, yc, pn)):
                xp, yp = 0.86 * x[n] + 0.14 * xcn, 0.86 * y[n] + 0.14 * ycn
                if self.show_path_directions:
                    self.ax.quiver(0.5 * (xp[0]+ xp[1]), 0.5 * (yp[0]+ yp[1]), 0.3 * (xp[1] - xp[0]), 0.3 * (yp[1] - yp[0]), color=[1, 0.5, 0.2], pivot='mid', angles='xy', scale=1, scale_units='xy')
                self.ax.plot(np.append(xp, xp[0]), np.append(yp, yp[0]), color=[1, 0.5, 0.2])
                if self.show_path_ids:
                    if self.path_labels is None:
                        self.ax.annotate(i.__str__(), (xcn, ycn), color=[1, 0.5, 0.2], ha='center', va='center')
                    else:
                        self.ax.annotate(self.path_labels[i].__str__(), (xcn, ycn), color=[1, 0.5, 0.2], ha='center', va='center')
        return self.fig, self.ax



class ArrayPlot:

    node_quantities = {
        "phi": 0, "phase": 0, "phases": 0, "U": 1,
        "potential": 1, "UThermal": 2, "Uthermal": 2,
        "U_thermal": 2, "thermal_potential": 2,
        "current_base": 3, "Ibase": 3, "I_base": 3, "IBase": 3,
        "external_current_base": 4, "Iext": 4, "I_ext": 4, "IExt": 4

    }

    junction_quantities = {
        "th": 0, "theta": 0, "phase_difference": 0,  "gauge_invariant_phase_difference": 0,
        "V": 1, "voltage": 1, "V_thermal": 2, "VThermal": 2,  "Vthermal": 2, "thermal_voltage": 2,
        "I": 3, "current": 3, "I_thermal": 4, "thermal_current": 4, "Ithermal": 4,  "IThermal": 4,
        "external_current": 5, "external_junction_current": 5, "I_ext_J": 5, "IExtJ": 5,
        "EJ": 6, "josephson_energy": 6, "EM": 7, "magnetic_energy": 7, "EC": 8, "capacitive_energy": 8,
        "capacitance_energy": 8, "Etot": 9, "E_tot": 9, "ETot": 9, "total_energy": 9, "energy": 9,
        "EM_thermal": 10, "thermal_magnetic_energy": 10,
        "EC_thermal": 11, "thermal_capacitive_energy": 11, "thermal_capacitance_energy": 11,
        "Etot_thermal": 12, "E_tot_thermal": 12, "ETot_thermal": 12, "thermal_total_energy": 12, "thermal_energy": 12
    }

    path_quantities = {
        "Phi": 0, "flux": 0, "magnetic_flux": 0,
        "Phi_thermal": 1, "thermal_flux": 1, "thermal_magnetic_flux": 1,
        "n": 2, "vortices": 2, "vortex_configuration": 2, "path_current": 3, "J": 3,
        "thermal_path_current": 4, "J_thermal": 4,  "Jthermal": 4, "JThermal": 4
    }

    def __init__(self, config: StaticConfiguration | DynamicConfiguration,
                 time_point=0, show_vortices=True, vortex_diameter=0.25, vortex_color=(0, 0, 0),
                 anti_vortex_color=(0.8, 0.1, 0.2), vortex_alpha=1, show_grid=True, grid_width=1,
                 grid_color=(0.3, 0.5, 0.9), grid_alpha=0.5, show_colorbar=True, show_arrows=True,
                 arrow_quantity="I", arrow_width=0.005, arrow_scale=1, arrow_headwidth=3, arrow_headlength=5,
                 arrow_headaxislength=4.5, arrow_minshaft=1, arrow_minlength=1, arrow_color=(0.2, 0.4, 0.7),
                 arrow_alpha=1,  show_nodes=True, node_diameter=0.2,
                 node_face_color=(1,1,1), node_edge_color=(0, 0, 0), node_alpha=1, show_node_quantity=False,
                 node_quantity="phase", node_quantity_cmap=None, node_quantity_clim=(0, 1), node_quantity_alpha=1,
                 node_quantity_logarithmic_colors=False, show_path_quantity=False, path_quantity="n",
                 path_quantity_cmap=None, path_quantity_clim=(0, 1), path_quantity_alpha=1,
                 path_quantity_logarithmic_colors=False,
                 figsize=None, title=""):
        self.config = config
        if not isinstance(config, (StaticConfiguration, DynamicConfiguration)):
            raise ValueError("config must be a StaticConfiguration or DynamicConfiguration object")
        self.time_point = time_point
        if isinstance(config, DynamicConfiguration):
            if not config.problem.store_time_steps[self.time_point]:
                raise ValueError("The requested timepoint from config to plot has not been stored during "
                                 "simulation (set with the config.store_time_steps property)")
        self.show_vortices = show_vortices
        self.vortex_diameter = vortex_diameter
        self.vortex_color = vortex_color
        self.anti_vortex_color = anti_vortex_color
        self.vortex_alpha = vortex_alpha
        self.show_grid = show_grid
        self.grid_width = grid_width
        self.grid_color = grid_color
        self.grid_alpha = grid_alpha
        self.show_colorbar = show_colorbar
        self.show_arrows = show_arrows
        self.arrow_quantity = arrow_quantity
        self.arrow_width = arrow_width
        self.arrow_scale = arrow_scale
        self.arrow_headwidth = arrow_headwidth
        self.arrow_headlength = arrow_headlength
        self.arrow_headaxislength = arrow_headaxislength
        self.arrow_minshaft = arrow_minshaft
        self.arrow_minlength = arrow_minlength
        self.arrow_color = arrow_color
        self.arrow_alpha = arrow_alpha
        self.show_nodes = show_nodes
        self.node_diameter = node_diameter
        self.node_face_color = node_face_color
        self.node_edge_color = node_edge_color
        self.node_alpha = node_alpha
        self.show_node_quantity = show_node_quantity
        self.node_quantity = node_quantity
        self.node_quantity_cmap = node_quantity_cmap
        self.node_quantity_clim = node_quantity_clim
        self.node_quantity_alpha = node_quantity_alpha
        self.node_quantity_logarithmic_colors = node_quantity_logarithmic_colors
        self.show_path_quantity = show_path_quantity
        self.path_quantity = path_quantity
        self.path_quantity_cmap = path_quantity_cmap
        self.path_quantity_clim = path_quantity_clim
        self.path_quantity_alpha = path_quantity_alpha
        self.path_quantity_logarithmic_colors = path_quantity_logarithmic_colors
        self.figsize = figsize if figsize is not None else [6.4, 4.8]
        self.colorbar = None
        self.title = title

    def _is_static(self):
        return isinstance(self.config, StaticConfiguration)

    def _get_node_quantity(self):
        if isinstance(self.node_quantity, np.ndarray):
            return self.node_quantity.flatten()
        quantity = self.node_quantities[self.node_quantity]
        if quantity == 0:   # phi
            out = self.config.get_phi() if self._is_static() else self.config.get_phi(self.time_point)
            out = out.copy()
            out -= np.round(out / (np.pi * 2.0)).astype(out.dtype) * np.pi * 2.0
            return out

        if quantity == 1:   # U
            return self.config.get_U(self.time_point)[..., 0]
        if quantity == 2:   # U_thermal
            return self.config.get_U_thermal(self.time_point)[..., 0]
        if quantity == 3:   # I_base
            return self.config.array()._Ibase()
        if quantity == 4:   # I_ext
            return self.config.problem.Ip() if self._is_static() else self.config.problem.Ip(self.time_point)[..., 0]

    def _get_junction_quantity(self):
        if isinstance(self.arrow_quantity, np.ndarray):
            return self.arrow_quantity.flatten()
        quantity = self.junction_quantities[self.arrow_quantity]
        if quantity == 0:   # theta
            out = self.config.get_theta() if self._is_static() else self.config.get_theta(self.time_point)[..., 0]
            out = out.copy()
            out -= np.round(out / (np.pi * 2.0)).astype(out.dtype) * np.pi * 2.0
            return out
        if quantity == 1:   # V
            return self.config.get_V(self.time_point)[..., 0]
        if quantity == 2:   # V_thermal
            return self.config.get_V_thermal(self.time_point)[..., 0]
        if quantity == 3:   # I
            return self.config.get_I() if self._is_static() else self.config.get_I(self.time_point)[..., 0]
        if quantity == 4:   # I_thermal
            return self.config.get_I_thermal(self.time_point)[..., 0]
        if quantity == 5:   # I_ext_J
            return self.config.problem.Iext() if self._is_static() else self.config.problem.IpJ(self.time_point)[..., 0]
        if quantity == 6:   # EJ
            return self.config.get_EJ() if self._is_static() else self.config.get_EJ(self.time_point)[..., 0]
        if quantity == 7:   # EM
            return self.config.get_EM() if self._is_static() else self.config.get_EM(self.time_point)[..., 0]
        if quantity == 8:   # EC
            return self.config.get_EC(self.time_point)[..., 0]
        if quantity == 9:   # Etot
            return self.config.get_Etot() if self._is_static() else self.config.get_Etot(self.time_point)[..., 0]
        if quantity == 10:   # EM_thermal
            return self.config.get_EM_thermal(self.time_point)[..., 0]
        if quantity == 11:   # EC_thermal
            return self.config.get_EC_thermal(self.time_point)[..., 0]
        if quantity == 12:   # Etot_thermal
            return self.config.get_Etot_thermal(self.time_point)[..., 0]

    def _get_path_quantity(self):
        if isinstance(self.path_quantity, np.ndarray):
            return self.path_quantity.flatten()
        quantity = self.path_quantities[self.path_quantity]
        if quantity == 0:   # Phi
            return self.config.get_flux() if self._is_static() else self.config.get_flux(self.time_point)[..., 0]
        if quantity == 1:   # Phi_thermal
            return self.config.get_flux_thermal(self.time_point)[..., 0]
        if quantity == 2:   # n
            return  self.config.get_n() if self._is_static() else self.config.get_n(self.time_point)[..., 0]
        if quantity == 3:   # J
            return self.config.get_J() if self._is_static() else self.config.get_J(self.time_point)[..., 0]
        if quantity == 4:   # J_thermal
            return self.config.get_J_thermal(self.time_point)[..., 0]

    def _get_junc_xy(self):
        array = self.config.array()
        x, y = array.get_node_coordinates()
        x1, y1 = x[array.node1], y[array.node1]
        x2, y2 = x[array.node2], y[array.node2]
        return x1, y1, x2, y2

    def make(self):
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        plt.title(self.title)
        self._set_axes()
        if self._is_static():
            n = self.config.get_n()
        else:
            n = self.config.get_n(self.time_point)[..., 0]
        if n.ndim >= 2:
            if np.prod(n.shape[:-1]) == 1:
                n = n.reshape(-1)
            else:
                raise ValueError("must select single configuration")

        node_quantity, path_quantity, arrow_quantity = None, None, None
        if self.show_nodes and self.show_node_quantity:
            node_quantity = self._get_node_quantity()
            if node_quantity.ndim >= 2:
                if np.prod(node_quantity.shape[:-1]) == 1:
                    node_quantity = node_quantity.reshape(-1)
                else:
                    raise ValueError("must select single configuration")
            node_quantity = np.append(node_quantity, 0)
        if self.show_path_quantity:
            path_quantity = self._get_path_quantity()
            if path_quantity.ndim >= 2:
                if np.prod(path_quantity.shape[:-1]) == 1:
                    path_quantity = path_quantity.reshape(-1)
                else:
                    raise ValueError("must select single configuration")
        if self.show_arrows:
            arrow_quantity = self._get_junction_quantity()
            if arrow_quantity.ndim >= 2:
                if np.prod(arrow_quantity.shape[:-1]) == 1:
                    arrow_quantity = arrow_quantity.reshape(-1)
                else:
                    raise ValueError("must select single configuration")
        if self.show_grid:
            self._plot_grid()
        if self.show_path_quantity:
            self._plot_paths(path_quantity)
        if self.show_nodes:
            self._plot_nodes(node_quantity)
        if self.show_arrows:
            self._plot_arrows(arrow_quantity)
        if self.show_vortices:
            self._plot_vortices(n)
        if self.colorbar is not None:
            return self.fig, self.ax, self.colorbar
        else:
            return self.fig, self.ax

    def _get_lims(self):
        x, y = self.config.array().get_node_coordinates()
        xmin = np.min(x)
        xmax = np.max(x)
        ymin = np.min(y)
        ymax = np.max(y)
        dx, dy = xmax - xmin, ymax - ymin
        D = self.node_diameter * 0.5
        return xmin - 0.05 * dx - D, xmax + 0.05 * dx + D, ymin - 0.05 * dy - D, ymax + 0.05 * dy + D

    def _set_axes(self):
        xmin, xmax, ymin, ymax = self._get_lims()
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)
        x0, y0, width, height = self.ax.get_position().bounds
        a_width = width * self.figsize[0]
        a_height = height * self.figsize[1]
        if a_width / (xmax - xmin) > a_height / (ymax - ymin):
            new_width = a_height * (xmax - xmin) / (ymax - ymin) / self.figsize[0]
            x0 = x0 + (width - new_width) / 2
            width = new_width
        else:
            new_height = a_width * (ymax - ymin) / (xmax - xmin) / self.figsize[1]
            y0 = y0 + (height - new_height) / 2
            height = new_height
        self.ax.set_position([x0, y0, width, height])

    def _marker_scale_factor(self):
        xlim = self.ax.get_xlim()
        x0, y0, width, height = self.ax.get_position().bounds
        return (width * self.figsize[0]) / (xlim[1] - xlim[0]) *72

    def _plot_grid(self):
        x1, y1, x2, y2 = self._get_junc_xy()
        self.ax.plot(np.stack((x1, x2)), np.stack((y1, y2)), color=self.grid_color,
                     alpha=self.grid_alpha, linewidth=self.grid_width, zorder=0)

    def _plot_paths(self, path_quantity):
        nodes = self.config.array().get_faces()
        x, y = self.config.array().get_node_coordinates()
        verts = [np.stack((x[n], y[n]), axis=-1) for n in nodes]
        cnorm = Normalize(*self.path_quantity_clim) if not self.path_quantity_logarithmic_colors else LogNorm(*self.path_quantity_clim)
        coll = PolyCollection(verts, array=path_quantity, edgecolors='none', cmap=self.path_quantity_cmap,
                              norm=cnorm, alpha=self.path_quantity_alpha, zorder=-1)
        self.ax.add_collection(coll)
        if self.show_colorbar and not (self.show_nodes and self.show_node_quantity):
            label = self.path_quantity if isinstance(self.path_quantity, str) else ""
            self.colorbar = plt.colorbar(cm.ScalarMappable(norm=cnorm, cmap=self.path_quantity_cmap), ax=self.ax, label=label)

    def _plot_nodes(self, node_quantity):
        x, y = self.config.array().get_node_coordinates()
        marker_size = self.node_diameter * self._marker_scale_factor()
        if not self.show_node_quantity:
            self.ax.plot([x], [y], markeredgecolor=self.node_edge_color, markerfacecolor=self.node_face_color,
                         markersize=marker_size, marker="o", alpha=self.node_alpha, zorder=2)
        else:
            cnorm = Normalize(*self.node_quantity_clim) if not self.node_quantity_logarithmic_colors else LogNorm(*self.node_quantity_clim)
            self.ax.scatter(x.flatten(), y.flatten(), s=marker_size**2, c=node_quantity, cmap=self.node_quantity_cmap,
                            edgecolors=self.node_edge_color, alpha=self.node_quantity_alpha, norm=cnorm)
            if self.show_colorbar:
                label = self.node_quantity if isinstance(self.node_quantity, str) else ""
                self.colorbar = plt.colorbar(cm.ScalarMappable(norm=cnorm, cmap=self.node_quantity_cmap), ax=self.ax, label=label)

    def _plot_arrows(self, arrow_quantity):
        I = arrow_quantity * self.arrow_scale
        x1, y1, x2, y2 = self._get_junc_xy()
        xq = x1 + 0.5 * (1 - I) * (x2 - x1)
        yq = y1 + 0.5 * (1 - I) * (y2 - y1)
        dxq, dyq = I * (x2 - x1), I * (y2 - y1)
        self.ax.quiver(xq, yq, dxq, dyq, edgecolor=self.arrow_color, facecolor=self.arrow_color,
                   angles='xy', scale=1, scale_units='xy', width=self.arrow_width,
                   headwidth=self.arrow_headwidth, headlength=self.arrow_headlength,
                   headaxislength=self.arrow_headaxislength, minshaft=self.arrow_minshaft,
                   minlength=self.arrow_minlength, alpha=self.arrow_alpha, zorder=3)

    def _plot_vortices(self, n):

        marker_size = self.vortex_diameter * self._marker_scale_factor()
        xc, yc = self.config.array().centroids()
        ns = np.unique(n)
        for ni in ns:
            if ni != 0:
                if ni > 0:
                    color = self.vortex_color
                else:
                    color = self.anti_vortex_color
                na = np.abs(ni)
                for k in reversed(range(na)):
                    frac = (2 * k + 1)/(2 * na - 1)
                    self.ax.plot(xc[n == ni], yc[n == ni], markerfacecolor=color,
                                 markeredgecolor=color, marker="o", linestyle="",
                                 markersize= frac * marker_size, alpha=self.vortex_alpha, zorder=4)
                    if k > 0:
                        frac = (2 * k) / (2 * na - 1)
                        self.ax.plot(xc[n == ni], yc[n == ni], markerfacecolor=[1,1,1],
                                     markeredgecolor=[1,1,1], marker="o", linestyle="",
                                     markersize=frac * marker_size, alpha=self.vortex_alpha, zorder=4)





class ArrayMovie:

    def __init__(self, config: DynamicConfiguration, time_points=None, show_vortices=True,
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
        self.config = config
        if not isinstance(config, DynamicConfiguration):
            raise ValueError("config must be a DynamicConfiguration object")
        if not self.config.shape() == ():
            raise ValueError("select a single configuration to animate (by indexing in config[...])")
        self.time_points = time_points
        if time_points is None:
            self.time_points = np.ones(self.config.problem.Nt(), dtype=bool)
        if not isinstance(self.time_points.dtype, (bool, np.bool)):
            try:
                self.time_points = np.zeros(self.config.problem.Nt(), dtype=bool)
                self.time_points[time_points] = True
            except:
                raise ValueError("Invalid time_points; must be None, mask, slice or index array")
        self.time_points &= self.config.problem.store_time_steps
        self.time_points_nz = np.flatnonzero(self.time_points)
        self.show_vortices = show_vortices
        self.vortex_diameter = vortex_diameter
        self.vortex_color = vortex_color
        self.anti_vortex_color = anti_vortex_color
        self.vortex_alpha = vortex_alpha
        self.show_grid = show_grid
        self.grid_width = grid_width
        self.grid_color = grid_color
        self.grid_alpha = grid_alpha
        self.show_colorbar = show_colorbar
        self.show_arrows = show_arrows
        self.arrow_quantity = arrow_quantity
        self.arrow_width = arrow_width
        self.arrow_scale = arrow_scale
        self.arrow_headwidth = arrow_headwidth
        self.arrow_headlength = arrow_headlength
        self.arrow_headaxislength = arrow_headaxislength
        self.arrow_minshaft = arrow_minshaft
        self.arrow_minlength = arrow_minlength
        self.arrow_color = arrow_color
        self.arrow_alpha = arrow_alpha
        self.show_nodes = show_nodes
        self.node_diameter = node_diameter
        self.node_face_color = node_face_color
        self.node_edge_color = node_edge_color
        self.node_alpha = node_alpha
        self.show_node_quantity = show_node_quantity
        self.node_quantity = node_quantity
        self.node_quantity_cmap = node_quantity_cmap
        self.node_quantity_clim = node_quantity_clim
        self.node_quantity_alpha = node_quantity_alpha
        self.node_quantity_logarithmic_colors = node_quantity_logarithmic_colors
        self.show_path_quantity = show_path_quantity
        self.path_quantity = path_quantity
        self.path_quantity_cmap = path_quantity_cmap
        self.path_quantity_clim = path_quantity_clim
        self.path_quantity_alpha = path_quantity_alpha
        self.path_quantity_logarithmic_colors = path_quantity_logarithmic_colors
        self.figsize = figsize if figsize is not None else [6.4, 4.8]
        self.paths_handle, self.nodes_handle, self.arrows_handle, self.vortices_handle = None, None, None, []
        self.item = None
        self.node_quantity_data = None
        self.path_quantity_data = None
        self.arrow_quantity_data = None
        self.n_data = None
        self.colorbar = None
        self.animate_interval = animate_interval
        self.title = title

    node_quantities = {
        "phi": 0, "phase": 0, "phases": 0, "U": 1,
        "potential": 1, "UThermal": 2, "Uthermal": 2,
        "U_thermal": 2, "thermal_potential": 2,
        "current_base": 3, "Ibase": 3, "I_base": 3, "IBase": 3,
        "external_current_base": 4, "Iext": 4, "I_ext": 4, "IExt": 4
    }

    junction_quantities = {
        "th": 0, "theta": 0, "phase_difference": 0,  "gauge_invariant_phase_difference": 0,
        "V": 1, "voltage": 1, "V_thermal": 2, "VThermal": 2,  "Vthermal": 2, "thermal_voltage": 2,
        "I": 3, "current": 3, "I_thermal": 4, "thermal_current": 4, "Ithermal": 4,  "IThermal": 4,
        "EJ": 6, "josephson_energy": 6, "EM": 7, "magnetic_energy": 7, "EC": 8, "capacitive_energy": 8,
        "capacitance_energy": 8, "Etot": 9, "E_tot": 9, "ETot": 9, "total_energy": 9, "energy": 9,
        "EM_thermal": 10, "thermal_magnetic_energy": 10,
        "EC_thermal": 11, "thermal_capacitive_energy": 11, "thermal_capacitance_energy": 11,
        "Etot_thermal": 12, "E_tot_thermal": 12, "ETot_thermal": 12, "thermal_total_energy": 12, "thermal_energy": 12
    }

    path_quantities = {
        "Phi": 0, "flux": 0, "magnetic_flux": 0,
        "Phi_thermal": 1, "thermal_flux": 1, "thermal_magnetic_flux": 1,
        "n": 2, "vortices": 2, "vortex_configuration": 2, "path_current": 3, "J": 3,
        "thermal_path_current": 4, "J_thermal": 4,  "Jthermal": 4, "JThermal": 4
    }

    def show(self):
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        self._set_axes()
        plt.title(self.title)
        time_points = self.time_points
        self.n_data = self.config.get_n(time_points)
        if self.show_nodes and self.show_node_quantity:
            self.node_quantity_data = self._get_node_quantity(time_points)
            print(self.config.array().Nn())
            print(self.node_quantity_data.shape)
            self.node_quantity_data = np.append(self.node_quantity_data, np.zeros((1,) + self.node_quantity_data.shape[1:]), axis=0)
        if self.show_path_quantity:
            self.path_quantity_data = self._get_path_quantity(time_points)
        if self.show_arrows:
            self.arrow_quantity_data = self._get_junction_quantity(time_points)
        if self.show_grid:
            self._plot_grid()
        time_point_list = np.arange(self.n_data.shape[-1], dtype=int)
        self.ani = animation.FuncAnimation(self.fig, self._animate, time_point_list,
                                           init_func=self._init, interval=self.animate_interval, blit=True)
        if self.colorbar is not None:
            return self.ani, self.fig, self.ax, self.colorbar
        else:
            return self.ani, self.fig, self.ax

    def _get_time_point_mask(self, time_point):
        mask = np.zeros(self.config.problem.Nt(), dtype=bool)
        mask[time_point] = True
        return mask

    def _get_node_quantity(self, time_points):
        quantity = self.node_quantities[self.node_quantity]
        # time_points = self._get_time_point_mask(time_point)
        if quantity == 0:   # phi
            out = self.config.get_phi(time_points).copy()
            out -= np.round(out / (np.pi * 2.0)).astype(out.dtype) * np.pi * 2.0
            return out
        if quantity == 1:   # U
            return self.config.get_U(time_points)
        if quantity == 2:   # U_thermal
            return self.config.get_U_thermal(time_points)
        if quantity == 3:   # I_base
            return self.config.array()._Ibase()
        if quantity == 4:   # I_ext
            return self.config.problem.Ip(time_points)

    def _get_junction_quantity(self, time_points):
        quantity = self.junction_quantities[self.arrow_quantity]
        # time_points = self._get_time_point_mask(time_point)
        if quantity == 0:   # theta
            out = self.config.get_theta(time_points).copy()
            out -= np.round(out / (np.pi * 2.0)).astype(out.dtype) * np.pi * 2.0
            return out
        if quantity == 1:   # V
            return self.config.get_V(time_points)
        if quantity == 2:   # V_thermal
            return self.config.get_V_thermal(time_points)
        if quantity == 3:   # I
            return self.config.get_I(time_points)
        if quantity == 4:   # I_thermal
            return self.config.get_I_thermal(time_points)
        if quantity == 6:   # EJ
            return self.config.get_EJ(time_points)
        if quantity == 7:   # EM
            return self.config.get_EM(time_points)
        if quantity == 8:   # EC
            return self.config.get_EC(time_points)
        if quantity == 9:   # Etot
            return self.config.get_Etot(time_points)
        if quantity == 10:   # EM_thermal
            return self.config.get_EM_thermal(time_points)
        if quantity == 11:   # EC_thermal
            return self.config.get_EC_thermal(time_points)
        if quantity == 12:   # Etot_thermal
            return self.config.get_Etot_thermal(time_points)

    def _get_path_quantity(self, time_points):
        quantity = self.path_quantities[self.path_quantity]
        # time_points = self._get_time_point_mask(time_point)
        if quantity == 0:   # Phi
            return self.config.get_flux(time_points)
        if quantity == 1:   # Phi_thermal
            return self.config.get_flux_thermal(time_points)
        if quantity == 2:   # n
            return self.config.get_n(time_points)
        if quantity == 3:   # J
            return self.config.get_J(time_points)
        if quantity == 4:   # J_thermal
            return self.config.get_J_thermal(time_points)

    def _get_junc_xy(self):
        array = self.config.array()
        x, y = array.get_node_coordinates()
        x1, y1 = x[array.node1], y[array.node1]
        x2, y2 = x[array.node2], y[array.node2]
        self.DX = x2 - x1
        self.DY = y2 - y1
        return x1, y1, x2, y2

    def _animate(self, i):
        if self.show_path_quantity:
            self.paths_handle = self._update_paths(i)
        if self.show_nodes:
            self.nodes_handle = self._update_nodes(i)
        if self.show_arrows:
            self.arrows_handle = self._update_arrows(i)
        if self.show_vortices:
            self.vortex_handles =self._plot_vortices(i)
        self.time_label.set_text(str(self.time_points_nz[i]))
        handles = [self.nodes_handle, self.arrows_handle, self.paths_handle, self.time_label] + self.vortex_handles
        return [h for h in handles if h is not None]

    def _init(self):
        if self.show_path_quantity:
            self.paths_handle = self._plot_paths()
        if self.show_nodes:
            self.nodes_handle = self._plot_nodes()
        if self.show_arrows:
            self.arrows_handle = self._plot_arrows()
        if self.show_vortices:
            self.vortex_handles = self._plot_vortices(0)
        handles = [self.paths_handle, self.nodes_handle, self.arrows_handle, self.time_label] + self.vortex_handles
        return [h for h in handles if h is not None]

    def _get_lims(self):
        x, y = self.config.array().get_node_coordinates()
        xmin = np.min(x)
        xmax = np.max(x)
        ymin = np.min(y)
        ymax = np.max(y)
        dx, dy = xmax - xmin, ymax - ymin
        D = self.node_diameter * 0.5
        return xmin - 0.05 * dx - D, xmax + 0.05 * dx + D, ymin - 0.05 * dy - D, ymax + 0.05 * dy + D

    def _set_axes(self):
        xmin, xmax, ymin, ymax = self._get_lims()
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)
        self.time_label = self.ax.annotate("", (xmin + 0.99 * (xmax - xmin), ymin + 0.98 * (ymax - ymin)), color=[1, 0.5, 0.2], ha='right', va='center')
        x0, y0, width, height = self.ax.get_position().bounds
        a_width = width * self.figsize[0]
        a_height = height * self.figsize[1]
        if a_width / (xmax - xmin) > a_height / (ymax - ymin):
            new_width = a_height * (xmax - xmin) / (ymax - ymin) / self.figsize[0]
            x0 = x0 + (width - new_width) / 2
            width = new_width
        else:
            new_height = a_width * (ymax - ymin) / (xmax - xmin) / self.figsize[1]
            y0 = y0 + (height - new_height) / 2
            height = new_height
        self.ax.set_position([x0, y0, width, height])

    def _marker_scale_factor(self):
        xlim = self.ax.get_xlim()
        x0, y0, width, height = self.ax.get_position().bounds
        return (width * self.figsize[0]) / (xlim[1] - xlim[0]) *72

    def _plot_grid(self):
        x1, y1, x2, y2 = self._get_junc_xy()
        self.ax.plot(np.stack((x1, x2)), np.stack((y1, y2)), color=self.grid_color,
                     alpha=self.grid_alpha, linewidth=self.grid_width, zorder=0)

    def _plot_paths(self):
        nodes = self.config.array().path_nodes
        x, y = self.config.array().get_node_coordinates()
        verts = [np.stack((x[n], y[n]), axis=-1) for n in nodes]
        path_quantity = self.path_quantity_data[:, 0]
        cnorm = Normalize(*self.path_quantity_clim) if not self.path_quantity_logarithmic_colors else LogNorm(*self.path_quantity_clim)
        coll = PolyCollection(verts, array=path_quantity, edgecolors='none', cmap=self.path_quantity_cmap,
                              norm=cnorm, alpha=self.path_quantity_alpha, zorder=-1)
        paths_handle = self.ax.add_collection(coll)
        if self.show_colorbar and not (self.show_nodes and self.show_node_quantity):
            label = self.path_quantity if isinstance(self.path_quantity, str) else ""
            if self.colorbar is None:
                self.colorbar = plt.colorbar(cm.ScalarMappable(norm=cnorm, cmap=self.path_quantity_cmap), ax=self.ax, label=label)

        return paths_handle

    def _update_paths(self, i):
        path_quantity = self.path_quantity_data[:, i]
        self.paths_handle.set_array(path_quantity)
        return self.paths_handle

    def _plot_nodes(self):
        print("updateing plot_nodes")
        x, y = self.config.array().get_node_coordinates()
        marker_size = self.node_diameter * self._marker_scale_factor()
        if not self.show_node_quantity:
            nodes_handle = self.ax.plot(x, y, markeredgecolor=self.node_edge_color, markerfacecolor=self.node_face_color,
                         markersize=marker_size, marker="o", alpha=self.node_alpha, zorder=2, linestyle="")
            nodes_handle = nodes_handle[0]
        else:
            if self.node_quantity_data.ndim >= 2:
                node_quantity = self.node_quantity_data[:, 0]
            else:
                node_quantity = self.node_quantity_data
            cnorm = Normalize(*self.node_quantity_clim) if not self.node_quantity_logarithmic_colors else LogNorm(*self.node_quantity_clim)
            nodes_handle = self.ax.scatter(x.flatten(), y.flatten(), s=marker_size**2, c=node_quantity, cmap=self.node_quantity_cmap,
                            edgecolors=self.node_edge_color, alpha=self.node_quantity_alpha, norm=cnorm)
            if self.show_colorbar:
                label = self.node_quantity if isinstance(self.node_quantity, str) else ""
                if self.colorbar is None:
                    self.colorbar = plt.colorbar(cm.ScalarMappable(norm=cnorm, cmap=self.node_quantity_cmap), ax=self.ax, label=label)

        return nodes_handle

    def _update_nodes(self, i):
        if self.show_node_quantity:
            if self.node_quantity_data.ndim >= 2:
                node_quantity = self.node_quantity_data[:, i]
            else:
                node_quantity = self.node_quantity_data
            self.nodes_handle.set_array(node_quantity)
        return self.nodes_handle

    def _plot_arrows(self):
        I = self.arrow_quantity_data[:, 0] * self.arrow_scale
        x1, y1, x2, y2 = self._get_junc_xy()
        xq = 0.5 * (x2 + x1)
        yq = 0.5 * (y2 + y1)
        dxq, dyq = I * (x2 - x1), I * (y2 - y1)
        arrows_handle = self.ax.quiver(xq, yq, dxq, dyq, edgecolor=self.arrow_color, facecolor=self.arrow_color,
                   angles='xy', scale=1, scale_units='xy', pivot='mid', width=self.arrow_width,
                   headwidth=self.arrow_headwidth, headlength=self.arrow_headlength,
                   headaxislength=self.arrow_headaxislength, minshaft=self.arrow_minshaft,
                   minlength=self.arrow_minlength, alpha=self.arrow_alpha, zorder=3)
        return arrows_handle

    def _update_arrows(self, i):
        I = self.arrow_quantity_data[:, i] * self.arrow_scale
        self.arrows_handle.set_UVC(I * self.DX, I * self.DY)
        return self.arrows_handle

    def _plot_vortices(self, i):
        n_v = self.n_data[:, i]
        marker_size = self.vortex_diameter * self._marker_scale_factor()
        xc, yc = self.config.array().centroids()
        ns = np.unique(n_v)
        vort_handles = []
        for ni in ns:
            if ni != 0:
                if ni > 0:
                    color = self.vortex_color
                else:
                    color = self.anti_vortex_color
                na = np.abs(ni)
                for k in reversed(range(na)):
                    frac = (2 * k + 1)/(2 * na - 1)
                    p = self.ax.plot(xc[n_v == ni], yc[n_v == ni], markerfacecolor=color,
                                 markeredgecolor=color, marker="o", linestyle="",
                                 markersize= frac * marker_size, alpha=self.vortex_alpha, zorder=4)
                    vort_handles += p
                    if k > 0:
                        frac = (2 * k) / (2 * na - 1)
                        p = self.ax.plot(xc[n_v == ni], yc[n_v == ni], markerfacecolor=[1,1,1],
                                     markeredgecolor=[1,1,1], marker="o", linestyle="",
                                     markersize=frac * marker_size, alpha=self.vortex_alpha, zorder=4)
                        vort_handles += p
        return vort_handles

