import matplotlib.pyplot as plt
from matplotlib.dates import datestr2num, DateFormatter
import seaborn as sns

days = ['30/01/2019', '31/01/2019', '01/02/2019', '02/02/2019', '03/02/2019', '04/02/2019']
y = [1, 9, 10, 3, 7, 6]

x = datestr2num(days)

fig, ax = plt.subplots()
sns.lineplot(x=x, y=y, ax=ax)
ax.xaxis.set_major_formatter(DateFormatter("%d/%m/%Y"))

plt.show()
