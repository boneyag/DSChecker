import numpy as np

x = np.array([[-1, 2, 3], [-4, -2, 8]], dtype=np.float32)

where_value = np.ones_like(x, dtype=np.bool_)
initial_value = np.inf

res = np.amin(
    a=x, axis=1, keepdims=False, initial=initial_value, where=where_value, out=None
)
print(res)
