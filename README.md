# EC504-video-encoder

### Midterm demo
Our midterm demo code, along with instructions to run, may be found in the [proto-mpeg](proto-mpeg) folder.

#### Example of an encoded and decoded image

Before encoding: 640x480 pixels and 217 kB

![before_encoding](http://i.imgur.com/allxWlg.jpg)

After encoding and decoding: 640x480 pixels and 35 kB

![after_decoding](http://i.imgur.com/5cVy778.png)

### Dependencies
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

### Overview of the proto-mpeg encoder and decoder