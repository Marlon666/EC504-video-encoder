f = open('outputnew.bin', 'rb')
decoded_bits = BitStream(f)
fra1 = decoded_bits.readto('0b' + codes.EOF)
fra2 = decoded_bits.readto('0b' + codes.EOF)
fra3 = decoded_bits.readto('0b' + codes.EOF)

f = open('output0.bin', 'rb')
decoded_bits = BitStream(f)
f1 = decoded_bits.readto('0b' + codes.EOF)

f = open('output1.bin', 'rb')
decoded_bits = BitStream(f)
f2 = decoded_bits.readto('0b' + codes.EOF)

f = open('output2.bin', 'rb')
decoded_bits = BitStream(f)
f3 = decoded_bits.readto('0b' + codes.EOF)
