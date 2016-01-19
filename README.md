
# Crime Incident Analysis on Data from SFPD


This report summarizes my findings on the crime incident data provided freely by the SFPD through the [portal](https://data.sfgov.org/), as part of my sumbission for the _Crime Analytics_ assignment for the course __Communicating Data Science Results__ by University of Washington, Coursera.


#### important notes
 * The assumptions made for this study as well as the conclusions drawn are based on my personal intuition and abillity of interpretation, thus they should not be treated as valid scientific facts.
 * For the needs of this assignment I worked on a subset of the crime incident data that corresponds to the Summer of 2014. The scripts that supplement this report are tested upon that subset of the data and are not promised to be working on the whole dataset.

## Finding 1 

---

## Crime incidents happen more frequently near the city center

The first assumption I made was whether the incidents happen more frequently near specific areas / districts. Since each report includes the specific geo coordinates, of the place where the incident happened, it was quite convenient to start by investigating that correlation.

So, I started by plotting all the available data points using the Longitude values on the x-axis and the Latitude values on the y-axis. I also colored the data points based on the district they belong in. The script bellow produces that scatter plot.


```python
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

```

![alt text][density_1]

[density_1]: http://raw.githubusercontent.com/PGryllos/SanFranciscoCrimeAnalysis/master/figures/figure_1_density.png

The red marker incidates the coordinates of the city center.

As you may be able to see there is is an increased density of data points near the city center. I believe that it is quite apparent that the areas near the center contribute more data points in comparison to the rest but it is not so clear whether that difference is significant or not. It is also quite difficult from that plot to understand exactly which color corresponds to which district. That makes it even harder, especially for someone who is not familiar with those areas, to make an estimation of the criminal activity level of each district.

The next plot presents the distribution of data points (the two plots on top and on the right), on the two axes that were used previously (Longitute, Latitude), while also uses hue on the scatter plot to indicate areas with greater density.


```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


sanfIncidents = pd.read_csv('sanfrancisco_incidents_summer_2014.csv')
sb.jointplot('X', 'Y', data=sanfIncidents, color='r', kind='hex')

plt.show()
```

![alt text][density_2]

[density_2]: http://raw.githubusercontent.com/PGryllos/SanFranciscoCrimeAnalysis/master/figures/figure_2_density.png

By inspecting the two distribution plots, it is much easier now to be sure that there is significant difference in the density of incidents that happen near the center. Specifically the two global maximums point us at (37.783, -122.407) and we can also see that the main activity happens around that area.

But again information is not that easily infered from that plot. And that's mostly due to the use of geo coordinates, since it's very hard to have an aproximation of which district correspond to which area of the plot.

For having a clearer overview of the levels of contribution, I estimated the amount of incidents corresponding to each district and created a bar chart


```python
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
```

![alt text][density_3]

[density_3]: https://raw.githubusercontent.com/PGryllos/SanFranciscoCrimeAnalysis/master/figures/figure_3_density.png

Now we can be sure that Southern is by far the district attracting more criminal activity since it hosts nearly 20% of all incidents. We can also see that the areas around Southern, like Northern, Mission, Central and Tenderloin also belong in the high-activity zone since together they host about 65% of all incidents.

It's important to note that Tenderloin, although it's low on the percentage scale, it should definitely be considered as a high activity area. Although that didn't come up in the last plot, probably because Tenderloin is much smaller than the other districts, from the second plot it is clear that relatively to it's size it's one of the most, if not the most, active area.

Given that there exist 10 different districts, the fact that 5 of them host 65% of all criminal activity doesn's seem that striking. But, have in mind that those five districts occupy nearly 1/3 of the whole map. So, the activity on those areas should be considered significantly higher than the rest.

## Finding 2

---

## Larceny / Theft is the most frequent crime in San Francisco

Since we have identified the most active areas it would be valueable to find out what type of incidents happen in those areas. In a first attempt I created a scatter plot of the geographical distribution (similar to the first one) and colored the data points based on the incident type.


```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


marker_style = dict(linestyle=':', marker='D', markersize=5, color='red')

sanfIncidents = pd.read_csv('sanfrancisco_incidents_summer_2014.csv')
sb.lmplot('X', 'Y', data=sanfIncidents, hue='Category', fit_reg=False)

# place marker at the city center
plt.plot(-122.419416, 37.774929, **marker_style)

plt.ylabel('Latitude')
plt.xlabel('Longitude')
plt.title('San Francisco incidents summer 2014 colored by incident category')

plt.show()
```

![alt text][category_2]

[category_2]: http://raw.githubusercontent.com/PGryllos/SanFranciscoCrimeAnalysis/master/figures/figure_5_category.png

In that plot it is easy to see that the city center is dominated not by orange (Larceny/Theft) but by green and blue points. Though, it's not that easy to be sure exactly to which category corresponds each color.

For that reason I thought it would be a good idea to see exactly in what frequency each crime is happening in a district. So, I created a bar chart that showcases the percentage that each crime type occupies. The districts that are taken into account are defined by the variable `__top__`. For example if `__top__ == 1` then only Southern will be included. If `__top__ == 10` then all districts will be included. 


```python
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
```

![alt text][category_1]

[category_1]: http://raw.githubusercontent.com/PGryllos/SanFranciscoCrimeAnalysis/master/figures/figure_10_category.png

Unfortunatelly the names had to be small in order to not be cropped but you can probably see that Largency / Theft is by far the most frequent crime. Although for the plot above only the top 5, in sense of criminal activity, districts were taken into account a similar pattern is displayed if we take all districts into account. That came as a suprise since the colors indicated that of the green or blue categories should be on top. But apparently it's not.

Then why did the blue and green points pop up instead of the orange ones? Probably that's because a lot of categories are represented in the plot by colors similar to green and blue and those data points in total create that effect which gives the false sense that one of those categories is the most frequent when in reality all of those categories together constitute a big part of the criminal activity. But the most frequent category is Larceny / Theft.

## Finding 3

---

## Crime activity increases as summer evolves


```python
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
```

![alt text][month]

[month]: https://raw.githubusercontent.com/PGryllos/SanFranciscoCrimeAnalysis/master/figures/figure_6_month.png

## Finding 4

---

## San Francisco is safer during early morning hours

In a first attemp to inspect how criminal activity evolves during a whole day (24h) I categorized each incident by the value of the hour when it happened and counted the amount of incidents per hour of the day. That gave the following


```python
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
```

![alt text][month]

[month]: https://raw.githubusercontent.com/PGryllos/SanFranciscoCrimeAnalysis/master/figures/figure_7_time.png

From that plot it is obvious that the criminal activity drops during early morning hours (01-05am) and then increases until it reaches its peak late at afternoon, around 06pm. I was a bit surprised because I was expecting the exact opposite. So, I decided instead of an aggregated plot of all the categories to create a separate plot for each category that would showcase the category's evolution during a day. 

In the next script the `__top__` variable determines how many categories will be plotted based on their frequency.
If you choose to experiment with the script and set a different value for the parameter have in mind that you should also adjust the subplot axes accordingly.


```python
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
```

![alt text][month]

[month]: https://raw.githubusercontent.com/PGryllos/SanFranciscoCrimeAnalysis/master/figures/figure_8_category.png

The original finding seems to be confirmed through that plot too. As you can see all categories have a significantly lower presense during the hours around 05am. Also most categories reach their peak around the same
time late at afternoon.

The only exception to the peaking rule seems to be the category Missing Person. I suspect that this is probably happening because of the procedure that must be followed in order for a person to be declared missing. When a family wants to declare someone missing, in most countries, they have to wait until the next morning until they can do so. But this is just a guess that I haven't investigated.

Here ends my report. I hope I provided a coherent and informative post. I encourage you to install jupyter and run the scripts yourself if you haven't already done that. I wasn't familiar with the notebook at first but I found it very usefull and handy. I will more than happy to have your feedback.

Thank you for your time. Best luck with the rest of the course.

__author__ 

---
Prokopios Gryllos - gryllosprokopis@gmail.com

[density_1]: https://raw.githubusercontent.com/PGryllos/SanFranciscoCrimeAnalysis/master/figure_1_density.png "Logo Title Text 1"
[density_2]: http://raw.githubusercontent.com/PGryllos/SanFranciscoCrimeAnalysis/master/figure_2_density.png "Logo Title Text 1"
