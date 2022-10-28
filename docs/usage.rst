Usage
=====

Fitting a function to data
--------------------------

To plot a power saturation curve, 
you can use the ``fitting_functions.power_saturation()`` function:

.. autofunction:: fitting_functions.power_saturation

This is a hyperbolic function modeling the saturation of SPE emission under
increasing excitation laser power. The function has the form

.. math::
           I(P) = \frac{I_{inf}  P} {P + P_{sat}}
           
where :math:`I_{inf}` is the asymptotic emission intensity, and :math:`P_{sat}` is 
the power at which :math:`I(P) = \frac{1}{2} I_{inf}`.

Here is a simple example of its use:

>>> from fitting_functions import power_saturation
>>> intensities = power_saturation(powers, p0=[I_inf, P_sat])
[0.1, 1.4, ..., 5.7]
