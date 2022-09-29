"""
A collection of python functions all your data processing and analysis needs.
Currently in no particular order.
"""

__version__ = "0.1.0"

import numpy as np

def load_files():
    """
    About: Creates popup window for user to select datasets.

    Returns
    -------
    files_path : List
        A list of the file paths to each dataset selected. 
        If only one file is selected, then the list has only one element.
    """
    from tkinter import filedialog, Tk
    root = Tk()
    root.withdraw()
    files_path = filedialog.askopenfilenames(initialdir = "C:", title = "Select files", filetypes = (("all files","*.*"), ("text files","*.txt")))
    root.attributes('-topmost', True)
    return files_path

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
        [N * [amplitude, horizontal offset, FWHM, vertical offset]]

    Returns
    -------
    1D array
        Intensity of spectrum
    """
    y = np.zeros_like(x)
    for i in range(0, len(p0), 4):
        a = p0[i]
        x0 = p0[i+1]
        FWHM = p0[i+2]
        c = p0[i+3]
        y += a/(1 + 4 * (x-x0)**2 / FWHM**2) + c
    return y

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
        [N * [amplitude, horizontal offset, FWHM, vertical offset]]

    Returns
    -------
    1D array
        Intensity of spectrum
    """
    y = np.zeros_like(x)
    for i in range(0, len(p0), 4):
        a = p0[i]
        x0 = p0[i+1]
        FWHM = p0[i+2]
        c = p0[i+3]
        y += a * np.exp(- 4 * np.log(2) * (x-x0)**2 / FWHM**2) + c
    return y

def Voigt_FWHM(x, *p0):
    """
    About: Defines a Voigt curve parameterised by FWHMs of Gaussian and 
           Lorentzian constituents.
           
    Parameters
    ----------
    x : 1D array
        Energy values
    *p0 : List
        [amplitude, horizontal offset, Gaussian FWHM, Lorentzian FWHM, vertical offset]

    Returns
    -------
    1D array
        Intensity of spectrum
    """
    a = p0[1]
    x0 = p0[2]
    Gaussian_FWHM = p0[3]
    alpha = 0.5*Gaussian_FWHM
    Lorentzian_FWHM = p0[4]
    gamma = 0.5*Lorentzian_FWHM
    c = p0[5]
    sigma = alpha / np.sqrt(2 * np.log(2))
    return a * np.real(wofz(((x-x0) + 1j*gamma)/sigma/np.sqrt(2))) / sigma /np.sqrt(2*np.pi) + c

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


def g2_rabi2(x, *p0):
    """
    About: Alex Clark's ~most correct~ Rabi g2 function.
           See 10.1103/PhysRevA.94.063839

    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    *p0 : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    purity = p0[0]
    x0 = p0[1]
    cts = p0[2]
    t1 = p0[3]
    t2star = p0[4]
    Omega = p0[5]
    Gamma1 = 1/t1
    Gamma2 = 1/(2*t1) + 1/t2star
    p = Gamma1 + Gamma2
    q = complex(0) + np.emath.sqrt((Gamma1 - Gamma2)**2 - 4*Omega**2)
    return np.real(cts - cts*purity*(p+q)*np.exp(-0.5*(p-q)*np.abs(x-x0))/(2*q) + cts*purity*(p-q)*np.exp(-0.5*(p+q)*np.abs(x-x0))/(2*q))










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