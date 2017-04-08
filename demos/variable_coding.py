from bitstring import BitArray, BitStream
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
        sign_bit = '0b1'
    if run_level in encoder_table:
        encoded_bits.append(run_level)
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

f = open('encode_test.bin', 'rb')
decoded_bits = BitStream(f)
print(decoded_bits.bin)


