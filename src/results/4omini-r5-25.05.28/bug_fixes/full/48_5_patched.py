import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

file_list = [
    os.path.join(root, file)
    for root, _, files in os.walk("48_data")
    for file in files
    if file.endswith(".csv")
]

for file in file_list:
    with open(file) as f:
        df = pd.read_csv(f, header=0, skipinitialspace=True)
    plt.figure()
    fig_name = os.path.splitext(file)[0]
    plt.savefig(f"{fig_name}.png")
