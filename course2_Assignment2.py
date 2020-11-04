
# coding: utf-8

# # Assignment 2

# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[53]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[3]:

pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(400))


# In[145]:

import numpy as np

totdata= pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

totdata = totdata[['Date', 'Element', 'Data_Value']]

#윤일 삭제
totdata['Year'] = totdata['Date'].str[:4]
totdata['Day'] = totdata['Date'].str[5:]
totdata = totdata.where(totdata['Day']!='02-29').dropna().reset_index(drop=True)

#~2014 / 2015 분리
before2014 = totdata[totdata['Year']!='2015']
year2015 = totdata[totdata['Year']=='2015']

#max min 분리
before2014_max = before2014[before2014['Element']=='TMAX']
before2014_min = before2014[before2014['Element']=='TMIN']
year2015_max = year2015[year2015['Element']=='TMAX']
year2015_min = year2015[year2015['Element']=='TMIN']
    
#sorting
before2014_max = before2014_max.set_index("Day").groupby(level=0)['Data_Value'].agg({'max_value' : max}).reset_index()
before2014_min = before2014_min.set_index("Day").groupby(level=0)['Data_Value'].agg({'min_value' : min}).reset_index()
year2015_max = year2015_max.set_index("Day").groupby(level=0)['Data_Value'].agg({'max_value' : max}).reset_index()
year2015_min = year2015_min.set_index("Day").groupby(level=0)['Data_Value'].agg({'min_value' : min}).reset_index()

#그래프 그리기
plt.figure(figsize = [16,9])

plt.plot(before2014_max['max_value']/10, color = 'lightcoral')
plt.plot(before2014_min['min_value']/10, color = 'skyblue')

plt.xlabel('Date')
plt.ylabel('Temperature(°C)')
plt.title('Temperature in Ann Arbour, Michigan, United States (2005-2015)')

plt.gca().fill_between(range(len(before2014_max['max_value'])),
                       before2014_max['max_value']/10,((before2014_min['min_value']/10)+(before2014_max['max_value']/10))/2,alpha = 0.04, color = 'red')
plt.gca().fill_between(range(len(before2014_max['max_value'])),
                       before2014_min['min_value']/10,((before2014_min['min_value']/10)+(before2014_max['max_value']/10))/2,alpha = 0.04, color = 'blue')
#2015년 점 찍기
year2015_max = year2015_max.where(year2015_max['max_value'] > before2014_max['max_value']).dropna()
year2015_min = year2015_min.where(year2015_min['min_value'] < before2014_min['min_value']).dropna()

plt.plot(year2015_max['max_value']/10, 'or', ms = 4)
plt.plot(year2015_min['min_value']/10,'ob', ms = 4)

plt.legend(['High Temperature (2005-2014)','Low Temperature (2005-2014)','High Temperature (2015)','Low Temperature (2015)'])

month_starts = [1,32,61,92,122,153,183,214,245,275,306,336]
month_names = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec'] 

plt.gca().set_xticks(month_starts)
plt.gca().set_xticklabels(month_names)

plt.show()

