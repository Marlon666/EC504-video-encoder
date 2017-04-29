import proto_mpeg_x as pm
from os import listdir, remove

# Get some images
#img_directory = '../testing/480p-assorted/'
img_directory = '../testing/motion/'
filenames = sorted(listdir(img_directory))
files = [img_directory + fname for fname in filenames]

# Encode
pm.encodeVideo('out.bin',files[:5], mot_est='none', mot_clip=50, QF=1)

# Decode
pm.playVideo('out.bin', realTime=False, delay=0.05)

# Clean up
# remove('out.bin')