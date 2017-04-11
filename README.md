# EC504-video-encoder

### Midterm demo
Our midterm demo code, along with instructions to run, may be found in the [proto-mpeg](proto-mpeg) folder.
We also have a prototype GUI completed. The prototype code and instructions to run may be found in the [GUI](GUI) folder.

#### Example of an encoded and decoded image

Before encoding: 640x480 pixels and 217 kB

![before_encoding](http://i.imgur.com/allxWlg.jpg)

After encoding and decoding: 640x480 pixels and 35 kB

![after_decoding](http://i.imgur.com/5cVy778.png)

### Overview of the proto-mpeg encoder and decoder
Our proto-mpeg encoder and decoder is modeled after the methodology recommended by the MPEG-1 standard for video encoding. In the overview that follows, we will point out significant departures from the MPEG standard.

![example_image](http://i.imgur.com/gUOViH1.png)

To begin, we assume that we have an image with some dimensions in pixels `h, w` with three color components `r`, `g`, and `b`. Most commonly, images are represented using 24 bits of color information per pixel: 8 bits for red, 8 for green, and 8 for blue. The value of each 8-bit code is almost universally interpreted as an unsigned integer, with values in the interval [0, 255]. The RBG is not the only color space, and in fact, the MPEG standard heavily utilizes the YCbCr color space (where Y is the luminosity, and Cb and Cr are chromacity components). It is straighforward to convert the RGB value for a pixel to other color spaces. We will touch on color spaces again shortly.

The ultimate goal of a video encoder is to convert a series of images into a stream of bits. Similarly, the decoder's job is to accept a stream of bits and (with any luck) reconstruct a likeness of the original images.

The approach used by all MPEG algorithms (even modern ones) are lossy. *Good* encoders are lossy in ways that are not readily perceptible to the human vision system. Similarly to how an audio compression algorithm might throw away all spectral components over 10 kHz due to lack of human sensitivity, video encoders seek to discard the information that will be missed the least. Though we do not plan to cover the topic in depth, it is important to recognize that the intricacies of our visual response to different colors and spatial frequencies has had a tremendous impact on video encoding technology.

The first step in our encoding process is the divison of a `h x w` matrix for each of the three color components into *macroblocks* of size `16 x 16` pixels. The image below provides an illustration of the macroblock segmentation process for the red color component. The number of macroblocks obtained per component is a function of the original size `h x w` of the image. It is no coincidence that most "standard" video dimensions are evenly divisble into maroblocks. For example, 640 x 480 video measures 40 macroblocks across and 30 macroblocks in height. 4k video (3840 x 2160 pixels) measures 240 macroblocks in width and 135 in height.

![macroblocks](http://i.imgur.com/usDrLqX.png)

After each color component has been broken into a collection of macroblocks, they are further broken down into *blocks* of `8 x 8` pixels. In the image below, the red macroblock is broken into four blocks, and its data is unchanged. On the other hand, we subsample the green and blue color components in order to construct a single block for each. By discarding 75% of the data for 2 of the three color components, we have discarded 50% of our original image data.


![blocks](http://i.imgur.com/IOO8dDS.png)

Our choice to retain all information for the red color component and to subsample green and blue was arbitrary. On the other hand, the MPEG-1 standard converts image information to the YCbCr color space prior to this step. Simialrly to how we treat the red component, the MPEG-1 standard retains all color information for the Y (luminance) component, to which the eye is more sensitive. It subsamples the Cb and Cr components (just as we have done with green and blue) due to our weaker visual sensitivity.

After converting the original image into a collection of blocks, we apply the 2D discrete cosine transform to each block. This step allows us to express the values in each block in terms of a sum of spatial frequencies. Because the human vision system is generally more sensitive to lower spatial frequenies than it is to higher spatial frequencies, the 2-D DCT gives us another opportunity to strategically throw away image information.

The left table below provides an example of a block of pixel values for a single color component. When we apply the 2D DCT to an 8x8 block, we obtain a new 8x8 block of DCT coefficients. The right table shows the result of applying a 2D DCT to the original pixel values (note that red values are negative).

![DCT1](http://i.imgur.com/dLHmvAs.png)

The spatial frequencies represented by each DCT coefficient increase from the top left to the bottom right. In this example, the lowest frequency is 1527 and the highest frequency is -0.61. We use these DCT coefficients to encode the images, but only after throwing away some of the high-frequency data. This is done through a process called *quantization*.

The MPEG-1 standard provides a quantization matrix. The values in the quantization matrix increase with spatial frequency. The quantization process is performed by dividing the DCT coefficients by the quantization values, and then rounding the result to the nearest integer. Division by a larger value translates into an increased likelihood that the rounded result will be zero. The table below shows the MPEG-1 quantization matrix and the results of quantizing our DCT coefficients.

![DCT2](http://i.imgur.com/cngmDId.png)

Behold! What was once 64 unique DCT coefficients are now the numbers 191, 1, and 0. Though it may seem that we discarded *too* much data, we can get a qualitatively better feeling about this process through inspection of the original pixel values: they are all fairly close. The range of `194-188 = 6` corresponds to only 2% of the 0-255 scale. So perhaps it's not too crazy to represent this entire block using three unique values.

The final step in our encoding process utilizes variable length codes in order to encode the quantized DCT coefficients. This is done by first flattening the `8x8` array in order of increasing spatial frequency. The most common pattern used is the *zig-zag* pattern, illustrated below.

![zigzag](http://i.imgur.com/CWhbc2H.png)

If we apply the zig-zag pattern to our example, we obtain `191 0 1` followed by a long string of zeros. We encode this string in the form:

`<DC term>  <run, level>  <EOB>`

where the DC term is simply our first value (191); ` <run, level> ` indicates a string of `run` zeros that is terminated by a non-zero value `level`; and `EOB` is an "end of block" character that indicates the balance of coefficients in the block are zero. For our example, we would represent the data in our quantized block with the sequence

`191 (1, 1) 'EOB'`

There may be multiple `<run, level>` pairs before the end of block character. The common `<run, level>` pairs, as well as the `<EOB>` character, are assigned Huffman codes by the MPEG-1 standard (which we utilize verbatim). We code the DC term for every block as an unsigned 8-bit integer.

Finally, we'd like to point out how it is possible to delineate different images within a single encoded file. Thanks to the design of the MPEG-1 Huffman codes, it is possible to design special bit strings that are guaranteed not to collide with image data. In our proto-mpeg encoder, we implement special codes by writing 4.5 bytes of zeros, followed by a 4-bit code that can signal various things--such as "end of this image" or "end of the video".

That's the strategy in a nutshell. The decoder performs the same process, in reverse.