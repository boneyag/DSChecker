import numpy as np

np.random.seed(42)

A = np.random.rand(100, 50)
B = np.random.rand(50, 100)

res = np.trace(np.dot(A, B))
print(res)
