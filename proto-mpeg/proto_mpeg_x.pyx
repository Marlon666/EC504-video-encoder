import numpy as np
from os import listdir
import color_convert
import skimage.io
import matplotlib.pyplot as plt
#import dct_fast as dct
import proto_mpeg_computation as dct
import huffman_mpeg
from bitstring import BitArray, BitStream, Bits, ReadError
import proto_mpeg_computation
import time
import matplotlib as mpl
# import queue commend

ycbcr=True

quant_intra=np.array([[ 1, 16, 19, 22, 26, 27, 29, 34],
             [16, 16, 22, 24, 27, 29, 34, 37],
             [19, 22, 26, 27, 29, 34, 34, 38],
             [22, 22, 26, 27, 29, 34, 37, 40],
             [22, 26, 27, 29, 32, 35, 40, 48],
             [26, 27, 29, 32, 35, 40, 48, 58],
             [26, 27, 29, 34, 38, 46, 56, 69],
             [27, 29, 35, 38, 46, 56, 69, 83]])

# This is an array of indices that we use to sample a flattened DCT array in zigzag order.
zz_indices = [ 0,  1,  8, 16,  9,  2,  3, 10,
               17, 24, 32, 25, 18, 11, 4,  5,
               12, 19, 26, 33, 40, 48, 41, 34,
               27, 20, 13,  6,  7, 14, 21, 28,
               35, 42, 49, 56, 57, 50, 43, 36,
               29, 22, 15, 23, 30, 37, 44, 51,
               58, 59, 52, 45, 38, 31, 39, 46,
               53, 60, 61, 54, 47, 55, 62, 63]

class frame:
    def __init__(self, *image, QF=1):
        '''
        :param image: RBG image of shape (height, width, 3)
        '''
        self.QF=QF
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

    def load_from_file(self, path):
        image = skimage.io.imread(path)
        self.r = image[:, :, 0]
        self.g = image[:, :, 1]
        self.b = image[:, :, 2]
        self.v_mblocks = np.shape(self.r)[0] // 16
        self.h_mblocks = np.shape(self.r)[1] // 16
        
    def show(self):
        reconstructed_image = np.dstack((self.r, self.g, self.b))
        #ec504viewer.view_single(reconstructed_image)

    def image_to_blocks(self):
        """
        Convert the stored image into a sequence of 8x8 pixel blocks for encoding
        :return: (x, 8, 8) shaped array. x depends on dimensions of original image
        """
        return proto_mpeg_computation.image_to_blocks(self.r, self.g, self.b)

    def blocks_to_image(self, blocks):
        """
        Given a sequence of blocks, reconstruct the original image. This routine relies on knowing the original dim.
        of the image through self.h_mblocks and self.h_vblocks
        :param blocks: a sequence of blocks that represent a single image
        :return: tuple of (r,g,b) color components of the image
        """

        # TODO: Investigate why this function gets floats instead of uint8s from the decoder
        return proto_mpeg_computation.blocks_to_image(blocks.astype(np.uint8), self.v_mblocks, self.h_mblocks)

    def set_image(self, blocks):
        """
        Given a sequence of blocks (x, 8, 8), reconstruct the image and save it as my stored image
        :param blocks: Sequence of blocks that represent a single image
        :return: None
        """
        #print("type seen by set_image function:", type(blocks[0, 0, 0]))
        image = self.blocks_to_image(blocks)
        (self.r, self.g, self.b) = (image[:, :, 0], image[:, :, 1], image[:, :, 2])
        # (self.r, self.g, self.b) = self.blocks_to_image(blocks)

    def quantize_intra(self, F):
        quant_matrix=np.ceil(quant_intra*self.QF)
        quant_matrix[quant_matrix>255]=255
        return np.rint(F/quant_matrix).astype(np.int)

    def dequantize_intra(self, F):
        quant_matrix=np.ceil(quant_intra*self.QF)
        quant_matrix[quant_matrix>255]=255
        return F*quant_matrix

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
        #print("Beginning encoding for", total_blocks, "blocks.")

        # Get the encoder table for converting (run, level) codes into bits
        encoder_table = huffman_mpeg.make_encoder_table()

        # Create a BitArray that will hold all encoded bits
        output = BitArray()

        # Counter and checkpoints used to provide % complete
        i = 0
        #checkpoints = set(np.rint(np.linspace(0, total_blocks, 11, endpoint=True)))

        for block in img_blocks:

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

        #print("Beginning decoding for", total_blocks, "blocks.")

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
                    bl_recon = np.rint(dct.idct(self.dequantize_intra(self.zigzag_to_block(decoded_zz_summary)).astype(float)))
                    bl_recon[bl_recon<0]=0
                    bl_recon[bl_recon>255]=255
                    blocks = np.append(blocks, [bl_recon.astype(np.uint8)], axis=0)

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
        #self.h_mblocks = h_mblocks
        #self.v_mblocks = v_mblocks
        #self.set_image(blocks)
        img=proto_mpeg_computation.blocks_to_image(blocks.astype(np.uint8), v_mblocks, h_mblocks)
        if(ycbcr):
            img=color_convert.ycbcr2rgb(img).astype(np.uint8)
        return proto_mpeg_computation.blocks_to_image(blocks.astype(np.uint8), v_mblocks, h_mblocks)

def get_jpegs(directory, number):
    images = []
    i = 1
    for file in sorted(listdir(directory)):
        if file.endswith('.jpg'):
            img=skimage.io.imread(directory + '/' + file)
            if(ycbcr):
                img=color_convert.rgb2ycbcr(img.astype(float))
            images.append(img)
        if i == number:
            break
        i=i+1
    return images

def encode_video_old(files, output_file, compression_level): # queue):
    """
    Given a list of files, encode them into output_file with compression_level
    :param files: 
    :param output_file: 
    :param compression_level: 
    :return: None
    """

    # Open output file
    try:
        f = open(output_file, 'wb')
    except:
        raise Exception("Could not open output file", output_file, "for writing.")

    # Get a frame object
    img = frame()

    # Create output bit array
    output = BitArray()

    i = 1

    for path in files:
        # Load an image
        img.load_from_file(path)
        # Append the encoded bits to the output
        output.append(img.encode_to_bits())
        # Append an end of frame character
        output.append('0b' + huffman_mpeg.EOF)

        print("File", i, "of", len(files), "encoded.")
        i += 1

        # queue.put(100/len(files))


    # WRITE HEADER
    # v_mblocks and h_mblocks will be encoded as 8-bit unsigned integers
    output.prepend('uint:8=' + str(img.h_mblocks))
    output.prepend('uint:8=' + str(img.v_mblocks))
    # number of images written as 20-bit unsigned integer
    output.prepend('uint:20=' + str(len(files)))

    output.tofile(f)
    f.close()


def decode_video_old(file):
    """
    :param file: 
    :return: (height, width, 3, x) series of x images
    """

    # Open a BitStream from the file
    try:
        f = open(file, 'rb')
    except:
        raise Exception("Could not open input file", file, "for reading.")

    decoder_bits = BitStream(f)

    # READ HEADER
    num_imgs  = decoder_bits.read('uint:20')
    v_mblocks = decoder_bits.read('uint:8')
    h_mblocks = decoder_bits.read('uint:8')

    video = np.empty((v_mblocks*16, h_mblocks*16, 3, num_imgs), dtype=np.uint8)

    img = frame()

    for i in range(num_imgs):

        this_image_bits = decoder_bits.readto('0b' + huffman_mpeg.EOF)[:-1*len(huffman_mpeg.EOF)]
        video[:, :, :, i] = img.decode_from_bits(this_image_bits, h_mblocks, v_mblocks)
        print("decoded", i+1, "out of", num_imgs, "images")
        print(decoder_bits.pos, len(decoder_bits))

    f.close()

    return video


import huffman_mpeg as codes
import motion as mot

def convert2uint8(arr):
    arr[arr<0]=0
    arr[arr>255]=255
    return arr.astype(np.uint8)
def encodeMot(mot_vec,nbits):
    print(mot_vec.shape)
    out=BitArray()
    mot_vec=mot_vec.reshape([-1])
    for k in range(len(mot_vec)):
        out.append('0b'+np.binary_repr(mot_vec[k],width=nbits))
    print(len(out))
    return out

def decodeMot(mot_bin,nbits,w,l):
    print(w*l*2)
    print(len(mot_bin))
    mot_vec = np.zeros(w*l*2)
    for k in range(len(mot_vec)):
        mot_vec[k]=mot_bin[k*nbits:(k+1)*nbits].uint
    return mot_vec.reshape([w,l,2]).astype(int)

def encodeVideo(outname,files,mot_est='none',mot_clip=100,Ssize=7,QF=1):
    """
    Given list of files encode them into a single file
    Inputs
    outname(string):name of the output file
    files(list): list of image directions to be encoded
    mot_est(string): Algorithm to use in motion estimation. Chose from following three
                        -'none'
                        -'frame_difference'
                        -'block_matching'
    mot_clip(int): Value used for clipping the motion pixels
    Ssize(int): Size of the search window for 'block_matching'. Probably we wont need to change it
    QF(float): Compression factor
    """

    # Assign an integer ID to each type of motion encoding, to be written in the file header
    if(mot_est=='none'):
        # No motion estimation. Only I-frames are encoded.
        mot_code=0
    elif(mot_est=='frame_difference'):
        # Encode repetitions of one I frame and three P frames
        mot_code=1
    elif(mot_est=='block_matching'):
        # Use block matching motion estimation
        mot_code=2
    else:
        mot_code=0
        print("Invalid motion coded provided. Defaulting to I-frame encoding.")

    start=time.time()
    images = []
    for path in files:
        images.append(skimage.io.imread(path))

    output=BitArray()
    # Create a frame object initialized with our image
    print("Encoding image-1")
    t=time.time()
    fr = frame(images[0],QF=QF)
    # Retreive the binary encoding of the image
    output.append(fr.encode_to_bits())
    # Append an end of frame character
    output.append('0b' + codes.EOF)
    print(str(time.time()-t)+' seconds')

    for k in range(1,len(images)):
        # Create a frame object initialized with our image
        print("Encoding image-"+str(k+1))
        t=time.time()
        if(mot_est=='none' or np.mod(k,4)==0):
            code=images[k]
        else:
            if(mot_est=='frame_difference'):
                err=images[k].astype(int)-images[k-1].astype(int)
            elif(mot_est=='block_matching'):
                mot_vec,err = mot.blockMatching(images[k-1],images[k],Bsize=8,Ssize=Ssize)
            err[err<-mot_clip]=-mot_clip
            err[err>mot_clip]=mot_clip
            code=convert2uint8(err+mot_clip)#.astype(np.uint8)
        fr = frame(code,QF=QF)
        # Retreive the binary encoding of the image
        output.append(fr.encode_to_bits())
        output.append('0b' + codes.EOF)

        if(mot_est=='block_matching' and np.mod(k,4)!=0):
            mot_vec = mot_vec+Ssize
            nbits = int(np.ceil(np.log2(2*Ssize+1)))
            mot_bin=encodeMot(mot_vec,nbits)
            output.append(mot_bin)
            output.append('0b' + codes.EOF)
            # Append an end of frame character
        print(str(time.time()-t)+' seconds')

    # BUILD HEADER

    # v_mblocks and h_mblocks will be encoded as 8-bit unsigned integers
    output.prepend('uint:8=' + str(fr.h_mblocks))
    output.prepend('uint:8=' + str(fr.v_mblocks))

    # number of images written as 20-bit unsigned integer
    output.prepend('uint:20=' + str(len(files)))

    # include all motion encoding parameters
    output.prepend('uint:2='+str(mot_code))
    output.prepend('uint:8='+str(mot_clip))
    output.prepend('uint:4='+str(Ssize))
    output.prepend('float:32='+str(QF))

    # Write file
    with open(outname, 'wb') as f:
        output.tofile(f)

    print('Encode time for one frame is %.3f seconds'%((time.time()-start)/(len(images))))

def playVideo(fname, realTime=True, delay=1):
    ''' 
    Plays the encoded file from fname
    Inputs
    fname(string): Path of the encoded binary file
    realTime(boolean):	If True, show each frame after decoding
        If Flase, first decode all frames than show time 
    delay(float): time between showing consecutive frames. It is used only if realTime=True
    '''
    start=time.time()
    f = open(fname, 'rb')
    decoded_bits = BitStream(f)
    QF=decoded_bits.read('float:32')
    Ssize=decoded_bits.read('uint:4')
    mot_clip=decoded_bits.read('uint:8')
    mot_code=decoded_bits.read('uint:2')
    num_imgs  = decoded_bits.read('uint:20')
    v_mblocks = decoded_bits.read('uint:8')
    h_mblocks = decoded_bits.read('uint:8')

    '''
    plt.ion()
    ax = plt.gca()
    ax.axis('off')
    fig = plt.gcf()
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.canvas.set_window_title("EC504 Viewer")
    plt.pause(.001)
    '''
    # New setup
    mpl.rcParams['toolbar'] = 'None'
    fig, ax = plt.subplots(1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.canvas.set_window_title("EC504 Viewer")
    im = ax.imshow(np.zeros((256, 256, 3)), extent=(0, 1, 1, 0))
    ax.axis('tight')
    ax.axis('off')
    fig.set_size_inches(8, v_mblocks/h_mblocks*8, forward=True) # This makes sure we get the aspect ratio correct
    fig.show()


    k=0
    prev_image=mot_clip*np.ones([v_mblocks*16,h_mblocks*16,3]).astype(np.uint8)
    frames=list()
    while(True):
        # Read the stream up to the end of frame (EOF) character.
        try:
            framebits = decoded_bits.readto('0b' + codes.EOF)[:-1*len(codes.EOF)]
        except ReadError:
            break
        print("Decoding image-"+str(k))
        t=time.time()
        # Create a frame object from the proto_mpeg library
        fr = frame(QF=QF)
        # Decode the bits and reconstruct the image
        code = fr.decode_from_bits(framebits, h_mblocks, v_mblocks)
        if(mot_code==0 or np.mod(k,4)==0):
            image=code
            prev_image=image
        elif(mot_code==1):
            image=convert2uint8(prev_image.astype(int)+code.astype(int)-mot_clip)
            prev_image=image
        elif(mot_code==2):
            if(k==0):
                image=code
            else:
                nbits = int(np.ceil(np.log2(2*Ssize+1)))
                motbits = decoded_bits.read(v_mblocks*h_mblocks*8*nbits)
                tmp = decoded_bits.readto('0b' + codes.EOF)
                mot_arr=decodeMot(motbits,nbits,v_mblocks*2, h_mblocks*2)-Ssize
                prev_image_w=mot.wrap(prev_image,mot_arr)
                image=convert2uint8(prev_image_w.astype(int)-code.astype(int)+mot_clip)
            prev_image=image
        print(str(time.time()-t)+' seconds')
        if(realTime):
            im.set_data(image)
            im.axes.figure.canvas.draw()

            #plt.imshow(image, extent=(0, 1, 1, 0))
            #plt.draw()
            #plt.pause(.001)
        else:
            frames.append(image)
        del fr
        k+=1
    f.close()
    print('Decode time for one frame is %.3f seconds'%((time.time()-start)/k))

    if(not realTime):
        for k in range(len(frames)):
            image=frames[k]
            '''
            plt.imshow(image, extent=(0, 1, 1, 0))
            plt.draw()
            plt.pause(delay)
            '''
            im.set_data(image)
            im.axes.figure.canvas.draw()
            time.sleep(delay)
    input("Press [enter] to continue.")