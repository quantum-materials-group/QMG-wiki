"""
A collection of functions to fit to experimental data.
"""

__version__ = "0.1.0"


class InvalidKindError(Exception):
    """Raised if the kind is invalid."""
    pass

def power_saturation(x, *p0):
    """
    A hyperbolic function modeling the saturation of SPE emission under
           increasing excitation laser power. The function has the form
           I(P) = I_inf * P / (P + P_sat)
           where I_inf is the asymptotic emission intensity, and
                 P_sat is the power at which I(P) = 0.5*I_inf.
    :param x: 1D array of power values
    :type x: list[float] or np.array([float])
    :param *p0: Parameters for hyperbolic function
    :type *p0: list[I_inf, P_sat]
    :raise fitting_functions.InvalidKindError: If the kind is invalid.
    :return: 1D array of intensity values
    :rtype: type(x)
    """
    return p0[0]*x / (x + p0[1])
