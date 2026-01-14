import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': ['10', '20', '30', '40'],
    'C': [True, False, True, True]
})

df.set_index('A')
print(df.loc[4])
