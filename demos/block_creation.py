import numpy as np

'''
This file demonstrates the block creation process

Say for example "Bx" is an 8x8 array of pixels

A 16x16 pixel image I would be composed of:

B1 B2
B3 B4

This code demonstrates how an image I can be decomposed into blocks:

[B1, B2, B3, B4]

'''

# Create an example image (16x16 pixels) and print it
x = np.arange(1,257)
x = np.reshape(x, (16, 16))
print("Original shape is:", np.shape(x), '\n')
print(x, '\n')

# Figure out how many vertical and horizontal blocks we can make
img_shape = np.shape(x)
v_blocks = img_shape[0]//8 # Note that // discards decimal pts. and returns an integer after divison
h_blocks = img_shape[1]//8

# Break the image into blocks
# This uses array slicing and list comprehension. Not very pretty, but it works.
x = [x[i * 8:(i + 1) * 8:, j * 8:(j + 1) * 8:] for i in range(0, v_blocks) for j in range(0, h_blocks)]

# Print the blocks
print("Converted to blocks. New shape is:", np.shape(x), '\n')
print(*x, sep='\n\n')

# Reconstruct the image
y = np.vstack((
    np.hstack((x[j*h_blocks+i] for i in range(0, h_blocks)))
    for j in range(0, v_blocks)
    ))

# Print the reconstructed image
print("\n\nReconstructed image from blocks. New shape is: ", np.shape(y), '\n')
print(y)



