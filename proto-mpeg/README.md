# proto-mpeg encoder and decoder

## How to run

1. First, make sure you have installed all required dependencies.
2. Clone or download this repository to a local drive.
3. Run `python3 proto_mpeg_test.py` to encode and decode an image. The prototype is slow. Be prepared to wait on the order of 10 minutes for both encode and decode operations.

## Overview of file structure

### dct.py
This is a naive implementation of the 2-D DCT. It is the primary culprit for the lackluster speed of our code. One of our next steps is to implement a fast cosine transform method and either wr


