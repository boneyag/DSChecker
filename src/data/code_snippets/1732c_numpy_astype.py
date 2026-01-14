import numpy as np

original_data = np.array([0, 1, 2, 3])

sinc_result = np.sinc(original_data).astype(original_data.dtype)

assert sinc_result[0] == 1, "Results not equal to one"
assert sinc_result[1] == 0, "Results not equal to zero"
