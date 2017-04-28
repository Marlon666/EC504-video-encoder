import proto_mpeg_x as proto_mpeg
import time
import numpy as np
from bitstring import BitStream
from bitstring import BitArray, ReadError
import huffman_mpeg as codes
import matplotlib.pyplot as plt
import motion as mot
import skimage.io

def convert2uint8(arr):
	arr[arr<0]=0
	arr[arr>255]=255
	return arr.astype(np.uint8)
def encodeMot(mot_vec,nbits):
	print(mot_vec.shape)
	out=BitArray()
	mot_vec=mot_vec.reshape([-1])
	for k in range(len(mot_vec)):
		out.append('0b'+np.binary_repr(mot_vec[k],width=nbits))
	print(len(out))
	return out
	
def decodeMot(mot_bin,nbits,w,l):
	print(w*l*2)
	print(len(mot_bin))
	mot_vec = np.zeros(w*l*2)
	for k in range(len(mot_vec)):
		mot_vec[k]=mot_bin[k*nbits:(k+1)*nbits].uint
	return mot_vec.reshape([w,l,2]).astype(int)
		
		
def encodeVideo(outname,files,mot_est='none',mot_clip=100,Ssize=7,QF=1):
	'''
	Given list of files encode them into a single file
	Inputs
	outname(string):name of the output file
	files(list): list of image directions to be encoded
	mot_est(string): Algorithm to use in motion estimation. Chose from following three
						-'none'
						-'frame_difference'
						-'block_matching'
	mot_clip(int): Value used for clipping the motion pixels
	Ssize(int): Size of the search window for 'block_matching'. Probably we wont need to change it
	QF(float): Compression factor
	'''
	
	start=time.time()
	images = []#proto_mpeg.get_jpegs(fname,nframes)#[0]
	for path in files:
		images.append(skimage.io.imread(path))
	
	output=BitArray()
	# Create a frame object initialized with our image
	print("Encoding image-1")
	t=time.time()
	frame = proto_mpeg.frame(images[0],QF=QF)
	# Retreive the binary encoding of the image
	output.append(frame.encode_to_bits())
	# Append an end of frame character
	output.append('0b' + codes.EOF)
	print(str(time.time()-t)+' seconds')
	
	#Code integer for mot_est
	if(mot_est=='none'):
		mot_code=0
	elif(mot_est=='frame_difference'):
		mot_code=1
	elif(mot_est=='block_matching'):
		mot_code=2
		
	for k in range(1,len(images)):
		# Create a frame object initialized with our image
		print("Encoding image-"+str(k+1))
		t=time.time()
		if(mot_est=='none' or np.mod(k,4)==0):
			code=images[k]
		else:
			if(mot_est=='frame_difference'):
				err=images[k].astype(int)-images[k-1].astype(int)
			elif(mot_est=='block_matching'):
				mot_vec,err = mot.blockMatching(images[k-1],images[k],Bsize=8,Ssize=Ssize)
			err[err<-mot_clip]=-mot_clip
			err[err>mot_clip]=mot_clip
			code=convert2uint8(err+mot_clip)#.astype(np.uint8)
		frame = proto_mpeg.frame(code,QF=QF)
		# Retreive the binary encoding of the image
		output.append(frame.encode_to_bits())
		output.append('0b' + codes.EOF)
		
		if(mot_est=='block_matching' and np.mod(k,4)!=0):
			mot_vec = mot_vec+Ssize
			nbits = int(np.ceil(np.log2(2*Ssize+1)))
			mot_bin=encodeMot(mot_vec,nbits)
			output.append(mot_bin)
			output.append('0b' + codes.EOF)
		# Append an end of frame character
		
		print(str(time.time()-t)+' seconds')

	f = open(outname, 'wb')
	# WRITE HEADER
	# v_mblocks and h_mblocks will be encoded as 8-bit unsigned integers
	#BitArray(float=QF,length=32))
	output.prepend('uint:8=' + str(frame.h_mblocks))
	output.prepend('uint:8=' + str(frame.v_mblocks))
	# number of images written as 20-bit unsigned integer
	output.prepend('uint:20=' + str(len(files)))
	output.prepend('uint:2='+str(mot_code))
	output.prepend('uint:8='+str(mot_clip))
	output.prepend('uint:4='+str(Ssize))
	output.prepend('float:32='+str(QF))
	output.tofile(f)
	f.close()
	del frame
	print('Encode time for one frame is %.3f seconds'%((time.time()-start)/(len(images))))
	
def playVideo(fname,realTime=True,delay=1):
	'''
	Plays the encoded file from fname
	Inputs
	fname(string): Path of the encoded binary file
	realTime(boolean):	If True, show each frame after decoding
						If Flase, first decode all frames than show time 
	delay(float): time between showing consecutive frames. It is used only if realTime=True
	'''
	start=time.time()
	f = open(fname, 'rb')
	decoded_bits = BitStream(f)
	
	QF=decoded_bits.read('float:32')
	Ssize=decoded_bits.read('uint:4')
	mot_clip=decoded_bits.read('uint:8')
	mot_code=decoded_bits.read('uint:2')
	num_imgs  = decoded_bits.read('uint:20')
	v_mblocks = decoded_bits.read('uint:8')
	h_mblocks = decoded_bits.read('uint:8')
    
	plt.ion()
	ax = plt.gca()
	ax.axis('off')
	fig = plt.gcf()
	fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
	fig.canvas.set_window_title("EC504 Viewer")
	plt.pause(.001)
	
	k=0
	prev_image=mot_clip*np.ones([v_mblocks*16,h_mblocks*16,3]).astype(np.uint8)
	frames=list()
	while(True):
		# Read the stream up to the end of frame (EOF) character.
		try:
			framebits = decoded_bits.readto('0b' + codes.EOF)[:-1*len(codes.EOF)]
		except ReadError:
			break
		print("Decoding image-"+str(k))
			
		t=time.time()
		# Create a frame object from the proto_mpeg library
		frame = proto_mpeg.frame(QF=QF)
		# Decode the bits and reconstruct the image
		code = frame.decode_from_bits(framebits, h_mblocks, v_mblocks)
		if(mot_code==0 or np.mod(k,4)==0):
			image=code
			prev_image=image
		elif(mot_code==1):
			#print(prev_image)
			#print(code)
			image=convert2uint8(prev_image.astype(int)+code.astype(int)-mot_clip)
			prev_image=image
		elif(mot_code==2):
			if(k==0):
				image=code
			else:
				nbits = int(np.ceil(np.log2(2*Ssize+1)))
				motbits = decoded_bits.read(v_mblocks*h_mblocks*8*nbits)
				tmp = decoded_bits.readto('0b' + codes.EOF)
				mot_arr=decodeMot(motbits,nbits,v_mblocks*2, h_mblocks*2)-Ssize			
				prev_image_w=mot.wrap(prev_image,mot_arr)
				image=convert2uint8(prev_image_w.astype(int)-code.astype(int)+mot_clip)
			prev_image=image
		print(str(time.time()-t)+' seconds')
		if(realTime):
			plt.imshow(image, extent=(0, 1, 1, 0))
			plt.draw()
			plt.pause(.001)
		else:
			frames.append(image)
		del frame
		k+=1
	f.close()
	print('Decode time for one frame is %.3f seconds'%((time.time()-start)/k))
	
	if(not realTime):
		for k in range(len(frames)):
			image=frames[k]
			plt.imshow(image, extent=(0, 1, 1, 0))
			plt.draw()
			plt.pause(delay)
	input("Press [enter] to continue.")
