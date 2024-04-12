import numpy as np
import matplotlib.pyplot as plt
from phd_fns import load_files, singleSpectrum, save_figure, save_figure_here

#%%

files_path = load_files()

#%% This script is used when plotting files obtained from the NEW SPECTROMETER SOFTWARE
#   For files obtained from OLD SPECTROMETER SOFTWARE, use the SpeFile as in plot_PL_single.py

wav_i, data_i = singleSpectrum(files_path[0])

plt.figure(dpi=200)
plt.plot(wav_i, data_i)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity (arb. units)')
plt.tight_layout()

# This function makes a PNG of the figure and names it the same as the data file
save_figure_here(files_path[0])

# This function makes a PNG of the figure and names it PL-figure.png
save_figure(files_path[0], 'PL-figure')
