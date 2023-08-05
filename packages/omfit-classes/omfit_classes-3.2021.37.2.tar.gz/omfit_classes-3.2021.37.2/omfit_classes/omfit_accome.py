try:
    # framework is running
    from .startup_choice import *
except ImportError as _excp:
    # class is imported by itself
    if (
        'attempted relative import with no known parent package' in str(_excp)
        or 'No module named \'omfit_classes\'' in str(_excp)
        or "No module named '__main__.startup_choice'" in str(_excp)
    ):
        from startup_choice import *
    else:
        raise

import numpy as np
from omfit_classes.omfit_ascii import OMFITascii
import fortranformat

__all__ = ['OMFITaccomeEquilibrium']


class OMFITaccomeEquilibrium(SortedDict, OMFITascii):
    r"""
    Class used to interface equilibrium files generated by ACCOME

    :param filename: filename passed to OMFITascii class

    :param \**kw: keyword dictionary passed to OMFITascii class
    """

    def __init__(self, filename, **kw):
        OMFITascii.__init__(self, filename, **kw)
        SortedDict.__init__(self, caseInsensitive=True)
        self.dynaLoad = True

    def load(self):
        def splitter(inv, step=16):
            value = []
            for k in range(len(inv) // step):
                value.append(inv[step * k : step * (k + 1)])
            return value

        with open(self.filename, 'r') as f:
            lines = f.read().split('\n')
        header = lines[0].split()
        self['HEADER'] = ''.join([x.ljust(8) for x in header[:-4]])
        _ = int(header[-4])  # obsolete variable
        # number of points in the horizontal and vertical directions respectively
        self['NR'] = NR = int(header[-3])
        self['NZ'] = NZ = int(header[-2])
        # number of poloidal flux surfaces
        self['NV'] = N = int(header[-1])
        f2020 = fortranformat.FortranRecordWriter('5e16.9')

        block = []
        for k in range(1, 5):
            block.extend(splitter(lines[k]))
        data0d = list(map(float, block))
        name0d = [
            'RBOX',  # the nominal full-width of the rectangle
            'ZBOX',  # the nominal full-height of the rectangle
            'RADMAJ',  # nominal major radius of the plasma axis
            'RBOXDST',  # major radius of the inner edge of the rectangular grid
            'YMIDEQ',  # the vertical shift of the rectangular box in the up-down symmetry plane
            'RAXIS',  # major radius of the magnetic axis
            'ZAXIS',  # vertical height of the magnetic axis
            'PSIMAG',  # poloidal flux function values at the magnetic axis
            'PSILIM',  # poloidal flux function values at the last closed flux surface
            'BTOR',  # toroidal magnetic field at raxis
            'TOTEQD',  # toroidal plasma current
            '_PSIMX1',  # poloidal flux function at the magnetic axis (again!)
            '_PSIMX2',  # obsolete variable
            '_XAX1',  # major radius of the magnetic axes(xax1 is the same as raxis above)
            '_XAX2',  # xax2 is not used (xax2 = xax1)
            '_ZAX1',  # vertical height of the magnetic axes(xax1 is the same as zaxis above)
            '_ZAX2',  # zax2 is not used (zax2 = zax1)
            '_PSISEP',  # obsolete variable
            '_XSEP',  # obsolete variable
            '_ZSEP',  # obsolete variable
        ]
        for name, data in zip(name0d, data0d):
            if not name.startswith('_'):
                self[name] = data

        block = []
        n = 5 + 4 * int(np.ceil(N / 5.0))
        for k in range(5, n):
            block.extend(splitter(lines[k]))
        data1d = np.reshape(np.array(list(map(float, block))), (4, N))
        self['FPSIAR'] = data1d[0, :]  # 1-D array of (R * B_phi) on "NV" equi-spaced points in psi
        self['PRAR'] = data1d[1, :]  # 1-D array of pressure on "NV" equi-spaced points in psi
        self['FFPAR'] = data1d[2, :]  # 1-D array of f-f_prime on "NV" equi-spaced points in psi
        self['PPAR'] = data1d[3, :]  # 1-D array of p-p_prime on "NV" equi-spaced points in psi

        block = []
        for k in range(n, len(lines)):
            block.extend(splitter(lines[k]))
            if len(block) == NR * NZ:
                break
        self['PSI'] = np.reshape(np.array(list(map(float, block))), (NR, NZ))  # 2-D array of psi values on an "NR" by "NZ" grid

        n = n + int(np.ceil(NR * NZ / 5.0))
        block = []
        for k in range(n, len(lines)):
            block.extend(splitter(lines[k]))
        data = np.array(list(map(float, block)))

        self['Q'] = data[:N]  # array of safety factor on "NV" equi-spaced points in psi

        r, z = np.reshape(data[N:], (-1, 2)).T
        index = np.where((r == r[0]) & (z == z[0]))[0][1] + 1
        self['RBBBS'] = r[:index]
        self['ZBBBS'] = z[:index]
        self['RLIM'] = r[index:]
        self['ZLIM'] = z[index:]


############################################
if '__main__' == __name__:
    test_classes_main_header()

    tmp = OMFITaccomeEquilibrium(OMFITsrc + '/../samples/accome_equilibrium.dat')
    tmp.load()
