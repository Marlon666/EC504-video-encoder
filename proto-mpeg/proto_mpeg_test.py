import proto_mpeg
from bitstring import BitStream
import huffman_mpeg
import numpy as np

EOF = '0000 0000 0000 0000 0000 0000 0000 0001'.replace(' ', '')

# Encode...
'''
print("Reading image.")
image = proto_mpeg.get_jpegs('../testing/480p-assorted/',1)[0]

print("Preparing image for encoding.")
frame = proto_mpeg.frame(image)

(output,zz) = frame.encode_to_bits()

print("Length of encoded bits is:", len(output))
print("Total zigzag entries:", len(zz))

output.append('0b' + EOF)

f = open('output.bin', 'wb')
output.tofile(f)
f.close()

# try to save zigzag summary to file, so that the decoder can use it to check its work
np.save('original_zz.npy', zz)

'''

# Decode...
#278707 bits

# try to load zigzag summary from file
zz_from_file = np.load('original_zz.npy').item()
#print("Do dictionaries match?", zz==zz_from_file)

# Get bitstream from file
f = open('output.bin', 'rb')
decoded_bits = BitStream(f)

frame1bits = decoded_bits.readto('0b' + EOF)[:-1*len(EOF)]

frame = proto_mpeg.frame()
frame.decode_from_bits(frame1bits, 40, 30, zz_from_file)




