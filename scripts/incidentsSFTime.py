import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


inc = pd.read_csv('sanfrancisco_incidents_summer_2014.csv',
                  na_values=['', ' '])
inc.dropna()

inc['Time'] = inc['Time'].apply(
            lambda dt: int(dt.split(':')[0]))

incCount = inc.groupby('Time').count()
incCount['Time'] = incCount.index
sns.set_style("whitegrid")

plt.plot(incCount['Time'], incCount['IncidntNum'], '-')
plt.ylabel('Count of incidents')
plt.xlabel('hour of the day')
plt.title('Count of incidents per hour of the day')
plt.show()
