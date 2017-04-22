import proto_mpeg_x
import proto_mpeg
from bitstring import BitStream
import huffman_mpeg as codes
import proto_mpeg_computation
import numpy as np
import time

'''
# Test image_to_blocks

y = np.rint(np.random.rand(640, 480, 3)*10 + 150).astype(np.uint8)
frame = proto_mpeg.frame(y)
st = time.time()
frame.image_to_blocks()
en = time.time()
print("Took", en-st, "seconds to convert to blocks with CPython")

st = time.time()
proto_mpeg_computation.image_to_blocks_c(y[:, :, 0], y[:, :, 1], y[:, :, 2])
en = time.time()
print("Took", en-st, "seconds to convert to blocks with Cython")
'''

'''
Encode and save a single image
'''

# Get a single 640x480 image
print("Reading image.")
image = proto_mpeg_x.get_jpegs('../testing/480p-assorted/',1)[0]

# Create a frame object initialized with our image
print("Preparing image for encoding.")
frame = proto_mpeg_x.frame(image)

# Retreive the binary encoding of the image
output = frame.encode_to_bits()
print("Number of bits needed to represent image:", len(output))

# Append an end of frame character
output.append('0b' + codes.EOF)

# Write the frame to file
f = open('output.bin', 'wb')
output.tofile(f)
f.close()
del frame


'''
Decode and show the image
'''

# Open a BitStream from the file
f = open('output.bin', 'rb')
decoded_bits = BitStream(f)

# Read the stream up to the end of frame (EOF) character.
frame1bits = decoded_bits.readto('0b' + codes.EOF)[:-1*len(codes.EOF)]

# Create a frame object from the proto_mpeg library
frame = proto_mpeg.frame()

# Decode the bits and reconstruct the image
frame.decode_from_bits(frame1bits, 40, 30)

# View the image
frame.show()

f.close()
