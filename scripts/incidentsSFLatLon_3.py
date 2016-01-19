import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


sanfIncidents = pd.read_csv('sanfrancisco_incidents_summer_2014.csv')
sb.jointplot('X', 'Y', data=sanfIncidents, color='r', kind='hex')

plt.show()
