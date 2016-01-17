import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

__top__ = 9

# load data
inc = pd.read_csv('sanfrancisco_incidents_summer_2014.csv')

inc['Time'] = inc['Time'].apply(
            lambda time: int(time.split(':')[0]))
catCount = inc.groupby('Category').count()
catCount = catCount.sort_values(
           'IncidntNum', ascending=False).head(__top__)
# filter out the incidents that do not belong in the top freq categories
inc = inc.loc[inc['Category'].isin(catCount.index.values)]
inc = inc.groupby(['Time', 'Category']).count()
categories = pd.DataFrame(columns=[cat for cat in catCount.index.values])

for cat in catCount.index.values:
    for i in range(0, 24):
        categories.loc[i, cat] = inc.ix[(i, cat), 1]

fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(9, 9))
sb.set_style("whitegrid")

for i in [0, 1, 2]:
    for j in [0, 1, 2]:
        axes[i, j].plot(categories.index.values, categories.ix[:, i*3+j])
        axes[i, j].set_title(catCount.index[i*3+j])

fig.subplots_adjust(hspace=0.4)
plt.show()
