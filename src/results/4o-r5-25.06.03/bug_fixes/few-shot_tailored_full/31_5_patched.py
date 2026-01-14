import matplotlib.pyplot as plt
import seaborn as sns

iris = sns.load_dataset("iris")
print(type(iris))
fig, ax = plt.subplots(figsize=(5, 10))

ax.axvspan(4.5, 7.5, color="red", alpha=0.3, label="Problem Area")
sns.scatterplot(x="sepal_length", y="sepal_width", data=iris, color="green", ax=ax)
plt.show()
