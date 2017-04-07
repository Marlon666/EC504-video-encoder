import bitstring
import proto_mpeg
import numpy as np
import matplotlib.pyplot as plt

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
Continuing development...
'''

# Load a saved tblock to avoid overhead
test_block = np.loadtxt('testblock.txt')

# Run DCT and quantization on a single block
test_block_dctq = proto_mpeg.dct(test_block)
test_block_dctq = proto_mpeg.quantize_intra(test_block_dctq)

# Reduce DCT block down to zigzag summary
zz_summary = proto_mpeg.zigzag_block(test_block_dctq)
print(zz_summary)
# Convert zigzag summary into bitstream



