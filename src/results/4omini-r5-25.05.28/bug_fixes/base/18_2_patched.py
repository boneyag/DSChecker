import seaborn as sns

data = sns.load_dataset("tips")

sns.histplot(data=data, x="tip", stat="density", bins=30)
