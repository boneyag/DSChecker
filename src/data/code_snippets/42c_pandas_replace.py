import pandas as pd

df = pd.DataFrame({
    'l1': [1, 2, 3, 4, 5, 6, 7],
    'l2': ['a. 12', 'b. 75', '23', 'sc/a 34', '85', 'a 32', 'b 345']
})

df['l2'].replace(to_replace=r'^\d+$', value=0, regex=True, inplace=True)
