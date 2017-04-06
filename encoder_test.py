import encoder_lib as enc

dir =   './testing/720p-10'
fname = 'test.mpg'

#Encode the images in 'dir' into 'fname'
#It creates 'test.mpg' which is nearly the same size as the sum of the 
#sizes of all frames
enc.encode(dir,fname)
#Decode the images written in 'fname' and display them
enc.decode(fname,.3)
