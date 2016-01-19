from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb


sanfIncidents = pd.read_csv('sanfrancisco_incidents_summer_2014.csv')

districtCount = sanfIncidents.groupby('PdDistrict').count()
y_pos = np.arange(len(districtCount.index.values))
total = sum(districtCount['IncidntNum'])
districtCount['IncidntNum'] = districtCount['IncidntNum'].apply(
                        lambda count:  count / total)

plt.barh(y_pos, districtCount['IncidntNum'])
plt.yticks(y_pos, districtCount.index.values)
plt.xlabel('Percantile contribution %')
plt.title(
    'Incidents in San Francisco, per district, for Summer 2014')
plt.show()
