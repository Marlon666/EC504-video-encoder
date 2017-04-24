import proto_mpeg_x
import proto_mpeg
from bitstring import BitStream
import huffman_mpeg as codes
import proto_mpeg_computation
import numpy as np
import time
from os import listdir
import ec504viewer

'''
Test multi-file encoding
'''
img_directory = '../testing/720p-10/'
filenames = sorted(listdir(img_directory))
#print(sorted(listdir(img_directory)))
files = [img_directory + fname for fname in filenames]
#print(files)

proto_mpeg_x.encode_video(files[0:3], 'video.bin', 1)

'''
Test multi-file decoding
'''
video = proto_mpeg_x.decode_video('video.bin')
print(np.shape(video))

ec504viewer.view_single(video[:, :, :, 0].astype(np.uint8))
ec504viewer.view_single(video[:, :, :, 1])
ec504viewer.view_single(video[:, :, :, 2])

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
# Test blocks_to_image

z = np.rint(np.random.rand(480, 640, 3)*10 + 145).astype(np.uint8)
v_mblocks = np.shape(z[:, :, 0])[0] // 16
h_mblocks = np.shape(z[:, :, 0])[1] // 16

(c1, c2, c3) = (z[:, :, 0], z[:, :, 1], z[:, :, 1])
blocks = proto_mpeg_computation.image_to_blocks(c1, c2, c3)

# Test original python implementation
frame = proto_mpeg.frame()
frame.v_mblocks = v_mblocks
frame.h_mblocks = h_mblocks

st = time.time()
frame.blocks_to_image(blocks)
en = time.time()
print("Image reconstruction took", en-st, "seconds with CPython")

# Test cython
st = time.time()
reconstructed_image = proto_mpeg_computation.blocks_to_image(blocks, v_mblocks, h_mblocks)
en = time.time()
print("Image reconstruction took", en-st, "seconds with Cython")
print(np.shape(reconstructed_image))
'''

'''
Encode and save a single image
'''
'''
st = time.time()

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

en = time.time()
print("Took", en-st, "seconds to encode and write image")

f.close()
del frame
'''

'''
Decode and show the image
'''
'''
st = time.time()

# Open a BitStream from the file
f = open('output.bin', 'rb')
decoded_bits = BitStream(f)

# Read the stream up to the end of frame (EOF) character.
frame1bits = decoded_bits.readto('0b' + codes.EOF)[:-1*len(codes.EOF)]

# Create a frame object from the proto_mpeg library
frame = proto_mpeg_x.frame()

# Decode the bits and reconstruct the image
frame.decode_from_bits(frame1bits, 40, 30)

en = time.time()
print("Took", en-st, "seconds to read and decode image")

# View the image
#frame.show()

f.close()
'''