import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter, datestr2num

days = [
    "30/01/2019",
    "31/01/2019",
    "01/02/2019",
    "02/02/2019",
    "03/02/2019",
    "04/02/2019",
]
y = [1, 9, 10, 3, 7, 6]

x = [datestr2num(day) for day in days]

fig, ax = plt.subplots()
sns.lineplot(x=x, y=y, ax=ax)
ax.xaxis.set_major_formatter(DateFormatter("%d/%m/%Y"))

plt.show()
