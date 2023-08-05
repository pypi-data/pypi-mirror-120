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


from omfit_classes.omfit_ascii import OMFITascii
from omfit_classes.omfit_json import OMFITjson
from omfit_classes.sortedDict import SortedDict
import fortranformat
import numpy as np
from scipy import integrate, interpolate

__all__ = ['OMFITdskgato', 'OMFITo4gta', 'OMFITgatohelp', 'OMFITgatoDiagnostic']


class OMFITdskgato(SortedDict, OMFITascii):
    r"""
    OMFIT class used to interface to equilibria files generated by GATO (.dskgato files)

    NOTE: this object is "READ ONLY", meaning that the changes to the entries of this object will not be saved to a file. Method .save() could be written if becomes necessary

    :param filename: filename passed to OMFITobject class

    :param \**kw: keyword dictionary passed to OMFITobject class
    """

    def __init__(self, filename='', **kw):
        OMFITascii.__init__(self, filename, **kw)
        SortedDict.__init__(self)
        self.dynaLoad = True

    @dynaLoad
    def load(self):
        # Parser based on prgen_reqd_dskgato.f90 in GACODE

        with open(self.filename, 'r') as f:
            lines = f.read()
        fr = fortranformat.FortranRecordReader
        f10 = fr('1p4e19.12')

        def read_array(n=None):
            tmp = []
            if n is None:
                while True:
                    try:
                        tmp.extend(f10.read(next(lines_iter)))
                    except Exception:
                        return np.array(tmp).astype(float)
            else:
                for k in range(n // 4 + 1):
                    tmp.extend(f10.read(next(lines_iter)))
                return np.array(tmp).astype(float)[:n]

        lines_iter = iter(lines.split('\n'))

        self.clear()
        self['__header__'] = ''
        while True:
            try:
                tmp = next(lines_iter)
                if len(tmp.split()) == 2:
                    self['NSURF'], self['NTHT'] = list(map(int, tmp.split()[:2]))
                    self['SYMMETRIC'] = 1
                    break
                elif len(tmp.split()) == 3:
                    self['NSURF'], self['NTHT'], self['SYMMETRIC'] = list(map(int, tmp.split()[:3]))
                    break
            except ValueError:
                self['__header__'] += tmp

        self['NSURF'] = self['NSURF'] - 1  # Accounting for magnetic axis
        self['NARC'] = 2 * (self['NTHT'] - 1) + 1  # ! Repeat point

        self['RCENTR'], self['RMAXIS'], self['ZMAXIS'], self['BCENTR'] = f10.read(next(lines_iter))
        self['CURRENT'], self['axddxz'], dummy, dummy = f10.read(next(lines_iter))

        self['PSI'] = read_array(self['NSURF'])
        self['FPOL'] = read_array(self['NSURF'])
        self['FFPRIM'] = read_array(self['NSURF'])
        self['PRES'] = read_array(self['NSURF'])
        self['PPRIME'] = read_array(self['NSURF'])
        self['QPSI'] = read_array(self['NSURF'])
        self['NE'] = read_array(self['NSURF'])

        self['SEQDPDR'] = read_array(self['NTHT'])
        self['SEQDPDZ'] = read_array(self['NTHT'])

        for item in ['R', 'Z', 'Br', 'Bz']:
            try:
                self[item] = np.reshape(read_array(self['NTHT'] * (self['NSURF'] + 1)), (-1, self['NSURF'] + 1))
            except StopIteration:
                break
            except ValueError:
                # sometimes Br and Bz may not be written (eg. by TOQ code)
                self[item] = []

        # Parse extra namelist that is sometimes appended at the bottom (eg. by TOQ code)
        if False and '&' in lines:
            from omfit_classes.namelist import NamelistFile

            nml_txt = '&' + '&'.join(lines.split('&')[1:]).strip()
            self['AuxNamelist'] = NamelistFile(input_string=nml_txt, nospaceIsComment=True, bang_comment_symbol='<', collect_arrays=False)

        self.add_derived()

    def add_derived(self):
        """
        Compute additional quantities that are not in the DSKGATO file itself
        """
        self['SIMAG'] = self['PSI'][0]
        self['SIBRY'] = self['PSI'][-1]

        # Calculate RHOVN from PSI and Q profile
        phi = integrate.cumtrapz(self['QPSI'], np.linspace(self['SIMAG'], self['SIBRY'], len(self['QPSI'])), initial=0)
        self['RHOVN'] = np.sqrt(np.abs(2 * np.pi * phi / (np.pi * self['BCENTR'])))
        self['RHOVN'] = self['RHOVN'] / np.max(self['RHOVN'])

        # Boundaries
        if 'R' in self and 'Z' in self:
            self['RADIAL'] = np.sqrt((self['R'] - self['RMAXIS']) ** 2 + (self['Z'] - self['ZMAXIS']) ** 2)
            self['THETA'] = np.arctan2((self['Z'] - self['ZMAXIS']), self['R'] - self['RMAXIS'])
            R = self['R']
            Z = self['Z']
            if self['SYMMETRIC']:
                R = np.vstack((R, R[self['NSURF'] - 1 :: -1, :]))
                Z = np.vstack((Z, -Z[self['NSURF'] - 1 :: -1, :]))
            self['RBBBS'] = R[:, -1]
            self['ZBBBS'] = Z[:, -1]

    def plot(self, usePsi=False, only2D=False, **kw):
        r"""
        Function used to plot dskgato-files.
        This plot shows flux surfaces in the vessel, pressure, q profiles, P' and FF'

        :param usePsi: In the plots, use psi instead of rho

        :param only2D: only make flux surface plot

        :param levels: list of sorted numeric values to pass to 2D plot as contour levels

        :param label: plot item label to apply lines in 1D plots (only the q plot has legend called by the geqdsk class
            itself) and to the boundary contour in the 2D plot (this plot doesn't call legend by itself)

        :param ax: Axes instance to plot in when using only2D

        :param \**kw: Standard plot keywords (e.g. color, linewidth) will be passed to Axes.plot() calls.
        """
        import matplotlib
        from matplotlib import pyplot

        label = kw.pop('label', None)  # Take this out so the legend doesn't get spammed by repeated labels

        def plot2D(ax, **kw):
            kw1 = copy.copy(kw)
            kw1['linewidth'] = kw['linewidth'] + 1

            # boundary
            ax.plot(self['RBBBS'], self['ZBBBS'], label=label, **kw1)

            # get the color
            kw1.setdefault('color', ax.lines[-1].get_color())

            if 'R' in self and 'Z' in self:
                # number of levels
                m = int(np.ceil(self['NSURF'] / 10.0))

                # flux surfaces
                R = self['R']
                Z = self['Z']
                if self['SYMMETRIC']:
                    R = np.vstack((R, R[self['NSURF'] - 1 :: -1, :]))
                    Z = np.vstack((Z, -Z[self['NSURF'] - 1 :: -1, :]))

                if usePsi:
                    psin = (self['PSI'] - self['PSI'][0]) / (self['PSI'][-1] - self['PSI'][0])
                    R = interpolate.interp1d(psin, R[:, 1:])(np.linspace(0, 1, 10))
                    Z = interpolate.interp1d(psin, Z[:, 1:])(np.linspace(0, 1, 10))
                else:
                    R = interpolate.interp1d(self['RHOVN'], R[:, 1:])(np.linspace(0, 1, 10))
                    Z = interpolate.interp1d(self['RHOVN'], Z[:, 1:])(np.linspace(0, 1, 10))

                R = np.vstack((R, R[0, :] * np.nan)).T
                Z = np.vstack((Z, Z[0, :] * np.nan)).T
                ax.plot(R.flatten(), Z.flatten(), **kw)

            # magnetic axis
            ax.plot(self['RMAXIS'], self['ZMAXIS'], '+', **kw1)

            # aspect_ratio
            ax.set_aspect('equal')
            ax.set_xlim((np.array(ax.get_xlim()) - self['RMAXIS']) * 1.05 + self['RMAXIS'])
            ax.set_ylim((np.array(ax.get_ylim()) - self['ZMAXIS']) * 1.05 + self['ZMAXIS'])

        kw.setdefault('linewidth', 1)

        if not only2D:
            fig = pyplot.gcf()
            kw.pop('ax', None)  # This option can't be used in this context, so remove it to avoid trouble.
            pyplot.subplots_adjust(wspace=0.23)

            if usePsi:
                xName = '$\\psi$'
                x = np.linspace(0, 1, len(self['PRES']))
            else:
                xName = '$\\rho$'
                if 'RHOVN' in self and np.sum(self['RHOVN']):
                    x = self['RHOVN']
                else:
                    x = self['AuxQuantities']['RHO']

            ax = fig.add_subplot(232)
            ax.plot(x, self['PRES'], **kw)
            kw.setdefault('color', ax.lines[-1].get_color())
            ax.set_title(r'$\,$ Pressure')
            ax.ticklabel_format(style='sci', scilimits=(-1, 2), axis='y')
            pyplot.setp(ax.get_xticklabels(), visible=False)

            ax = fig.add_subplot(233, sharex=ax)
            ax.plot(x, self['QPSI'], **kw)
            ax.set_title('$q$ Safety factor')
            ax.ticklabel_format(style='sci', scilimits=(-1, 2), axis='y')
            if label:
                try:
                    ax.legend(labelspacing=0.2, loc=0).draggable(state=True)
                except Exception:
                    pass
            pyplot.setp(ax.get_xticklabels(), visible=False)

            ax = fig.add_subplot(235, sharex=ax)
            ax.plot(x, self['PPRIME'], **kw)
            ax.set_title(r"$P\,^\prime$ source function")
            ax.ticklabel_format(style='sci', scilimits=(-1, 2), axis='y')
            pyplot.xlabel(xName)

            ax = fig.add_subplot(236, sharex=ax)
            ax.plot(x, self['FFPRIM'], **kw)
            ax.set_title(r"$FF\,^\prime$ source function")
            ax.ticklabel_format(style='sci', scilimits=(-1, 2), axis='y')
            pyplot.xlabel(xName)

            ax = fig.add_subplot(131, aspect='equal')
            ax.set_frame_on(False)
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
        else:
            ax = kw.pop('ax', pyplot.gca())

        plot2D(ax, **kw)


class OMFITo4gta(SortedDict, OMFITascii):
    r"""
    OMFIT class used to interface with GATO o4gta files

    :param filename: filename passed to OMFITascii class

    :param \**kw: keyword dictionary passed to OMFITascii class
    """

    def __init__(self, filename, **kw):
        SortedDict.__init__(self)
        OMFITascii.__init__(self, filename, **kw)
        self.dynaLoad = True

    @dynaLoad
    def load(self):
        with open(self.filename, 'r') as f:
            d = f.readlines()
        passed_amp = False
        for i, ival in enumerate(d):
            if passed_amp:
                if 'Relative' in ival or 'Imaginary Amplitudes' in ival or 'Fourier' in ival:
                    break
                if 'psval' in ival:
                    x = ival.split()
                    for mode in x:
                        try:
                            mode = int(mode)
                        except ValueError:
                            pass
                        self[mode] = []
                elif ival != '':
                    xx = ival.split()
                    if len(xx):
                        for j, mode in enumerate(x):
                            try:
                                mode = int(mode)
                            except ValueError:
                                pass
                            self[mode].append(float(xx[j]))

            if 'Real Amplitudes' in ival:
                passed_amp = True
        for item in self:
            if isinstance(self[item], list):
                self[item] = np.array(self[item])

    @property
    def modes(self):
        return [item for item in self if isinstance(item, int)]

    def plot(self, asinh_transform=1.0):
        """
        :param asinh_transform: apply `xi_mod = arcsinh(xi * asinh_transform)` transformation
        """
        from matplotlib import pyplot

        tmp = []
        for mode in self.modes:
            tmp.append(self[mode])
        tmp = np.array(tmp)
        if asinh_transform:
            tmp = arcsinh(tmp * asinh_transform)
        M = np.max(abs(tmp.flatten()))
        C = pyplot.pcolor(self['psval'], self.modes, tmp, vmin=-M, vmax=M, cmap=pyplot.get_cmap('seismic'))
        pyplot.colorbar(C)
        pyplot.xlabel(r'$\psi$')
        pyplot.title(r'$\xi$')
        pyplot.ylabel('m')
        pyplot.legend(loc=0)


def OMFITgatohelp(*args, **kw):
    r"""
    generates help dictionary for GATO namelist starting from smaphXXX.f

    :param \*args: arguments passed to OMFITascii object

    :param \**kw: keyworkd arguments passed to OMFITascii object

    :return: OMFITjson with parsed help definitions and default values
    """

    obj = OMFITascii(*args, **kw)
    with open(obj.filename, 'r') as f:
        lines = [re.sub('\r', '', x).rstrip('\\') for x in f.read().split('\n')]

    entries = OMFITjson('GATO_help.json')
    state = None
    mapper = {}
    npxdm = None
    for line in lines:
        if line.startswith('c     Physical Case:'):
            state = 'definitions'
        if line.startswith('c 1.0 Define constants and default parameters'):
            state = None
        if line.startswith('c 1.4 Set namelist defaults'):
            state = 'defaults'
        if line.startswith('c 2.0 Read namelist input file'):
            state = None
        if npxdm is None and line.strip().startswith('parameter (npx='):
            npxdm = eval(re.sub(r'\s+parameter\s*\(npx=([0-9]+),.*', r'\1', line))
            print('npx=%d' % npxdm)
        if state == 'definitions':
            if re.match(r'^c\s+[\w\(\)\,]+:\s*\w+.*', line):
                entry = re.sub(r'^c\s+([\w\(\)\,]+):\s+\w+.*', r'\1', line)
                entry = entry.split('(')[0]
                entries[group][entry] = {}
                entries[group][entry]['description'] = re.sub(r'^c\s+[\w\(\)\,]+:\s+(\w+.*)', r'\1', line).strip() + '\n'
                entries[group][entry]['default'] = 0
                mapper[entry] = group
            elif re.match(r'^c     \w.*:$', line.strip()):
                group = re.sub(r'^c\s+(\w.*):', r'\1', line)
                print('* ' + group)
                entries[group] = {}
            else:
                entries[group][entry]['description'] += re.sub(r'^c\s+(.+)', r'\1', line).strip() + '\n'
        if state == 'defaults':
            if line.startswith('c') or not len(line.strip()) or re.match(r'^[0-9].*', line.strip()):
                continue
            entry, value = line.strip().split('=')
            entry = entry.strip()
            value = value.strip()
            max0 = lambda *x: max(x)
            min0 = lambda *x: min(x)
            ncxdm = 2 * npxdm
            npk = npxdm
            try:
                locals()[entry] = eval(value)
                entries[mapper[entry]][entry]['default'] = eval(value)
            except KeyError:
                pass

    return entries


class OMFITgatoDiagnostic(SortedDict, OMFITascii):
    r"""
    OMFIT class used to interface with GATO diagnostic.dat files

    :param filename: filename passed to OMFITascii class

    :param \**kw: keyword dictionary passed to OMFITascii class
    """

    def __init__(self, filename, **kw):
        SortedDict.__init__(self)
        OMFITascii.__init__(self, filename, **kw)
        self.dynaLoad = True

    @dynaLoad
    def load(self):
        with open(self.filename, 'r') as f:
            d = f.readlines()

        # Read lines and put data into lists
        # Acting on tmp dictionary seems to be faster than acting on self here
        tmpDict = {}
        item = 'beginning'
        tmpDict[item] = []
        for i, line in enumerate(d):
            if 'i=1' in line or 'j=1' in line:
                item = ''.join(line.split())
                tmpDict[item] = []
            else:
                vals = line.split()
                for mode in vals:
                    try:
                        tmpDict[item].append(float(mode))
                    except ValueError:
                        pass

        # Reshape 1D list into 1D or 2D array and rename
        for item in tmpDict:
            if 'j=1' in item and 'i=1' in item:
                try:
                    jpsi = int(item.split('j=1,')[1].split(',')[0])
                    itht = int(item.split('i=1,')[1])
                    tmpDict[item] = np.reshape(np.array(tmpDict[item]), (itht, jpsi))
                    item_short = item.split(',j=1')[0]

                    self[item_short] = tmpDict[item]
                except Exception:
                    self[item] = 'Could not be parsed'
            elif 'i=1' in item:
                tmpDict[item] = np.array(tmpDict[item])
                item_short = item.split(',i=1')[0]
                self[item_short] = tmpDict[item]
            elif 'j=1' in item:
                tmpDict[item] = np.array(tmpDict[item])
                item_short = item.split(',j=1')[0]
                self[item_short] = tmpDict[item]
            else:
                self[item] = 'Could not be parsed'

    def plot(self, item='xreal(j,i)'):
        """
        :param item: is plotting item against R, Z grid
        """
        from matplotlib import pyplot

        fig = pyplot.figure()
        ax = fig.add_subplot(111)
        pyplot.plot(self['rwall(i)'], self['zwall(i)'], color='k')
        C = pyplot.contourf(self['rcc(j,i)'], self['zcc(j,i)'], self[item], cmap=pyplot.get_cmap('seismic'))
        pyplot.colorbar(C)
        ax.set_aspect('equal')
        pyplot.xlabel(r'$R (m)$')
        pyplot.ylabel(r'$Z (m)$')
        pyplot.title(item)

    def plot_modes(self, item='xreal(j,i)', tolerance=0.25):
        """
        :param item: plotting item against R, Z grid

        :param tolerance: size of mode needed to be plotted relative to the largest mode
        """
        psi = self['psimesh(j,i)'][0, :]
        xfft = np.fft.fft(self[item], axis=0)
        xfft_ar = abs(np.real(xfft[:, :]))
        tlen = len(xfft[0, :])
        freqs = np.fft.fftfreq(tlen, d=1.0 / tlen)
        maxval = max(np.sum(xfft, axis=1))

        for i in range(tlen):
            if np.sum(xfft_ar[i, :]) > tolerance * maxval:
                pyplot.plot(psi, xfft_ar[i, :], label=freqs[i])

        pyplot.xlabel(r'$\psi$')
        pyplot.ylabel(item)
        pyplot.legend(loc='upper left')


############################################
if '__main__' == __name__:
    test_classes_main_header()

    tmp1 = OMFITdskgato(OMFITsrc + '/../samples/29.dskgato')

    from matplotlib import pyplot

    pyplot.figure()
    tmp1.plot(usePsi=False)

    pyplot.figure()
    tmp1.plot(usePsi=True)

    pyplot.show()
