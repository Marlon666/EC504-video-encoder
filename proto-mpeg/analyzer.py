import proto_mpeg_x as pm
from os import listdir
import os
import time
import numpy as np

'''
This analyzer script measures:
-encode times (total over all files)
-decode times (total over all files)
-compression ratios
for a matrix of quantization factors and motion encoding algorithms.

Note that the decoder function playVideo must not be set up to open a window
or try to play back a decoded file in order for this profiling to work.
'''


# Get 4 images
img_directory = '../testing/beach_288p/'
filenames = sorted(listdir(img_directory))
files = [img_directory + fname for fname in filenames]
files = files[:4]

# Calculate original file size
original_size_B = 0
for file in files:
    original_size_B += os.path.getsize(file)
print(original_size_B)

# Run baseline encoding algorithm for a single mot_est setting over a list of QF's
def analyze(QF_list, mot_est_setting):
    out_name = 'analyzer.bin'
    compressed_sizes = np.empty(0)
    encode_times = np.empty(0)
    decode_times = np.empty(0)
    for this_QF in QF_list:
        # Encode
        st = time.time()
        pm.encodeVideo(out_name,files, mot_est=mot_est_setting, mot_clip=50, QF=this_QF)
        en = time.time()
        compressed_sizes = np.append(compressed_sizes, os.path.getsize(out_name))
        encode_times = np.append(encode_times, en-st)
        # Decode
        st = time.time()
        pm.playVideo(out_name, realTime=False)
        en = time.time()
        decode_times = np.append(decode_times, en-st)
        os.remove(out_name)
    return (compressed_sizes, encode_times, decode_times)


QFs_to_test = [0.75, 1.0, 2.0, 3.0, 4.0, 5.0]
algs = ['none', 'frame_difference', 'block_matching']

f = open('analyzer.txt', 'w')
f.write("Proto mpeg analysis for " + str(len(files)) + " files from directory " + img_directory + '\n')

for alg in algs:
    (compressed_sizes, e_times, d_times) = analyze(QFs_to_test, alg)
    f.write("Test results for mot_est = " + alg + ":" + '\n')
    f.write("QF settings:" + str(QFs_to_test) + '\n')
    f.write("Encode times (s):" + str(e_times) + '\n')
    f.write("Decode times (s):" + str(d_times) + '\n')
    ratios = original_size_B/compressed_sizes
    f.write("Compression ratios:" + str(ratios) + '\n\n')

f.close()
