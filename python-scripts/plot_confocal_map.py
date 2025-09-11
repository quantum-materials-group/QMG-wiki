# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from phd_fns import load_files, save_figure

#%%

files_path = load_files()

#%%

spanX = 100    # horizontal span (micron)
spanY = 100    # vertical span (micron)

plt.figure(figsize=(1*3.5,1*2.675), dpi=600)
plt.rcParams['font.size'] = '10'

cf_map = np.genfromtxt(files_path[0])
cf_map = np.rot90(cf_map)
cf_map /= np.max(cf_map)    # normalisation

plt.imshow(cf_map, extent=(-spanX/2,spanX/2, -spanY/2, spanY/2))
plt.xlabel(r'x ($\mu$m)')
plt.ylabel(r'y ($\mu$m)')
plt.colorbar(label='Intensity (arb. units)')

plt.tight_layout()

save_figure(files_path[0], 'cf-map')
