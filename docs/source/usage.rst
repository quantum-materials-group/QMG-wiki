Usage
=====

Fitting a function to data
--------------------------

To plot a power saturation curve, 
you can use the ``fitting_functions.power_saturation()`` function:

.. autofunction:: fitting_functions.power_saturation

Here is a simple example:

>>> from fitting_functions import power_saturation
>>> intensities = power_saturation(powers, p0=[I_inf, P_sat])
[0.1, 1.4, ..., 5.7]

