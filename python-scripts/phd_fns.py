"""
A collection of python functions all your data processing and analysis needs.
Currently in no particular order.
"""

__version__ = "9"

import numpy as np
import matplotlib.pyplot as plt

def load_files():
    """
    About: Creates popup window for user to select datasets.

    Returns
    -------
    files_path : List
        A list of the file paths to each dataset selected. 
        If only one file is selected, then the list has only one element.
    """
    
    import os
    file_dir = os.path.realpath(__file__)
    file_dir = '\\'.join(file_dir.split('\\')[:-2])
    
    from tkinter import filedialog, Tk
    root = Tk()
    root.withdraw()
    files_path = filedialog.askopenfilenames(initialdir = file_dir, title = "Select files", filetypes = (("all files","*.*"), ("text files","*.txt")))
    root.attributes('-topmost', True)
    return files_path

def save_figure(file_path, img_name):
    """
    About: saves a PNG figure into a specified folder.
    
    Parameters
    ----------
    file_path : string
        System path to the folder where the image will be saved.
    img_name : string
        Name of image (without image type suffix).

    Returns
    -------
    empty
    """
    folder_path = "/".join(file_path.split('/')[:-1])
    plt.savefig(folder_path + '/' + img_name + '.png')
    
def save_figure_here(file_path):
    """
    About: saves a PNG figure into the same folder as the data file.
    
    Parameters
    ----------
    file_path : string
        System path to the folder where the image will be saved.
        Usually "save_figure_here(files_path[0])" is sufficient.
    Returns
    -------
    empty
    """
    folder_path = "/".join(file_path.split('/')[:-1])
    img_name = file_path.split('/')[-1][:-4]
    plt.savefig(folder_path + '/' + img_name + '.png')

def Lorentzian_FWHM(x, *p0):
    """
    About: Defines a Lorentzian curve parameterised by FWHM.
    
    Parameters
    ----------
    x : 1D array
        Energy values
    *p0 : List
        [amplitude, horizontal offset, FWHM, vertical offset]

    Returns
    -------
    1D array
        Intensity of spectrum
    """
    a = p0[0]
    x0 = p0[1]
    FWHM = p0[2]
    c = p0[3]
    return a/(1 + 4 * (x-x0)**2 / FWHM**2) + c

def Lorentzian_FWHM_multi(x, *p0):
    """
    About: Defines a function consisting of the sum of arbitrarily many
           Lorentzian curves, each parameterised by FWHM.
           
    Note: Convert PL spectrum data from units of wavelength to units of energy
          before performing Lorentzian fit --> E = hc/lambda
           
    Parameters
    ----------
    x : 1D array
        Energy values
    *p0 : List
        [N * [amplitude, horizontal offset, FWHM], vertical offset]

    Returns
    -------
    1D array
        Intensity of spectrum
    """
    y = np.zeros_like(x)
    for i in range(0, len(p0)-1, 3):
        a = p0[i]
        x0 = p0[i+1]
        FWHM = p0[i+2]
        y += a / (1 + 4 * (x-x0)**2 / FWHM**2)
    return y + p0[-1]

def Gaussian_FWHM(x, *p0):
    """
    About: Defines a Gaussian curve parameterised by FWHM.
    
    Parameters
    ----------
    x : 1D array
        Energy values
    *p0 : List
        [amplitude, horizontal offset, FWHM, vertical offset]

    Returns
    -------
    1D array
        Intensity of spectrum
    """
    a = p0[0]
    x0 = p0[1]
    FWHM = p0[2]
    c = p0[3]
    return a * np.exp(- 4 * np.log(2) * (x-x0)**2 / FWHM**2) + c

def Gaussian_FWHM_multi(x, *p0):
    """
    About: Defines a function consisting of the sum of arbitrarily many
           Gaussian curves, each parameterised by FWHM.
           
    Note: Convert PL spectrum data from units of wavelength to units of energy
          before performing Gaussian fit --> E = hc/lambda
           
    Parameters
    ----------
    x : 1D array
        Energy values
    *p0 : List
        [N * [amplitude, horizontal offset, FWHM], vertical offset]

    Returns
    -------
    1D array
        Intensity of spectrum
    """
    y = np.zeros_like(x)
    for i in range(0, len(p0)-1, 3):
        a = p0[i]
        x0 = p0[i+1]
        FWHM = p0[i+2]
        y += a * np.exp(- 4 * np.log(2) * (x-x0)**2 / FWHM**2)
    return y + p0[-1]

def Voigt_FWHM(x, *p0):
    """
    About: Defines a Voigt curve parameterised by FWHMs of Gaussian and 
           Lorentzian constituents.
           
    Parameters
    ----------
    x : 1D array
        Energy values
    *p0 : List
        [amplitude, Gaussian FWHM, Lorentzian FWHM, vertical offset]

    Returns
    -------
    1D array
        Intensity of spectrum
    """
    from scipy.special import wofz
    
    a = p0[0]
    
    G_FWHM = p0[1]
    sigma = G_FWHM / np.sqrt(8 * np.log(2))
    
    L_FWHM = p0[2]
    gamma = L_FWHM / 2
    
    c = p0[3]
    
    z = (x + 1j*gamma) / (sigma * np.sqrt(2))
    
    return a * np.real(wofz(z)) / (sigma * np.sqrt(2 * np.pi)) + c

def Voigt_linewidth(G_FWHM, L_FWHM):
    """
    About: Computes FWHM of Voigt function, given constituent widths.
           
    Parameters
    ----------
    G_FWHM : float
        FWHM of Gaussian component
    L_FWHM : float
        FWHM of Lorentzian component

    Returns
    -------
    float
        FWHM of Voigt function
    """
    return 0.5346 * L_FWHM + np.sqrt(0.2166 * L_FWHM**2 + G_FWHM**2)

def power_saturation(x, *p0):
    """
    About: A hyperbolic function modeling the saturation of SPE emission under
           increasing excitation laser power. The function has the form
           I(P) = I_inf * P / (P + P_sat)
           where I_inf is the asymptotic emission intensity, and
                 P_sat is the power at which I(P) = 0.5*I_inf.

    Parameters
    ----------
    x : 1D array
        Power values
    *p0 : list
        [I_inf, P_sat]

    Returns
    -------
    1D array
        Intensity values

    """
    return p0[0]*x / (x + p0[1])

def power_saturation_bgc(x, *p0):
    """
    About: Power saturation in the presence of non-negligible background
           scattering/fluorescence. The function has the form
           I(P) = I_inf * P / (P + P_sat) + k * P
           where the background is assumed to be linearly proportional to
           excitation power with constant k.

    Parameters
    ----------
    x : 1D array
        Power values
    *p0 : list
        [I_inf, P_sat, k]

    Returns
    -------
    1D array
        Intensity values

    """
    return p0[0]*x / (x + p0[1]) + p0[2]*x

def xy_bin(xs, ys, binNum):
    """
    About: Reduces density of data via averaging. Helpful for reducing figure clutter.
    
    Note: Best to fit functions to raw data, not this binned data.
    
    Parameters
    ----------
    xs : 1D array
        x-axis data
    ys : 1D array
        y-axis data
    binNum : int
        Desired length of new arrays

    Returns
    -------
    xbin : 1D array
        x array with length binNum
    ybin : 1D array
        y array with length binNum
    """
    xbin = np.linspace(min(xs), max(xs), binNum+1)
    ybin = np.zeros(binNum)
    for j in range(binNum):
        ys2 = ys[np.where((xs>xbin[j])&(xs<xbin[j+1]))]
        if ys2.size>0:
            ybin[j] = np.mean(ys[np.where((xs>xbin[j])&(xs<xbin[j+1]))])
        else:
            ybin[j] = np.nan
    xbin = xbin[:-1] + 0.5*(xbin[1] - xbin[0])
    return xbin, ybin

def xy_bin_err(xs, ys, binNum):
    """
    About: also returns standard deviation per bin
    
    Parameters
    ----------
    xs : 1D array
        x-axis data
    ys : 1D array
        y-axis data
    binNum : int
        Desired length of new arrays

    Returns
    -------
    xbin : 1D array
        x array with length binNum
    ybin : 1D array
        y array with length binNum
    yerr : 1D array
        error array with length binNum
    """
    xbin = np.linspace(min(xs), max(xs), binNum+1)
    ybin = np.zeros(binNum)
    yerr = np.zeros(binNum)
    for j in range(binNum):
        ys2 = ys[np.where((xs>xbin[j])&(xs<xbin[j+1]))]
        if ys2.size>0:
            ybin[j] = np.mean(ys[np.where((xs>xbin[j])&(xs<xbin[j+1]))])
            yerr[j] = np.std(ys[np.where((xs>xbin[j])&(xs<xbin[j+1]))])
        else:
            ybin[j] = np.nan
    xbin = xbin[:-1] + 0.5*(xbin[1] - xbin[0])
    return xbin, ybin, yerr

def xy_bin_log(xs, ys, binNum):
    """
    About: Same as xy_bin() but returns logarithmic x-axis.
    
    Note: Best to fit functions to raw data, not this binned data.
    
    Parameters
    ----------
    xs : 1D array
        x-axis data
    ys : 1D array
        y-axis data
    binNum : int
        Desired length of new arrays

    Returns
    -------
    xbin : 1D array
        x array with length binNum
    ybin : 1D array
        y array with length binNum
    """
    xbin = np.logspace(np.log(min(xs[xs>0])), np.log(max(xs)), binNum+1)
    ybin = np.zeros(binNum)
    for j in range(binNum):
        ys2 = ys[np.where((xs>xbin[j])&(xs<xbin[j+1]))]
        if ys2.size>0:
            ybin[j] = np.mean(ys[np.where((xs>xbin[j])&(xs<xbin[j+1]))])
        else:
            ybin[j] = np.nan
    xbin = xbin[:-1] + 0.5*(xbin[1] - xbin[0])
    return xbin, ybin

def xy_bin_log_err(xs, ys, binNum):
    """
    About: also returns standard deviation per bin
    
    Note: Best to fit functions to raw data, not this binned data.
    
    Parameters
    ----------
    xs : 1D array
        x-axis data
    ys : 1D array
        y-axis data
    binNum : int
        Desired length of new arrays

    Returns
    -------
    xbin : 1D array
        x array with length binNum
    ybin : 1D array
        y array with length binNum
    """
    xbin = np.logspace(np.log(min(xs[xs>0])), np.log(max(xs)), binNum+1)
    ybin = np.zeros(binNum)
    yerr = np.zeros(binNum)
    for j in range(binNum):
        ys2 = ys[np.where((xs>xbin[j])&(xs<xbin[j+1]))]
        if ys2.size>0:
            ybin[j] = np.mean(ys[np.where((xs>xbin[j])&(xs<xbin[j+1]))])
            yerr[j] = np.std(ys[np.where((xs>xbin[j])&(xs<xbin[j+1]))])
        else:
            ybin[j] = np.nan
    xbin = xbin[:-1] + 0.5*(xbin[1] - xbin[0])
    return xbin, ybin, yerr
    
def xy_subset(x, y, xL, xR):
    """
    About: gives a subset of x-y data based on x-range
    
    Parameters
    ----------
    xs : 1D array
        x-axis data
    ys : 1D array
        y-axis data
    xL : float
        Minimum value of x-axis data
    xR : float
        Maximum value of x-axis data

    Returns
    -------
    xs : 1D array
        x array with length binNum
    ys : 1D array
        y array with length binNum
    """
    xs = x[np.where((x>xL) & (x<xR))]
    ys = y[np.where((x>xL) & (x<xR))]
    return xs, ys

def xy_remove(x, y, xL, xR):
    """
    About: removes a subset of x-y data based on x-range. Useful for rejecting
    crosstalk from a g2 fit.
    
    Parameters
    ----------
    xs : 1D array
        x-axis data
    ys : 1D array
        y-axis data
    xL : float
        Minimum value of x-axis data
    xR : float
        Maximum value of x-axis data

    Returns
    -------
    xs : 1D array
        x array with length binNum
    ys : 1D array
        y array with length binNum
    """
    xs = x[np.where((x<xL) | (x>xR))]
    ys = y[np.where((x<xL) | (x>xR))]
    return xs, ys

def moving_average(data, window_size):
    """
    About: transforms a dataset by replacing each datum with the average within
           a neighbouring window. Good for reducing high frequency noise,
           an alternative to xy_bin.
           
    Parameters
    ----------
    data : 1D array
        Raw input data
    window_size : int
        Size of data subset over which averaging is performed for each datum

    Returns
    -------
    1D array
        Averaged data set
    """
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(data, window, 'same')

def nm2meV(x):
    """
    About: Convert an array from units of wavelength to units of energy. Useful for
           PL spectrum plots that need wavelength as well as energy.

    Parameters
    ----------
    x : 1D array
        Absolute wavelength values in nanometres

    Returns
    -------
    1D array
        Absolute energy values in millielectron volts
    """
    h = 6.626e-34       # m^2 kg / s
    c = 299792458       # m / s
    k = 6.242e21        # converts Newton-metres to millielectron-volts
    return h * c * k * 1e9 / x
    
def nm2meV_relative(x, lambda0):
    """
    About: Convert an array from units of wavelength to units of energy, where
           the energy is relative to the given wavelength lambda0. Useful for
           PL spectrum plots that need absolute wavelength as well as energy
           relative to the ZPL.

    Parameters
    ----------
    x : 1D array
        Absolute wavelength values in nanometres
    lambda0 : float
        The wavelength in nanometres that sets the zero-point for relative 
        energy, e.g. the ZPL

    Returns
    -------
    1D array
        Relative energy values in millielectron volts
    """
    h = 6.626e-34       # m^2 kg / s
    c = 299792458       # m / s
    k = 6.242e21        # converts Newton-metres to millielectron-volts
    return h * c * k * 1e9 * ( 1 / x - 1 / lambda0 )

def meV2nm(x):
    """
    About: Convert an array from units of energy to units of wavelength. Useful for
           PL spectrum plots that need absolute wavelength as well as energy.
           {Functionally equivalent to nm2meV()}
           
    Parameters
    ----------
    x : 1D array
        Absolute energy values in millielectron volts

    Returns
    -------
    1D array
        Absolute wavelength values in nanometres
    """
    h = 6.626e-34       # m^2 kg / s
    c = 299792458       # m / s
    k = 6.242e21        # converts Newton-metres to millielectron-volts
    return h * c * k * 1e9 / x
    
def meV2nm_relative(x, lambda0):
    """
    About: Convert an array from units of energy to units of wavelength, where
           the energy is relative to the given wavelength lambda0. Useful for
           PL spectrum plots that need absolute wavelength as well as energy
           relative to the ZPL.

    Parameters
    ----------
    x : 1D array
        Relative energy values in millielectron volts
    lambda0 : float
        The wavelength in nanometres that sets the zero-point for relative 
        energy, e.g. the ZPL

    Returns
    -------
    1D array
        Absolute wavelength values in nanometres
    """
    h = 6.626e-34       # m^2 kg / s
    c = 299792458       # m / s
    k = 6.242e21        # converts Newton-metres to millielectron-volts
    return h * c * k * 1e9 * lambda0 / (x * lambda0 + h * c * k * 1e9)

def ASD(data, freq):
    '''
    About: Transforms a signal from the time domain to the frequency domain
           via fast Fourier Transform (FFT). The units of the output are the
           amplitudes of constituent sinusoids of varying frequency.
    Parameters
    ----------
    data : 1D array
        Time series of signal in time domain [s].
    freq : float
        Sample rate of time series [Hz].

    Returns
    -------
    1D array
        Frequencies [Hz]
    1D array
        Amplitude of each frequency [V]

    '''
    L = len(data)
    freqs = freq * np.fft.fftfreq(L)
    mask = freqs>0
    asd = 2*np.abs(np.fft.fft(data)/L)
    return freqs[mask], asd[mask]

def g2_2LS(x, *p0):
    """
    About: The second order correlation function for a two level system, 
           accounting for horizontal offset and vertical scaling. This is
           sufficient for any 'short' g2, but note that values of g2 greater
           than 1.0 around the shoulder of the central dip may indicate
           some other phenomenon such as bunching due to a third system level.

    Parameters
    ----------
    x : 1D array
        Delay time between photon detection events across APDs.
    *p0 : List
        [amplitude, purity, horizontal offset, lifetime]

    Returns
    -------
    1D array
        Second order correlation.
    """
    amp = p0[0]
    purity = p0[1]
    x0 = p0[2]
    tau1 = p0[3]
    return amp * (1 - purity * np.exp( - np.abs(x - x0) / tau1))

def g2_3LS(x, *p0):
    """
    About: The second order correlation function for a three level system, 
           accounting for horizontal offset and vertical scaling. Relevant when
           values of g2 around the shoulder of the dip are greater than 1.0.
           See Sontheimer 2017 10.1103/PhysRevB.96.121202 but note that our
           function utilises a purity parameter (with range 0 to 1) where
           Sontheimer uses unity, meaning our function accounts for experimental
           values of g2(0) greater than 0.

    Parameters
    ----------
    x : 1D array
        Delay time between photon detection events across APDs.
    *p0 : List
        [amplitude, purity, horizontal offset, lifetime, 
         bunching amplitude, bunching lifetime]

    Returns
    -------
    1D array
        Second order correlation.
    """
    amp = p0[0]
    purity = p0[1]
    x0 = p0[2]
    tau1 = p0[3]
    bunching = p0[4]
    tau2 = p0[5]
    return amp * (1 - (purity + bunching) * np.exp( - np.abs(x - x0) / tau1) + bunching * np.exp( - np.abs(x - x0) / tau2))

def g2_rabi(x, *p0):
    """
    About: Alex Clark's ~most correct~ Rabi g2 function.
           See 10.1103/PhysRevA.94.063839

    Parameters
    ----------
    x : 1D array
        Delay time between photon detection events across APDs.
    *p0 : List
        [amplitude, purity, horizontal offset, lifetime, 
         pure dephasing time, Rabi frequency]

    Returns
    -------
    1D array
        Second order correlation.
    """
    amp = p0[0]
    purity = p0[1]
    x0 = p0[2]
    t1 = p0[3]
    t2star = p0[4]
    Omega = p0[5]
    Gamma1 = 1/t1
    Gamma2 = 1/(2*t1) + 1/t2star
    p = Gamma1 + Gamma2
    q = complex(0) + np.emath.sqrt((Gamma1 - Gamma2)**2 - 4*Omega**2)
    return np.real(amp * (1 - purity*(p+q)*np.exp(-0.5*(p-q)*np.abs(x-x0))/(2*q) + purity*(p-q)*np.exp(-0.5*(p+q)*np.abs(x-x0))/(2*q)))

def double_sided_exp(x, *p0):
    """
    About: For use in pulsed g2 fits.

    Parameters
    ----------
    x : 1D array
        Delay time between photon detection events across APDs.
    *p0 : List
        [amplitude, horizontal offset, lifetime, 
         vertical offset]

    Returns
    -------
    1D array
        Second order correlation.
    """
    A = p0[0]
    x0 = p0[1]
    T1 = p0[2]
    c = p0[3]
    return A * np.exp(-np.abs(x - x0)/T1) + c

def sort_by_x(x, y):
    """
    About: To sort two arrays relative to the first array.
    
    Parameters
    ----------
    x : arbitrary 1D array
    y : arbitrary 1D array

    Returns
    -------
    2x1D array, where elements in both arrays are sorted according to x
    """
    a = np.vstack((x, y)).T
    a = a[a[:, 0].argsort()]
    x = a[:,0]
    y = a[:,1]
    return x, y






def Read_PHU(fname):
    import struct
    import time
    # Tag Types
    tyEmpty8      = struct.unpack(">i", bytes.fromhex("FFFF0008"))[0]
    tyBool8       = struct.unpack(">i", bytes.fromhex("00000008"))[0]
    tyInt8        = struct.unpack(">i", bytes.fromhex("10000008"))[0]
    tyBitSet64    = struct.unpack(">i", bytes.fromhex("11000008"))[0]
    tyColor8      = struct.unpack(">i", bytes.fromhex("12000008"))[0]
    tyFloat8      = struct.unpack(">i", bytes.fromhex("20000008"))[0]
    tyTDateTime   = struct.unpack(">i", bytes.fromhex("21000008"))[0]
    tyFloat8Array = struct.unpack(">i", bytes.fromhex("2001FFFF"))[0]
    tyAnsiString  = struct.unpack(">i", bytes.fromhex("4001FFFF"))[0]
    tyWideString  = struct.unpack(">i", bytes.fromhex("4002FFFF"))[0]
    tyBinaryBlob  = struct.unpack(">i", bytes.fromhex("FFFFFFFF"))[0]    
    
    inputfile = open(fname, "rb")
    outputfile = open('temp.txt', "w+")
    
    # Check if inputfile is a valid PHU file
    # Python strings don't have terminating NULL characters, so they're stripped
    magic = inputfile.read(8).decode("ascii").strip('\0')
    if magic != "PQHISTO":
        print("ERROR: Magic invalid, this is not a PHU file.")
        exit(0)
    
    version = inputfile.read(8).decode("ascii").strip('\0')
    outputfile.write("Tag version: %s\n" % version)
    
    # Write the header data to outputfile and also save it in memory.
    # There's no do ... while in Python, so an if statement inside the while loop
    # breaks out of it
    tagDataList = []    # Contains tuples of (tagName, tagValue)
    while True:
        tagIdent = inputfile.read(32).decode("ascii").strip('\0')
        tagIdx = struct.unpack("<i", inputfile.read(4))[0]
        tagTyp = struct.unpack("<i", inputfile.read(4))[0]
        if tagIdx > -1:
            evalName = tagIdent + '(' + str(tagIdx) + ')'
        else:
            evalName = tagIdent
        outputfile.write("\n%-40s" % evalName)
        if tagTyp == tyEmpty8:
            inputfile.read(8)
            outputfile.write("<empty Tag>")
            tagDataList.append((evalName, "<empty Tag>"))
        elif tagTyp == tyBool8:
            tagInt = struct.unpack("<q", inputfile.read(8))[0]
            if tagInt == 0:
                outputfile.write("False")
                tagDataList.append((evalName, "False"))
            else:
                outputfile.write("True")
                tagDataList.append((evalName, "True"))
        elif tagTyp == tyInt8:
            tagInt = struct.unpack("<q", inputfile.read(8))[0]
            outputfile.write("%d" % tagInt)
            tagDataList.append((evalName, tagInt))
        elif tagTyp == tyBitSet64:
            tagInt = struct.unpack("<q", inputfile.read(8))[0]
            outputfile.write("{0:#0{1}x}".format(tagInt,18)) # hex with trailing 0s
            tagDataList.append((evalName, tagInt))
        elif tagTyp == tyColor8:
            tagInt = struct.unpack("<q", inputfile.read(8))[0]
            outputfile.write("{0:#0{1}x}".format(tagInt,18)) # hex with trailing 0s
            tagDataList.append((evalName, tagInt))
        elif tagTyp == tyFloat8:
            tagFloat = struct.unpack("<d", inputfile.read(8))[0]
            outputfile.write("%-3E" % tagFloat)
            tagDataList.append((evalName, tagFloat))
        elif tagTyp == tyFloat8Array:
            tagInt = struct.unpack("<q", inputfile.read(8))[0]
            outputfile.write("<Float array with %d entries>" % tagInt/8)
            tagDataList.append((evalName, tagInt))
        elif tagTyp == tyTDateTime:
            tagFloat = struct.unpack("<d", inputfile.read(8))[0]
            tagTime = int((tagFloat - 25569) * 86400)
            tagTime = time.gmtime(tagTime)
            outputfile.write(time.strftime("%a %b %d %H:%M:%S %Y", tagTime))
            tagDataList.append((evalName, tagTime))
        elif tagTyp == tyAnsiString:
            tagInt = struct.unpack("<q", inputfile.read(8))[0]
            tagString = inputfile.read(tagInt).decode("ascii").strip("\0")
            outputfile.write("%s" % tagString)
            tagDataList.append((evalName, tagString))
        elif tagTyp == tyWideString:
            tagInt = struct.unpack("<q", inputfile.read(8))[0]
            tagString = inputfile.read(tagInt).decode("ascii").strip("\0")
            outputfile.write("%s" % tagString)
            tagDataList.append((evalName, tagString))
        elif tagTyp == tyBinaryBlob:
            tagInt = struct.unpack("<q", inputfile.read(8))[0]
            outputfile.write("<Binary blob with %d bytes>" % tagInt)
            tagDataList.append((evalName, tagInt))
        else:
            print("ERROR: Unknown tag type")
            exit(0)
        if tagIdent == "Header_End":
            break
    
    # Reformat the saved data for easier access
    tagNames = [tagDataList[i][0] for i in range(0, len(tagDataList))]
    tagValues = [tagDataList[i][1] for i in range(0, len(tagDataList))]
    
    # Write histogram data to file
    curveIndices = [tagValues[i] for i in range(0, len(tagNames))\
                    if tagNames[i][0:-3] == "HistResDscr_CurveIndex"]
    for i in curveIndices:
        outputfile.write("\n-----------------------")
        histogramBins = tagValues[tagNames.index("HistResDscr_HistogramBins(%d)" % i)]
        resolution = tagValues[tagNames.index("HistResDscr_MDescResolution(%d)" % i)]
        outputfile.write("\nCurve#  %d" % i)
        outputfile.write("\nnBins:  %d" % histogramBins)
        outputfile.write("\nResol:  %3E" % resolution)
        outputfile.write("\nCounts:")
        for j in range(0, histogramBins):
            try:
                histogramData = struct.unpack("<i", inputfile.read(4))[0]
            except:
                print("The file ended earlier than expected, at bin %d/%d."\
                      % (j, histogramBins))
            outputfile.write("\n%d" % histogramData)
    
    inputfile.close()
    outputfile.close()
    
    x1 = np.linspace(0,histogramBins,histogramBins)*resolution
    y1 = np.loadtxt('temp.txt',skiprows=92)
    
    data = np.array((x1, y1))

    return data

  
  
  
  
  
  
  
  
  
  
  
  



''' winspec.py - read SPE files created by WinSpec with Princeton Instruments' cameras. '''

import ctypes, os
import struct
import logging

__all__ = ['SpeFile', 'print_offsets']

# __author__ = "Anton Loukianov"
# __email__ = "anton.loukianov@gmail.com"
# __license__ = "BSD"
# __version__ = "0.2.1"

log = logging.getLogger('winspec')

# Definitions of types
spe_byte = ctypes.c_ubyte
spe_word = ctypes.c_ushort
spe_dword = ctypes.c_uint

spe_char = ctypes.c_char # 1 byte
spe_short = ctypes.c_short # 2 bytes

# long is 4 bytes in the manual. It is 8 bytes on my machine
spe_long = ctypes.c_int # 4 bytes

spe_float = ctypes.c_float # 4 bytes
spe_double = ctypes.c_double # 8 bytes

class ROIinfo(ctypes.Structure):
    pass

class AxisCalibration(ctypes.Structure):
    pass

class Header(ctypes.Structure):
    pass

def print_offsets():
    ''' Print the attribute names, sizes and offsets in the C structure
    
    Assuming that the sizes are correct and add up to an offset of 4100 bytes, 
    everything should add up correctly. This information was taken from the 
    WinSpec 2.6 Spectroscopy Software User Manual version 2.6B, page 251.
    If this table doesn't add up, something changed in the definitions of the 
    datatype widths. Fix this in winspec.structs file and let me know!
    '''

    import inspect, re

    A = Header()

    for i in [Header, AxisCalibration, ROIinfo]:
        fields = []

        print('\n{:30s}[{:4s}]\tsize'.format(repr(i), 'offs'))
        
        for name,obj in inspect.getmembers(i):
            if inspect.isdatadescriptor(obj) and not inspect.ismemberdescriptor(obj) \
                and not inspect.isgetsetdescriptor(obj):
                
                fields.append((name, obj))

        fields = sorted(fields, key=lambda x: x[1].offset)

        for name, obj in fields:
            print('{:30s}[{:4d}]\t{:4d}'.format(name, obj.size, obj.offset))


class SpeFile(object):
    ''' A file that represents the SPE file.
    All details written in the file are contained in the `header` structure. Data is 
    accessed by using the `data` property.
    Once the object is created and data accessed, the file is NOT read again. Create
    a new object if you want to reread the file.
    '''

    # Map between header datatype field and numpy datatype 
    _datatype_map = {0 : np.float32, 1 : np.int32, 2 : np.int16, 3 : np.uint16}

    def __init__(self, name):
        ''' Open file `name` to read the header.'''

        with open(name, mode='rb') as f:
            self.header = Header()
            self.path = os.path.realpath(name) 
            self._data = None
            self._xaxis = None
            self._yaxis = None

            # Deprecated method, but FileIO apparently can't be used with numpy
            f.readinto(self.header)

        # set some useful properties
        self.reversed = True if self.header.geometric == 2 else False
        self.gain = self.header.gain

        if self.header.ADCtype == 8:
            self.adc = 'Low Noise'
        elif self.header.ADCtype == 9:
            self.adc = 'High Capacity'
        else:
            self.adc = 'Unknown'

        if self.header.ADCrate == 12:
            self.adc_rate = '2 MHz'
        elif self.header.ADCrate == 6:
            self.adc_rate = '100 KHz'
        else:
            self.adc_rate = 'Unknown'

        self.readout_time = self.header.ReadoutTime

    def _read(self):
        ''' Read the data segment of the file and create an appropriately-shaped numpy array
        Based on the header, the right datatype is selected and returned as a numpy array.  I took 
        the convention that the frame index is the first, followed by the x,y coordinates.
        '''

        if self._data is not None:
            log.debug('using cached data')
            return self._data

        # In python 2.7, apparently file and FileIO cannot be used interchangably
        with open(self.path, mode='rb') as f:
            f.seek(4100) # Skip header (4100 bytes)

            _count = self.header.xdim * self.header.ydim * self.header.NumFrames
            
            self._data = np.fromfile(f, dtype=SpeFile._datatype_map[self.header.datatype], count=_count)

            # Also, apparently the ordering of the data corresponds to how it is stored by the shift register
            # Thus, it appears a little backwards...
            self._data = self._data.reshape((self.header.NumFrames, self.header.ydim, self.header.xdim))

            # Orient the structure so that it is indexed like [NumFrames][x, y]
            self._data = np.rollaxis(self._data, 2, 1)

            # flip data
            if all([self.reversed == True, self.adc == '100 KHz']):
                pass
            elif any([self.reversed == True, self.adc == '100 KHz']):
                self._data = self._data[:, ::-1, :]
                log.debug('flipped data because of nonstandard ADC setting ' +\
                        'or reversed setting')

            return self._data

    @property
    def xaxis(self):
        if self._xaxis is not None:
            log.debug('using cached xaxis')
            return self._xaxis

        px, py = self._make_axes()

        return px

    @property
    def yaxis(self):
        if self._yaxis is not None:
            log.debug('using cached yaxis')
            return self._yaxis

        px, py = self._make_axes()

        return py

    @property
    def xaxis_label(self):
        '''Read the x axis label
        '''
        return self.header.xcalibration.string.decode('ascii')

    @property
    def yaxis_label(self):
        '''Read the y axis label
        '''
        return self.header.ycalibration.string.decode('ascii')


    def _make_axes(self):
        '''Construct axes from calibration fields in header file
        '''
        xcalib = self.header.xcalibration
        ycalib = self.header.ycalibration

        xcalib_valid = struct.unpack('?', xcalib.calib_valid)

        if xcalib_valid:
            xcalib_order, = struct.unpack('>B', xcalib.polynom_order) # polynomial order
            px = xcalib.polynom_coeff[:xcalib_order+1]
            px = np.array(px[::-1]) # reverse coefficients to use numpy polyval
            pixels = np.arange(1, self.header.xdim + 1)
            px = np.polyval(px, pixels)
        else:
            px = np.arange(1, self.header.xdim + 1)

        ycalib_valid = struct.unpack('?', ycalib.calib_valid)

        if ycalib_valid:
            ycalib_order, = struct.unpack('>B', ycalib.polynom_order) # polynomial order
            py = ycalib.polynom_coeff[:ycalib_order+1]
            py = np.array(py[::-1]) # reverse coefficients to use numpy polyval
            pixels = np.arange(1, self.header.ydim + 1)
            py = np.polyval(py, pixels)
        else:
            py = np.arange(1, self.header.ydim + 1)

        self._xaxis = px
        self._yaxis = py

        return px, py


    ''' Data recorded in the file, returned as a numpy array. 
    
    The convention for indexes is that the first index is the frame index, followed by x,y region of 
    interest.
    '''
    data = property(fget=_read)

    def __str__(self):
        return 'SPE File \n\t{:d}x{:d} area, {:d} frames\n\tTaken on {:s}' \
                .format(self.header.xdim, self.header.ydim, 
                        self.header.NumFrames, self.header.date.decode())

    def __repr__(self):
        return str(self)


# Lengths of arrays used in header
HDRNAMEMAX = 120
USERINFOMAX = 1000
COMMENTMAX = 80
LABELMAX = 16
FILEVERMAX = 16
DATEMAX = 10
ROIMAX = 10
TIMEMAX = 7

# Definitions of WinSpec structures

# Region of interest defs
ROIinfo._pack_ = 1
ROIinfo._fields_ = [
    ('startx', spe_word), 
    ('endx', spe_word),
    ('groupx', spe_word),
    ('starty', spe_word),
    ('endy', spe_word),
    ('groupy', spe_word)]

# Calibration structure for X and Y axes
AxisCalibration._pack_ = 1
AxisCalibration._fields_ = [
    ('offset', spe_double), 
    ('factor', spe_double),
    ('current_unit', spe_char),
    ('reserved1', spe_char),
    ('string', spe_char * 40),
    ('reserved2', spe_char * 40), 
    ('calib_valid', spe_char),
    ('input_unit', spe_char),
    ('polynom_unit', spe_char),
    ('polynom_order', spe_char),
    ('calib_count', spe_char),
    ('pixel_position', spe_double * 10),
    ('calib_value', spe_double * 10), 
    ('polynom_coeff', spe_double * 6),
    ('laser_position', spe_double),
    ('reserved3', spe_char),
    ('new_calib_flag', spe_byte),
    ('calib_label', spe_char * 81),
    ('expansion', spe_char * 87)]

# Full header definition
Header._pack_ = 1
Header._fields_ = [
    ('ControllerVersion', spe_short),
    ('LogicOutput', spe_short),
    ('AmpHiCapLowNoise', spe_word),
    ('xDimDet', spe_word),
    ('mode', spe_short),
    ('exp_sec', spe_float),
    ('VChipXdim', spe_short),
    ('VChipYdim', spe_short),
    ('yDimDet', spe_word),
    ('date', spe_char * DATEMAX),
    ('VirtualChipFlag', spe_short),
    ('Spare_1', spe_char * 2), # Unused data
    ('noscan', spe_short),
    ('DetTemperature', spe_float),
    ('DetType', spe_short),
    ('xdim', spe_word),
    ('stdiode', spe_short),
    ('DelayTime', spe_float),
    ('ShutterControl', spe_word),
    ('AbsorbLive', spe_short),
    ('AbsorbMode', spe_word),
    ('CanDoVirtualChipFlag', spe_short),
    ('ThresholdMinLive', spe_short),
    ('ThresholdMinVal', spe_float), 
    ('ThresholdMaxLive', spe_short), 
    ('ThresholdMaxVal', spe_float),
    ('SpecAutoSpectroMode', spe_short),
    ('SpecCenterWlNm', spe_float),
    ('SpecGlueFlag', spe_short),
    ('SpecGlueStartWlNm', spe_float),
    ('SpecGlueEndWlNm', spe_float),
    ('SpecGlueMinOvrlpNm', spe_float),
    ('SpecGlueFinalResNm', spe_float),
    ('PulserType', spe_short),
    ('CustomChipFlag', spe_short),
    ('XPrePixels', spe_short),
    ('XPostPixels', spe_short),
    ('YPrePixels', spe_short),
    ('YPostPixels', spe_short),
    ('asynen', spe_short),
    ('datatype', spe_short), # 0 - float, 1 - long, 2 - short, 3 - ushort
    ('PulserMode', spe_short),
    ('PulserOnChipAccums', spe_word),
    ('PulserRepeatExp', spe_dword),
    ('PulseRepWidth', spe_float),
    ('PulseRepDelay', spe_float),
    ('PulseSeqStartWidth', spe_float),
    ('PulseSeqEndWidth', spe_float),
    ('PulseSeqStartDelay', spe_float),
    ('PulseSeqEndDelay', spe_float),
    ('PulseSeqIncMode', spe_short),
    ('PImaxUsed', spe_short),
    ('PImaxMode', spe_short),
    ('PImaxGain', spe_short),
    ('BackGrndApplied', spe_short),
    ('PImax2nsBrdUsed', spe_short),
    ('minblk', spe_word),
    ('numminblk', spe_word),
    ('SpecMirrorLocation', spe_short * 2),
    ('SpecSlitLocation', spe_short * 4),
    ('CustomTimingFlag', spe_short),
    ('ExperimentTimeLocal', spe_char * TIMEMAX),
    ('ExperimentTimeUTC', spe_char * TIMEMAX),
    ('ExposUnits', spe_short),
    ('ADCoffset', spe_word),
    ('ADCrate', spe_word),
    ('ADCtype', spe_word),
    ('ADCresolution', spe_word),
    ('ADCbitAdjust', spe_word),
    ('gain', spe_word),
    ('Comments', spe_char * 5 * COMMENTMAX),
    ('geometric', spe_word), # x01 - rotate, x02 - reverse, x04 flip
    ('xlabel', spe_char * LABELMAX),
    ('cleans', spe_word),
    ('NumSkpPerCln', spe_word),
    ('SpecMirrorPos', spe_short * 2),
    ('SpecSlitPos', spe_float * 4), 
    ('AutoCleansActive', spe_short),
    ('UseContCleansInst', spe_short),
    ('AbsorbStripNum', spe_short), 
    ('SpecSlipPosUnits', spe_short),
    ('SpecGrooves', spe_float),
    ('srccmp', spe_short),
    ('ydim', spe_word), 
    ('scramble', spe_short),
    ('ContinuousCleansFlag', spe_short), 
    ('ExternalTriggerFlag', spe_short), 
    ('lnoscan', spe_long), # Longs are 4 bytes  
    ('lavgexp', spe_long), # 4 bytes
    ('ReadoutTime', spe_float), 
    ('TriggeredModeFlag', spe_short), 
    ('Spare_2', spe_char * 10), 
    ('sw_version', spe_char * FILEVERMAX), 
    ('type', spe_short),
    ('flatFieldApplied', spe_short), 
    ('Spare_3', spe_char * 16), 
    ('kin_trig_mode', spe_short), 
    ('dlabel', spe_char * LABELMAX), 
    ('Spare_4', spe_char * 436), 
    ('PulseFileName', spe_char * HDRNAMEMAX), 
    ('AbsorbFileName', spe_char * HDRNAMEMAX),
    ('NumExpRepeats', spe_dword),
    ('NumExpAccums', spe_dword),
    ('YT_Flag', spe_short), 
    ('clkspd_us', spe_float),
    ('HWaccumFlag', spe_short),
    ('StoreSync', spe_short),
    ('BlemishApplied', spe_short),
    ('CosmicApplied', spe_short), 
    ('CosmicType', spe_short),
    ('CosmicThreshold', spe_float), 
    ('NumFrames', spe_long),
    ('MaxIntensity', spe_float),
    ('MinIntensity', spe_float),
    ('ylabel', spe_char * LABELMAX),
    ('ShutterType', spe_word),
    ('shutterComp', spe_float),
    ('readoutMode', spe_word),
    ('WindowSize', spe_word),
    ('clkspd', spe_word),
    ('interface_type', spe_word),
    ('NumROIsInExperiment', spe_short),
    ('Spare_5', spe_char * 16),
    ('controllerNum', spe_word),
    ('SWmade', spe_word),
    ('NumROI', spe_short),
    ('ROIinfblk', ROIinfo * ROIMAX),
    ('FlatField', spe_char * HDRNAMEMAX),
    ('background', spe_char * HDRNAMEMAX),
    ('blemish', spe_char * HDRNAMEMAX),
    ('file_header_ver', spe_float),
    ('YT_Info', spe_char * 1000),
    ('WinView_id', spe_long),
    ('xcalibration', AxisCalibration),
    ('ycalibration', AxisCalibration),
    ('Istring', spe_char * 40),
    ('Spare_6', spe_char * 25),
    ('SpecType', spe_byte),
    ('SpecModel', spe_byte),
    ('PulseBurstUsed', spe_byte),
    ('PulseBurstCount', spe_dword),
    ('PulseBurstPeriod', spe_double),
    ('PulseBracketUsed', spe_byte),
    ('PulseBracketType', spe_byte),
    ('PulseTimeConstFast', spe_double),
    ('PulseAmplitudeFast', spe_double),
    ('PulseTimeConstSlow', spe_double),
    ('PulseAmplitudeSlow', spe_double),
    ('AnalogGain', spe_short),
    ('AvGainUsed', spe_short),
    ('AvGain', spe_short),
    ('lastvalue', spe_short)]










#--------- Reading and plotting functions for NEW SPECTROMETER SOFTWARE ----------#
# Typically you should only need to import singleSpectrum and/or waterfallSpectrum

#Reading Bytes
def from_bytes(b, format, offset):
    calcsize = struct.calcsize(format)
    return struct.unpack(format, b[offset:offset+calcsize])[0]

#Reading the XML Line of SPE3.x Files
def openXMLline(filename):
    num_lines = sum(1 for line in open(filename, "rb"))
    f = open(filename, "rb")
    lines = f.readlines()
    
    Txt_Dai = open("Dai_new.txt", "w")  

    f = open(filename, "rb")
    lines = f.readlines()

    i = 0
    while i < num_lines:
        Txt_Dai.write(str(lines[i]) + "\n")
        i += 1
    Txt_Dai.close()

    XMLline = str(lines[num_lines-1])
    startXML = XMLline.find("<SpeFormat")
    XMLline = XMLline[startXML:]
    
    PosVersion = XMLline.find("version") + 9
    Version = XMLline[PosVersion:PosVersion+3]
   
    PosFrame = XMLline.find("Frame") + 14
    Frame = XMLline[PosFrame:]
    PosFrameEnd = Frame.find("\"")
    Frame = Frame[:PosFrameEnd]
    
    PosWidth = XMLline.find("width") + 7
    Width = XMLline[PosWidth:]
    PosWidthEnd = Width.find("\"")
    Width = Width[:PosWidthEnd]
    
    PosHeight = XMLline.find("height") + 8
    Height = XMLline[PosHeight:]
    PosHeightEnd = Height.find("\"")
    Height = Height[:PosHeightEnd]
    
    PosLaser = XMLline.find("WavelengthLaserLine")
    Laser = XMLline[PosLaser:]
    PosLaser = Laser.find("\">") + 2
    Laser = Laser[PosLaser:]
    PosLaserEnd = Laser.find("<")
    Laser = Laser[:PosLaserEnd]
    
    PosCreate = XMLline.find("created") + 9
    Created = XMLline[PosCreate:]
    PosTime = Created.find("T")
    Date = Created[:PosTime]
    PosTimeEnd = Created.find(".")
    Time = Created[PosTime+1:PosTimeEnd]
    
    PosWave = XMLline.find("<Wavelength ")
    PosWaveEnd = XMLline.find("</Wavelength>")
    WaveData = XMLline[PosWave:PosWaveEnd]
    WaveData = WaveData[(WaveData.find("\">")+2):]
    
    Wavedata = []
    WavedataRound = []
    i = 0
    
    while i < int(Width):
        PosNext = WaveData.find(",")
        Wavedata.append(WaveData[:PosNext])
        WavedataRound.append(round(float(WaveData[:PosNext]), 2))
        WaveData = WaveData[PosNext+1:]
        i += 1

    PosExpTime = XMLline.find("<ExposureTime")
    PosExpTimeEnd = XMLline.find("</ExposureTime>")
    ExpTimeData = XMLline[PosExpTime:PosExpTimeEnd]
    ExpTime = ExpTimeData[(ExpTimeData.find("\">")+2):]
    ExpTime = int(float(ExpTime)/1000)
    
    PosCWL = XMLline.find("<CenterWavelength")
    PosCWLEnd = XMLline.find("</CenterWavelength>")
    CWLData = XMLline[PosCWL:PosCWLEnd]
    CWL = CWLData[(CWLData.find("\">")+2):]

    PosBG = (XMLline.find("<BackgroundCorrection><Enabled") + 25)
    BGData = XMLline[PosBG:]
    PosBGBegin = (BGData.find(">")+1)
    PosBGEnd = BGData.find("<")
    BG = BGData[PosBGBegin:PosBGEnd]

    PosGrating = XMLline.find("<Grating><Selected")
    GratingData = XMLline[PosGrating:]
    PosGratingBegin = GratingData.find("[")
    PosGratingEnd = (GratingData.find("]")+1)
    Grating = GratingData[PosGratingBegin:PosGratingEnd]

    return Version, Frame, Width, Height, Laser, Date, Time, ExpTime, CWL, Grating, BG, Wavedata, WavedataRound

#Getting all the important setup informations out of the SPE-Header (SPE2.x), or the XML-Footer (SPE3.x) 
def getData(filename):
    file = open(filename, "rb")
    bytes = file.read()

    SPEVersion = round(from_bytes(bytes, "f", 1992),1)

    datatype = from_bytes(bytes, "h", 108)
    frame_width = from_bytes(bytes, "H", 42)
    frame_height = from_bytes(bytes, "H", 656)
    num_frames = from_bytes(bytes, "i", 1446)
    to_np_type = [np.float32, np.int32, np.int16, np.uint16, None, np.float64, np.uint8, None, np.uint32]
    np_type = to_np_type[datatype]
    itemsize = np.dtype(np_type).itemsize
    XMLOffset = from_bytes(bytes, "64Q", 678)

    Count = frame_width * frame_height

    if SPEVersion >= 3:
        Version, Frame, Width, Height, Laser, Date, Time, ExpTime, CWL, Grating, BG, Wavedata, WavedataRound = openXMLline(filename)
    else:
        Version = SPEVersion
        Frame = num_frames
        Width = frame_width
        Height = frame_height
        Laser = from_bytes(bytes, "d", 3311)
        LocalDate = from_bytes(bytes, "16s", 20)
        LocalDate = LocalDate.decode("utf-8", "ignore")
        Day = LocalDate[:2]
        Year = LocalDate[5:9]
        Month = LocalDate[2:5]
        if Month == "Jan":
            Month = "01"
        elif Month == "Feb":
            Month = "02"
        elif Month == "Mar":
            Month = "03"
        elif Month == "Apr":
            Month = "04"
        elif Month == "May":
            Month = "05"
        elif Month == "Jun":
            Month = "06"
        elif Month == "Jul":
            Month = "07"
        elif Month == "Aug":
            Month = "08"
        elif Month == "Sep":
            Month = "09"
        elif Month == "Oct":
            Month = "10"
        elif Month == "Nov":
            Month = "11"
        elif Month == "Dec":
            Month = "12"
        else:
            Month = "00"
        Date = Year + "-" + Month + "-" + Day
        LocalTime = from_bytes(bytes, "6s", 172)
        LocalTime = LocalTime.decode("utf-8", "ignore")
        Time = LocalTime[:2] + ":" + LocalTime[2:4] + ":" + LocalTime[4:]
        UTCTime = from_bytes(bytes, "6s", 179)
        UTCTime = UTCTime.decode("utf-8", "ignore")
        ExpTime = from_bytes(bytes, "f", 10)
        CWL = from_bytes(bytes, "f", 72)
        Grating = from_bytes(bytes, "32f", 650)
        BG = from_bytes(bytes, "i", 150)
        XStartNM = from_bytes(bytes, "d", 3183)
        XStopNM = from_bytes(bytes, "d", 3199)

        PXSize = (XStopNM-XStartNM)/(Count-1)
        Wavedata = []
        WavedataRound = []
        j = 0
        while j < Count:
            val = XStartNM + (j * PXSize)
            Wavedata.append(val)
            WavedataRound.append(round(val, 2))
            j += 1

    return np_type, itemsize, Count, Version, Frame, Width, Height, Laser, Date, Time, ExpTime, CWL, Grating, BG, Wavedata, WavedataRound

def singleSpectrum(filename):
    gotData = getData(filename)
    np_type = gotData[0]
    Count = int(gotData[2])
    WavedataRound = gotData[-1]
    
    file = open(filename, "rb")
    bytes = file.read()
    data = np.frombuffer(bytes, dtype=np_type, count=Count, offset=4100)
    file.close()
    
    return WavedataRound, data

def waterfallSpectrum(filename):
    gotData = getData(filename)
    np_type = gotData[0]
    Frame = int(gotData[4])
    Itemsize = int(gotData[1])
    Count = int(gotData[2])
    WavedataRound = gotData[-1]
    Data = np.zeros((Frame, Count))

    file = open(filename, "rb")
    bytes = file.read()

    for i in range(0, Frame):
        offset = 4100 + i*Count*Itemsize
        data = np.frombuffer(bytes, dtype=np_type, count=Count, offset=offset)
        Data[i,:] = data

    file.close()
    
    return WavedataRound, Data
