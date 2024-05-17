Scratch Notepad: Useful notes for  within the Group
===================================================

1. Radiative Lifetime
----------------------
- **Definition:** Lifetime of an electronic state in the (hypothetical) situation where only radiative processes depopulate that level

The radiative lifetime of an electronic state refers to the lifetime which would be obtained through radiative decay only via "spontaneous emission". It is given by the equation

.. math:: 
    \frac{1}{\tau_{rad}} = \frac{8\pi n^2}{c^2} \int v^2 \sigma_{em}(v) \, dv = 8\pi n^2 c \int \frac{\sigma_{em} (\lambda)}{\lambda^4} \, d\lambda



2. Lifetime Measurements: Radiative vs Non-Radiative
-----------------------------------------------------

> *Explanation from Nathan - Written by Ben*

**UNDER CONSTRUCTION - 17/05/24**


- **Question:** In a lifetime measurement, we are only measuring photons incident on the detector. How then, is the final histogram a combination of both radiative and non-radiative decay rates?

Let's consider a two level system with both a radiative and non-radiative decay path (Fig 2.1). These two rates are acting on the excited state population......

An analogy can be used to help explain the effects of two separate rates acting on the same population.

Consider having $100 to survive 4 days with. Each day we decide to spend 10% of our remaining money on food. Here is a histogram for the amount spent on food each day (Fig 2.2).
Day 1 we spend $10, Day 2 we have $90 left so we only spend $9 and so on...
This could then be fit with an exponential and described as a rate.

But let us include a competing rate to the system. Each day, an additional 20% of remaining money is spent on beer.
Fig 2.3a shows the **new** amount spent on food each day and Fig 2.3b shows the amount spent on beer.
The amount spent on food each day is lower than the previous histogram because to each day's new total is consecutively lower due to beer also being purchased.
This shows how the rate of expenditure on food is affected by the inclusion of a second, competing rate to the system.

To bring this back to a two level system, the radiative and non-radiative decay rates can be the rate of expenditure on food and beer respectively. 
The $100 we started with is the excited state population. Or more accurately, the number of measurement repetitions on a single photon emitter.
When we measure lifetime, we can only physically measure photons emitted via the radiative decay. This is the food expenditure histogram. The non-radiative beer expenditure histogram is "hidden" from us because if the APD doesn't click... we don't know what happened.
However, as can be seen in the food/beer analogy, the inclusion of a second rate influences the measured outcome of the first rate, regardless if we actually know what is occurring in that second histogram.
This means that our measured lifetime is always a convolution of both the radiative and non-radiative decay rates and cannot be separated with a single measurement.

**Bonus Point:** Using the same analogy, we can also show that by decreasing the non-radiative decay rate i.e. from 20% to 10%, the measured lifetime is *reduced*. Both of the histograms for food expenditure when amount spent on beer is either 20% or 10% of remaining money are shown below (Fig 2.4).




















