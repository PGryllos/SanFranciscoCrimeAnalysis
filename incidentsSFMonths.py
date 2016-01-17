from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime


labels = {6: 'June', 7: 'July', 8: 'August'}

inc = pd.read_csv('sanfrancisco_incidents_summer_2014.csv',
                  na_values=['', ' '])
inc.dropna()

inc['Date'] = inc['Date'].apply(
            lambda date: int(date.split('/')[0]))

incCount = inc.groupby('Date').count()
incCount['Month'] = incCount.index

incCount['Month'] = incCount['Month'].apply(
            lambda month: labels[month])

sns.set_style("whitegrid")
sns.barplot(x='Month', y='IncidntNum', data=incCount, color='salmon',
            saturation=.5)
plt.ylabel('Count of incidents')
plt.title('Count of incidents per month of summer 2014')
plt.show()
