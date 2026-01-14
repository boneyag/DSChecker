import matplotlib.pyplot as plt
import seaborn as sbn

tips = sbn.load_dataset("tips")

fig, ax = plt.subplots(figsize=(5, 6))
sbn.scatterplot(data=tips, x="total_bill", y="tip", ax=ax)
ax.legend(["Total Bill vs Tip"])
plt.show()
