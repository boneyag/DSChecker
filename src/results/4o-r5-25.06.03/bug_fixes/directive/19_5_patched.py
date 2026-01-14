import matplotlib.pyplot as plt
import seaborn as sbn

tips = sbn.load_dataset("tips")

fig, ax = plt.subplots(figsize=(5, 6))
sbn.scatterplot(data=tips, x="total_bill", y="tip", ax=ax)
labels = tips["day"].unique()
sbn.scatterplot(data=tips, x="total_bill", y="tip", hue="day", ax=ax)
ax.legend(labels=labels)
plt.show()
