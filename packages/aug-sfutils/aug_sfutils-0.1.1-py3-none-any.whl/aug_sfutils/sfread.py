import os, sys, time, datetime
from struct import unpack
import numpy as np
try:
    from . import sfdics, sfhread, sfobj, manage_ed
except:
    import sfdics, sfhread, sfobj, manage_ed

verbose = True
verbose = False
PPGCLOCK = [1e-6, 1e-5, 1e-4, 1e-3]

def to_str(str_or_byt):
    """
    Converts a plain string to a byte string (python3 compatibility)
    """

    str_out = str_or_byt.decode('utf8') if isinstance(str_or_byt, bytes) else str_or_byt
    return str_out.strip()


def parse_url(url, blen=100):
    """
    Read URL content
    """

    try:
        import urllib3
        url_lib = 'urllib3'
    except:
        try:
            import urllib2
            url_lib = 'urllib2'
        except:
            try:
                import urllib
                url_lib = 'urllib'
            except:
                print('No URL lib found, exiting')
                return None
    print('URL reading with %s' %url_lib)
    url_not_found = 'URLs %s not found, exiting' %url
    if url_lib == 'urllib3':
        http = urllib3.PoolManager()
        try:
            tmp = http.request('GET', url)
        except:
            print(url_not_found)
            return None
        bshot = tmp.data
    elif url_lib == 'urllib2':
        try:
            bshot = urllib2.urlopen(url).read(blen)
        except:
            print(url_not_found)
            return None
    elif url_lib == 'urllib':
        try:
            bshot = request.urlopen(url).read()
        except:
            print(url_not_found)
            return None

    return bshot

    
def getlastshot():
    """
    Gets last shot number from the AUG webpage(s)
    """
    url1 = 'http://ssr-mir.aug.ipp.mpg.de:9090/Diag/ShotNumber.dta'
    url2 = 'https://www.aug.ipp.mpg.de/aug/local/aug_only/journal_today_2.html'
    bshot = parse_url(url1)
    if bshot is None:
        page = parse_url(url2, blen=5000)
        if page is None:
            return None
        else:
            page = to_str(page)
            idx = page.find("Current shot:")
            if idx < 0:
                print('Missing substring "Current shot:" in %s, exiting' %url2)
                return None
            substr = page[idx:idx+30]
            a = substr.find('>')+1
            b = substr.find('<', a)
            nshot = int(substr[a:b])-1
    else:
        sshot = to_str(bshot)
        try:
            nshot = int(sshot)
        except:
            print('ERROR sfread.getlastshot: cannot convert string %s to integer' %sshot)
            nshot = None

    return nshot


def get_ts06(nshot):
    """
    Gets the absolute time (ns) of a discharge trigger 
    """
    diag = 'CTI'
    cti = SFREAD(nshot, diag)
    try:
        cdev = cti.getdevice('LAM')
        ts06 = cdev['PhyReset']
        if ts06 == 0:
            ts06 = cdev['TS06']
        if ts06 == 0:
            ts06 = cdev['CT_TS06']
    except: # shot < 35318
        cdev = cti.getdevice('TS6')
        ts06 = cdev['TRIGGER']

    return ts06


def get_gc(nshot=30136):
    """
    Returns first wall contours for plotting
    """
    ygc_sf = [1996, 8646, 8650, 9401, 11300, 11301, 11320, 12751, 13231, 14051, 14601, 16310, 16315, 18204, 19551, 21485, 25891, 30136]
    ygc_sf = np.array(ygc_sf)
    nshot = np.max(ygc_sf[ygc_sf <= nshot])
    ygc = SFREAD(nshot, 'YGC')
    if ygc is not None:
        rrgc     = ygc.getobject('RrGC')
        zzgc     = ygc.getobject('zzGC')
        inxlen   = ygc.getobject('inxlen')
        flag_use = ygc.getobject('ixplin')
        gcnames  = ygc.getobject('chGCnm')

    comp_r = {}
    comp_z = {}

    inxbeg = np.cumsum(np.append(0, inxlen))

    if gcnames is None:
        for jcom, leng in enumerate(inxlen):
            comp_r[jcom] = rrgc[inxbeg[jcom]:inxbeg[jcom+1]]
            comp_z[jcom] = zzgc[inxbeg[jcom]:inxbeg[jcom+1]]
    else:
        for jcom, lbl in enumerate(gcnames):
            lbl = to_str(lbl)
            if flag_use[jcom] > 0:
                comp_r[lbl] = rrgc[inxbeg[jcom]:inxbeg[jcom+1]]
                comp_z[lbl] = zzgc[inxbeg[jcom]:inxbeg[jcom+1]]
    
    return comp_r, comp_z


class SFREAD:
    """
    Class for reading ASDEX Upgrade shotfile data
    """

    def __init__(self, *args, **kwargs):
        """
        Opens a shotfile, reads the header
        """

        n_args = len(args) 
        if n_args == 0:
            print('No argument given, need at least diag_name')
            return
        if isinstance(args[0], str) and len(args[0].strip()) == 3:
            diag = args[0].strip()
            if n_args > 1: 
                if isinstance(args[1], (int, np.integer)):
                    nshot = args[1]
        elif isinstance(args[0], (int, np.integer)):
            nshot = args[0]
            if n_args > 1:
                if isinstance(args[1], str) and len(args[1].strip()) == 3:
                    diag = args[1].strip()
        if 'nshot' not in locals(): 
            print('No argument is a shot number (int), taking last AUG shot')
            nshot = getlastshot()
        if 'diag' not in locals():
            diag = input('Please enter a diag_name (str(3), no delimiter):\n')

        if 'exp' in kwargs.keys():
            exp = kwargs['exp']
        else:
            exp = 'AUGD'
        if 'ed' in kwargs.keys():
            ed = kwargs['ed']
        else:
            ed = 0

        tbeg = time.time()
        self.sfile, self.ed = manage_ed.sf_path(nshot, diag, exp=exp, ed=ed)
        if self.sfile is not None:
            self.shot = nshot
            self.diag = diag
            self.exp  = exp  # unused herein, but useful docu
            if os.path.isfile(self.sfile):
                self.time = datetime.datetime.fromtimestamp(os.path.getctime(self.sfile))
                with open(self.sfile, 'rb') as f:
                    byt_str = f.read(128000)
                    if len(byt_str) < 128:
                        print('Error: shotfile %s has < 128 bytes, ignored' %(self.sfile))
                        self.status = False
                        return
                    self.sfh = sfhread.read_sfh(byt_str)
        self.status = hasattr(self, 'sfh')
        if self.status:
            self.objects = [ i for i in self.sfh['obj_nam'] if self.sfh[i].obj_type in [6, 7, 8, 13] ]
            self.parsets = [ i for i in self.sfh['obj_nam'] if self.sfh[i].obj_type in [3, 4] ]
        self.cache = {}


    def __call__(self, name):
        if not self.status:
            return None
        if name in self.cache.keys():
            return self.cache[name]
        if name in self.objects:
            self.cache[name] = self.getobject(name)
            return self.getobject(name)
        if name in self.parsets:
            self.cache[name] = self.getparset(name)
            return self.getparset(name)
        return None


    def getchunk(self, start, length):
        """
        Reads the requested byteblock from the actual file, not the byt_str
        """
        rdata = None
        with open(self.sfile, 'rb') as f:
            f.seek(start)
            rdata = f.read(length)
        return rdata


    def gettimebase(self, obj):
        """
        Reads the timebase of a given SIG, SGR or AB
        """

        obj = to_str(obj)
        sfo = self.sfh[obj]
        otyp = sfo.obj_type
        if otyp == 8:
            return self.getobject(obj)
        elif otyp in (6, 7, 13):
            rels = self.get_rel_names(obj)
            for rel in rels:
                if self.sfh[rel].obj_type == 8:
                    return self.getobject(rel)
        return None


    def getareabase(self, obj):
        """
        Reads the areabase of a given SIG or SGR
        """

        obj = to_str(obj)
        sfo = self.sfh[obj]
        otyp = sfo.obj_type
        if otyp == 13:
            return self.getobject(obj)
        elif otyp in (6, 7):
            rels = self.get_rel_names(obj)
            for rel in rels:
                if self.sfh[rel].obj_type == 13:
                    return self.getobject(rel)
        return None


    def getobject(self, obj, cal=False):
        """
        Reads the data of a given TB, AB, SIG or SGR
        """

        obj = to_str(obj)
        data = None
        if obj not in self.sfh.keys():
            return None

        sfo = self.sfh[obj]
        if sfo.status != 0:
            print('Status of SF object %s is %d' %(obj, sfo.status))
            return None
        otyp = sfo.obj_type
        if otyp in (6, 7):
            shape_arr = sfo.index[::-1][:sfo.num_dims]
        elif otyp == 8:
            shape_arr = np.array([sfo.n_steps])
        elif otyp == 13:
            x = np.array([sfo.size_x, sfo.size_y, sfo.size_z, sfo.n_steps])
            shape_arr = x[x != 0]
        else:
            return None

        if otyp in (6, 7, 8, 13):
            dfmt = sfo.data_format
            if otyp == 8 and sfo.length == 0:
                if sfo.tbase_type == 1: # PPG_prog, e.g. END:T-LM_END
                    dout = self.ppg_time(obj)
                else:   # ADC_intern, e.g. DCN:T-ADC-SL
                    dout = (np.arange(sfo.n_steps, dtype=np.float32) - sfo.n_pre)/sfo.s_rate
            else:
                if dfmt in sfdics.fmt2len.keys(): # char variable
                    dlen = sfdics.fmt2len[dfmt]
                    bytlen = np.prod(shape_arr) * dlen
                    data = np.chararray(shape_arr, itemsize=dlen, buffer=self.getchunk(sfo.address, bytlen), order='F')
                else: # numerical variable
                    sfmt = sfdics.fmt2struc[dfmt]
                    dt  = np.dtype(sfdics.fmt2np[dfmt])
                    dt = dt.newbyteorder('>')
                    bytlen = np.prod(shape_arr) * np.dtype(sfmt).itemsize
                    data = np.ndarray(shape_arr, '>%s' %sfmt, self.getchunk(sfo.address, bytlen), order='F')

# LongLong in [ns] and no zero at TS06
                if otyp == 8 and dfmt == 13: # RMC:TIME-AD0
                    dout = 1e-9*(data - get_ts06(self.shot))
                else:
                    dout = sfobj.SFOBJ(data, sfho=sfo) # Add metadata
                if otyp in (6, 7) and cal:
                    pscal = self.lincalib(obj)
                    if pscal is not None:
                        for j in range(10):
                            mult = 'MULTIA0%d' %j
                            shif = 'SHIFTB0%d' %j
                            if mult in pscal.keys():
# we need to fix the content of pscal for signagroups
# assuming first entry wins
                                if (pscal[mult].size > 1):
                                    pscal[mult] = pscal[mult][0]
                                    pscal[shif] = pscal[shif][0]
                                dout = dout * pscal[mult] + pscal[shif]
                            else:
                                break
                        if self.diag in ('DCN', 'DCK', 'DCR'):
                            dout.phys_unit = '1/m^2'
 
        else:
            dout = None
        return dout


    def ppg_time(self, tbobj):
        """
        Returns the time-array in [s] for TB of type PPG_prog
        """

        for rel in self.get_rel_names(tbobj):
            if self.sfh[rel].obj_type == 3:
                ppg = self.getdevice(rel)
                if 'PRETRIG' in ppg.keys():
                    pretrig = ppg['PRETRIG']
                if self.sfh[tbobj].n_pre > 0:
                    if pretrig > 0:
                        dt = ppg['RESOLUT'][15] * PPGCLOCK[ppg['RESFACT'][15]] + 1e-6
                    else:
                        dt = 0.
                    start_time = -dt*ppg['PULSES'][0]
                else:
                    start_time = 0.
                time_ppg = []
                start_phase = start_time
                for jphase in range(16):
                    if ppg['PULSES'][jphase] > 0:
                        dt = ppg['RESOLUT'][jphase]*PPGCLOCK[ppg['RESFACT'][jphase]]
                        dtyp = sfdics.fmt2np[self.sfh[tbobj].data_format]
                        tb_phase = dt*np.arange(ppg['PULSES'][jphase], dtype=dtyp) + start_phase
                        time_ppg = np.append(time_ppg, tb_phase)
                        start_phase = time_ppg[-1] + dt
                if len(time_ppg) == 0:
                    return None
                else:
                    return time_ppg
        return None


    def lincalib(self, obj):
        """
        Returns coefficients for signal(group) calibration
        """
        obj = to_str(obj)
        for rel in self.get_rel_names(obj):
            if self.sfh[rel].obj_type == 4:
                caltyp = to_str(sfdics.cal_type[self.sfh[rel].cal_type])
                if caltyp == 'LinCalib':
                    print('PSet for calib: %s' %rel)
                    return self.getparset(rel)
        return None


    def getparset(self, pset):
        """
        Returns data and metadata of a Parameter Set
        """

        pset = to_str(pset)
        sfo = self.sfh[pset]
        otyp = sfo.obj_type
        if otyp not in (3, 4):
            return None

        buf = self.getchunk(sfo.address, sfo.length)

        j0 = 0
        sfo.par_d = {}
        for j in range(sfo.items):
            pname = to_str(buf[j0: j0+8])
            unit, dfmt, n_items = unpack('>3H', buf[j0+8:  j0+14])
            if verbose:
                print(pname, unit, dfmt, n_items)
            status = unpack('>h', buf[j0+14:  j0+16])[0]
            j0 += 16
            if dfmt in sfdics.fmt2len.keys(): # char variable
                dlen = sfdics.fmt2len[dfmt]
                bytlen = n_items * dlen
                value = np.chararray((n_items,), itemsize=dlen, buffer=buf[j0+2: j0+2+bytlen])
                dj0 = 8 * ( (bytlen + 9)//8 )
                j0 += dj0
            else: # number
                sfmt = sfdics.fmt2struc[dfmt]
                val_len = n_items + 2
                bytlen = val_len * np.dtype(sfmt).itemsize
                fmt = '>%d%s' %(val_len, sfmt)
                if dfmt == 7:
                    value = unpack(sfmt, buf[j0+5: j0+6])[0]
                else:
                    value = unpack(fmt, buf[j0: j0+bytlen])
                    value = np.squeeze(value[2:])
                dj0 = 8 * ( (bytlen + 7)//8 )
                j0 += dj0

            if verbose:
                print(pname, value)
            sfo.par_d[pname] = value

        return sfo.par_d


    def getlist(self, obj=None):
        """
        Returns a list of data-objects of a shotfile
        """
        if obj is None:
            obj = 'SIGNALS'
        else:
            obj = to_str(obj)
        sfo = self.sfh[obj]
        otyp = sfo.obj_type
        dfmt = sfo.data_format
        if otyp != 2:
            return None
        buf = self.getchunk(sfo.address, sfo.length)
        sfmt = sfdics.fmt2struc[dfmt]
        list_ids = unpack('>%d%s' %(sfo.items, sfmt), buf)

        return [self.get_obj_name(jid) for jid in list_ids]


    def get_obj_name(self, jobj):
        """
        Returns the object name for an inpur object ID
        """

        return self.sfh['obj_nam'][jobj]


    def get_obj_id(self, lbl):
        """
        Returns the object ID for a given objeect
        """

        lbl = to_str(lbl)
        return self.sfh['obj_id'][lbl]


    def get_rel_names(self, lbl):
        """
        Returns the relation names of a given object
        """

        lbl = to_str(lbl)
        rels_id = self.sfh[lbl].rel
        return [self.get_obj_name(jobj) for jobj in rels_id if jobj < 65535]


    def getdevice(self, lbl):
        """
        Returns a DEVICE object
        """

        return self.getparset(lbl)
