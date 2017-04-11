from os import listdir

import matplotlib.pyplot as plt
import numpy as np
import skimage.io

quant_intra=[[ 8, 16, 19, 22, 26, 27, 29, 34],
             [16, 16, 22, 24, 27, 29, 34, 37],
             [19, 22, 26, 27, 29, 34, 34, 38],
             [22, 22, 26, 27, 29, 34, 37, 40],
             [22, 26, 27, 29, 32, 35, 40, 48],
             [26, 27, 29, 32, 35, 40, 48, 58],
             [26, 27, 29, 34, 38, 46, 56, 69],
             [27, 29, 35, 38, 46, 56, 69, 83]]


def get_jpegs(directory, number):
    directory =  '../testing/720p-10/'
    images = []
    i = 1
    for file in sorted(listdir(directory)):
        if file.endswith('.jpg'):
            images.append(skimage.io.imread(directory + '/' + file))
        if i == number:
            break
    return images

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
            f[x, y] = idct_sum(F, x, y)
    return f

def idct_sum(F, x, y):
    sum = 0
    for u in range(0,8):
        for v in range(0,8):
           sum = sum + C(u)*C(v)/4*F[u, v]*np.cos((2*x + 1)*u*np.pi/16)*np.cos((2*y + 1)*v*np.pi/16)
    return sum

def main():

    # Read an image
    image = get_jpegs('a', 1)[0]
    r = image[:, :, 0]
    g = image[:, :, 1]
    b = image[:, :, 2]

    # Break each image into blocks
    h_blocks = np.shape(r)[0] // 8
    v_blocks = np.shape(r)[1] // 8

    r_blocks = [r[i * 8:(i + 1) * 8:, j * 8:(j + 1) * 8:] for i in range(0, v_blocks) for j in range(0, h_blocks)]
    g_blocks = [g[i * 8:(i + 1) * 8:, j * 8:(j + 1) * 8:] for i in range(0, v_blocks) for j in range(0, h_blocks)]
    b_blocks = [b[i * 8:(i + 1) * 8:, j * 8:(j + 1) * 8:] for i in range(0, v_blocks) for j in range(0, h_blocks)]

    # Grab only the upper left hand corner block to use for testing
    r_test = r_blocks[0]
    g_test = g_blocks[0]
    b_test = b_blocks[0]

    '''
    DCT TRANSOFRM

    I am fairly certain that the scipy dct function is a 1D-only transform and is not what we want

    So I have written 2D DCT functions following their defintion in the MPEG standard
    As, written, they are slow. They might be sped up by using a different computation method.
    '''
    #r_test_dct = scipy.fftpack.dct(r_test, norm='ortho')
    #g_test_dct = scipy.fftpack.dct(g_test, norm='ortho')
    #b_test_dct = scipy.fftpack.dct(b_test, norm='ortho')
    r_test_dct = dct(r_test)
    g_test_dct = dct(g_test)
    b_test_dct = dct(b_test)

    '''
    FORWARD QUANTIZATION

    The purpose of quantization is to allow us to discard higher-frequency information. The quantization matrix used
    is given by the MPEG standard. However, if we want to be more lossy, we can of course modify it. The act of discarding
    information is done by rounding the results of the quantization division. We end up with many zero-valued DCT coefficients
    that may be efficiently encoded into a file

    '''
    enable_quantization = True

    if(enable_quantization):

        # See what DCT'd array looks like before quantization:
        print("Before quantization:")
        print(r_test_dct)

        # Apply quantization and round to nearest integer
        r_test_dct = np.rint(r_test_dct / quant_intra)
        g_test_dct = np.rint(g_test_dct / quant_intra)
        b_test_dct = np.rint(b_test_dct / quant_intra)

        # See what the array looks like with quantization
        print("Quantized array:")
        print(r_test_dct)

    '''
    ENCODER FILE WRITE
    '''


    '''
    DECODER FILE READ
    '''

    '''
    REVERSE QUANTIZATION
    '''
    if(enable_quantization):
        # Reverse quantization
        r_test_dct = r_test_dct * quant_intra
        g_test_dct = g_test_dct * quant_intra
        b_test_dct = b_test_dct * quant_intra


    '''
    INVERSE DCT TRANSFORM
    Take the inverse DCT to recover the images
    Note that the rint and astype calls first round the results to the nearest integer, and then
    change the data format from a float to an int
    '''
    #r_test_idct = scipy.fftpack.idct(r_test_dct, norm='ortho').astype(np.uint8)
    #g_test_idct = scipy.fftpack.idct(g_test_dct, norm='ortho').astype(np.uint8)
    #b_test_idct = scipy.fftpack.idct(b_test_dct, norm='ortho').astype(np.uint8)
    r_test_idct = np.rint(idct(r_test_dct)).astype(np.uint8)
    g_test_idct = np.rint(idct(g_test_dct)).astype(np.uint8)
    b_test_idct = np.rint(idct(b_test_dct)).astype(np.uint8)

    print(np.allclose(r_test, r_test_idct)) # This compares the original data to the recovered data. Returns true if equal. It will be false if we modify the dct values with quantization
    print(np.allclose(g_test, g_test_idct))
    print(np.allclose(b_test, b_test_idct))

    # Compare reconstructed results
    print("Comparing original array with reconstructed results:")
    print(r_test_idct)
    print(r_test)

    '''
    print("R test", np.shape(r_test))
    print(r_test)

    print("G test", np.shape(r_test))
    print(g_test)

    print("B test", np.shape(r_test))
    print(b_test)
    '''

    # Reonstruct the upper left hand corner from the test blocks
    recon_test = np.dstack((r_test_idct, g_test_idct, b_test_idct))
    print("Recon test", np.shape(recon_test))
    plt.imshow(recon_test)
    #plt.show()


if __name__ == "__main__":
    main()