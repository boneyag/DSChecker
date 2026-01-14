import seaborn as sns

data = sns.load_dataset('tips')

sns.distplot(data.tip, norm_hist=False)
