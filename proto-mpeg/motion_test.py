##Test Code for motion

import proto_mpeg
from bitstring import BitStream
import huffman_mpeg as codes
import os
from bitstring import BitArray, ReadError
import matplotlib.pyplot as plt
import time
import numpy as np
import video_lib as vl
import motion as mot

images = proto_mpeg.get_jpegs('../testing/motion/',3)
fr1=images[1]
fr2=images[2]


print('Basic block matching started')
t=time.time()
fr1_mot,diff_wrapped = mot.blockMatching(fr1,fr2,Bsize=8,Ssize=7)
print('%.2f seconds'%(time.time()-t))
fr1_w=fr2.astype(int)+diff_wrapped
fr1_w2=mot.wrap(fr1,fr1_mot).astype(int)

print(np.sum(fr1_w-fr1_w2))
print(fr1_mot.shape)
print(np.mean(np.abs(diff_wrapped)))
print(np.mean(np.abs(fr1.astype(int)-fr2.astype(int))))

