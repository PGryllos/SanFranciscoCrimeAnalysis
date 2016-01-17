import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


marker_style = dict(color='red', linestyle=':', marker='D',
                    markersize=5)


sanfIncidents = pd.read_csv('sanfrancisco_incidents_summer_2014.csv')
sb.lmplot('X', 'Y', data=sanfIncidents, hue='PdDistrict', fit_reg=False)
plt.ylabel('Latitude')
plt.xlabel('Longitude')
plt.title('San Francisco incidents summer 2014 colored by district')

# place marker at the city center
plt.plot(-122.419416, 37.774929, **marker_style)

plt.show()
