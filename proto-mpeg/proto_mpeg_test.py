import proto_mpeg

print("Reading image.")
image = proto_mpeg.get_jpegs('../testing/480p-assorted/',1)[0]

print("Preparing image for encoding.")
frame = proto_mpeg.frame(image)

output = frame.encode_to_bits()

f = open('output.bin', 'wb')
output.tofile(f)
f.close()