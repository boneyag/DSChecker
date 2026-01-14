import os

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, "34_1_data.csv")

df = pd.read_csv(csv_file_path, header=0)

impt = SimpleImputer(missing_values=np.nan, strategy="mean")

imp_array = impt.fit_transform(df)

print(imp_array[:, 1])
