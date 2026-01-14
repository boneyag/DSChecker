import numpy as np

x = np.array([[-1, 2, 3], [-4, -2, 8]], dtype=np.float32)

initial_value = None
where_value = None

res = np.amin(
    a=x, axis=1, keepdims=False, initial=0, where=np.ones_like(x, dtype=bool), out=None
)
print(res)
