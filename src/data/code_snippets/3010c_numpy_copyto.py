import numpy as np

np.random.seed(42)

size = 1000000
a = np.random.rand(size)
cp = np.random.rand(size)
mask = np.random.randint(2, size=size, dtype=bool)

np.copyto(a, cp, where=mask)
