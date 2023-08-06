Routines reading ASDEX Upgrade shotfiles (without wrappers) and
manipulating equilibria
See https://www2.ipp.mpg.de/~git/pyaug

Developed at Max-Planck-Institut fuer Plasmaphysik, Garching, Germany

Requirements:
- python with scipy, numpy, matplotlib (recommended: anaconda)
- pip
- afs client and access to the ASDEX-Upgrade shotfile system

Typical usage:

pip install aug_sfread
python3

import aug_sfutils as sfu
equ = sfu.EQU(28053)
cez = sfu.SFREAD(28053, 'CEZ')
if cez.status:
    tim  = cez.gettimebase('Ti_c')
    rmaj = cez('R_time').T
    zin  = cez('z_time').T
    Ti   = cez('Ti_c')

    rho_t = sfu.rz2rho(equ, rmaj, zin, t_in=tim, coord_out='rho_tor', extrapolate=False)
    jt_plot = len(tim)//2
    plt.figure(1)
    plt.xlabel(r'$\rho_{tor}$')
    plt.ylabel('Ti [keV]')
    plt.figtext(0.5, 0.95, '#%s  at t = %9.4f' %(nshot, tim[jt_plot]))
    plt.plot(rho_t[jt_plot, :], Ti[jt_plot, :], 'go')
    plt.show()
