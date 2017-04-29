import numpy as np
import skimage.io
import skimage.color

def blockCost(bl1,bl2,func):
	if(func == 'mse'):
		return np.sum((bl1-bl2)**2)


def blockMatching(fr1,fr2,Bsize=8,Ssize=7):
	'''
	Block Matching
	fr1,fr2 : input frames
	Bsize : Block Size
	Ssize : search space size
	
	Returns
	mot=array of motion vectors
	diff_wrappd = difference between fr1 and fr2 after applying block matching
	'''
	fr1_gray=skimage.color.rgb2gray(fr1)
	fr2_gray=skimage.color.rgb2gray(fr2)
	
	row, col = fr1_gray.shape

	fr1_wrapped=fr1.copy()
	
	fr1_mot=np.zeros((int(row/Bsize),int(col/Bsize),2))
	HBsize=np.ceil(Bsize/2).astype(int)

	for i in range(HBsize,row,Bsize):
		for j in range(HBsize,col,Bsize):
			ref_block = fr1_gray[i-HBsize:i+HBsize,j-HBsize:j+HBsize]
			min_diff=1000000
			for m in range(i-Ssize,i+Ssize+1):
				for n in range(j-Ssize,j+Ssize+1):
					if(m>=HBsize and n>=HBsize and m+HBsize<=row and n+HBsize<=col):
						current_block = fr2_gray[m-HBsize:m+HBsize,n-HBsize:n+HBsize]
						current_cost = blockCost(ref_block,current_block,'mse')
						#print(current_cost)
						if(current_cost<min_diff):
							min_diff=current_cost
							motY=m-i
							motX=n-j

			fr1_wrapped[motY+i-HBsize:motY+i+HBsize,motX+j-HBsize:motX+j+HBsize,:]=fr1[i-HBsize:i+HBsize,j-HBsize:j+HBsize,:]
			#fr1_wrapped[i-HBsize:i+HBsize,j-HBsize:j+HBsize,:]=fr1[-motY+i-HBsize:-motY+i+HBsize,-motX+j-HBsize:-motX+j+HBsize,:]
							
			fr1_mot[int((i-HBsize)/Bsize),int((j-HBsize)/Bsize),0]=motX
			fr1_mot[int((i-HBsize)/Bsize),int((j-HBsize)/Bsize),1]=motY
	diff_wrapped=fr1_wrapped.astype(int)-fr2.astype(int)
	return fr1_mot.astype(int),diff_wrapped
	
def wrap(fr,mot,Bsize=8):
	'''
	fr:input frame
	mot:array of motion vectors
	Bsize : block size
	
	Returns
	fr_wrapped: mootion applied to the input frame
	'''
	row, col,tmp = mot.shape
	fr_wrapped=fr.copy()
	for i in range(row):
		for j in range(col):
			motX=mot[i,j,0]
			motY=mot[i,j,1]
			fr_wrapped[motY+i*Bsize:motY+(i+1)*Bsize,motX+j*Bsize:motX+(j+1)*Bsize,:]=fr[i*Bsize:(i+1)*Bsize,j*Bsize:(j+1)*Bsize,:]
	return fr_wrapped
