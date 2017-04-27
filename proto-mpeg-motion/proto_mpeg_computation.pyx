import numpy as np
cimport numpy as np
cimport cython
from cython.view cimport array as cvarray
from libc.math cimport round
ctypedef unsigned char DTYPE_pixel
import scipy.fftpack as fft
from bitstring import BitStream

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef image_to_blocks (DTYPE_pixel [:, :] c1, DTYPE_pixel [:, :] c2, DTYPE_pixel [:, :] c3):
    # Try to write a c-style function that converts the image to an array of blocks
    # The function definition here create a typed MemoryViews for each color component c1, c2, c3

    cdef int v_mblocks = c1.shape[0] / 16
    cdef int h_mblocks = c1.shape[1] / 16
    cdef int total_mblocks = v_mblocks * h_mblocks
    cdef int total_blocks = total_mblocks * 6
    cdef int i, j, k
    cdef int row, col

    # allocate a cython array to store the blocks ("B" means unsigned char)
    blocks = cvarray(shape=(total_blocks, 8, 8), itemsize=sizeof(DTYPE_pixel), format="B")

    # create a cython MemoryView of the output array
    cdef DTYPE_pixel [:, :, :] blocks_view = blocks
    cdef DTYPE_pixel [:, :] tvc2
    cdef DTYPE_pixel [:, :] tvc3

    for i in range(0, total_blocks, 6):
        # This loop processes a single macroblock from c1, c2, and c3 in each iteration
        # The index i corresponds to the index of the block we store in output array, blocks

        # calculate the macroblock row and column
        # macroblocks can get obtained by slicing like c1[row*16: (row+1)*16, col*16: (col+1)*16]
        row = i/6 / h_mblocks
        col = i/6 % h_mblocks

        # blocks i, i+1, i+2, i+3 should be blocks from the c1 component.
        # note that we access c1 via a double slice. The first slice gets the macroblock, and
        #   the second slice like [:8, :8] gets the block
        blocks_view[i    , :, :] = (c1[row*16: (row+1)*16, col*16: (col+1)*16])[:8, :8]
        blocks_view[i + 1, :, :] = (c1[row*16: (row+1)*16, col*16: (col+1)*16])[:8, 8:]
        blocks_view[i + 2, :, :] = (c1[row*16: (row+1)*16, col*16: (col+1)*16])[8:, :8]
        blocks_view[i + 3, :, :] = (c1[row*16: (row+1)*16, col*16: (col+1)*16])[8:, 8:]

        # create temporary views of the current macroblock from components c2, c3
        # this serves only to make within-macroblock slicing a little cleaner in the next step
        tvc2 = c2[row*16: (row+1)*16, col*16: (col+1)*16]
        tvc3 = c3[row*16: (row+1)*16, col*16: (col+1)*16]

        # block i+4 is from c2, which we subsample from the current macroblock tvc2
        # similarly, block i+5 is from c3, subsampled from the current macroblock tvc3
        for j in range(8):
            for k in range(8):
                blocks_view[i + 4, j, k] = <DTYPE_pixel>round((<double>tvc2[j*2, k*2] + <double>tvc2[j*2 + 1, k*2] + <double>tvc2[j*2, k*2 + 1] + <double>tvc2[j*2 + 1, k*2 + 1])/4.0)
                blocks_view[i + 5, j, k] = <DTYPE_pixel>round((<double>tvc3[j*2, k*2] + <double>tvc3[j*2 + 1, k*2] + <double>tvc3[j*2, k*2 + 1] + <double>tvc3[j*2 + 1, k*2 + 1])/4.0)

    # Force numpy to create an ndarray object from our cython MemoryView. This avoids a copy.
    return np.asarray(blocks_view)

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef blocks_to_image(DTYPE_pixel[:, :, :] blocks, int v_mblocks, int h_mblocks):
    # Given an array of blocks like (x, 8, 8), reconstruct the original image
    # Return reconstructed in the form (image height, image width, 3)

    cdef int i, j, k, m
    cdef int fb

    # allocate cython array to store reconstructed image
    img = cvarray(shape=(v_mblocks*16, h_mblocks*16, 3), itemsize=sizeof(DTYPE_pixel), format="B")

    # create memoryview of the reconstructed image array
    cdef DTYPE_pixel [:, :, :] img_view = img

    # create temp memoryview for individual macroblocks
    cdef DTYPE_pixel [:, :] tvc1
    cdef DTYPE_pixel [:, :] tvc2
    cdef DTYPE_pixel [:, :] tvc3

    for i in range(v_mblocks):
        for j in range(h_mblocks):
            # This loop iterates over all macroblocks in the reconstructed image

            # get the index of the first block for the current macroblock
            # the sequential macroblock number is (i * h_mblocks + j)
            # so the first block for this macroblock starts at 6 * (i * h_mblocks + j)
            fb = 6 * (i * h_mblocks + j)

            # get a view of the c1 macroblock in the array we will eventually return
            tvc1 = img_view[i*16:(i+1)*16,j*16:(j+1)*16 , 0]

            # reconstruct the c1 macroblock from four blocks
            tvc1[:8, :8] = blocks[fb, :, :]
            tvc1[:8, 8:] = blocks[fb+1, :, :]
            tvc1[8:, :8] = blocks[fb+2, :, :]
            tvc1[8:, 8:] = blocks[fb+3, :, :]

            # get a view of the c2 and c3 macroblocks in the array we will eventually return
            tvc2 = img_view[i*16:(i+1)*16,j*16:(j+1)*16 , 1]
            tvc3 = img_view[i*16:(i+1)*16,j*16:(j+1)*16 , 2]

            # reconstruct the c2 macroblock from block fb+4 by blowing it up to macroblock size
            for k in range(8):
                for m in range(8):
                    tvc2[2*k:2*k+2, 2*m:2*m+2] = blocks[fb + 4, k , m]
                    tvc3[2*k:2*k+2, 2*m:2*m+2] = blocks[fb + 5, k , m]

    return np.asarray(img_view)

# Typed DCT functions. Not currently in use.
cpdef dct(np.ndarray[DTYPE_pixel, ndim=2] f):
    F=fft.dct(fft.dct(f, axis=0, norm='ortho', type=2), axis=1, norm='ortho', type=2)
    F[0,0]=F[0,0]/64.
    return fft.dct(fft.dct(f, axis=0, norm='ortho', type=2), axis=1, norm='ortho', type=2)

cpdef idct(np.ndarray[double, ndim=2] F):
    F[0,0]=F[0,0]*64
    return fft.idct(fft.idct(F, axis=0, norm='ortho', type=2), axis=1, norm='ortho', type=2)

# Sandbox

# Read entire bitstream one bit at a time
# 1.35e-5 seconds per bit
cpdef bitstream_test(bs):
    length = len(bs)
    while (bs.pos != length):
        bs.read('bin:1')

# Read bitstream 32 bits at a time
# 4.94e-7 seconds per bit
cpdef bitstream_test_2(bs):
    while bs.pos <= len(bs)-32:
        bs.read('bin:32')

# Read bitstream 64 bits at a time
#  seconds per bit
cpdef bitstream_test_3(bs):
    while bs.pos <= len(bs)-64:
        bs.read('bin:64')
