import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb


sanfIncidents = pd.read_csv('sanfrancisco_incidents_summer_2014.csv')

districtCount = sanfIncidents.groupby('PdDistrict').count()
y_pos = np.arange(len(districtCount.index.values))
plt.barh(y_pos, districtCount['IncidntNum'])
plt.yticks(y_pos, districtCount.index.values)
plt.title('Amount of incidents in San Francisco, per district, for Summer 2014')
plt.show()
