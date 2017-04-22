import dct
import time
import numpy as np

test_block = (np.random.rand(8, 8)*3 + 190).astype(np.uint8)
print("Original data:\n", test_block)
st = time.time()
test_block_dct = dct.dct(test_block)
en = time.time()
print("Fast DCT:\n", test_block_dct)
print("Running time:", (en-st)*1000, "milliseconds\n\n")