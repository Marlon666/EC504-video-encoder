import numpy as np
cimport numpy as np
cimport cython
ctypedef unsigned char DTYPE_pixel


cpdef np.ndarray[DTYPE_pixel, ndim=2] subsample (np.ndarray[DTYPE_pixel, ndim=2] block):
    cdef int i, j = 0

cpdef np.ndarray[DTYPE_pixel, ndim=3] image_to_mblocks(unsigned char[:, :] image_component):
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
    cdef int v_mblocks = image_component.shape[0] / 16
    cdef int h_mblocks = image_component.shape[1] / 16

    cdef np.ndarray[DTYPE_pixel, ndim=3] x = np.empty((v_mblocks*h_mblocks, 16, 16), dtype=np.uint8) # initializing at declaration seems to help a lot (as opposed to two separate steps)

    for j in range(h_mblocks):
        for i in range(v_mblocks):
            #x = np.append(x, [image_component[i * 16:(i + 1) * 16:, j * 16:(j + 1) * 16:]], axis=0)
            #pass
            # x[k] = np.array(image_component[i * 16:(i + 1) * 16:, j * 16:(j + 1) * 16:])
            x[k] = image_component[i * 16:(i + 1) * 16:, j * 16:(j + 1) * 16:]
            k += 1

    return x

    '''
    for j in range(h_mblocks):
        for i in range(v_mblocks):
            n = 0
            for l in range(i*16, (i+1)*16):
                o = 0
                for m in range(j*16, (j+1)*16):
                    x[k][n][o] = 1 #image_component[l][m]
                    o += 1
                o += 1
            n += 1
            k += 1
    return x
    '''