import numpy as np
import pandas as pd

np.random.seed(123)
df = pd.DataFrame(np.random.randint(0, 100, (5, 4)), columns=list("ABCD"))

df.loc[1:3, "B"] = 2
print(df)
