import proto_mpeg_x
import skimage.io
import numpy as np
from bitstring import BitStream
import huffman_mpeg as codes

img = skimage.io.imread('../testing/mountain_32_32.jpg')
print(type(img[0, 0, 0]))

thing = proto_mpeg_x.frame(img)

thing.show()

bits = thing.encode_to_bits()
bits.append('0b' + codes.EOF)

with open('mountain_32_32.bin', 'wb') as f:
    bits.tofile(f)

del thing

# Open a BitStream from the file
f = open('mountain_32_32.bin', 'rb')
decoded_bits = BitStream(f)

# Read the stream up to the end of frame (EOF) character.
frame1bits = decoded_bits.readto('0b' + codes.EOF)[:-1*len(codes.EOF)]

# Create a frame object from the proto_mpeg library
frame = proto_mpeg_x.frame()

# Decode the bits and reconstruct the image
img = frame.decode_from_bits(frame1bits, 2, 2)

thing = proto_mpeg_x.frame(img)
thing.show()


with open('mountain_32_32_b.txt', 'wb') as f:
    np.savetxt(f, img[:,:,2], fmt='%3u')
    #img.tofile(f, sep=" ", format='%u')
