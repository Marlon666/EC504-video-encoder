# proto-mpeg encoder and decoder

## Dependencies
Our code was written with Python 3.5. Minimum compatible version is Python 3.2. We have utilized free Python libraries to implement our encoder and decoder prototype. The complete list may be found below. Each item links to the installation instructions.

- [numpy](www.numpy.com): for array manipulation
- [matplotlib](http://matplotlib.org/users/installing.html): for image viewing
- [scikit-image](http://scikit-image.org/download.html): to read .jpeg files
- [bitstring](https://pypi.python.org/pypi/bitstring/3.1.3): for binary data manipulation
- [cython](http://cython.org/#download): for improvement of running time

To install these libraries using `pip`, run the folllowing.

```
pip install numpy
pip install matplotlib
pip install -U scikit-image
pip install bitstring
pip install Cython
```

## How to run

Our code uses Cython for improvement of running time. Cython is an optimizing C-compiler for python code. More information on our use of Cython may be found in our report.
To build our code on your machine, `cd` into the `proto-mpeg` folder and run:

```
python3 setup.py build_ext --inplace
```
(Note that your Python 3.2+ interpreter may have a different name.)

This commmand will prompt Cython to generate and then compile pure C code for our encoder and decoder software.

After this is done, you are all set to run our software!

We have written easy-to-use command-line interfaces to run encode and decode operations.

To use the GUI instead, run `python3 gui.py`.

**Typical usage for encode operation:**

```
python3 encode.py --limit 10 ../testing/beach_288p/
```

To see help for encode.py usage:
```
$ python3 encode.py -h

usage: encode.py [-h] [--out OUT] [--alg {n,fd,bm}] [--qf {1,2,3,4}]
                 [--limit LIMIT]
                 ...

EC504 proto-mpeg encoder for jpeg images

positional arguments:
  input            Either a single directory or a list of files to encode,
                   separated by spaces.

optional arguments:
  -h, --help       show this help message and exit
  --out OUT        filename of encoded file. default is output.bin
  --alg {n,fd,bm}  temporal compression algorithm. n=none; fd=frame
                   difference; bm=block matching. Default is none.
  --qf {1,2,3,4}   quantization factor for HF suppression. Default is 1.
                   Higher values achieve higher compression.
  --limit LIMIT    cap the number of images that will be encoded. Default is
                   no limit (all files).
```

**Typical usage for decode operaton:**

```
python3 decode.py output.bin
```

To see help for decode.py usage:
```
$ python3 decode.py -h

usage: decode.py [-h] input

EC504 proto-mpeg decoder

positional arguments:
  input       file to be decoded

optional arguments:
  -h, --help  show this help message and exit
```