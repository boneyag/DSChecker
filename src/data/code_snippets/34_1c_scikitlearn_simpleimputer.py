from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, '34_1_data.csv')

df = pd.read_csv(csv_file_path, header=0)

impt = SimpleImputer(missing_values=np.nan, strategy="constant", fill_value=0.0001)

imp_array = impt.fit_transform(df)

print(imp_array[:, 1])
