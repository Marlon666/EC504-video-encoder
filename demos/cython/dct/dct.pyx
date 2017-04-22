import scipy.fftpack as fft

import numpy as np

cimport numpy as np
cimport cython

ctypedef unsigned char DTYPE_DCT

cpdef dct(np.ndarray[DTYPE_DCT, ndim=2] f):
    return fft.dct(fft.dct(f, axis=0, norm='ortho', type=2), axis=1, norm='ortho', type=2)

cpdef idct(F):
    return fft.idct(fft.idct(F, axis=0, norm='ortho', type=2), axis=1, norm='ortho', type=2)