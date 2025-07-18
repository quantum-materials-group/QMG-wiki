import numpy as np
import matplotlib.pyplot as plt
from phd_fns import load_files, Read_PHU, xy_subset, double_sided_exp
from scipy.optimize import curve_fit

#%%

files_path = load_files()

#%%

data = Read_PHU(files_path[0])
dx = 103 # ns                            <--- this number depends on your setup
x = data[0,:]*1e9 - dx
y = data[1,:]

pulse_rate = 40 # MHz                    <--- this number depends on your setup
pulse_spacing = 1/pulse_rate * 1e3 # ns

# Select a range from the raw data:
pulse_left = -3
pulse_right = 50
xs, ys = xy_subset(x, y, (pulse_left-0.5)*pulse_spacing, (pulse_right+0.5)*pulse_spacing)

plt.figure(figsize=(2*3.5,1*2.675), dpi=600)
plt.rcParams['font.size'] = '10'

plt.subplot(121)
plt.plot(x, y, label='Raw data')
plt.plot(xs, ys, label='Selected data')
plt.xlim([-100, 100])
plt.xlabel(r'Time $\tau$ (ns)')
plt.ylabel(r'$g^{(2)}(\tau)$ (arb. units)')
plt.legend(fontsize=8)

plt.subplot(122)
plt.plot(x/1000, y, label='Raw data')
plt.plot(xs/1000, ys, label='Selected data')
plt.xlabel(r'Time $\tau$ ($\mu$s)')
plt.ylabel(r'$g^{(2)}(\tau)$ (arb. units)')
plt.legend(fontsize=8)

plt.tight_layout()



#%% PLOT as PEAK FITS

plt.figure(figsize=(1*3.5,1*2.675), dpi=600)
plt.rcParams['font.size'] = '10'

maxes = np.zeros(pulse_right-pulse_left+1)
T1s = np.zeros(len(maxes))
bases = np.zeros(len(maxes))
xfit = np.array([])
yfit = np.array([])
for j in range(len(maxes)):
    xj, yj = xy_subset(xs, ys, (pulse_left-0.5+j)*pulse_spacing, (pulse_left-0.5+j+1)*pulse_spacing)
    
    popt, pcov = curve_fit(double_sided_exp, xj, yj, p0=[max(yj), xj[np.argmax(yj)], 2, min(yj)])
    xfit = np.append(xfit, xj)
    yfit_j = double_sided_exp(xj, *popt)
    yfit = np.append(yfit, yfit_j)
    
    maxes[j] = max(yfit_j)
    T1s[j] = popt[2]
    bases[j] = popt[-1]

# "Background correction"
base = np.mean(bases)
maxes -= base
ys -= base
yfit -= base

# Normalisation
norm = np.mean(maxes[-pulse_right+1:])
ys /= norm
yfit /= norm
maxes /= norm

plt.plot(xs, ys, '.', ms=2, c='C0', alpha=0.3, label='Data')
plt.plot(xfit, yfit, c='C1', label='Fit')
plt.plot([min(xs), max(xs)], [1, 1], 'k--', alpha=0.3)
plt.plot([min(xs), max(xs)], [0.5, 0.5], 'k--', alpha=0.3)
plt.xlabel(r'Time $\tau$ (ns)')
plt.ylabel(r'$g^{(2)}(\tau)$ (arb. units)')
plt.title(r'$g^{(2)}(0)$ = %.2f, $T_1$ = %.2f ns' % (maxes[-pulse_left], np.mean(T1s)))
plt.xlim([-100, 200])
plt.legend(fontsize=8)

plt.tight_layout()


#%% PLOT as BARS

plt.figure(figsize=(1*3.5,1*2.675), dpi=600)
plt.rcParams['font.size'] = '10'

sums = np.zeros(pulse_right-pulse_left+1)
T1s = np.zeros(len(sums))
bases = np.zeros(len(sums))
for j in range(len(sums)):
    xj, yj = xy_subset(xs, ys, (pulse_left-0.5+j)*pulse_spacing, (pulse_left-0.5+j+1)*pulse_spacing)
    
    popt, pcov = curve_fit(double_sided_exp, xj, yj, p0=[max(yj), xj[np.argmax(yj)], 2, min(yj)])
    yfit = double_sided_exp(xj, *popt)
    
    sums[j] = np.sum(yfit)
    T1s[j] = popt[2]
    bases[j] = popt[-1]

# "Background correction"
base = np.mean(bases)
sums -= base

# Normalisation
norm = np.mean(sums[-pulse_right+1:])
sums /= norm

peak_centres = np.linspace(pulse_left*pulse_spacing, pulse_right*pulse_spacing, len(sums))
plt.bar(peak_centres, sums, width=pulse_spacing*0.8)
plt.plot([min(xs), max(xs)], [1, 1], 'k--', alpha=0.3)
plt.plot([min(xs), max(xs)], [0.5, 0.5], 'k--', alpha=0.3)
plt.xlabel(r'Time $\tau$ (ns)')
plt.ylabel(r'$g^{(2)}(\tau)$ (arb. units)')
plt.title(r'$g^{(2)}(0)$ = %.2f, $T_1$ = %.2f ns' % (sums[-pulse_left], np.mean(T1s)))
plt.ylim([0, 1.2])

plt.tight_layout()
