import numpy as np

arr = np.ones((3, 4))

for i in range(len(arr)):
    arr[i] = np.insert(arr[i], 1, 3)
