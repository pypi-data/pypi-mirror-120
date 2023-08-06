Routines reading ASDEX Upgrade shotfiles without wrappers
See https://www2.ipp.mpg.de/~git/pyaug/sfread.html

Developed at Max-Planck-Institut fuer Plasmaphysik, Garching, Germany

Requirements:
- python with scipy, numpy, matplotlib (recommended: anaconda)
- pip
- afs client and access to the ASDEX-Upgrade shotfile system

Typical usage:

pip install aug_sfread
python3
>>>import aug_sfread as sf
>>>a = sf.SFREAD(28053, 'CEZ')
>>>a('Ti')
