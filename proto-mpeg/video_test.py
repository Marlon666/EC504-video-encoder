import video_lib as vl
import time
'''
Encode and decode images
'''


# Get a single 640x480 image
t=time.time()
vl.encodeVideo('block5.mpg','../testing/motion/',nframes=5,
						mot_est='block_matching',mot_clip=50)
print('TOTAL ENCODING TIME IS %.3f SECONDS'%(time.time()-t))

t=time.time()
vl.playVideo('block5.mpg',realTime=False,size=[432,720],mot_est='block_matching',mot_clip=50)
print('TOTAL DECODING TIME IS %.3f SECONDS'%(time.time()-t))


