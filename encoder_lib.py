import matplotlib
matplotlib.use('TkAgg')

import numpy as np
from os import listdir
import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import re
from PIL import Image
import io


mpl.rcParams['toolbar'] = 'None'

#A special character for specifying end of frame
spec_char=bytes('ero','utf-8')

def encode(dir,fname):
    '''
    Comnines all of the '.jpg' images in dir into a single binary file 
    and writes it to fname.
    :dir: Directory of the folder containing images
    :fname: name for the output folder
    '''
    #List for holding the binary codes of '.jpg' images
    imBins= []
    for file in sorted(listdir(dir)):
        if file.endswith('.jpg'):
            print(file)
            with open(dir + '/' + file,'rb') as f:
                imBins.append(f.read()) #Read as binary
    print("Read", len(imBins), "images")

    #Combine binary objects and write them into a single file.
    #Uses spec_char between consecutive frames
    with open(fname,'wb') as f:
        for k in range(len(imBins)):
            f.write(imBins[k])
            f.write(spec_char)
          
            
def decode(fname,delay):
    '''
    Decodes the binary information written in fname and displays the 
    images consecutively with 'delay' seconds between them
    :param fname: driectory of the encoded file
    :param delay: time (seconds) to show each image
    :return: none
    '''
    with open(fname,'rb') as f:
        vidBins = f.read()
	
    spec_locs = [(0,0)]
    for m in re.finditer(spec_char, vidBins):
        spec_locs.append((m.start(), m.end()))

    fig, ax = plt.subplots(1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.canvas.set_window_title("EC504 Viewer")
    im = ax.imshow(np.zeros((256, 256, 3)), extent=(0, 1, 1, 0))
    ax.axis('tight')
    ax.axis('off')
    fig.show()

    for k in range(len(spec_locs)-1):
        imBins=vidBins[spec_locs[k][1]:spec_locs[k+1][0]]
        image = Image.open(io.BytesIO(imBins))
        im.set_data(image)
        im.axes.figure.canvas.draw()
        time.sleep(delay)

