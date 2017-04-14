
import scipy.fftpack as fft

def dct(f):
    F=fft.dct(fft.dct(f,norm='ortho').T,norm='ortho').T
    return F

def idct(F):
    f=fft.dct(fft.dct(F,type=3,norm='ortho').T,type=3,norm='ortho').T
    return f

