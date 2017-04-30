import numpy as np
import matplotlib.pyplot as plt

QF = [0.75, 1.0, 2.0, 3.0, 4.0, 5.0]

# Results for no motion estimation
encode_time_none = np.array([10.12392211, 8.12144279, 5.31368852, 4.2285552, 3.73490286, 3.40658712])/41.89198923
decode_time_none = np.array([51.01390362, 40.85215712, 22.7261095, 16.08058071, 12.7659142, 11.07156968])/51.01390362
comp_none = np.array([3.62368823,   4.52025135,   8.62258272,  12.98569249,  16.92870702, 20.24843221])

# Results for frame difference alg
encode_time_diff = np.array([9.36980271, 7.98100543, 4.96672606, 3.82418299, 3.49121785, 3.20037246])/41.89198923
decode_time_diff = np.array([47.80498934, 38.71991777, 23.93657827, 14.5955081, 11.34192514, 9.89231753])/51.01390362
comp_diff = np.array([3.83027332, 4.79604067, 9.33011708, 14.45364034, 19.3588436, 23.41277713])

# Results for block matching alg
encode_time_bm = np.array([39.19982719, 41.89198923, 37.16327906, 36.6418395, 39.07675767, 36.54084444])/41.89198923
decode_time_bm = np.array([29.08233023, 22.9178853, 13.97205925, 11.38587379, 10.18791008, 9.32760978])/51.01390362
comp_bm = np.array([6.39528504, 8.01925547, 13.61640814, 17.26636548, 19.40699161, 20.69140395])

# COMPRESSION RATIOS
fig, ax1 = plt.subplots()
ax1.plot(QF, comp_none, label='None', color='r', marker='<')
ax1.plot(QF, comp_diff, label='Difference', color='g', marker='x')
ax1.plot(QF, comp_bm, label='Block match', color='b', marker='d')
plt.grid(True)
plt.xlabel("Quantization factor")
plt.ylabel("Compression ratio")
plt.legend(title='Motion algorithm')
plt.suptitle("Compression ratios", fontsize=14)
plt.savefig('compression_ratio.png', dpi=200)
plt.cla()
plt.clf()

# NORMALIZED ENCODING TIMES
fig, ax1 = plt.subplots()
ax1.plot(QF, encode_time_none, label='None', color='r', marker='<')
ax1.plot(QF, encode_time_diff, label='Difference', color='g', marker='x')
ax1.plot(QF, encode_time_bm, label='Block match', color='b', marker='d')
plt.grid(True)
plt.xlabel("Quantization factor")
plt.ylabel("Normalized encode time")
plt.legend(title='Motion algorithm')
plt.suptitle("Normalized encode time", fontsize=14)
plt.savefig('encode_time.png', dpi=200)
plt.cla()
plt.clf()

# NORMALIZED DECODING TIMES
fig, ax1 = plt.subplots()
ax1.plot(QF, decode_time_none, label='None', color='r', marker='<')
ax1.plot(QF, decode_time_diff, label='Difference', color='g', marker='x')
ax1.plot(QF, decode_time_bm, label='Block match', color='b', marker='d')
plt.grid(True)
plt.xlabel("Quantization factor")
plt.ylabel("Normalized decoding time")
plt.legend(title='Motion algorithm')
plt.suptitle("Normalized decode time", fontsize=14)
plt.savefig('decode_time.png', dpi=200)
plt.cla()
plt.clf()
