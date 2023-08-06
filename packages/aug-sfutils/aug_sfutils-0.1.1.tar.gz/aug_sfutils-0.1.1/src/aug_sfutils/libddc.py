import os
import sys

def get_diagprefix(name):
    ''' Determine prefix for path expansion based on static diag list

        The list is copied from gerrit: codac/daq/libddww8/src/islevel0diag.c
        as of 2021-08-20.
    '''
    check=False
    if not isinstance(name, str) or len(name) != 3:
        return None

    shotlsdiags = [
        "L0/BES", "L1/BLB", "L1/BLC", "L0/BLK", "L0/BLV", "L0/BOS", "L1/BPD", "L0/BRD", "L0/BSK",
        "L0/CAR", "L0/CDL", "L1/CEC", "L0/CER", "L1/CEZ", "L0/CFR", "L0/CHR", "L1/CLF", "L1/CLF",
        "L0/CMR", "L1/CMZ", "L0/CNR", "L1/COF", "L0/CON", "L0/COO", "L0/COR", "L0/CPR", "L1/CPZ",
        "L1/CSX", "L0/CTI", "L0/CUR", "XX/CXB", "L0/CXR", "L0/DCD", "L0/DCN", "L1/DCR", "L1/DCS",
        "L1/DDS", "L0/DSM", "L0/DST", "L0/DTM", "L1/DTN", "YY/DTS", "L0/DUS", "L0/DVS", "L1/ECK",
        "L1/ECK", "L0/ECN", "YY/ECR", "L1/ECS", "L1/ECS", "L0/ECU", "L1/ECV", "L1/ECV", "L0/END",
        "L1/ENR", "L1/EQH", "L1/EQH", "L1/EQI", "L1/EQR", "L0/EVS", "L0/EVV", "L0/EZC", "L0/EZD",
        "XX/FHA", "XX/FHC", "L0/FHF", "L1/FPC", "L1/FPG", "L1/FPP", "L0/FVS", "L1/GIW", "L1/GPI",
        "L1/GQH", "L1/GQH", "L1/GQI", "L0/GRA", "L0/GRF", "L0/GRG", "L0/GVS", "L0/HAM", "L0/HBD",
        "YY/HEB", "L0/HFB", "L1/HFC", "L0/HST", "L0/HXR", "XX/ICA", "L0/ICG", "L1/ICH", "L0/ICL",
        "L1/ICP", "XX/ICS", "L1/IDA", "L1/INJ", "L1/IOB", "L0/JMO", "L1/JOU", "L1/JOW", "YY/KRF",
        "L0/KWN", "L0/KWS", "XX/LIZ", "L0/LSB", "L0/LSF", "YY/LSG", "L0/LVS", "L0/MAC", "L0/MAD",
        "L1/MAE", "L0/MAG", "L0/MAH", "L0/MAI", "L0/MAM", "L1/MAN", "L1/MAP", "L1/MAR", "L0/MAS",
        "L0/MAU", "L0/MAW", "L0/MAX", "L0/MAY", "L1/MBI", "L0/MBR", "L1/MDI", "L1/MDI", "L1/MDI",
        "L0/MGS", "MH/MHC", "MH/MHI", "L1/MOD", "L0/MPC", "L0/MPG", "L1/MRI", "L0/MSP", "L1/MSR",
        "L0/MSS", "XX/MSX", "L0/MUM", "L1/NEO", "L0/NIB", "L0/NIK", "L1/NIS", "L0/NPA", "XX/NSA",
        "L1/NSP", "L1/OBS", "L0/OSI", "XX/PCR", "XX/PCS", "L0/PHB", "YY/PID", "L0/PKG", "L0/POT",
        "L1/RAB", "L0/RAD", "L1/RAP", "XX/RMC", "L1/RMD", "L1/RRC", "L0/SCJ", "L1/SCL", "L0/SIF",
        "L0/SMF", "L0/SPU", "L0/SST", "L1/SSX", "SX/SXA", "SX/SXB", "SX/SXC", "SX/SXD", "SX/SXF",
        "SX/SXG", "SX/SXH", "SX/SXI", "SX/SXJ", "SX/SXK", "SX/SXL", "SX/SXM", "SX/SXN", "SX/SXO",
        "SX/SXS", "SX/SXT", "L0/TAA", "L0/TAB", "L0/TAC", "L0/TAD", "L0/TAE", "L0/TAF", "L0/TAG",
        "L0/TAH", "L1/TBM", "L1/TFM", "L0/TLS", "L1/TOT", "L1/TOT", "L1/TTH", "L0/UVD", "YY/UVE",
        "L1/UVS", "L1/UVS", "L1/UVS", "L1/UVS", "L1/VTA", "YY/WPG", "XX/XPR", "L1/XRT", "XX/XVR",
        "XX/XVS", "YY/XVT", "L0/ZEF"
    ]

    # order of dictionary is important due to L0 duplicates !!
    diags = {}
    diags['MH'] = [
        "MHA", "MHB", "MHC", "MHD", "MHE", "MHF", "MHG", "MHH", "MHI"
    ]
    diags['SX'] = [
        "SXA", "SXB", "SXC", "SXD", "SXF", "SXG", "SXH", "SXI", "SXJ", "SXK",
        "SXL", "SXM", "SXN", "SXO", "SXS", "SXT"
    ]
    diags['XX'] = [
        "CTA", "CTC", "FHA", "FHB", "FHC", "ICA", "ICS", "LIZ", "MSX", "NSA",
        "PCR", "PCS", "PRA", "PRC", "PRD", "RFL", "RMA", "RMB", "RMC", "TDI",
        "TSX", "XPR", "XVR", "XVS", "CGF", "CXB", "PRF"
    ]
    diags['YY'] = [
        "CEF", "DTS", "ECQ", "ECE", "HEB", "KRF", "LSG", "PID", "TSC", "UVS",
        "WPG", "XVT", "XVU", "ECR", "NPI", "UVE"
    ]
    diags['L1'] = [
        "JCU", "JFE", "SPC", "MNO", "NSP"
    ]
    diags['L0'] = [
        "ACA", "ACB", "ACQ", "BMT", "BOF", "BOL", "BRD", "BSK", "CCD", "CDH",
        "CER", "CHR", "CMT", "COM", "COO", "CTF", "CXR", "DCN", "DEP", "DIN",
        "DIV", "DSM", "DST", "DVM", "ECH", "END", "EVU", "EVV", "GRA", "HAM",
        "HAR", "HDV", "HEL", "HST", "HTS", "HVS", "HXR", "IFM", "ICF", "ICR",
        "ICT", "ION", "JMO", "JOH", "KMT", "KWK", "KWN", "LBM", "LBO", "LEN",
        "LIA", "LIB", "LIC", "LIF", "LPS", "LSB", "LSF", "LSW", "LVS", "MAB",
        "MAD", "MAF", "MAG", "MAI", "MAK", "MAS", "MBR", "MER", "MHA", "MHB",
        "MHC", "MHD", "MHE", "MHF", "MHG", "MHH", "MIC", "MIR", "MSE", "MSP",
        "MSX", "MUM", "NIB", "NIK", "NIR", "NIT", "NWB", "NWK", "PEL", "PHA",
        "PKG", "POT", "PPA", "PPT", "PSL", "RAD", "RAH", "RAV", "REF", "REH",
        "REI", "REV", "RFL", "RMA", "RMB", "ROE", "RWB", "SCJ", "TAA", "TAB",
        "TAC", "TAD", "TAE", "TAF", "TAG", "TAH", "TEO", "TER", "TET", "TLS",
        "UVD", "VEC", "VSS", "VTS", "ZEA", "ZEB", "ZEF", "CTI", "BEP", "BES",
        "BLK", "BLV", "CAR", "CDL", "CMR", "CNR", "CON", "CPR", "DCD", "DTM",
        "DVS", "EVS", "FVS", "GRF", "GRG", "GVS", "HBD", "HFB", "ICG", "ICL",
        "KWS", "MAC", "MAH", "MAM", "MAU", "MAW", "MAX", "MAY", "MGS", "MPC",
        "BOS", "CFR", "COR", "CUR", "DUS", "ECN", "ECU", "EZC", "EZD", "FHF",
        "LSM", "NPA", "RSG", "MPG", "MSS", "OSI", "PHB", "SIF", "SMF", "SPU",
        "SST"
    ]

    if check:
        diagnew = {}
        diagnew['L0'] = []
        diagnew['XX'] = []
        diagnew['YY'] = []
        for pr in shotlsdiags:
            prs = pr.split('/')
            if not prs[1] in diags[prs[0]]:
                if prs[0] != 'L1':
                    diagnew[prs[0]].append(prs[1])
        for i in diagnew.keys():
            print(i+':')
            for j in diagnew[i]:
                sys.stdout.write('"'+j+'", ')
            print("")

        return ""

    for pr in diags.keys():
        if name in diags[pr]:
            return pr

    return 'L1'

def shf(dirlist, i):
    ''' Check existence of shotfile in the directory given
    '''
    for d in dirlist:
        if d.startswith(str(i)):
            return True
    return False

def ddcshotnr(diag, shot=99999, experiment='AUGD'):
    ''' Pythonic implementation of ddww routine: ddcshotnr

        Gets latest/most recent shotnumber of specified diagnostic from
        specified experiment up to the provided shotnumber.
        Error codes:
            -1  :  no suitable shot found under given experiment
            -2  :  wrong input shotnumber (wrong type or out of range)
    '''
    # shotnumber needs to be an int and in range, else no result
    if not isinstance(shot, int) or shot > 99999:
        return -3
    # AUGD shotfiles follow a particular path-specification
    if experiment == 'AUGD':
        basepath = '/afs/ipp-garching.mpg.de/u/augd/shots/'
        prefix = get_diagprefix(diag)
        fac = 10
    else:
        # private shotfiles use a different path logic
        basepath = '/afs/ipp-garching.mpg.de/u/'+experiment.lower()+'/shotfiles/'+diag+'/'
        fac = 1000

    # go backwards starting with directory of given shot
    for sr in range(int(shot/fac), -1, -1):
        fullpath = basepath + '%04d' % sr + '/' + prefix + '/' + diag \
            if experiment == 'AUGD' else basepath + str(sr)
        if not os.path.isdir(fullpath):
            continue
        dirlist = os.listdir(fullpath)
        ista = 9 if experiment == 'AUGD' else 999
        for i in range(ista, -1, -1):
            # if maxshot happens to be smaller than current check, skip the check
            if shot < sr*fac+i:
                continue
            fshot = '%05d' % int(sr*fac+i) if experiment == 'AUGD' else '%03d' % i
            if shf(dirlist, fshot):
                return sr*fac+i

    # no result found anywhere, return -1
    return -1

if __name__ == "__main__":
    pass
