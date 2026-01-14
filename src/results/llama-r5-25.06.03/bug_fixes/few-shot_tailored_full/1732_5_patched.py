import numpy as np

original_data = np.array([0, 1, 2, 3])

sinc_result = np.sinc(original_data)

assert np.isclose(sinc_result[0], 1), "Results not equal to one"
assert np.isclose(sinc_result[1], np.sinc(1)), "Results not equal to np.sinc(1)"
