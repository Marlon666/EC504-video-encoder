
import scipy.fftpack as fft

def dct(f):
	F=fft.dct(fft.dct(f,norm='ortho').T,norm='ortho').T
	F[0,0]=F[0,0]/64.
	return F

def idct(F):
	F[0,0]=F[0,0]*64.
	f=fft.dct(fft.dct(F,type=3,norm='ortho').T,type=3,norm='ortho').T
	return f

# TODO: Using dct and idct args axis=1 and axis=0 can avoid the need to transpose the arrays. Compare running times?
