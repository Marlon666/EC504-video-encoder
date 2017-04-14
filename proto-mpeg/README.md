# proto-mpeg encoder and decoder

## Dependencies
Our code was written with Python 3.5. We have utilized free Python libraries to implement our encoder and decoder prototype. The complete list may be found below. Each item links to the installation instructions.

- [numpy](www.numpy.com): for array manipulation
- [matplotlib](http://matplotlib.org/users/installing.html): for image viewing
- [scikit-image](http://scikit-image.org/download.html): to read .jpeg files
- [bitstring](https://pypi.python.org/pypi/bitstring/3.1.3): for binary data manipulation

To install these libraries using `pip`, run the folllowing.

```
pip install numpy
pip install matplotlib
pip install -U scikit-image
pip install bitstring
```

## How to run

1. First, make sure you have installed all required dependencies.
2. Clone or download this repository to a local drive.
3. Run `python3 proto_mpeg_test.py` to encode and decode an image. The prototype is slow. Be prepared to wait on the order of 10 minutes for both encode and decode operations.

## Overview of file structure

#### dct.py
This library contains a naive implementation of the 2-D DCT and I-DCT. It is the primary culprit for the lackluster speed of our code. One of our next steps is to implement a fast cosine transform method in either pure C or in Cython-wrapped Python.

#### huffman_mpeg
This library is used to generate the lookup tables for the encoder and decoder. The lookup tables map `(run, level)` pairs to variable-length Huffman code and vice-versa. We used the Huffman codes that were recommended by the MPEG-1 standard. The lookup tables are implemented using Python dictionaries. These permit O(1)
lookups.

#### proto_mpeg
This library is the meat and potates of our encoder-decoder implementation. It handles all of the array manipulation and logic that is required to turn an image into a stream of bits and vice-versa. More detail about how the encoder-decoder functions may be found in the top-level readme.

#### ec504viewer
This library is used to display images or a series of images with the help of matplotlib.

#### proto_mpeg_test
This is a short script that demonstrates how to use the proto_mpeg library to encode, decode, and view an image.
