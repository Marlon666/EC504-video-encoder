import numpy as np
cimport numpy as np
cimport cython
from cython.view cimport array as cvarray
from libc.math cimport round
ctypedef unsigned char DTYPE_pixel

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

cpdef blocks_to_image(DTYPE_pixel[:, :, :] blocks, int v_mblocks, int h_mblocks):
    # Given an array of blocks like (x, 8, 8), reconstruct the original image
    # Return reconstructed in the form (image height, image width, 3)
    pass