import seaborn as sns

tips = sns.load_dataset('tips')

tips_new = tips.drop(['sex', 'smoker', 'time','total_bill'], axis=1)
df_heatmap = tips_new.pivot_table("tip", "day", "size")

g = sns.heatmap(df_heatmap, square=True, cbar_kws={'fraction': 0.01}, cmap='OrRd', linewidth=1)
