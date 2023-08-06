import numpy as np
import scipy.special

def stencil_derivative(x, y, stencil, order=1):

    """
    computes n-th order numerical derivative of y(x) using a datapoint stencil.

    Notes:
    - a stencil [-1, 0, 1] means to determine dy[i], the x,y points at i-1, i and i+1 are used.
    - x must be ascending but need not be equally spaced.
    - at the edges it uses a shifted stencil such that no points outside the data range are used.
      For example, if stencil=[-2, 0, 3], at point i=1 the stencil used will be [-1, 1, 4].
    - The length of stencil, called s, must be larger than order. So for first derivative, at least
      two stencil points are needed, but more can be used to reduce the numerical error.
    - The length of x, y, called N,  must exceed max(stencil) - min(stencil).
    - Can compute derivative of multiple curves of length N simultaneously. x and y must be arrays
      with broadcast compatible shapes where the last axis of both must equal N.

    input:
        x, y      (..., N) double, N > max(stencil) - min(stencil)
        stencil   (s,) int; s > order
        order     int

    output:
        dy        (..., N) double

    Example:
        x = [0, 0.5,  1, 2, 4,    4.5]
        y = [0, 0.25, 1, 4, 16, 20.25]
        dy = stencil_derivative(x, y, [-1, 1], 1)     -> np.array([1.  1.  2.5 5.  6.5 6.5])
        dy = stencil_derivative(x, y, [-1, 0, 1], 1)  -> np.array([0. 1. 2. 4. 8. 9.])
        ddy = stencil_derivative(x, y, [-1, 0, 1], 2) -> np.array([2. 2. 2. 2. 2. 2.])

    """

    x, y = np.atleast_1d(x),  np.atleast_1d(y)
    N = x.shape[-1]
    x, y = np.broadcast_arrays(x, y)

    stencil = np.atleast_1d(stencil).astype(int).flatten()
    if stencil.ndim > 1:
        raise ValueError("stencil must be 1d list of integers")
    if y.shape[-1] != N:
        raise ValueError("x and y must be same (..., N) shaped arrays with the same N")
    if N <= (np.max(stencil) - np.min(stencil)):
        raise ValueError("x.shape[-1] must be larger than max(stencil)-min(stencil)")
    if not (np.all(np.unique(stencil) == stencil) and len(np.unique(stencil)) == len(stencil)):
        raise ValueError("stencil must be list of sorted unique integers")

    left_pad = -np.min(stencil)
    right_pad = np.max(stencil)
    left_ids = np.arange(left_pad)
    mid_ids = np.arange(left_pad, N-right_pad)
    right_ids = np.arange(N-right_pad, N)

    dy = np.zeros(x.shape, dtype=x.dtype)

    # left edge
    left_pinned_stencil = stencil + left_pad
    for i in left_ids:
        ci = get_stencil_coefficients(x[..., left_pinned_stencil] - x[..., i][..., None], order)
        dy[..., i] = np.sum(y[..., left_pinned_stencil] * ci, axis=-1)

    # middle section
    mid_coeffs = get_stencil_coefficients(x[..., mid_ids[:, None] + stencil] - x[..., mid_ids[..., None]], order)
    dy[..., mid_ids] = np.sum(y[..., mid_ids[:, None] + stencil] * mid_coeffs, axis=-1)

    # right edge
    right_pinned_stencil = stencil + (N - 1) - right_pad
    for i in right_ids:
        ci = get_stencil_coefficients(x[..., right_pinned_stencil] - x[..., i][..., None], order)
        dy[..., i] = np.sum(y[..., right_pinned_stencil] * ci, axis=-1)

    return dy


def get_stencil_coefficients(stencil, order=1):
    # stencil (..., s); s > order. stencil need not be integers.
    stencil = np.atleast_2d(stencil)
    out_shape = stencil.shape
    s = stencil.shape[-1]
    stencil = stencil.reshape(-1, s)
    if s - order <= 0:
        raise ValueError("stencil too small to take derivative")
    idx = np.arange(s)[:, None]
    b = np.zeros(s, dtype=np.double)
    b[order] = 1
    return np.linalg.solve((stencil[:, None, :] ** idx)/ scipy.special.factorial(idx), b[None, :]).reshape(out_shape)

