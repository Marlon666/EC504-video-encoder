import skimage.io
import sys
import numpy as np
import ec504viewer
from os import listdir


def main():

    # Create and view an array of binary data
    data = bytearray([0, 1, 16])
    print(data)

    # Write the binary data to a binary data file, then close it
    with open('test.bin', 'wb') as f:
        f.write(data)

    # Open that same file, read the data, and print it
    f = open('test.bin', 'rb')
    recovered_data = bytearray(f.read())
    print(recovered_data)

    # Read all 720p test images
    directory =  'testing/720p-10/'
    images = []
    for file in sorted(listdir(directory)):
        if file.endswith('.jpg'):
            print(file)
            images.append(skimage.io.imread(directory + '/' + file))
    print("Read", len(images), "images")

    # View all images with a 0.2 second delay between images
    ec504viewer.view(images, 0.2)


if __name__ == '__main__':
    main()