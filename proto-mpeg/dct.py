import numpy as np

def C(u):
    if u == 0:
        return 2**(-1/2)
    else:
        return 1

def dct(f):
    '''
    Two-dimensional discrete cosine transform
    This is a slow, proof-of-concept implementation.
    :param f: 8x8 array of pixels
    :return: 8x8 array of DCT coefficients
    '''
    F = np.empty((8, 8), dtype=float)
    for u in range(0,8):
        for v in range(0,8):
            F[u, v] = dct_sum(f, u, v)
    return F

def dct_sum(f, u, v):
    '''
    :param f: 8x8 array of pixels
    :param u: horizontal frequency index
    :param v: vertical frequency index
    :return: F(u,v)
    '''
    coeff = C(u)*C(v)/4
    sum = 0
    for y in range(0,8):
        for x in range(0,8):
           sum = sum + f[x, y]*np.cos((2*x+1)*u*np.pi/16)*np.cos((2*y+1)*v*np.pi/16)
    return coeff * sum

def idct(F):
    f = np.empty((8, 8), dtype=float)
    for x in range(0,8):
        for y in range(0,8):
            value = idct_sum(F, x, y)
            if value > 255:
                # Make sure that we restrict the IDCT to uint8 values
                # print("IDCT produced value greater than 255:", value)
                f[x, y] = 255
            else:
                f[x, y] = value
    return f

def idct_sum(F, x, y):
    sum = 0
    for u in range(0,8):
        for v in range(0,8):
           sum = sum + C(u)*C(v)/4*F[u, v]*np.cos((2*x + 1)*u*np.pi/16)*np.cos((2*y + 1)*v*np.pi/16)
    return sum