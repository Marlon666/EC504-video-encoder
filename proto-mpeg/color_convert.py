
import numpy as np	
import skimage.color

def rgb2ycbcr(im):
	im_r = im[:,:,0]
	im_g = im[:,:,1]
	im_b = im[:,:,2]

	im_ycbcr=np.zeros(im.shape)
	im_ycbcr[:,:,0]=.299*im_r+.587*im_g+.114*im_b
	im_ycbcr[:,:,1]=128.-.168736*im_r-.331264*im_g+.5*im_b
	im_ycbcr[:,:,2]=128.+.5*im_r-.418688*im_g-.081312*im_b
	return im_ycbcr

def ycbcr2rgb(im):
	im_y=im[:,:,0]
	im_cb=im[:,:,1]
	im_cr=im[:,:,2]

	im_rgb=np.zeros(im.shape)
	im_rgb[:,:,0]=im_y+1.402*(im_cr-128.)
	im_rgb[:,:,1]=im_y-.344136*(im_cb-128.)-.714136*(im_cr-128.)
	im_rgb[:,:,2]=im_y+1.772*(im_cb-128.)
	return im_rgb
