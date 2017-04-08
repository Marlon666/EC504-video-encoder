from bitstring import BitArray, BitStream, Bits
import proto_mpeg
import numpy as np
import matplotlib.pyplot as plt
import huffman_mpeg

'''
OVERVIEW
The purpose of this file is to show how to manipulate images with an early version of the proto_mpeg library.
We can turn an RBG image into a series of MPEG-style "blocks" that will go through DCT, quantization, and encoding into
a bit stream.
We then take a single block, do the aforementioned processing, encode it using huffman codes, and then decode it.
'''

'''
# Load a single image
image = proto_mpeg.get_jpegs('../testing/720p-10/',1)[0]

# Create a proto_mpeg.frame image object
test_image = proto_mpeg.frame(image)

# Use the image object to create a sequence of blocks for encoding
img_blocks = test_image.image_to_blocks()

np.savetxt('testblock.txt', img_blocks[0])
'''

'''
Encode a block
'''

# Load a saved block to avoid overhead.
test_block = np.loadtxt('testblock.txt')

# Run DCT and quantization on a single block
test_block_dctq = proto_mpeg.dct(test_block)
test_block_dctq = proto_mpeg.quantize_intra(test_block_dctq)
print("Original quantized block:\n", test_block_dctq)

# Reduce DCT block down to zigzag summary
zz_summary = proto_mpeg.zigzag_block(test_block_dctq)
print("Summary to encode:", zz_summary)

# Get the encoder table for converting (run, level) codes into bits
encoder_table = huffman_mpeg.make_encoder_table()

# Encode the DC term into a BitArray
encoded_bits = BitArray(zz_summary[0])
print("Encoded bits after adding DC term:", encoded_bits.bin)

# Encode the AC terms
for i in range(1, len(zz_summary)-1):
    run_level = zz_summary[i]
    # Check to see if the level is negative. Note only positive levels are stored in encoder table.
    if run_level[1] < 0:
        run_level = tuple(map(abs, run_level))
        # Level is negative, so we will write a sign bit of 1
        sign_bit = '0b1'
    else:
        # Level is positive, so we will write a sign bit of 0
        sign_bit = '0b0'
    if run_level in encoder_table:
        encoded_bits.append(encoder_table[run_level])
        encoded_bits.append(sign_bit)
    else:
        print("Warning. Tuple", zz_summary[i] ,"not found in encoder table.")

print("Encoded bits after adding AC terms:", encoded_bits.bin)

# Encode the EOB term
encoded_bits.append(encoder_table['EOB'])
print("Encoded bits after adding EOB term:", encoded_bits.bin)

# Write the binary data to file. NOTE: This routine will zero-pad the end of the array to write a whole # of bytes.
f = open('encode_test.bin', 'wb')
encoded_bits.tofile(f)
f.close()

'''
Decode the block
'''

# Get the decoder table for converting Bits into (run, level)
decoder_table = huffman_mpeg.make_decoder_table()

f = open('encode_test.bin', 'rb')
decoded_bits = BitStream(f)

# Read DC term
decoded_zz_summary = list()
decoded_zz_summary.append(decoded_bits.read('uint:8'))

# Read up to EOB, giving us a bit string of encoded AC data followed by an EOB character
AC_string = decoded_bits.readto(encoder_table['EOB'])

# Loop through AC data and extract a zigzag summary
bit_string = str()
for i in range(1, len(AC_string)-2): # Why -2? There is an EOB and a sign bit at the end that we don't need to peek at.
    bit_string = Bits('0b' + AC_string.peek('bin:' +  str(i)))
    # print("Testing bit string:", bit_string.bin)
    if bit_string in decoder_table:
        run_level = decoder_table[bit_string]
        if run_level != 'ESC':
            print("Found", bit_string, "in decoder table with (run,level) =", run_level)
            bit_string = AC_string.read('bin:' + str(i+1))
            # print("Final read bit string:", bit_string)
            if (bit_string[-1]) == '1':
                # The sign bit is negative, so we need to change the sign of the level
                run_level = (run_level[0], run_level[1]*-1)
                decoded_zz_summary.append(run_level)
        else:
            pass
            # We have an escape character, and need to read the bits directly

# Finally, append the EOB character
decoded_zz_summary.append('EOB')

print("Decoded zigag summary:", decoded_zz_summary)

# Turn the zig-zag summary back into a bock
print(proto_mpeg.zigzag_to_block(decoded_zz_summary))

