import numpy as np

x = np.array([[-1, 2, 3], [-4, -2, 8]], dtype=np.float32)

initial_value = None
where_value = np.ones(x.shape, dtype=bool)

res = np.amin(
    a=x, axis=1, keepdims=False, initial=initial_value, where=where_value, out=None
)
print(res)
