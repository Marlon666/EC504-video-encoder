import bitstring
import proto_mpeg
import numpy as np
import matplotlib.pyplot as plt

image = proto_mpeg.get_jpegs('../testing/720p-10/',1)[0]


test_image = proto_mpeg.frame(image)
img_blocks = test_image.image_to_blocks()
# test_image.set_image(img_blocks)



