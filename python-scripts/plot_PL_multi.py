import numpy as np
import matplotlib.pyplot as plt
from phd_fns import load_files, SpeFile, save_figure_here

#%%

files_path = load_files()

#%%

for i in range(len(files_path)):
  wav_i = SpeFile(files_path[i]).xaxis
  data_i = np.reshape(SpeFile(files_path[i]).data[0,:],-1)

  plt.figure(dpi=200)
  plt.plot(wav_i, data_i)
  plt.xlabel('Wavelength (nm)')
  plt.ylabel('Intensity (arb. units)')
  plt.tight_layout()

  # This function makes a PNG of the figure and names it the same as the data file
  save_figure_here(files_path[i])
