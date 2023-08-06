from __future__ import annotations
from typing import Any

import time

import numpy as np
import scipy
import scipy.sparse.linalg
import scipy.optimize

from josephson_junction_array import Array

__all__ = ["CurrentPhaseRelation", "DefaultCurrentPhaseRelation",
           "StaticProblem", "StaticConfiguration"]

class CurrentPhaseRelation:

    def __init__(self, func, d_func, i_func):
        self.func = func
        self.d_func = d_func
        self.i_func = i_func

    def eval(self, Ic, theta):
        return self.func(Ic, theta)

    def d_eval(self, Ic, theta):
        return self.d_func(Ic, theta)

    def i_eval(self, Ic, theta):
        return self.i_func(Ic, theta)

class DefaultCurrentPhaseRelation(CurrentPhaseRelation):

    def __init__(self):
        super().__init__(lambda Ic, th: Ic * np.sin(th),
                         lambda Ic, th: Ic * np.cos(th),
                         lambda Ic, th: Ic * (1.0 - np.cos(th)))

class StabilityCheckInfo:

    def __init__(self, shape, tol, maxiter):
        self.shape = shape
        self.tol = tol
        self.maxiter = maxiter

        self.iter_count = np.zeros(shape, dtype=int).flatten()
        self.max_eigenvalue = np.zeros(shape, dtype=np.double).flatten()
        self.is_stable = np.zeros(shape, dtype=bool).flatten()
        self.elapsed_time = 0.0

    def get_tol(self):
        return self.tol

    def get_maxiter(self):
        return self.maxiter


    def _set(self, i, max_eigenvalue, residual):
        self.max_eigenvalue[i] = max_eigenvalue
        self.iter_count[i] = len(residual)
        self.is_stable[i] = max_eigenvalue < self.tol

    def get_max_eigenvalue(self):
        return self.max_eigenvalue

    def get_iter_count(self):
        return self.iter_count

    def get_is_stable(self):
        return self.is_stable

    def get_elapsed_time(self):
        return self.elapsed_time

    def __str__(self):
        out = "stability check info: (tol=" + self.get_tol().__str__() +\
              ", maxiter=" + self.get_maxiter().__str__() + ")\n\t"
        out += "max_eigenvalue: " + self.get_max_eigenvalue().reshape(self.shape).__str__() + "\n\t"
        out += "get_is_stable: " + self.get_is_stable().reshape(self.shape).__str__() + "\n\t"
        out += "step count (of lobpcg method): " + self.get_iter_count().reshape(self.shape).__str__() + "\n\t"
        out += "elapsed time: " + self.elapsed_time.__str__() + "sec"
        return out

class NewtonIterInfo:
    def __init__(self, shape, tol, stop_tol, maxiter, has_path_error=False):
        self.iter_count = 0
        self.shape = shape
        self.tol = tol
        self.stop_tol = stop_tol
        self.maxiter = maxiter
        self.step_count = np.zeros(self.shape, dtype=int)
        self.kirchhoff_error = np.zeros((10,) + self.shape, dtype=np.double)
        self.has_path_error = has_path_error
        self.path_error = np.zeros((10,) + self.shape,  dtype=np.double)
        self.is_converged = np.zeros((10,) + self.shape, dtype=bool)
        self.stopped_prematurely_at = -np.ones(self.shape, dtype=int)
        self.elapsed_time = 0.0

    def _update(self, kirchhoff_error, is_hopeless, is_converged, path_error=None):
        kirchhoff_error = kirchhoff_error.reshape(self.shape)
        if self.has_path_error:
            path_error = path_error.reshape(self.shape)
        is_hopeless = is_hopeless.reshape(self.shape)
        is_converged = is_converged.reshape(self.shape)
        if self.iter_count == self.kirchhoff_error.shape[0]:
            self.kirchhoff_error = np.concatenate((self.kirchhoff_error, np.zeros(self.kirchhoff_error.shape)), axis=0)
            if self.has_path_error:
                self.path_error = np.concatenate((self.path_error, np.zeros(self.path_error.shape)), axis=0)
            self.is_converged = np.concatenate((self.is_converged, np.zeros(self.is_converged.shape)), axis=0)
        self.kirchhoff_error[self.iter_count, ...] = kirchhoff_error
        if self.has_path_error:
            self.path_error[self.iter_count, ...] = path_error
        self.is_converged[self.iter_count, ...] = is_converged
        self.step_count += (~is_converged).astype(int)
        cur_is_hopeless = self.stopped_prematurely_at != -1
        update_mask = (~cur_is_hopeless) & is_hopeless
        if self.shape == ():
            if update_mask:
                self.stopped_prematurely_at= self.step_count
        else:
            self.stopped_prematurely_at[update_mask] = self.step_count[update_mask]
        self.iter_count += 1

    def _finish(self, elapsed_time):
        self.kirchhoff_error = self.kirchhoff_error[:self.iter_count, ...]
        if self.has_path_error:
            self.path_error = self.path_error[:self.iter_count, ...]
        self.is_converged = self.is_converged[:self.iter_count, ...]
        self.elapsed_time = elapsed_time

    def get_tol(self):
        return self.tol

    def get_stop_tol(self):
        return self.stop_tol

    def get_max_iter(self):
        return self.maxiter

    def get_error(self):
        error = self.kirchhoff_error
        if self.has_path_error:
            error = np.maximum(error, self.path_error)
        return error

    def get_kirchhoff_error(self):
        return self.kirchhoff_error

    def get_path_error(self):
        return self.path_error

    def get_step_count(self):
        return self.step_count

    def get_has_converged(self):
        return self.is_converged

    def get_stopped_prematurely_at(self):
        return self.stopped_prematurely_at

    def get_elapsed_time(self):
        return self.elapsed_time

    def __str__(self):
        out = "newton iteration info: (tol=" + self.get_tol().__str__() + ", stop_tol=" +\
               self.get_stop_tol().__str__() + ", maxiter=" + self.get_max_iter().__str__() + ")\n\t"
        out += "elapsed time: " + self.get_elapsed_time().__str__() + "sec\n\t"
        if self.has_path_error:
            out += "kirchhoff error: " + self.get_kirchhoff_error().__str__() + "\n\t"
            out += "path error:      " + self.get_path_error().__str__() + "\n\t"
        else:
            out += "error: " + self.get_kirchhoff_error().__str__() + "\n\t"
        out += "has converged: " + self.get_has_converged()[-1, ...].__str__() + "\n\t"
        if np.any(self.get_stopped_prematurely_at() != -1):
            out += "stopped prematurely at: " + self.get_stopped_prematurely_at().__str__() + "\n\t"
        out += "step count: " + self.get_step_count().__str__()
        return out

class ParameterOptimizeInfo:

    def __init__(self, has_start_solution, lambda_history, I_history, f_history,
                 found_solution_history, newton_steps_history, newton_iter_info, stable_info,
                 elapsed_time):
        self.has_start_solution = has_start_solution
        self.lambda_history = lambda_history
        self.I_history = I_history
        self.f_history = f_history
        self.found_solution_history = found_solution_history
        self.newton_steps_history = newton_steps_history
        self.newton_iter_info = newton_iter_info
        self.stable_iter_info = stable_info
        self.elapsed_time = elapsed_time

    def get_has_start_solution(self):
        return self.has_start_solution

    def get_lambda(self):
        return self.lambda_history

    def get_I(self):
        return self.I_history

    def get_f(self):
        return self.f_history

    def get_found_solution(self):
        return self.found_solution_history

    def get_newton_steps(self):
        return self.newton_steps_history

    def get_newton_iter_all_info(self):
        return self.newton_iter_info

    def get_stable_iter_all_info(self):
        return self.stable_iter_info

    def get_elapsed_time(self):
        return self.elapsed_time

    def get_newton_iteration_elapsed_time(self):
        return np.sum([i.get_elapsed_time() for i in self.newton_iter_info])

    def get_stable_iteration_elapsed_time(self):
        return np.sum([i[1].get_elapsed_time() if hasattr(i[1], "get_elapsed_time") else 0.0
                       for i in self.stable_iter_info])

    def __str__(self):
        out = "parameter optimize info:\n\t"
        out += "elapsed time: " + float(self.get_elapsed_time()).__str__() + \
               "sec (newton: " + self.get_newton_iteration_elapsed_time().__str__() + ", stable: " + \
               self.get_stable_iteration_elapsed_time().__str__() + ")\n\t"
        out += "has start solution: " + self.get_has_start_solution().__str__() + "\n\t"
        out += "lambda: " + self.get_lambda().__str__() + "\n\t"
        out += "I:      " + self.get_I().__str__() + "\n\t"
        out += "f:      " + self.get_f().__str__() + "\n\t"
        out += "found:  " + self.get_found_solution().__str__() + "\n\t"
        out += "total newton steps:  " + self.get_newton_steps().__str__() + "\n\t"
        return out

class StaticProblem:
    """
    Define multiple static JJA problems problems with varying parameters.

    All problems are computed in one call, which is generally much faster than
    computing individual problems consecutively.

    One can compute three types of problems:
     - self.approximate(array)                  Computes an approximate solution
     - self.compute(array, initial_guess)       Compute exact solution
     - self.compute_maximal_current(array)      Compute maximal external current (ignores input Iext)

    approximate() and compute() result in a StaticConfiguration object containing
    the solution. compute_maximal_current() returns a lower and upper bound for Iext.

    One can specify physical input quantities:

    Physical input parameters:      (symbol)            (shape)
     - external_current             Iext                (...)
     - frustration                  f                   (..., Np or 1)
     - phase_zone                   z                   (..., Np or 1)
     - target_vortex_configuration  nt                  (..., Np or 1)
     - current_phase_relation       cp                  CurrentPhaseRelation object

     The variable ... shapes is the "problem space" and they must be
     numpy-broadcast-compatible. The shape of the space pr_shape can be found with
     self.shape() and its dimension count ndim=self.ndim()

    So the shape of the problem space is:
    pr_shape = np.broadcast_shapes(Iext.shape, f.shape[:-1], z.shape[:-1], nt.shape[:-1])

    """

    def __init__(self, array: Array, external_current: Any = 0, frustration: Any = 0, phase_zone: Any = 0,
                 target_vortex_configuration: Any = 0, current_phase_relation=DefaultCurrentPhaseRelation()):
        self.array = array
        self.external_current = np.array(external_current, dtype=np.double)
        self.frustration = np.atleast_1d(np.array(frustration, dtype=np.double))
        self.phase_zone = np.atleast_1d(np.array(phase_zone, dtype=int))
        self.target_vortex_configuration = np.atleast_1d(np.array(target_vortex_configuration, dtype=int))
        self.current_phase_relation = current_phase_relation
        self.prepared_Ip = None
        self.prepared_IpJ = None
        self.prepared_IpJ_norm = None
        self.prepared_df = None
        self.prepared_df_norm = None
        self.prepared_g = None

    def reset(self):
        self.prepared_Ip = None
        self.prepared_IpJ = None
        self.prepared_IpJ_norm = None
        self.prepared_df = None
        self.prepared_df_norm = None
        self.prepared_g = None
        return self

    def copy(self) -> StaticProblem:
        return StaticProblem(self.array, external_current=self.external_current,
                             frustration=self.frustration, phase_zone=self.phase_zone,
                             target_vortex_configuration=self.target_vortex_configuration,
                             current_phase_relation=self.current_phase_relation)

    def shape(self):
        return np.broadcast_shapes(self.external_current.shape, self.frustration.shape[:-1],
                                   self.phase_zone.shape[:-1], self.phase_zone.shape[:-1],
                                   self.target_vortex_configuration.shape[:-1])

    def ndim(self):
        return len(self.shape())

    def get_array(self) -> Array:
        return self.array

    def __getitem__(self, item):
        if not isinstance(item, tuple):
            item = (item,)
        Np = np.max([self.frustration.shape[-1], self.target_vortex_configuration.shape[-1], self.phase_zone.shape[-1]])
        self.external_current = np.broadcast_to(self.external_current, self.shape())
        self.frustration = np.broadcast_to(self.frustration, self.shape() + (Np,))
        self.phase_zone = np.broadcast_to(self.phase_zone, self.shape() + (Np,))
        self.target_vortex_configuration = np.broadcast_to(self.target_vortex_configuration, self.shape() + (Np,))
        s = (slice(None),)
        return StaticProblem(self.get_array(), external_current=self.external_current[item],
                             frustration=self.frustration[item + s],
                             phase_zone=self.phase_zone[item + s],
                             target_vortex_configuration=self.target_vortex_configuration[item + s],
                             current_phase_relation=self.current_phase_relation)

    def select_solutions(self, tol=1E-5, initial_guess=None, newton_stop_tol=3, newton_maxiter=100, stable=True, stable_maxiter=200, target_vortex_configuration=True,
                         return_mask=False) -> tuple[StaticProblem, np.ndarray] | StaticProblem:
        out = self.compute(initial_guess=initial_guess, tol=tol, stop_tol=newton_stop_tol,
                           maxiter=newton_maxiter)
        mask = out.is_solution(tol=tol)
        if stable:
            mask &= out.is_stable(maxiter=stable_maxiter, tol=tol)
        if target_vortex_configuration:
            mask &= out.satisfies_target_vortices()
        sel_prob = self[mask]
        if return_mask:
            return sel_prob, mask
        else:
            return sel_prob

    def set_external_current(self, Iext):
        shape = self.shape()
        self.external_current = Iext
        # if not self.shape() == shape:
        #     print("warning: changed problem shape")
        self.prepared_Ip = None
        self.prepared_IpJ = None
        self.prepared_IpJ_norm = None
        return self

    def set_frustration(self, f):
        shape = self.shape()
        self.frustration = f
        # if not self.shape() == shape:
        #     print("warning: changed problem shape")
        self.prepared_df = None
        self.prepared_df_norm = None
        self.prepared_g = None
        return self

    def set_target_vortex_configuration(self, nt):
        shape = self.shape()
        self.target_vortex_configuration = nt
        # if not self.shape() == shape:
        #     print("warning: changed problem shape")
        return self

    def set_phase_zone(self, z):
        shape = self.shape()
        self.phase_zone = z
        # if not self.shape() == shape:
        #     print("warning: changed problem shape")
        self.prepared_df = None
        self.prepared_df_norm = None
        self.prepared_g = None
        return self

    def Iext(self) -> np.ndarray:
        return self.external_current

    def f(self) -> np.ndarray:
        return self.frustration

    def nt(self) -> np.ndarray:
        return self.target_vortex_configuration

    def z(self) -> np.ndarray:
        return self.phase_zone

    def cp(self, Ic, theta):
        return self.current_phase_relation.eval(Ic, theta)

    def dcp(self, Ic, theta):
        return self.current_phase_relation.d_eval(Ic, theta)

    def icp(self, Ic, theta):
        return self.current_phase_relation.i_eval(Ic, theta)

    def Ip(self):
        if self.prepared_Ip is None:
            self.prepared_Ip = self.get_array()._Ibase_reduced() * self.Iext()[..., None]
        return self.prepared_Ip

    def IpJ(self):
        if self.prepared_IpJ is None:
            self.prepared_IpJ = self.get_array()._IbaseJ() * self.Iext()[..., None]
        return self.prepared_IpJ

    def IpJ_norm(self):
        if self.prepared_IpJ_norm is None:
            self.prepared_IpJ_norm = scipy.linalg.norm(self.IpJ(), axis=-1)
        return self.prepared_IpJ_norm

    def df(self):
        if self.prepared_df is None:
            self.prepared_df = 2 * np.pi * (self.z() - self.get_array().areas * self.f())
        return self.prepared_df

    def df_norm(self):
        if self.prepared_df_norm is None:
            self.prepared_df_norm = scipy.linalg.norm(self.df(), axis=-1)
        return self.prepared_df_norm

    def g(self):
        if self.prepared_g is None:
            s = self.get_array().solver
            Asq_solver = s.get_Asq_solver()
            self.prepared_g = 2 * np.pi * s.AT_dot(Asq_solver(s.pack(self.z() - self.get_array().areas * self.f())), p=False)
        return self.prepared_g

    def approximate(self, algorithm=0) -> StaticConfiguration:
        """
        Computes approximate array configurations. The approximation aims
        to be such that is vortex configurations equal the target vortex
        configurations, but this is not guaranteed.

        Has two algorithms; the arctan approximation or the london approximation.

        alg: name                  description
         0   arctan approximation  assigns phases that "wind" 2*pi around vortices in z=0 phase zone,
                                   phi(x,y) = sum_i 2 * pi * n_i * atan2(y-y_n_i,x-x_n_i)
         1   london approximation  Projects theta=0 onto the winding-rule-space in z=n phase zone
        """
        if algorithm == 0:
            theta = _approximate_arctan(self)
        elif algorithm == 1:
            theta = _approximate_london(self)
        else:
            raise ValueError("invalid algorithm")
        return StaticConfiguration(self, theta)

    def approximate_placed_vortices(self, x0, y0, n0, problem_indices) -> StaticConfiguration:
        theta = _approximate_arctan2(self, x0, y0, n0, problem_indices)
        out = StaticConfiguration(self, theta)
        self.target_vortex_configuration = out.get_n()
        return out

    def compute(self, initial_guess: StaticConfiguration | InitialCondition = None,
                tol=1e-5, stop_tol=3, maxiter=100) -> StaticConfiguration:

        from dynamic_problem import InitialCondition, DefaultIntialCondition
        """
        Compute solutions to the problem on an Josephson Array using Newton iteration.

        Requires an initial configuration. If None is specified; it is theta=0.

        """
        if initial_guess is None:
            initial_guess = DefaultIntialCondition()
        if isinstance(initial_guess, InitialCondition):
            initial_guess = initial_guess.generate(self)
        if maxiter is None:
            maxiter = 2 ** 30

        if self.get_array().has_inductance():
            theta, iter_info = _static_compute_inductance(self, initial_guess=initial_guess, tol=tol,
                                                           stop_tol=stop_tol, maxiter=maxiter)
        else:
            theta, iter_info = _static_compute_no_inductance(self, initial_guess=initial_guess, tol=tol,
                                                              stop_tol=stop_tol, maxiter=maxiter)

        return StaticConfiguration(self, theta, newton_iter_info=iter_info)


    def has_stable_solution(self, tol=1E-5, stable_maxiter=200):
        out = self.compute()
        return out.is_stable_target_solution(tol=tol, stable_maxiter=stable_maxiter)

    def annealing(self, Nt=10**4, dt=0.5, temperature_profile="default", search_temperature=0.15) -> StaticConfiguration:
        """
        Find low energy state by using a time evolution simulation with a slowly decreasing temperature
        (called annealing). The duration and temperature profile can be controlled.

        default temperature profile: [(0, 1), (0.25, Tsearch * 1.1), (0.75, Tsearch * 0.9), (1, 0)]
        """
        from dynamic_problem import DynamicProblem
        if temperature_profile == "default":
            temperature_profile = [(0, 1), (0.25, search_temperature * 1.1), (0.75, search_temperature * 0.9), (1, 0)]

        T = np.zeros(0, dtype=np.double)
        for i in range(len(temperature_profile) - 1):
            t_i = temperature_profile[i]
            t_ip1 = temperature_profile[i + 1]
            T = np.append(T, np.linspace(t_i[1], t_ip1[1], int(Nt * (t_ip1[0] - t_i[0]))))
        ts = np.zeros(Nt, dtype=bool)
        ts[-1] = True
        prob = DynamicProblem(self.get_array(), time_step_count=Nt, time_step=dt, external_current=0, frustration=self.frustration,
                              temperature=T, store_current=False, store_voltage=False, store_time_steps=ts)
        out = prob.compute()
        th = out.theta[..., -1]
        out = self.compute(StaticConfiguration(self, th))
        self.target_vortex_configuration = out.get_n()
        return out


    def compute_frustration_bounds(self, initial_guess: StaticConfiguration | InitialCondition = None,
                                   lambda_steps=20, lambda_stepsize=0.3, tol=1E-5,
                                   newton_stop_tol=3, newton_maxiter=100, stable_maxiter=200):
        f_lower_bound = np.zeros(self.shape(), dtype=np.double)
        f_upper_bound = np.zeros(self.shape(), dtype=np.double)
        mean_f = np.mean(self.nt() / self.get_array().areas, axis=-1)
        self.set_frustration(mean_f[..., None])
        self.set_external_current(np.zeros(self.shape(), dtype=np.double))
        mask = self.has_stable_solution(tol=tol, stable_maxiter=stable_maxiter)
        if self.shape() == ():
            if not mask:
                return (np.nan, np.nan), mask, (None, None), (None, None)
            start_f = self.frustration[0]
            If = np.array(lambda df: 0.0, dtype=object)
            f_funcs = np.array(lambda df, f_start=start_f: f_start + df, dtype=object)
            df_up, _, _, state_up, info_up = self.compute_maximal_parameter(If, f_funcs, initial_guess=initial_guess,
                                                             lambda_steps=lambda_steps,
                                                             lambda_stepsize=lambda_stepsize,
                                                             tol=tol, newton_stop_tol=newton_stop_tol,
                                                             newton_maxiter=newton_maxiter,
                                                             stable_maxiter=stable_maxiter)
            self.set_frustration(start_f[..., None])
            f_funcs = np.array(lambda df, f_start=start_f: f_start - df, dtype=object)
            df_down, _, _, state_down, info_down = self.compute_maximal_parameter(If, f_funcs, initial_guess=initial_guess,
                                                              lambda_steps=lambda_steps,
                                                              lambda_stepsize=lambda_stepsize,
                                                              tol=tol, newton_stop_tol=newton_stop_tol,
                                                              newton_maxiter=newton_maxiter,
                                                              stable_maxiter=stable_maxiter)
            return (start_f - df_down, start_f + df_up), mask, (state_down, state_up), (info_down, info_up)
        else:
            f_lower_bound[~mask] = np.nan
            f_upper_bound[~mask] = np.nan
            prob = self[mask]
            self.set_frustration(self.frustration[..., 0, None])
            prob.set_frustration(prob.frustration[..., 0, None])
        I_func = np.zeros(prob.shape(), dtype=object)
        fup_func = np.zeros(prob.shape(), dtype=object)
        fdown_func = np.zeros(prob.shape(), dtype=object)
        start_f = prob.frustration[..., 0].copy()
        for idx in np.ndindex(prob.shape()):
            I_func[idx]     = lambda df: 0.0
            fup_func[idx]   = lambda df, f_start=start_f[idx]: f_start + df
            fdown_func[idx] = lambda df, f_start=start_f[idx]: f_start - df
        df_up, _, _, state_up, info_up = prob.compute_maximal_parameter(I_func, fup_func, initial_guess=initial_guess,
                                                         lambda_steps=lambda_steps,
                                                         lambda_stepsize=lambda_stepsize,
                                                         tol=tol, newton_stop_tol=newton_stop_tol,
                                                         newton_maxiter=newton_maxiter,
                                                         stable_maxiter=stable_maxiter)
        prob.set_frustration(start_f[..., None])
        df_down, _, _, state_down, info_down = prob.compute_maximal_parameter(I_func, fdown_func, initial_guess=initial_guess,
                                                           lambda_steps=lambda_steps,
                                                           lambda_stepsize=lambda_stepsize,
                                                           tol=tol, newton_stop_tol=newton_stop_tol,
                                                           newton_maxiter=newton_maxiter,
                                                           stable_maxiter=stable_maxiter)
        f_upper_bound[mask] = start_f + df_up
        f_lower_bound[mask] = start_f - df_down
        return (f_lower_bound, f_upper_bound), mask, (state_down, state_up), (info_down, info_up)

    def compute_maximal_current(self, initial_guess: StaticConfiguration | InitialCondition = None,
                                I_steps=20, I_stepsize=0.3, tol=1E-5, newton_stop_tol=3,
                                newton_maxiter=100, stable_maxiter=200):
        if self.frustration.shape[-1] != 1:
            raise ValueError("frustration cannot be position-dependent")
        from dynamic_problem import InitialCondition, DefaultIntialCondition

        if initial_guess is None:
            initial_guess = DefaultIntialCondition()
        if isinstance(initial_guess, InitialCondition):
            I = self.external_current.copy()
            self.set_external_current(np.zeros(1, dtype=np.double))
            initial_guess = initial_guess.generate(self)
            self.set_external_current(I)
        I_lowerbound, I_upperbound, mask, lower_config, iteration_info = _compute_maximal_current(
            self, initial_guess, I_steps=I_steps, I_stepsize=I_stepsize,
            newton_maxiter=newton_maxiter, stable_maxiter=stable_maxiter, tol=tol,
            newton_stop_tol=newton_stop_tol)
        return I_lowerbound, I_upperbound, mask, lower_config, iteration_info

    def compute_maximal_parameter(self, IExt_func, f_func,
                                  initial_guess: StaticConfiguration | InitialCondition = None,
                                  lambda_steps=20, lambda_stepsize=0.3, tol=1E-5,
                                  newton_stop_tol=3, newton_maxiter=100, stable_maxiter=200):

        from dynamic_problem import InitialCondition, DefaultIntialCondition

        """
        Finds the largest value of lambda for which a problem which external_current=IExt_func(lambda)
        and frustration=f_func(lambda) has a stable stationary state. IExt_func and f_func must be arrays
        of scalar functions with a shape broadcastable to self.shape()

         - Must be able to find a stable configuration at lambda=0 to work, which may require
           to manually specify an initial_condition sufficiently close to a solution (at lambda=0).   
         - returns a lower- and upperbound for lambda, at the first a stable solution is found and 
           at the second none is found. Increase lambda_steps to improve accuracy.
         - furthermore returns lower_config containing the solutions at the lower_bound.
         - ignores self.external_current and self.frustration, and upon finishing it assigns 
           IExt_func(lambda_lowerbound) and f_func(lambda_lowerbound) to self.external_current 
           and self.frustration respectively.

        """
        self.set_external_current(np.zeros(IExt_func.shape, dtype=np.double))
        self.set_frustration(np.zeros(f_func.shape + (1,), dtype=np.double))
        self.assign_property_from_function("IExt", IExt_func, np.zeros(self.shape(), dtype=np.double))
        self.assign_property_from_function("f", f_func, np.zeros(self.shape(), dtype=np.double))

        if initial_guess is None:
            initial_guess = DefaultIntialCondition()
        if isinstance(initial_guess, InitialCondition):
            initial_guess = initial_guess.generate(self)
        lambda_lowerbound, lambda_upperbound, mask, lower_config, iteration_info = _compute_maximal_parameter(
            self, IExt_func, f_func, initial_guess, lambda_steps=lambda_steps,
            lambda_stepsize=lambda_stepsize, tol=tol, newton_stop_tol=newton_stop_tol,
            newton_maxiter=newton_maxiter, stable_maxiter=stable_maxiter)
        return lambda_lowerbound, lambda_upperbound, mask, lower_config, iteration_info

    def compute_current_dome(self, num_angles=20, manual_start_frustration=None,
                             start_initial_guess: StaticConfiguration | InitialCondition = None,
                             dome_centre_initial_guess: StaticConfiguration | InitialCondition = None,
                             lambda_steps=20, lambda_stepsize=0.3, tol=1E-5, newton_stop_tol=3,
                             newton_maxiter=100, stable_maxiter=200):
        if manual_start_frustration is None:
            self.set_frustration(np.mean(self.nt(), axis=-1)[..., None])
        else:
            self.set_frustration(manual_start_frustration[..., None])
        self.set_external_current(np.zeros((), dtype=np.double))
        if self.shape() == ():
            mask = self.has_stable_solution(tol=tol, stable_maxiter=stable_maxiter)
            if not mask:
                return np.nan, np.nan, None, None
            prob = self
        else:
            mask = self.has_stable_solution(tol=tol, stable_maxiter=stable_maxiter)
            prob = self[mask]
        f_bounds, _, _, _ = prob.compute_frustration_bounds(initial_guess=start_initial_guess,
                             lambda_steps=lambda_steps, lambda_stepsize=lambda_stepsize, tol=tol,
                             newton_stop_tol=newton_stop_tol,
                             newton_maxiter=newton_maxiter, stable_maxiter=stable_maxiter)
        f_lower, f_upper = f_bounds[0], f_bounds[1]
        prob.set_frustration((0.5 * (f_lower + f_upper))[..., None])
        dome_centre = prob.copy()
        I_max, _, _, _, _ = prob.compute_maximal_current(initial_guess=dome_centre_initial_guess,
                             I_steps=lambda_steps, I_stepsize=lambda_stepsize, tol=tol, newton_stop_tol=newton_stop_tol,
                             newton_maxiter=newton_maxiter, stable_maxiter=stable_maxiter)
        angles = np.linspace(0, np.pi, num_angles)
        I_out = np.zeros(prob.shape() + (num_angles,), dtype=np.double)
        f_out = np.zeros(prob.shape() + (num_angles,), dtype=np.double)
        all_iter_info = []
        for i, angle in enumerate(angles):
            I_func = np.zeros(prob.shape(), dtype=object)
            f_func = np.zeros(prob.shape(), dtype=object)
            for idx in np.ndindex(prob.shape()):
                df = 0.5 * (f_upper[idx] - f_lower[idx])
                fm = 0.5 * (f_upper[idx] + f_lower[idx])
                I_func[idx] = lambda l, a=angle, w=I_max[idx]: l * np.sin(a) * w
                f_func[idx] = lambda l, a=angle, w=df, o=fm: o + l * np.cos(a) * w
            l, _, _, _, iter_info = prob.compute_maximal_parameter(I_func, f_func, initial_guess=dome_centre_initial_guess,
                             lambda_steps=lambda_steps, lambda_stepsize=lambda_stepsize, tol=tol,
                             newton_stop_tol=newton_stop_tol,
                             newton_maxiter=newton_maxiter, stable_maxiter=stable_maxiter)
            all_iter_info += [(angle, iter_info)]
            if self.shape() != ():
                f_out[mask, i] = 0.5 * (f_upper + f_lower) + 0.5 * l * np.cos(angle) * (f_upper - f_lower)
                I_out[mask, i] = l * np.sin(angle) * I_max
            else:
                f_out[i] = 0.5 * (f_upper + f_lower) + 0.5 * l * np.cos(angle) * (f_upper - f_lower)
                I_out[i] = l * np.sin(angle) * I_max
        return f_out, I_out, dome_centre, all_iter_info

    def __str__(self):
        return "static problem: " + self.shape().__str__() + \
               "\n\texternal current: " + self.external_current.shape.__str__() + \
               "\n\tfrustration: " + self.frustration.shape.__str__() + \
               "\n\ttarget vortex configuration: " + self.target_vortex_configuration.shape.__str__() + \
               "\n\tphase zone: " + self.phase_zone.shape.__str__() + \
               "\n\tcurrent-phase relation: " + self.current_phase_relation.__str__()

    def assign_property_from_function(self, property, function, function_argument):
        property_array = np.zeros(self.shape(), dtype=np.double)
        function = np.broadcast_to(function, self.shape())
        with np.nditer(property_array, op_flags=['readwrite']) as property_it:
            for function_v, function_argument_v, property_it_v in \
                    zip(np.nditer(function, flags=["refs_ok"]), np.nditer(function_argument), property_it):
                property_it_v[...] = function_v.item()(function_argument_v)
        if property == "IExt":
            self.set_external_current(property_array)
        if property == "f":
            self.set_frustration(property_array[..., None])
        return self


class StaticConfiguration:
    """
    Represents an array (of shape pr_shape) of configurations of a Josephson
    array. One can query several properties of the array configurations:

    It is defined by a problem, array and theta. Here theta must be of shape
    equal (*pr_shape, Nj), where pr_shape = problem.shape().

    The properties are:                     (symbol)            (shape)
     - phases                               phi                 (pr_shape, Nn)
     - gauge_invariant_phase_difference     theta               (pr_shape, Nj)
     - vortex_configuration                 n                   (pr_shape, Nj)
     - junction_current                     I                   (pr_shape, Nj)
     - path_current                         J                   (pr_shape, Np)
     - josephson_energy                     EJ                  (pr_shape, Nj)
     - magnetic_energy                      EM                  (pr_shape, Nj)
     - total_energy                         Etot                (pr_shape, Nj)

    A property query is done with te command .get_[symbol]()

    It need not represent an exact solution to the specified problem. One can
    check this with the method .is_solution()

    To check how well it solves the system, one can use .get_error()
    This has two return quantities, the first represents how well the Kirchhoffs
    rules are satisfied, the second how well the path rules are satisfied.

    Lastly, one can check dynamic stability. A solution only indicates an
    extremum in the potential energy landscape, not necessarily a local
    minimum. .is_stable() is used to determine a local minimum.
    """

    def __init__(self, problem: StaticProblem, theta: np.ndarray,
                 newton_iter_info: NewtonIterInfo = None):
        self.problem = problem
        self.theta = theta
        self.newton_iter_info = newton_iter_info
        self.stable_iter_info = None

    def array(self) -> Array:
        return self.problem.get_array()

    def shape(self):
        return self.problem.shape()

    def get_newton_iter_info(self):
        return self.newton_iter_info

    def get_stable_iter_info(self):
        if self.stable_iter_info is None:
            self.is_stable()
        return self.stable_iter_info

    def _set_stable_iter_info(self, info):
        self.stable_iter_info = info

    def __getitem__(self, item):
        if not isinstance(item, tuple):
            item = (item,)
        return StaticConfiguration(self.problem[item], self.theta[item + (slice(None, ),)])

    def get_phi(self) -> np.ndarray:
        s = self.array().solver
        Msq_solver = s.get_Msq_solver()
        return s.unpack(Msq_solver(s.M_dot(self.theta, u=False)))

    def get_theta(self) -> np.ndarray:
        return self.theta

    def get_n(self) -> np.ndarray:
        s = self.array().solver
        return self.problem.z() - s.A_dot(np.round(self.theta / (2 * np.pi))).astype(int)

    def get_I(self) -> np.ndarray:
        return self.problem.current_phase_relation.eval(self.array().Ic(), self.theta)

    def get_J(self) -> np.ndarray:
        s = self.array().solver
        Asq_solver = s.get_Asq_solver()
        return s.unpack(Asq_solver(s.A_dot(self.get_I(), u=False)))

    def get_flux(self) -> np.ndarray:
        s = self.array().solver
        if self.array().has_inductance():
            return s.A_dot(s.L_dot(self.get_I(), u=False), p=False) / (2 * np.pi)
        else:
            return np.zeros(self.problem.shape() + (self.array().Np(),), dtype=np.double)

    def get_EM(self) -> np.ndarray:
        s = self.array().solver
        if self.array().has_inductance():
            return 0.5 * s.L_dot(self.get_I() ** 2)
        else:
            return np.zeros(self.problem.shape() + (self.array().Nj(),), dtype=np.double)

    def get_EJ(self) -> np.ndarray:
        return self.problem.icp(self.array().Ic(), self.theta)

    def get_Etot(self) -> np.ndarray:
        return self.get_EJ() + self.get_EM()

    def is_solution(self, tol=1E-5):
        return self.satisfies_kirchhoff_rules(tol) & self.satisfies_winding_rules(tol)

    def is_target_solution(self, tol=1E-5):
        return self.is_solution(tol=tol) & self.satisfies_target_vortices()

    def is_stable_target_solution(self, tol=1E-5, stable_maxiter=200):
        return self.is_target_solution(tol=tol) & self.is_stable(tol=tol, maxiter=stable_maxiter)

    def get_error(self):
        return self.get_error_kirchhoff_rules(), self.get_error_winding_rules()

    def is_stable(self, tol=1E-5, maxiter=200) -> np.ndarray:
        if self.array().has_inductance():
            stableQ, stable_info = _is_stable_inductance(self, tol=tol, maxiter=maxiter)
        else:
            stableQ, stable_info = _is_stable_no_inductance(self, tol=tol, maxiter=maxiter)
        self._set_stable_iter_info(stable_info)
        return stableQ

    def satisfies_kirchhoff_rules(self, tol=1E-5):
        return self.get_error_kirchhoff_rules() < tol

    def satisfies_winding_rules(self, tol=1E-5):
        return self.get_error_winding_rules() < tol

    def satisfies_target_vortices(self):
        return np.all(self.get_n() == self.problem.nt(), axis=-1)

    def get_error_kirchhoff_rules(self) -> np.ndarray:
        s = self.array().solver
        x = self.problem.cp(self.array().Ic(), self.theta)
        ref = np.maximum(scipy.linalg.norm(x, axis=-1), self.problem.IpJ_norm())
        ref = np.maximum(0.2 * np.sqrt(self.array().Nn()), ref)
        return scipy.linalg.norm(s.M_dot(x - self.problem.IpJ()), axis=-1) / ref

    def get_error_winding_rules(self) -> np.ndarray:
        s = self.array().solver

        if self.array().has_inductance():
            x = self.theta + s.L_dot(self.get_I())
            ref = np.maximum(0.2 * np.sqrt(self.array().Np()), self.problem.df_norm())
            ref = np.maximum(scipy.linalg.norm(x, axis=-1), ref)
            return scipy.linalg.norm(s.A_dot(x) - self.problem.df(), axis=-1) / ref
        else:
            ref = np.maximum(0.2 * np.sqrt(self.array().Np()), self.problem.df_norm())
            ref = np.maximum(scipy.linalg.norm(self.theta, axis=-1), ref)
            return scipy.linalg.norm(s.A_dot(self.theta) - self.problem.df(), axis=-1) / ref

    def project_onto_winding_rules(self, method=0):
        """
        Projects th onto the winding rules, so the projection satisfies the winding rules.


        So the map th -> th + Dth(df) is applied where df = 2*pi*(z-area*f).
        There are two methods:

            Method nr   Operation
            0 (no ind)  Dth = -AT @ ((A @ AT) \ (A @ th - df))
              (ind)     Dth = -AT @ ((A @ (Ic + L) @ AT) \ (A @ (Ic + L) @ th - df))
            1           Dth = array.A_solve(df - A @ th)

        Method 1 is faster, but changes theta's component in the cut space, whereas method 0
        preserves theta's component in the cut space (M @ Dth = 0 only for method 0).

        Projection only works if array has no inductance. (self.array.has_inductance()=False)
        However, for method 0 with inductance an approximation is made that will come close
        in practice, using the sin(th)=th approximation, and noting that with large inductance
        th will generally be close to 0 in the phase zone z=n
        """
        self.theta = _project_to_winding_rules(self.array(), self.theta, self.problem.df(), method=method)

    def change_phase_zone(self, new_phase_zone):
        self.theta = _change_phase_zone(self.array(), self.theta,
                                        self.problem.phase_zone, new_phase_zone)
        self.problem.phase_zone = new_phase_zone
        return self

    def plot(self, show_vortices=True, vortex_diameter=0.25, vortex_color=(0, 0, 0),
                 anti_vortex_color=(0.8, 0.1, 0.2), vortex_alpha=1, show_grid=True, grid_width=1,
                 grid_color=(0.3, 0.5, 0.9), grid_alpha=0.5, show_colorbar=True, show_arrows=True,
                 arrow_quantity="I", arrow_width=0.005, arrow_scale=1, arrow_headwidth=3, arrow_headlength=5,
                 arrow_headaxislength=4.5, arrow_minshaft=1, arrow_minlength=1, arrow_color=(0.2, 0.4, 0.7),
                 arrow_alpha=1, show_nodes=True, node_diameter=0.2,
                 node_face_color=(1,1,1), node_edge_color=(0, 0, 0), node_alpha=1, show_node_quantity=False,
                 node_quantity="phase", node_quantity_cmap=None, node_quantity_clim=(0, 1), node_quantity_alpha=1,
                 node_quantity_logarithmic_colors=False, show_path_quantity=False, path_quantity="n",
                 path_quantity_cmap=None, path_quantity_clim=(0, 1), path_quantity_alpha=1,
                 path_quantity_logarithmic_colors=False,
                 figsize=None, title="", **kwargs):

        from array_visualize import ArrayPlot

        return ArrayPlot(self, show_vortices = show_vortices, vortex_diameter = vortex_diameter,
                         vortex_color = vortex_color, anti_vortex_color = anti_vortex_color,
                         vortex_alpha = vortex_alpha, show_grid = show_grid, grid_width = grid_width,
                         grid_color = grid_color, grid_alpha = grid_alpha, show_colorbar=show_colorbar,
                         show_arrows = show_arrows,
                         arrow_quantity = arrow_quantity, arrow_width = arrow_width, arrow_scale = arrow_scale,
                         arrow_headwidth = arrow_headwidth, arrow_headlength = arrow_headlength,
                         arrow_headaxislength = arrow_headaxislength, arrow_minshaft = arrow_minshaft,
                         arrow_minlength = arrow_minlength, arrow_color = arrow_color,
                         arrow_alpha = arrow_alpha,
                         show_nodes = show_nodes, node_diameter = node_diameter,
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

    def report(self):
        print("Kirchhoff rules error:    ", self.get_error_kirchhoff_rules())
        print("Path rules error:         ", self.get_error_winding_rules())
        print("is stable:                ", self.is_stable())
        print("is target vortex solution:", self.satisfies_target_vortices())

# IMPLEMENTATIONS Static Array Problems
def _get_df(array: Array, f, z):
    return 2.0 * np.pi * (z - f * array.areas)

def _phi_r_solve(array: Array, theta_minus_g):
    s = array.solver
    Msq_solver = s.get_Msq_solver()
    x = s.M_dot(theta_minus_g, u=False)
    y = Msq_solver(x)
    return s.unpack(y)

def _project_to_winding_rules(array: Array, theta, df, method=0):
    s = array.solver
    Asq_solver = s.get_Asq_solver()
    if method == 0:
        if array.has_inductance():
            return _project_to_winding_rules_approximate_inductance(array, theta, df)
        else:
            return theta - s.AT_dot(Asq_solver(s.pack(s.A_dot(theta) - df)), p=False)
    if method == 1:
        return theta + s.A_solve(df - s.A_dot(theta))

def _project_to_winding_rules_approximate_inductance(array: Array, theta, df):
    s = array.solver
    Ls_solver = s.get_L_sandwich_solver(array.Ic(), 1)
    if np.allclose(theta, 0):
        out = theta + s.AT_dot(Ls_solver(s.pack(df)), p=False)
        if not np.allclose(np.round(out / (2 * np.pi)), 0):
            print("warning: winding rule approximation likely bad")
    else:
        dth =2 * np.pi * np.round(theta / (2 * np.pi))
        X = s.A_dot(s.L_dot(array.Ic() * (theta - dth)) + theta)
        out = theta - s.AT_dot(Ls_solver(s.pack(X - df)), p=False)
        if not np.allclose(2 * np.pi * np.round(out / (2 * np.pi)), dth):
            print("warning: winding rule approximation likely bad")
    return out

def _change_phase_zone(array: Array, theta, z_old, z_new):
    s = array.solver
    return theta + 2.0 * np.pi * s.A_solve(z_new - z_old)


def _arctan_phi_to_theta(prob: StaticProblem, phi):
    array = prob.get_array()
    s = array.solver
    theta = _project_to_winding_rules(array, s.MT_dot(phi), _get_df(array, prob.f(), 0), method=0)
    if not np.all(prob.z() == 0):
        theta = _change_phase_zone(array, theta, 0, prob.z())
    return theta

def _approximate_arctan(prob: StaticProblem):
    array = prob.get_array()
    phi = np.zeros(prob.shape() + (array.Nnr(),), dtype=np.double)
    centr_x, centr_y = array.centroids()
    x, y = array.get_node_coordinates()
    x, y = x[:-1], y[:-1]
    nt = prob.nt()
    ids = (nt != 0).nonzero()
    if len(ids) > 1:
        unique_vortex_locations = np.unique(ids[-1], return_inverse=True)
        x0, y0 = centr_x[unique_vortex_locations], centr_y[unique_vortex_locations]
        windings = -np.arctan2(y - y0[:, None], x - x0[:, None])
        for i in range(len(ids[-1])):
            i_ids = tuple([idx[i] for idx in ids])
            phi[..., i_ids[:-1], :] += nt[i_ids] * windings[i, :]
    else:
        x0, y0 = centr_x[nt != 0], centr_y[nt != 0]
        phi = -np.sum(np.arctan2(y - y0[:, None], x - x0[:, None]) * nt[nt != 0, None], axis=0)
    return _arctan_phi_to_theta(prob, phi)


def _approximate_arctan2(prob: StaticProblem, x0, y0, n0, prob_ids):
    array = prob.get_array()
    phi = np.zeros(prob.shape() + (array.Nnr(),), dtype=np.double)
    x0 = np.atleast_1d(np.array(x0, dtype=np.double))
    y0 = np.atleast_1d(np.array(y0, dtype=np.double))
    n0 = np.atleast_1d(np.array(n0, dtype=int))
    x, y = array.get_node_coordinates()
    x, y = x[:-1], y[:-1]
    if len(n0) > 1:
        windings = -np.arctan2(y - y0[:, None], x - x0[:, None])
        for i in range(len(n0)):
            phi[..., prob_ids[i]] += n0[i] * windings[i, :]
    else:
        phi = -np.sum(np.arctan2(y - y0[:, None], x - x0[:, None]) * n0, axis=0)
    return _arctan_phi_to_theta(prob, phi)


def _approximate_london(prob: StaticProblem):
    array = prob.get_array()
    df = _get_df(array, prob.f(), prob.nt())
    theta = _project_to_winding_rules(array, np.zeros(array.Nj(), dtype=np.double),
                                      df, method=0)
    if not np.all(prob.z() == prob.nt()):
        theta = _change_phase_zone(array, theta, prob.nt(), prob.z())
    return theta


def _compute_maximal_current(prob: StaticProblem, initial_guess=None, I_steps=20, I_stepsize=0.3,
                             tol=1E-5, newton_stop_tol=3, newton_maxiter=100, stable_maxiter=200):
    if prob.frustration.shape[-1] != 1:
        raise ValueError("frustration cannot be position-dependent")
    f = np.broadcast_to(prob.frustration[..., 0], prob.shape())
    I_func = np.zeros(prob.shape(), dtype=object)
    f_func = np.zeros(prob.shape(), dtype=object)
    for idx in np.ndindex(prob.shape()):
        I_func[idx] = lambda x: x
        f_func[idx] = lambda x, y=f[idx]: y
    return _compute_maximal_parameter(prob, I_func, f_func, initial_guess=initial_guess,
                                      lambda_steps=I_steps, lambda_stepsize=I_stepsize, tol=tol,
                                      newton_stop_tol=newton_stop_tol, newton_maxiter=newton_maxiter,
                                      stable_maxiter=stable_maxiter)


def _compute_maximal_parameter(prob: StaticProblem, IExt_func, f_func, initial_guess, lambda_steps=20,
                               lambda_stepsize=0.3, tol=1E-5, newton_stop_tol=3, newton_maxiter=100,
                               stable_maxiter=200):
    # IExt_func: array of scalar functions of shape broadcastable to prob.shape()
    # f_func: array of scalar functions of shape broadcastable to prob.shape()
    tic = time.perf_counter()
    lambda_val = np.zeros(prob.shape(), dtype=np.double)
    prob.assign_property_from_function("IExt", IExt_func, lambda_val)
    prob.assign_property_from_function("f", f_func, lambda_val)
    sel_prob, mask = prob.select_solutions(initial_guess=initial_guess, tol=tol, newton_stop_tol=newton_stop_tol,
                                           newton_maxiter=newton_maxiter,
                                           stable_maxiter=stable_maxiter, return_mask=True)

    if np.sum(mask) == 0:
        return np.nan, np.nan, None, None, {"problem_has_solution_at_start_value": mask, "lambda": [], "I": [], "f": [],
            "found_solution": [], "newton_steps": []}
    IExt_func = IExt_func[mask]
    f_func = f_func[mask]
    initial_guess = initial_guess[mask]

    lambda_val = np.zeros(sel_prob.shape(), dtype=np.double)
    found_upper_bound = np.zeros(sel_prob.shape(), dtype=bool)
    newton_steps_history = np.zeros(sel_prob.shape() + (lambda_steps,), dtype=int)
    lambda_history = np.zeros(sel_prob.shape()+ (lambda_steps,), dtype=np.double)
    I_history = np.zeros(sel_prob.shape() + (lambda_steps,), dtype=np.double)
    f_history = np.zeros(sel_prob.shape() + (lambda_steps,), dtype=np.double)
    found_history = np.zeros(sel_prob.shape()+ (lambda_steps,), dtype=bool)
    lambda_stepsz = np.array(np.ones(sel_prob.shape(), dtype=np.double) * lambda_stepsize, dtype=np.double)
    upper_bound_found = np.zeros(sel_prob.shape(), dtype=bool)

    all_stable_info = []
    all_newton_iter_info = []
    for I_step in range(lambda_steps):
        lambda_history[..., I_step] = lambda_val
        sel_prob.assign_property_from_function("IExt", IExt_func, lambda_val)
        sel_prob.assign_property_from_function("f", f_func, lambda_val)
        I_history[..., I_step] = sel_prob.external_current
        f_history[..., I_step] = sel_prob.frustration[..., 0]
        out = sel_prob.compute(initial_guess, maxiter=newton_maxiter, tol=tol, stop_tol=newton_stop_tol)
        newton_iter_info = out.get_newton_iter_info()
        all_newton_iter_info += [newton_iter_info]
        newton_steps_history[..., I_step] = newton_iter_info.get_step_count()
        solQ = out.is_target_solution(tol=tol)
        if solQ.size == 1:
            stableQ = out.is_stable(tol=tol, maxiter=stable_maxiter)
            solQ &= stableQ
        else:
            stableQ= out[solQ].is_stable(tol=tol, maxiter=stable_maxiter)
            solQ[solQ] &= stableQ
        all_stable_info += [(stableQ, out.get_stable_iter_info())]
        found_history[..., I_step] = solQ
        found_upper_bound = found_upper_bound | (~solQ)
        if sel_prob.shape() == ():
            if solQ:
                lambda_val += lambda_stepsz
                initial_guess.theta = out.theta
            else:
                lambda_val -= lambda_stepsz
            upper_bound_found |= (not solQ)
            if found_upper_bound:
                lambda_stepsz /= 2
        else:
            lambda_val[solQ] = lambda_val[solQ] + lambda_stepsz[solQ]
            initial_guess.theta[solQ, :] = out.theta[solQ, :]
            lambda_val[(~solQ)] = lambda_val[(~solQ) ] - lambda_stepsz[(~solQ)]
            upper_bound_found |= (~solQ)
            lambda_stepsz[found_upper_bound] = lambda_stepsz[found_upper_bound] / 2

    lower_bound = np.zeros(prob.shape(), dtype=np.double)
    upper_bound = np.zeros(prob.shape(), dtype=np.double)
    lower_bound[...], upper_bound[...] = np.nan, np.nan
    lower_bound[mask] = lambda_val - lambda_stepsz
    upper_bound[mask] = lambda_val.copy()
    upper_bound[mask][~upper_bound_found] = np.inf

    sel_prob.assign_property_from_function("IExt", IExt_func, lambda_val - lambda_stepsz)
    sel_prob.assign_property_from_function("f", f_func, lambda_val - lambda_stepsz)

    lower_config = sel_prob.compute(initial_guess, tol=tol, stop_tol=newton_stop_tol,
                                    maxiter=newton_maxiter)

    parameter_optimize_info = ParameterOptimizeInfo(mask, lambda_history, I_history,
                                                    f_history, found_history, newton_steps_history,
                                                    all_newton_iter_info, all_stable_info,
                                                    time.perf_counter() - tic)

    return lower_bound, upper_bound, mask, lower_config, parameter_optimize_info

def _static_compute_no_inductance(prob: StaticProblem, initial_guess=None, tol=1E-5, stop_tol=3, maxiter=100):
    iter_info = NewtonIterInfo(prob.shape(), tol, stop_tol, maxiter)
    tic = time.perf_counter()
    array = prob.get_array()
    s = array.solver
    Ic = array.Ic()[:, None]
    shape = prob.shape()
    theta = 0 if initial_guess is None else initial_guess.theta.copy()
    g1 = prob.g()
    g = np.broadcast_to(g1, shape + (array.Nj(),))
    phi = s.pack(np.broadcast_to(_phi_r_solve(array, theta - g), shape + (array.Nnr(),)).copy())
    prob_count = phi.shape[-1]
    g = s.pack(g)
    IpJ = s.pack(np.broadcast_to(prob.IpJ(), shape + (array.Nj(),)))
    ref_error = np.maximum(scipy.linalg.norm(IpJ, axis=0), 0.2 * np.sqrt(array.Nn()))
    Icp = prob.cp(array.Ic()[:, None], g + s.MT_dot(phi, p=False, u=False))

    ref = np.maximum(ref_error, scipy.linalg.norm(Icp, axis=0))
    error = scipy.linalg.norm(s.M_dot(Icp - IpJ, p=False, u=False), axis=0) / ref
    are_converged = error < tol
    are_hopeless = np.zeros(prob_count, dtype=bool)
    iter_info._update(error, are_hopeless, are_converged)
    iteration = 0
    while not np.all(are_converged | are_hopeless) and iteration < maxiter:
        select_mask = ~(are_converged | are_hopeless)
        phi_sel = phi[:, select_mask]
        g_sel = g[:, select_mask]
        th_sel = g_sel + s.MT_dot(phi_sel, p=False, u=False)
        IpJ_sel = IpJ[:, select_mask]

        b_sel = s.M_dot(prob.cp(Ic, th_sel) - IpJ_sel, p=False, u=False)
        for i in range(b_sel.shape[-1]):
            Ms_solver = s.get_M_sandwich_solver(prob.dcp(Ic.flatten(), th_sel[:, i]), force_factorize=True)
            phi_sel[:, i] -= Ms_solver(b_sel[:, i])
        phi[:, select_mask] = phi_sel
        Icp = prob.cp(Ic, g_sel + s.MT_dot(phi_sel, p=False, u=False))

        ref[select_mask] = np.maximum(ref_error[select_mask], scipy.linalg.norm(Icp, axis=0))
        error[select_mask] = scipy.linalg.norm(s.M_dot(Icp - IpJ_sel, p=False, u=False), axis=0) / ref[select_mask]
        hopeless_error = 10 ** (np.log(stop_tol)/np.log(10) - (1 - np.log(tol)/np.log(10))/maxiter * iteration)
        are_hopeless[select_mask] = (error[select_mask] > hopeless_error)
        are_converged = error < tol
        iter_info._update(error, are_hopeless, are_converged)
        iteration += 1
    s.MsqS_factorized = None
    iter_info._finish(time.perf_counter() - tic)
    return s.unpack(g + s.MT_dot(phi, p=False, u=False)), iter_info


def _static_compute_inductance(prob: StaticProblem, initial_guess=None, tol=1E-5, stop_tol=3, maxiter=100):
    iter_info = NewtonIterInfo(prob.shape(), tol, stop_tol, maxiter, has_path_error=True)
    tic = time.perf_counter()

    array = prob.get_array()
    s = array.solver
    Ic = array.Ic()[:, None]
    shape = prob.shape()
    theta = 0 if initial_guess is None else initial_guess.theta.copy()
    theta = s.pack(np.broadcast_to(theta, shape + (array.Nj(),)).copy())
    prob_count = theta.shape[-1]

    IpJ = s.pack(np.broadcast_to(prob.IpJ(), shape + (array.Nj(),)))
    df = s.pack(np.broadcast_to(prob.df(), shape + (array.Np(),)))
    J0 = df - s.A_dot(s.L_dot(IpJ, p=False, u=False), p=False, u=False)
    I = prob.cp(Ic, theta)

    kirch_ref_error = np.maximum(scipy.linalg.norm(IpJ, axis=0), 0.2 * np.sqrt(array.Nn()))
    kirch_ref = np.maximum(kirch_ref_error, scipy.linalg.norm(I, axis=0))
    error_kirchhoff = scipy.linalg.norm(s.M_dot(I - IpJ, p=False, u=False), axis=0) / kirch_ref
    path_theta = theta + s.L_dot(I, p=False, u=False)
    path_ref_error = np.maximum(scipy.linalg.norm(df, axis=0), 0.2 * np.sqrt(array.Np()))
    path_ref = np.maximum(path_ref_error, scipy.linalg.norm(path_theta, axis=0))
    error_path = scipy.linalg.norm(s.A_dot(path_theta, p=False, u=False) - df, axis=0) / path_ref
    error = np.maximum(error_kirchhoff, error_path)
    are_converged = error < tol
    are_hopeless = np.zeros(prob_count, dtype=bool)
    iter_info._update(error_kirchhoff, are_hopeless, are_converged, error_path)

    iteration = 0
    while not np.all(are_converged | are_hopeless) and iteration < maxiter:
        select_mask = ~(are_converged | are_hopeless)
        th_sel = theta[:, select_mask]
        I_sel = prob.cp(Ic, th_sel)
        J0_sel = J0[:, select_mask]
        IpJ_sel = IpJ[:, select_mask]
        df_sel = df[:, select_mask]
        P = prob.dcp(Ic, th_sel)
        J = J0_sel + s.A_dot((I_sel - IpJ_sel) / P - th_sel, p=False, u=False)
        for i in range(J.shape[-1]):
            Ls_solver = s.get_L_sandwich_solver(1.0, 1.0/P[:, i], force_factorize=True)
            J[:, i] = Ls_solver(J[:, i])
        th_sel += (s.AT_dot(J, p=False, u=False) - (I_sel - IpJ_sel)) / P
        theta[:, select_mask] = th_sel
        I_sel = prob.cp(Ic, th_sel)
        th_sel += s.L_dot(I_sel, p=False, u=False)
        kirch_ref[select_mask] = np.maximum(kirch_ref_error[select_mask], scipy.linalg.norm(I_sel, axis=0))
        path_ref[select_mask] = np.maximum(path_ref_error[select_mask], scipy.linalg.norm(th_sel, axis=0))
        error_kirchhoff[select_mask] = scipy.linalg.norm(s.M_dot(I_sel - IpJ_sel, p=False, u=False), axis=0) / kirch_ref[select_mask]
        error_path[select_mask] = scipy.linalg.norm(s.A_dot(th_sel, p=False, u=False) - df_sel, axis=0) / path_ref[select_mask]
        error = np.maximum(error_kirchhoff, error_path)
        hopeless_error = 10 ** (np.log(stop_tol)/np.log(10) - (1 - np.log(tol)/np.log(10))/maxiter * iteration)
        are_hopeless[select_mask] = (error[select_mask] > hopeless_error)
        are_converged = error < tol
        iter_info._update(error_kirchhoff, are_hopeless, are_converged, error_path)
        iteration += 1
    s.LsqS_factorized = None

    iter_info._finish(time.perf_counter() - tic)
    return s.unpack(theta), iter_info


def _is_stable_no_inductance(config: StaticConfiguration, tol=1E-5, maxiter=200):
    tic = time.perf_counter()
    stab_info = StabilityCheckInfo(config.shape(), tol, maxiter)
    array = config.array()
    s = array.solver
    d_theta = config.problem.dcp(array.Ic(), config.theta).reshape(-1, array.Nj())
    max_eigv = np.zeros(d_theta.shape[0], dtype=np.double)
    for i in range(d_theta.shape[0]):
        Ms_sq = s.get_M_sandwich(-d_theta[i, :])
        if np.all(d_theta[i, :] >=0):
            max_eigv[i] = 0.0
            stab_info._set(i, max_eigv[i], ())
        else:
            lu = scipy.sparse.linalg.splu(Ms_sq, diag_pivot_thresh=0)
            iter_out = [0.0] if np.all(lu.U.diagonal() < tol) else [np.inf]
            stab_info._set(i, iter_out[0], ())
            max_eigv[i] = iter_out[0]
    is_stable = max_eigv < tol
    s.MsqS_factorized = None
    stab_info.elapsed_time = time.perf_counter() - tic
    return is_stable.reshape(config.problem.shape()), stab_info

def _is_stable_inductance(config: StaticConfiguration, tol=1E-5, maxiter=200):
    tic = time.perf_counter()
    stab_info = StabilityCheckInfo(config.shape(), tol, maxiter)
    array = config.array()
    s = array.solver
    A = array.A()
    AT = array.AT()
    d_theta = config.problem.dcp(array.Ic(), config.theta).reshape(-1, array.Nj())
    is_stable = np.zeros(d_theta.shape[0], dtype=bool)
    L_solver = s.get_L_sandwich_solver(force_factorize=True)
    for i in range(d_theta.shape[0]):
        x0 = np.random.rand(array.Nj(), 1)
        def mat_vec(x):
            return -d_theta[i, :] * x.flatten() - AT @ L_solver(A @ x.flatten())
        A_lin = scipy.sparse.linalg.LinearOperator((array.Nj(), array.Nj()), mat_vec)
        lobpcg_out = scipy.sparse.linalg.lobpcg(A_lin, x0, maxiter=maxiter, tol=tol, retLambdaHistory=True,
                                                retResidualNormsHistory=True)
        stab_info._set(i, lobpcg_out[0], lobpcg_out[3])
        is_stable[i] = lobpcg_out[0] <= tol
    s.LsqS_factorized = None
    stab_info.elapsed_time = time.perf_counter() - tic
    return is_stable.reshape(config.problem.shape()), stab_info

