import numpy as np

arr = np.ones((3, 4))

for i in range(len(arr)):
    arr = np.insert(arr, i, 3, axis=1)
