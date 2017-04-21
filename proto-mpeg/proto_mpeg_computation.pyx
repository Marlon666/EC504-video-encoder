import numpy as np
cimport numpy as np
cimport cython
ctypedef unsigned char DTYPE_pixel



#cpdef image_to_mblocks(unsigned char[:, :] image_component, int v_mblocks, int h_mblocks):
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef image_to_mblocks(np.ndarray[DTYPE_pixel, ndim=2] image_component, int v_mblocks, int h_mblocks):
    """
    :param image_component: A SINGLE image component (for instance, 720x1080 red pixel component)
    :return: (x, 16, 16) array of macroblocks.
     The number of elements, x, in the first axis depends on the size of the image
     The second and third axes contain a 16x16 array (rows x cols) of pixel information
    """
    # Need to type all variables for cython to work optimally
    cdef int i
    cdef int j
    cdef int k = 0
    cdef int l, m
    cdef int n, o
    #cdef int v_mblocks = image_component.shape[0] / 16
    #cdef int h_mblocks = image_component.shape[1] / 16

    # cdef np.ndarray[DTYPE_pixel, ndim=3] x = np.empty((v_mblocks*h_mblocks, 16, 16), dtype=np.uint8) # initializing at declaration seems to help a lot (as opposed to two separate steps)

    # print(image_component.shape)
    '''
    for j in range(h_mblocks):
        for i in range(v_mblocks):
            #x = np.append(x, [image_component[i * 16:(i + 1) * 16:, j * 16:(j + 1) * 16:]], axis=0)
            #pass
            # x[k] = np.array(image_component[i * 16:(i + 1) * 16:, j * 16:(j + 1) * 16:])
            x[k] = image_component[i * 16:(i + 1) * 16:, j * 16:(j + 1) * 16:]
            k += 1

    return x
    '''
    return [image_component[i * 16:(i + 1) * 16:, j * 16:(j + 1) * 16:] for i in range(0, v_mblocks) for j in range(0, h_mblocks)]


cdef subsample(unsigned char[:, :] mblock):
    '''
    :param mblock: a (16,16) macroblock color component that we wish to average down to an (8x8)
    :return: (1,8,8) subsampled block
    From the inside out, this call function does the following:
        The list comprehension grabs (4,4) subarrays one at a time from the mblock
        We call np.mean on each (4,4) subarray
        The list comprehension produces a flattened array of shape (64,)
        The np.reshape turns the flattened array into shape (8,8)
        Np.rint rounds all numbers to the closest integer and .astype(np.unint8) does the actual conversion to ints
    '''
    return [np.rint(np.reshape(
        [np.mean(mblock[2 * i:2 * i + 2:, 2 * j:2 * j + 2:]) for i in range(0, 8) for j in range(0, 8)],
        (8, 8))).astype(np.uint8)]

cdef mblocks_to_blocks(r_mblock, g_mblock, b_mblock):
        '''
        :param r_mblock: 16x16 array of red pixels
        :param g_mblock: 16x16 array of green pixels
        :param b_mblock: 16x16 array of blue pixels
        :return: (6, 8, 8) array of blocks that contain data for a SINGLE macroblock
        R0 R1
        R2 R3
        G4
        B5
        '''

        # Break the r_mblock into 4 blocks
        blocks = [r_mblock[i * 8:(i + 1) * 8:, j * 8:(j + 1) * 8:] for i in range(0, 2) for j in range(0, 2)]

        # Subsample the green and blue macroblocks and append them to the array
        blocks = np.concatenate((blocks, subsample(g_mblock), subsample(b_mblock)), axis=0)

        return blocks

cpdef np.ndarray[DTYPE_pixel, ndim=3] image_to_blocks(unsigned char[:, :, :] image):

    cdef int v_mblocks = image[0].shape[0] / 16
    cdef int h_mblocks = image[0].shape[1] / 16
    cdef int total_mblocks = v_mblocks * h_mblocks
    cdef int i

    # Create array that will be returned
    cdef np.ndarray[DTYPE_pixel, ndim = 3] blocks = np.empty((total_mblocks * 6, 8, 8), dtype=np.uint8)

    # Convert each component to macroblocks

    cdef np.ndarray[DTYPE_pixel, ndim=3] r_mblocks = image_to_mblocks(image[0], v_mblocks, h_mblocks)
    cdef np.ndarray[DTYPE_pixel, ndim=3] g_mblocks = image_to_mblocks(image[1], v_mblocks, h_mblocks)
    cdef np.ndarray[DTYPE_pixel, ndim=3] b_mblocks = image_to_mblocks(image[2], v_mblocks, h_mblocks)

    # For each set of macroblocks:
    for i in range(total_mblocks):

        # Break image[0] (red or Y) into four blocks
        # Subsample image[1] and image[2] to get two blocks
        # Append results
        blocks[i*6:(i+1)*6, :, :] = mblocks_to_blocks(r_mblocks[i], g_mblocks[i], b_mblocks[i])

    return blocks