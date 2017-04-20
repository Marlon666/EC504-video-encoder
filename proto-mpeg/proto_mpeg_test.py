import proto_mpeg
from bitstring import BitStream
import huffman_mpeg as codes
import os
from bitstring import BitArray, ReadError
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import numpy as np

mpl.rcParams['toolbar'] = 'None'
'''
Encode and save a single image
'''

# Get a single 640x480 image
print("Reading image.")
image = proto_mpeg.get_jpegs('../testing/motion/',8)#[0]


'''
output=BitArray()
for k in range(len(image)):
	# Create a frame object initialized with our image
	print("Encoding image-"+str(k+1))
	frame = proto_mpeg.frame(image[k])
	# Retreive the binary encoding of the image
	output.append(frame.encode_to_bits())
	# Append an end of frame character
	output.append('0b' + codes.EOF)

f = open('output.mpg', 'wb')
output.tofile(f)
f.close()
del frame
'''

'''
Decode and show the image
'''

# Open a BitStream from the file
f = open('ref8.mpg', 'rb')
decoded_bits = BitStream(f)

plt.ion()
#plt.show()

ax = plt.gca()
#ax.axis('tight')
ax.axis('off')

fig = plt.gcf()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
fig.canvas.set_window_title("EC504 Viewer")

plt.pause(.001)
k=1
while(True):
	print("Decoding image-"+str(k))
	k+=1
	# Read the stream up to the end of frame (EOF) character.
	try:
		framebits = decoded_bits.readto('0b' + codes.EOF)[:-1*len(codes.EOF)]
	except ReadError:
		break
		

	# Create a frame object from the proto_mpeg library
	frame = proto_mpeg.frame()
	# Decode the bits and reconstruct the image
	frame.decode_from_bits(framebits, 45, 27)
	image = frame.getFrame()
	plt.imshow(image, extent=(0, 1, 1, 0))
	plt.draw()
	plt.pause(.001)
	del frame
f.close()
input("Press [enter] to continue.")





