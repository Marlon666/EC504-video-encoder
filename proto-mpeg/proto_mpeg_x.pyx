import numpy as np
from os import listdir
import skimage.io
import matplotlib.pyplot as plt
import dct_fast as dct
import huffman_mpeg
from bitstring import BitArray, BitStream, Bits
import ec504viewer
import proto_mpeg_computation

quant_intra=[[ 8, 16, 19, 22, 26, 27, 29, 34],
             [16, 16, 22, 24, 27, 29, 34, 37],
             [19, 22, 26, 27, 29, 34, 34, 38],
             [22, 22, 26, 27, 29, 34, 37, 40],
             [22, 26, 27, 29, 32, 35, 40, 48],
             [26, 27, 29, 32, 35, 40, 48, 58],
             [26, 27, 29, 34, 38, 46, 56, 69],
             [27, 29, 35, 38, 46, 56, 69, 83]]

# Zigzag order. Note that zigzag order != indicies.
zz_order = [[ 0,  1,  5,  6, 14, 15, 27, 28],
            [ 2,  4,  7, 13, 16, 26, 29, 42],
            [ 3,  8, 12, 17, 25, 30, 41, 43],
            [ 9, 11, 18, 24, 31, 40, 44, 53],
            [10, 19, 23, 32, 39, 45, 52, 54],
            [20, 22, 33, 38, 46, 51, 55, 60],
            [21, 34, 37, 47, 50, 56, 59, 61],
            [35, 36, 48, 49, 57, 58, 62, 63]]

# This is an array of indices that we use to sample a flattened DCT array in zigzag order.
zz_indices = [ 0,  1,  8, 16,  9,  2,  3, 10,
               17, 24, 32, 25, 18, 11, 4,  5,
               12, 19, 26, 33, 40, 48, 41, 34,
               27, 20, 13,  6,  7, 14, 21, 28,
               35, 42, 49, 56, 57, 50, 43, 36,
               29, 22, 15, 23, 30, 37, 44, 51,
               58, 59, 52, 45, 38, 31, 39, 46,
               53, 60, 61, 54, 47, 55, 62, 63]

zz_reverse_indices = [ 0,  1,  5,  6, 14, 15, 27, 28,
  2,  4,  7, 13, 16, 26, 29, 42,
  3,  8, 12, 17, 25, 30, 41, 43,
  9, 11, 18, 24, 31, 40, 44, 53,
 10, 19, 23, 32, 39, 45, 52, 54,
 20, 22, 33, 38, 46, 51, 55, 60,
 21, 34, 37, 47, 50, 56, 59, 61,
 35, 36, 48, 49, 57, 58, 62, 63]


class frame:
    def __init__(self, *image):
        '''
        :param image: RBG image of shape (height, width, 3)
        '''
        if len(image) == 1:
            data = image[0]
            self.r = data[:, :, 0]
            self.g = data[:, :, 1]
            self.b = data[:, :, 2]
            self.v_mblocks = np.shape(self.r)[0] // 16
            self.h_mblocks = np.shape(self.r)[1] // 16
        else:
            self.r = None
            self.g = None
            self.b = None
            self.v_mblocks = None
            self.h_mblocks = None
    def getFrame(self):
        reconstructed_image = np.dstack((self.r, self.g, self.b))
        return reconstructed_image
        
    def show(self):
        reconstructed_image = np.dstack((self.r, self.g, self.b))
        ec504viewer.view_single(reconstructed_image)

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
        )).astype(np.uint8)

    def image_to_blocks(self):
        """
        Convert the stored image into a sequence of 8x8 pixel blocks for encoding
        :return: (x, 8, 8) shaped array. x depends on dimensions of original image
        """
        # First create sequences of 16x16 pixel macroblocks
        r_mblocks = self.image_to_mblocks(self.r)
        g_mblocks = self.image_to_mblocks(self.g)
        b_mblocks = self.image_to_mblocks(self.b)

        # Now turn the macroblocks into a sequence of blocks
        # Each call to mblocks_to_blocks turns 3 macroblocks (RBG) into the block representation of a single macroblock.
        # Each mblocks_to_blocks call gives us a (6, 8, 8) shaped array
        num_macroblocks = np.shape(r_mblocks)[0]
        img_blocks = np.empty((0, 8, 8))
        for i in range(0, num_macroblocks):
            img_blocks = np.concatenate(
                (img_blocks, self.mblocks_to_blocks(r_mblocks[i], g_mblocks[i], b_mblocks[i])), axis=0)
        return img_blocks

    def blocks_to_image(self, blocks):
        """
        Given a sequence of blocks, reconstruct the original image. This routine relies on knowing the original dim.
        of the image through self.h_mblocks and self.h_vblocks
        :param blocks: a sequence of blocks that represent a single image
        :return: tuple of (r,g,b) color components of the image
        """
        # First, turn the blocks back into macroblocks
        recovered_r_mblocks = np.empty((0, 16, 16))
        recovered_g_mblocks = np.empty((0, 16, 16))
        recovered_b_mblocks = np.empty((0, 16, 16))
        num_macroblocks = np.shape(blocks)[0] // 6
        for i in range(0, num_macroblocks):
            [r, g, b] = self.blocks_to_mblock(blocks[i * 6:i * 6 + 7, :, :])
            recovered_r_mblocks = np.concatenate((recovered_r_mblocks, [r]), axis=0)
            recovered_g_mblocks = np.concatenate((recovered_g_mblocks, [g]), axis=0)
            recovered_b_mblocks = np.concatenate((recovered_b_mblocks, [b]), axis=0)
        # Second, turn the macroblocks back into an image
        r = self.mblocks_to_image(recovered_r_mblocks, self.h_mblocks, self.v_mblocks)
        g = self.mblocks_to_image(recovered_g_mblocks, self.h_mblocks, self.v_mblocks)
        b = self.mblocks_to_image(recovered_b_mblocks, self.h_mblocks, self.v_mblocks)
        return (r, g, b)

    def set_image(self, blocks):
        """
        Given a sequence of blocks (x, 8, 8), reconstruct the image and save it as my stored image
        :param blocks: Sequence of blocks that represent a single image
        :return: None
        """
        (self.r, self.g, self.b) = self.blocks_to_image(blocks)

    def quantize_intra(self, F):
        return np.rint(F/quant_intra).astype(np.int)

    def dequantize_intra(self, F):
        return F*quant_intra

    def zigzag_from_block(self, F):
        """
        Given a quantized 8x8 array of DCT coefficients, generate a string to encode the data
        :param F: array of quantized DCT coefficients, shape (8,8)
        :return: summary of DCT coefficients ready to be turned into bits
        """

        # First, we flatten the DCT array
        F = F.flatten()

        # Create a blank encoder string
        encoder_string = list()

        # Insert the DC value
        if F[0] < 0 or F[0] > 255:
            raise Warning("DC term " + str(F[0]) + " does not fit in uint8 format")
        encoder_string.append('uint:8=' + str(F[0]))

        # Insert a series of AC DCT coefficients in run/level format
        zero_count = 0
        for i in zz_indices[1:]:
            coeff = F[i]
            if coeff == 0:
                zero_count = zero_count + 1
            else:
                encoder_string.append((zero_count, coeff))
                zero_count = 0
        # Finally, append an EOB and return the result
        encoder_string.append('EOB')

        # ERROR CHECKING - DISABLE WHEN POSSIBLE
        min_length = 1  # set to 1 for DC term
        for (run, level) in encoder_string[1:-1]:
            #print(run, level)
            min_length = min_length + run + 1
        if min_length > 64:
            raise Exception("Attempted to encode too many bits from block\n", F, "\ninto a zigzag of\n", encoder_string)
        # END ERROR CHECKING

        return encoder_string

    def zigzag_to_block(self, zz):
        """
        :param zz: List of decoded entries that describe a block of data
        :return: 8x8 block of pixels
        """
        # Create a flattened array to reconstruct the data
        block = np.zeros((64,))

        # Insert the DC term
        block[0] = zz[0]

        # Insert the AC terms
        index = 0
        for i in range(1, len(zz)-1):
            # print("processing run, level", zz[i])
            run = zz[i][0]
            level = zz[i][1]
            index = index + run + 1
            # print("base index is", index)
            # print("zz_index is", zz_indices[index])

            block[zz_indices[index]] = level
            # print("block is now after insert:\n", block)
            #block[index] = level

        # Turn back into a 2d array and return
        return np.reshape(block, (8,8)).astype(np.int)

    def zigzag_to_bits(self, encoder_table, zz):

        # Encode the DC term into a BitArray
        encoded_bits = BitArray(zz[0])

        # Encode the AC terms
        for i in range(1, len(zz) - 1):
            run_level = zz[i]
            run_level_positive = tuple(map(abs, run_level))

            if run_level_positive in encoder_table:
                # Note only positive levels are stored in encoder table.
                encoded_bits.append(encoder_table[run_level_positive])
                # Check to see if the level is negative, write appropriate sign bit.
                if run_level[1] < 0:
                    # Level is negative, so we will write a sign bit of 1
                    encoded_bits.append('0b1')
                else:
                    # Level is positive, so we will write a sign bit of 0
                    encoded_bits.append('0b0')
            else:
                # The run_level combo was not fond in the encoder table. We will do the following:
                # i) encode an escape character
                # ii) encode a 6-bit unsigned integer for the run, which is at most 62
                # iii) encode a 16-bit signed integer for the level
                encoded_bits.append(encoder_table['ESC'])
                run = 'uint:6=' + str(run_level[0])
                level = 'int:16=' + str(run_level[1])
                encoded_bits.append(run)
                encoded_bits.append(level)

        # Encode the EOB term
        encoded_bits.append(encoder_table['EOB'])

        return encoded_bits

    def encode_to_bits(self):
        """
        Encode the stored image data into a bitstream. The calling function is responsible for writing start and
        end codes to the file to delineate different frames.
        :return: BitArray representation
        """
        img_blocks = self.image_to_blocks()
        total_blocks = np.shape(img_blocks)[0]
        print("Beginning encoding for", total_blocks, "blocks.")

        # Get the encoder table for converting (run, level) codes into bits
        encoder_table = huffman_mpeg.make_encoder_table()

        # Create a BitArray that will hold all encoded bits
        output = BitArray()

        # Counter and checkpoints used to provide % complete
        i = 0
        #checkpoints = set(np.rint(np.linspace(0, total_blocks, 11, endpoint=True)))

        for block in img_blocks:

            # Give progress update
            '''
            if i in checkpoints:
                print(int(i/total_blocks*100), '%')
            '''

            # First, we create a zig-zag summary for the block after DCT and quantization
            zz = self.zigzag_from_block(self.quantize_intra(dct.dct(block)))

            # Then, we convert that zig-zag summary into a stream of bits
            output.append(self.zigzag_to_bits(encoder_table, zz))

            i = i + 1

        return output

    def decode_from_bits(self, bits, h_mblocks, v_mblocks):

        # Get the decoder table for converting Bits into (run, level)
        decoder_table = huffman_mpeg.make_decoder_table()

        total_bits = len(bits)
        total_blocks = h_mblocks*v_mblocks*6 # Because there are 6 blocks to every macroblock

        print("Beginning decoding for", total_blocks, "blocks.")

        # This is the array we'll send to self.image_to_blocks after we've processed all bits
        blocks = np.empty((0, 8, 8))

        # As we decode bits, we will use this list to summarize one 8x8 block at a time.
        decoded_zz_summary = list()

        # Counter and checkpoints used to provide % complete
        j = 0
        #checkpoints = set(np.rint(np.linspace(0, total_blocks, 11, endpoint=True)))

        # Loop through remainder of data, until we reach the end
        i = 1
        while (bits.pos != total_bits):
            # If the zigzag summary is empty, we first need to read a DC term
            if len(decoded_zz_summary) == 0:
                decoded_zz_summary.append(bits.read('uint:8'))
            # Note: i is the number of bits to peek/read, beginning at decoded_bits.pos
            bit_string = Bits('0b' + bits.peek('bin:' + str(i)))
            # print("Testing bit string:", bit_string.bin)
            if bit_string in decoder_table:
                data = decoder_table[bit_string]
                # print("Found", data, "in decoder table with data =", data)
                if data == 'ESC':
                    # A 6-bit run and a 16-bit signed int is stored immediately after this ESC charater
                    # throw away the escape character
                    bits.read('bin:' + str(i))
                    # read the run (6 bit unsigned int) and the level (16-bit signed int)
                    run = bits.read('uint:6')
                    level = bits.read('int:16')
                    decoded_zz_summary.append((run, level))
                    # print("Handled escape character and appended run, level", (run, level))
                elif data == 'EOB':
                    # Throw away the EOB character, then append an EOB to our decoded zigzag summary of a single block
                    bits.read('bin:' + str(i))
                    decoded_zz_summary.append(data)

                    # Reconstruct a block from our completed zz summary, dequantize it, perform IDCT, store it
                    blocks = np.append(blocks, [np.rint(
                        dct.idct(self.dequantize_intra(self.zigzag_to_block(decoded_zz_summary)).astype(float))).astype(np.uint8)], axis=0)

                    # Reset the zigzag summary so that the next thing we do is read a DC term
                    decoded_zz_summary = list()

                    # Give a progress update
                    '''
                    if j in checkpoints:
                        print(int(j / total_blocks * 100), '%')
                    j = j + 1
                    '''
                else:
                    # We have a run, level pair. We read i + 1 bits so that we grab the trailing sign bit.
                    bits_read = bits.read('bin:' + str(i + 1))
                    # print("Read bits", bits_read)
                    if bits_read[-1] == '1':
                        # Sign bit is negative
                        data = (data[0], data[1] * -1)
                    decoded_zz_summary.append(data)
                # In all cases, we do a read and need to reset the peek distance
                i = 1
            else:
                # The bits we've peeked at don't match anything in the decoder table. Include one more bit in the search.
                i = i + 1
                # print("Length and position:", len(decoded_bits), decoded_bits.pos)
                if i + bits.pos > len(bits):
                    raise Exception("Attempted to read beyond end of bitstring during AC decoding.")

        # Reconstruct an image from our decoded blocks, and store it.
        self.h_mblocks = h_mblocks
        self.v_mblocks = v_mblocks
        self.set_image(blocks)

def get_jpegs(directory, number):
    images = []
    i = 1
    for file in sorted(listdir(directory)):
        if file.endswith('.jpg'):
            images.append(skimage.io.imread(directory + '/' + file))
        if i == number:
            break
        i=i+1
    return images
