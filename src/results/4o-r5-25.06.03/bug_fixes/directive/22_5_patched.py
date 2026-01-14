from math import factorial

import numpy as np

fact_21 = factorial(21)
if fact_21 > np.iinfo(np.int64).max:
    raise OverflowError("Factorial result is too large for a NumPy int64.")
