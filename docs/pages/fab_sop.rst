Fabrication Methods
===================

Overview
--------

Please be aware the following SOPs are not for untrained users but for people who have *had* training previously and just need a bit of reminder.


**The variables are subject to change depending on the application of your particular sample!!!**


Photolithography
----------------

For big wafers use big containers.


Stuff you need:

- DI water (MilliQ)

- Hot plate (100 deg C)

Cupboard:

- Developer AZ 726

- Photo resist AZ 1518

Fume Cupboard:

- Spin coater

Steps:

1. To clean substrate: use IPA (Isopropyl Alcohol), either wipe with Kimtech or use spin coater and spray IPA.

2. Select Program on spin coater with rpm ~4000 in vacuum:

   :math:`\rightarrow` Start
   
   - Squirt acetone and then IPA through lid hole.
     
   - Check surface, if not clean then wipe with Kimtech and then spin again with IPA ~ 1 min.

3. Drop resist all over and spread gently using the dropper (do not waste as we are poor):

   :math:`\rightarrow` Start

4. Place substrate on hot plate for 1 min to *bake*.

5. Place substrate on *marked mask* mask, coated side face down.

6. Plug vacuum line in, once aligned: 

7. Turn on *illumination* dial.

   - Pull side rod out for monitor view.
   - Check your pattern is aligned with microscope.

8. Put substrate in, turn down “illumination” to prevent exposure to resist.

9. WEC setting:

   - Close contact lever.
   - Follow instructions.

10. Parameters:

    - Exposure time ~2 sec
    
      :math:`\rightarrow` Load
      
    - Exposure (TURN AWAY).

11. Open lever, take substrate out.

12. Develop for 10 seconds (INSERT DIAGRAM) then immediately into water.

13. Dry surface with N :sub:`2`, bottom side with Kimtech.

14. Check with microscope.

Oxygen Plasma Cleaning
----------------------

1. Manual process. Make sure the bottom two buttons are not green.

2. Vent vacuum

   :math:`\rightarrow` Open Lid :math:`\rightarrow` Load sample :math:`\rightarrow` Close lid :math:`\rightarrow` Turn on vacuum and wait ???pA

3. Select recipe:

.. list-table::
   :widths: 25 25

   * - Pres. Set (mT), 10
     - 10
   * - ICP set
     - 5
   * - RIE set
     - 25
   * - Process time
     - 10
   * - O :sub:`2` Set
     - 25

4. Turn gas on

   :math:`\rightarrow` When gas is ready, turn RF on for 10 seconds.
   


Chemical Vapour Deposition - SEKI
----------------------------------
Please note that this is not a recipe for good growth of materials. It is to utilise the plasma for cleaning/defect activation.


1. Check that pump is attached to the main setup, make sure dial is turned off and the pumping valve is also off when starting.

2. Check if stage is vacuumed, if not, carefully open partially and slowly release.

3. Clean carbon puck and tube with IPA.

4. Load, elevate stage and place sample.

5. Pump on, open valve all the way.

6. Make sure pressure drops to 0.5 [INSERT REF TO INSTRUMENT 1]

   :math:`\rightarrow` SEKI is powered by the bottom right switch (under the big CVD) and is marked with AXSID. Once you hear air hissing it means it is on.
   
7. Turn on computer (pw: PAT2), open IE and select appropriate gas for your application (H :sub:`2`, N :sub:`2` and ?)

   - Check flow point: 0
   
   - After 10 mins, set point: 100-400
   
   :math:`\rightarrow` Start
   
8. Set point on pressure controllers, start at [A] ≈10 Torr, let it settle for a minute or so and then ignite plasma.
   
   -Turn on instrument [2]
   -HV: ON
   -Check F-Watt, if it ignites then it is OK
   
9. Use turning rods to get R Watt as close to 0 as possible

10. Go through set points [B] - [E] (if you need, SLOWLY)

To shut down:

1. Go backwards through set points [E] - [A]

   -When it is close to 10 Torr, turn HV: OFF then shut power, turn pressure to OPEN.
   
2. Turn gas set point: 0

3. Turn off at main power (AXSID marking).

4. Allow 20 mins to cool.

5. Shut off roughing pump

6. Bring down stage very slowly by dropping screws 1 mm each, vent a little Ar :sub:`2`  (green screw)

7. Slowly take screw off and lower stage. 

8. Shut stage, screw in and turn on roughing pump again.


PDMS
----
Making PDMS mould/anything

Stuff you need:

  - 184-Silicone SYLGARD

  - Curing Agent


.. image:: ../_static/pdms.png
  :width: 200

Option 1: (if only a little is needed)

   - Mix on glass lside or small palstic weigh boat
   
Option 2:
   - Mix in beaker (disposable only)
   
Place on heat stage to cure:

   ~ 150 C = 10 min
   
   ~ 100 C = 30 min
   
Lindberg Blue Tube Furnace (max 1100 C)
---------------------------------------


Stuff you need:

- EtOH (for cleaning)

- A clean tube

- Vacuum components (clamps, allan keys, o-rings--> call in the drawer beneath the furnace)

Loading sample:

1. Close B side of the tube

2. Wipe boat/tube with EtOH

3. Push sample to centre using cleaned rod

4. Close A side

To pump:

   :math:`\rightarrow` Pump down

   - Turn 'MAX' handle up, switch pump *on* at outlet.
   
   - Run Ar :sub:`2`
   
      -on computer: ``➔``
      
   - Set point 'B' to 100 sccm, check MFC is stabilised.
   
   - Wait 10 mins.

Program (setting annealing temp): 
``P``
``^``
``˅``
``<``

For top menu, press:

``P``

.. list-table::
   :widths: 25 25

   * - Pr n
     - Select the program number
     
Sub menu, press together x 2:

.. list-table::
   :widths: 25 25

   * - ``P``
     - ``<``
     
     
Blue Emitters in hBN 
---------------------
**Pre-characterisation using Cathodoluminescence**

Cathodoluminescence (CL) characterisation is necessary for making blue emitters in **Pristine** and **Annealed** Japanese flakes.

hBN flakes with a sharp UV emission at 305 nm (and associated phonon replicas at 320, 334, 351 nm) can host 436nm blue emitters after electron irradiation. However, the percentages of creation of blue emitters are different depending on the flake type. UV emission is not always uniform across a single hBN flake. See below for more info on hBN types.

- **Pristine:** As exfoliated high quality NIMS hBN (Japanese) requires pre-characterisation via CL. Only approx 5-10% of flakes have the required UV emission.

- **Pristine Annealed:** After annealing the NIMS hBN (Japanese) will have a higher percentage of flakes with UV emission. Pre-characterisation is still generally preferred as not all flakes show the UV emission.

- **Carbon Doped:** Blue emitters can be produced in all these flakes and pre-characterisation is not required. Generally the electron dose required for 436 nm emitter activation is significantly lower than the other hBN flakes.

NOTE: Thickness is especially important. Thicker flakes generally require a lower electron dose to activate emitters. 

**Electron Beam Irradiation** 

Suitable Irradiation Conditions

- Beam Energy: 1-15 keV
   
- Beam Current: At least 0.8 nA
  
- Dwell Time: At least 1 millisecond
   
- Total Time: Varied based on flake type.

As each flake is different it is important to test irradiations to achieve a suitable electron irradiation dose. Generally for carbon doped hBN the irradiation doses will be much lower than other hBN. For example a single spot may only require 0.5 s total time (~1 nA, 5kV) where pristine hBN may need >30 s for the same conditions.

The Helios SEM can pattern arrays in multiple ways. Either individual spots (set the circle pattern to 0um radius) using the array builder. This works well if a dose series is required as each spot can have a specific dose. If larger arrays of the same dose are required, the rectangular pattern tool can be used. Individual spots can patterned by increasing the pixel spacing to achieve the desired distance between spots. By default it will be very small eg. <100 nm. 

Regarding the chosen beam energy. 5 keV is a good starting point however increasing energy will result in slower activation rate. For the fastest activation rates use 3 keV if drift is controlled.
                                                            
**Issues**

- Carbon contamination:
Aim to have the cleanest hBN possible before beginning irradiations. Utilise one or more of hotplate annealing, plasma cleaning, ozone cleaning where applicable.
Utilise ozone cleaning after irradiation to reduce the background PL from carbon deposition.

- Drift:
Drift can be an issue when patterning with the SEM. If this occurs attempt to change the beam energy to reduce this, or use immersion mode.


**More Info**
Reference: `Gale et.al. (2022)
<https://pubs.acs.org/doi/10.1021/acsphotonics.2c00631>`.


VB- Emitters in hBN/BNNTs
-------------------------
Not all flakes have been tested for VB- creation, but Pristine Japanese flakes are most used. (See above for descriptions).
VB- does not survive high temperatures, so if your fabrication requires any annealing/harsh cleaning steps, irradiate as your last step.

To achieve an ideal pure beam, the species should be switched as early as possible. Switching beams right before irradiating will still create VB-, but for the best results, change the beam and ignite the nitrogen plasma a few hours before or even the night before.

*will insert helios screenshot later*


If you have not been trained on the ion plasma controls, do not change anything. Just make sure it says “Plasma ignited”, and on the Helios interface the “Beam On” button is not greyed out. This means the nitrogen plasma is running, and the longer it runs, the cleaner the beam will be.

To avoid carbon contamination, try to avoid imaging. Although it is necessary to use the electron beam to find the flake of interest, avoid taking high quality long exposure images. You should still save a fast, lower quality image to capture the exact irradiation region.

**Ion Beam Irradiation**

Suitable Irradiation Conditions

- Beam Species: Nitrogen

- Beam Energy: 1-30 keV 

- Beam Current: At least 0.1 nA

- Dwell Time: 300 ns – 1 us 

- Dose: 1E14 N/cm

- Overlap: As close to 100% as possible

- Total Time: Varied based on irradiation size.

Use the dose equation to find the correct time based on your irradiation box size.

*will insert equation later*

The following figure represents the boron vacancy distribution with various nitrogen beam energies. The peak of each curve marks the point of most damage, where the most boron vacancies will be created. Some things to note:

-	SRIM does not account for ion channelling. The incident ions will travel further through the crystal than shown here

-	Higher energies will reach further into the crystal than lower energies

-	The same trends are also seen for nitrogen vacancies. Be aware that too many vacancies created will lead to amorphization and the VB- signal will be impacted.

-	For thinner flakes (under 10 nm), it may be best to use higher energies. The beam will pass through and not create too many defects, so the lattice structure can still hold itself and host the VB-. 
 

**Issues:**
VB- creation experiences similar issues to blue emitter creation. See above to minimise carbon contamination and drift. Drift can also be helped with nearby conductive materials, such as metal clamp stubs or copper tape near the flake of interest. However, these contacts will result in more contamination.

More info: Hennessey et.al. (2024) <https://doi.org/10.1002/qute.202300459>
(Comparing energies/beam species/carbon contamination/sputter yields)

Note: Hydrogen does create VB- but nitrogen is more reliable.





