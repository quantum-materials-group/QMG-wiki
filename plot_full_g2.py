# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from phd_fns import load_files, save_figure

#%%

import os
file_dir = os.path.realpath(__file__)
file_dir = '\\'.join(file_dir.split('\\')[:-1])

ptu_path = file_dir + '\\readPTU-master\\readPTU'

import sys
if sys.path[0] != ptu_path:
    sys.path.insert(0, ptu_path)

from readPTU import PTUfile, PTUmeasurement

#%% Select .PTU file from popup window

files_path = load_files()

#%% Extract measurement parameters

ptu_file = PTUfile(files_path[0])
number_of_records = ptu_file.num_records
acquisition_seconds = ptu_file.acq_time / 1e12
acquisition_hours = acquisition_seconds / 3600
horizontal_offset = (ptu_file.tags['HWSync_Offset'])['value'] / 1e3 # (ns)

print('Number of records: \t %d' % (number_of_records))
print('Acquisition time: \t %d s' % (acquisition_seconds))
print('                  \t %d hr' % (acquisition_hours))
print('Horizontal offset: \t %d ns' % (horizontal_offset))

ptu_meas = PTUmeasurement(ptu_file)

#%% Plot APD count rates throughout measurement (takes a few minutes for large files)

resolution_timetrace = 10    # timetrace discretisation, in seconds
timetrace_x_0, timetrace_y_0, timetrace_recnum_0 = ptu_meas.timetrace(resolution=resolution_timetrace, channel=0)
count_rate_0 = np.mean(timetrace_y_0)

timetrace_x_1, timetrace_y_1, timetrace_recnum_1 = ptu_meas.timetrace(resolution=resolution_timetrace, channel=1)
count_rate_1 = np.mean(timetrace_y_1)

x_scale = 1/3600
y_scale = 1/resolution_timetrace/1000

plt.figure(figsize=(1*3.5, 1*2.675), dpi=600)
plt.rcParams['font.size'] = '10'

plt.plot(timetrace_x_0[:-1]*x_scale, timetrace_y_0[:-1]*y_scale, label='CH0')
plt.plot(timetrace_x_1[:-1]*x_scale, timetrace_y_1[:-1]*y_scale, label='CH1')
plt.ylim([0, max(max(timetrace_y_0[:-1]*y_scale), max(timetrace_y_1[:-1]*y_scale))*1.1])
plt.xlabel('Time (hrs)')
plt.ylabel('APD intensity (kcps)')
plt.legend()
plt.tight_layout()

save_figure(files_path[0], 'APD-count-rate')

#%% Compute full autocorrelation (takes a few minutes for large files)

resolution_g2 = 128e-12 # histogram discretisation, in seconds
histo_x, histo_y = ptu_meas.calculate_g2(correlation_window=1e-6,  # max time in histogram, in seconds
                                         resolution=resolution_g2, 
                                         n_threads=4, 
                                         mode='ring')
histo_x *= 1e9 # convert to nanoseconds
histo_x += horizontal_offset

#--- Histogram Normalisation ---#
# "Fake" normalisation
# histo_y /= np.mean(histo_y[-100:])

# "Real" normalisation
histo_y /= (count_rate_0 / resolution_timetrace) * (count_rate_1 / resolution_timetrace) * resolution_g2 * acquisition_seconds
#---                         ---#


plt.figure(figsize=(2*3.5, 1*2.675), dpi=600)
plt.rcParams['font.size'] = '10'

plt.subplot(121)
plt.plot(histo_x, histo_y, lw=1)
plt.xlim([-20, 20])
plt.ylim([0, 2])
plt.xlabel(r'Time $\tau$ (ns)')
plt.ylabel(r'$g^{(2)}(\tau)$')

plt.subplot(122)
plt.semilogx(histo_x, histo_y, lw=1)
plt.ylim([0, 2])
plt.xlabel(r'Time $\tau$ (ns)')
plt.ylabel(r'$g^{(2)}(\tau)$')

plt.tight_layout()

save_figure(files_path[0], 'full-g2')
