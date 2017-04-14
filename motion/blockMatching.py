import numpy as np
import skimage.io

def blockCost(bl1,bl2,func):
	if(func == 'mse'):
		return np.mean((bl1-bl2)**2)

directory = '../testing/motion/'
fr1=skimage.io.imread(directory + 'monkey5_001.jpg').astype(float)
fr2=skimage.io.imread(directory + 'monkey5_001.jpg').astype(float)

fr1_r=fr1[:,:,0]
fr2_r=fr2[:,:,0]


row, col = fr1_r.shape

fr1_mot=np.zeros((row,col,2))

Bsize = 8
Ssize = 7

HBsize=np.ceil(Bsize/2).astype(int)



fr1_r=fr1[:,:,0]
fr2_r=fr2[:,:,0]
for i in range(HBsize,row-HBsize,Bsize):
	print(i)
	for j in range(HBsize,col-HBsize,Bsize):
		ref_block = fr1_r[i-HBsize:i+HBsize,j-HBsize:j+HBsize]
		min_diff=100000
		for m in range(i-Ssize,i+Ssize+1):
			for n in range(j-Ssize,j+Ssize+1):
				if(m>=HBsize and n>=HBsize and m+HBsize<=row and n+HBsize<=col):
					current_block = fr2_r[m-HBsize:m+HBsize,n-HBsize:n+HBsize]
					current_cost = blockCost(ref_block,current_block,'mse')
					if(current_cost<=min_diff):
						min_diff=current_cost
						motY=m-i
						motX=n-j
		fr1_mot[i-HBsize:i+HBsize,j-HBsize:j+HBsize,0]=motX
		fr1_mot[i-HBsize:i+HBsize,j-HBsize:j+HBsize,1]=motY
		
				

