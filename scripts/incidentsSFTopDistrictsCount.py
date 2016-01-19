from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

__top__ = 5

# load data
sanFIncidents = pd.read_csv('sanfrancisco_incidents_summer_2014.csv')
# compute count of incidents per district
districtCount = sanFIncidents.groupby('PdDistrict').count()
# keep only the top==__top__ districts
districtCount = districtCount.sort_values(
        'IncidntNum', ascending=False).head(__top__)
# filter out the incidents that happened outside of the top freq districts
sanFIncidents = sanFIncidents[sanFIncidents['PdDistrict'].isin(
        districtCount.index.values)]
# compute count of incidents per incident Category
categoryCount = sanFIncidents.groupby('Category').count()
total = sum(categoryCount['IncidntNum'])
categoryCount['IncidntNum'] = categoryCount['IncidntNum'].apply(
                        lambda count:  count / total)
districts = ''
for district in districtCount.index.values:
    districts = districts + str(district) + ', '
districts = districts[:-2]
title = ('Incidents for districts ' + districts + ' per incident category')

y_pos = np.arange(len(categoryCount.index.values))
plt.barh(y_pos, categoryCount['IncidntNum'])
plt.yticks(y_pos, categoryCount.index.values)
plt.xlabel('Percantile contribution %')
plt.title(title)
plt.show()
