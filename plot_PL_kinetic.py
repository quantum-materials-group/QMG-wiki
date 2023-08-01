import numpy as np
import matplotlib.pyplot as plt
from phd_fns import load_files, SpeFile, save_figure_here

#%%

files_path = load_files()

#%%

wav = SpeFile(files_path[0]).xaxis
data = SpeFile(files_path[0]).data[:,:,0]

# Input the integration time (in seconds) of each spectrum
int_time = 1
t_end = data.shape[0] * int_time

plt.imshow(data, extent=[min(wav),max(wav),0,t_end], aspect=0.1)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Time (s)')
plt.colorbar(fraction=0.015, pad=0.02)
plt.tight_layout()

save_figure_here(files_path[0])
