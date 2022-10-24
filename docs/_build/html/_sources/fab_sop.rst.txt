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

   :math:`\rightarrow` Open Lid :math:`\rightarrow` Load sample :math:`\rightarrow` Close lid

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


.. image:: _static/pdms.png
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

**INCOMPLETE 07/10/22**

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




Spectrometer SpecWin Settings
-----------------------------

**INCOMPLETE 07/10/22**

Background Correction Steps

In order to take background correctly, the following settings must be in place under *Experiment Setup*

.. image:: ADC.png
  :width: 150pt
