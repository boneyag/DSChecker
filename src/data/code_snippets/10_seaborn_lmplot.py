import seaborn as sns

tips = sns.load_dataset('tips')

g = sns.FacetGrid(data=tips, col='time', row='sex')
g.map(sns.lmplot, 'total_bill', 'tip')
