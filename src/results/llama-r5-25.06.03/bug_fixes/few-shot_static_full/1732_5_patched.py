import numpy as np

original_data = np.array([0, 1, 2, 3])

sinc_result = np.sinc(original_data)

np.testing.assert_almost_equal(sinc_result[0], 1)
np.testing.assert_almost_equal(sinc_result[1], 0)
