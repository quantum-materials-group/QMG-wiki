"""
A collection of functions to fit to experimental data.
"""

__version__ = "0.1.0"

def power_saturation(x, p0):
    """
    A hyperbolic saturation function.

    :param x: 1D array of power values
    :type x: list[float] or np.array([float])
    :param p0: Parameters for hyperbolic function
    :type p0: list[I_inf, P_sat]
    :return: 1D array of intensity values
    :rtype: type(x)
    """
    return p0[0]*x / (x + p0[1])
