import video_lib as vl
from os import listdir
import time
'''
Encode and decode images
'''


# Get a single 640x480 image
img_directory = '../testing/motion/'
filenames = sorted(listdir(img_directory))
#print(sorted(listdir(img_directory)))

files = [img_directory + fname for fname in filenames]
#print(files)
nFrames=6

vl.encodeVideo('ref3.mpg',files[:nFrames],mot_est='none',mot_clip=50,QF=1.5)


vl.playVideo('ref3.mpg',realTime=False,delay=1)



