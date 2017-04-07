import bitstring
import proto_mpeg
import numpy as np
import matplotlib.pyplot as plt

image = proto_mpeg.get_jpegs('../testing/720p-10/',1)[0]


test_image = proto_mpeg.frame(image)

# try to break test image into macroblocks
# Figure out how many vertical and horizontal blocks we can make
'''
img_shape = np.shape(test_image.r)
if(img_shape[0] % 16 != 0 or img_shape[1] % 16 != 0):
    raise Exception("Image dimensions", img_shape, "not divisible by macroblock size. Someone tell the author to handle this.")

v_blocks = img_shape[0]//16 # Note that // discards decimal pts. and returns an integer after divison
h_blocks = img_shape[1]//16

print(v_blocks, h_blocks)

# Break the image into blocks
# This uses array slicing and list comprehension. Not very pretty, but it works.
def macroblocks(x, v_blocks, h_blocks):
    x = [x[i * 16:(i + 1) * 16:, j * 16:(j + 1) * 16:] for i in range(0, v_blocks) for j in range(0, h_blocks)]
    return x

blocks = macroblocks(test_image.r, v_blocks, h_blocks)
print(np.shape(blocks))

print(blocks[0])
'''

# Turn separare color components into (x, 720, 1080) shaped array of blocks
r_mblocks = test_image.image_to_mblocks(test_image.r)
g_mblocks = test_image.image_to_mblocks(test_image.g)
b_mblocks = test_image.image_to_mblocks(test_image.b)

print("Shape of test image red:", np.shape(test_image.r))
print("Shape of r_mblock:", np.shape(r_mblocks))

# Turn entite image into blocks
# Each call to mblocks_to_blocks turns 3 macroblocks (RBG) into the block representation of a single macroblock. We get back something that is (6, 8, 8)
# We run a for loop so that we can obtains a stream of blocks that represents the entire image
num_macroblocks = np.shape(r_mblocks)[0]
img_blocks = np.empty((0, 8, 8))
for i in range(0, num_macroblocks):
    img_blocks = np.concatenate((img_blocks, test_image.mblocks_to_blocks(r_mblocks[i], g_mblocks[i], b_mblocks[i])), axis=0)
print("Number of original macroblocks:", num_macroblocks)
print("Shape of img_blocks:", np.shape(img_blocks))

# checkpoint
print("33% complete")

# Turn the blocks back into macroblocks
recovered_r_mblocks = np.empty((0, 16, 16))
recovered_g_mblocks = np.empty((0, 16, 16))
recovered_b_mblocks = np.empty((0, 16, 16))
num_macroblocks = np.shape(img_blocks)[0] // 6
print("Number of recovered macroblocks:", num_macroblocks)
for i in range(0, 3600):
    [r, g, b] = test_image.blocks_to_mblock(img_blocks[i*6:i*6+7,:,:])
    #print(np.shape([r]), np.shape(recovered_r_mblocks))
    recovered_r_mblocks = np.concatenate((recovered_r_mblocks, [r]), axis=0)
    recovered_g_mblocks = np.concatenate((recovered_g_mblocks, [g]), axis=0)
    recovered_b_mblocks = np.concatenate((recovered_b_mblocks, [b]), axis=0)

# Turn the macroblocks back into an image

print("Shape of recovered red macroblocks:", np.shape(recovered_r_mblocks))
'''
v_blocks = 45
h_blocks = 80
g = np.vstack((
    np.hstack((recovered_g_mblocks[j*h_blocks+i] for i in range(0, h_blocks)))
    for j in range(0, v_blocks)
    ))
'''
g = test_image.mblocks_to_image(recovered_g_mblocks, 80, 45)

print("Shape of recovered red image component:", np.shape(g))
plt.imshow(g)
plt.show()