import numpy as np
from os import listdir
import skimage.io
import matplotlib.pyplot as plt

class frame:
    def __init__(self, image):
        '''
        :param image: RBG image of shape (height, width, 3)
        '''
        self.r = image[:, :, 0]
        self.g = image[:, :, 1]
        self.b = image[:, :, 2]

    def show(self):
        reconstructed_image = np.dstack((self.r, self.g, self.b))
        plt.imshow(reconstructed_image)
        plt.show()

    def image_to_mblocks(self, image_component):
        """
        :param image_component: A SINGLE image component (for instance, 720x1080 red pixel component)
        :return: (x, 16, 16) array of macroblocks.
         The number of elements, x, in the first axis depends on the size of the image
         The second and third axes contain a 16x16 array (rows x cols) of pixel information
        """
        img_shape = np.shape(image_component)
        if (img_shape[0] % 16 != 0 or img_shape[1] % 16 != 0):
            raise Exception("Image dimensions", img_shape,
                            "not divisible by macroblock size. Someone tell the author to handle this.")

        v_mblocks = img_shape[0] // 16  # Note that // discards decimal pts. and returns an integer after divison
        h_mblocks = img_shape[1] // 16

        # Break the image into blocks
        # This uses array slicing and list comprehension. Not very pretty, but it works.
        x = image_component
        x = [x[i * 16:(i + 1) * 16:, j * 16:(j + 1) * 16:] for i in range(0, v_mblocks) for j in range(0, h_mblocks)]
        return x

    def mblocks_to_blocks(self, r_mblock, g_mblock, b_mblock):
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
        blocks = np.concatenate((blocks, self.subsample(g_mblock), self.subsample(b_mblock)), axis=0)

        return blocks

    def subsample(self, mblock):
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

    def un_subsample(self, block):
        """
        :param block: an (8x8) block that we wish to blow back up to (16,16)
        :return: a (16,16) macroblock color component
        """
        mblock = block
        for i in reversed(range(0,8)):
            mblock = np.insert(mblock, i, block[i], axis=0)
        for i in reversed(range(0,8)):
            mblock = np.insert(mblock, i, mblock[:,i], axis=1)
        return mblock

    def blocks_to_mblock(self, blocks):
        """
        :param blocks: (6, 8, 8) array of blocks that represent the data for a single macroblock:
        R0 R1
        R2 R3
        G4
        B5
        Where the letters represent the color component and the numbers represent the location in the first axis.
        :return: (3, 16, 16) array reconstructed R(0),G(1),B(2) macroblock. (axis is in parentheses)
        """
        # Build up red macroblock
        (h_blocks, v_blocks) = (2,2)
        r_mblock = np.vstack((
            np.hstack((blocks[j * h_blocks + i] for i in range(0, h_blocks)))
            for j in range(0, v_blocks)
        ))
        # Expand green and blue macroblocks
        g_mblock = self.un_subsample(blocks[4])
        b_mblock = self.un_subsample(blocks[5])

        return [r_mblock, g_mblock, b_mblock]

    def mblocks_to_image(self, mblocks, h_mblocks, v_mblocks):
        """
        :param mblocks: (x, 16, 16) array of macroblocks for a single color component that we want to turn back into an image

        :return: (h, w) shaped array of image color components
        """
        return np.vstack((
            np.hstack((mblocks[j * h_mblocks + i] for i in range(0, h_mblocks)))
            for j in range(0, v_mblocks)
        ))

    def image_to_blocks(self):
        pass

    def blocks_to_image(self):
        pass

def get_jpegs(directory, number):
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