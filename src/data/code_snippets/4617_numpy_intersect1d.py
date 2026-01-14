import numpy as np

np.random.seed(42)

arr1 = np.arange(1000)
arr2 = np.arange(1000)

result = np.intersect1d(arr1, arr2)
