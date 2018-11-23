#!/usr/bin/env python
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
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

# In[ ]:





# In[1]:


import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib as mpl
import matplotlib.ticker as ticker


# In[2]:


d_v='Data_Value'
d_t='Date'


# In[3]:


df = pd.read_csv('data.csv')


# In[4]:


df.loc[:,d_v]*=0.1


# In[5]:


df['day']=pd.DatetimeIndex(df[d_t]).day
df['month']=pd.DatetimeIndex(df[d_t]).month
df=df.set_index(['month','day'])
df=df.sort_index()
df.head()


# In[6]:


not_required_df=df.loc[2,29]
not_required_df.head()


# In[7]:


df=df[~df.index.isin(not_required_df.index)]
df['Year']=pd.DatetimeIndex(df[d_t]).year
df_2015=df[df['Year']==2015]
df=df[df['Year']!=2015]


# In[8]:


max_temp_df = df[df['Element'] == 'TMAX']
min_temp_df = df[df['Element'] == 'TMIN'] 


# In[9]:


myLevel=['month','day']
max_temp = max_temp_df.groupby(level = myLevel)[d_v].max()  
min_temp = min_temp_df.groupby(level = myLevel)[d_v].min()


# In[10]:


max_temp_df_2015 = df_2015[df_2015['Element'] == 'TMAX']
min_temp_df_2015 = df_2015[df_2015['Element'] == 'TMIN'] 


# In[11]:


myList=[d_t,d_v]

max_temp_df_2015 = max_temp_df_2015.groupby(level = myLevel).max()[myList]
min_temp_df_2015 = min_temp_df_2015.groupby(level = myLevel).min()[myList]


# In[12]:


date_range = df_2015[d_t].unique()
date_range[5]


# In[13]:



fig, ax = plt.subplots( nrows=1, ncols=1, figsize = (10,5) ) 
ax.set_title('Ann Arbor, Michigan, United States Temperatures (2005-2014) and 2015')
ax.yaxis.grid()


# In[14]:


len(date_range),len(max_temp.values)


# In[ ]:





# In[ ]:





# In[15]:


plt.plot(date_range, max_temp.values, '#F00000', linewidth = 1.0, alpha=0.75, label = 'Highs from  2005-2014')

plt.plot(date_range, min_temp.values, '#000000', linewidth = 1, alpha=0.75, label = 'Lows from 2005-2014 ')


# In[16]:


plt.fill_between(date_range, min_temp, max_temp, facecolor='#0000ff')


# In[17]:


plt.legend(loc = 1).get_frame().set_edgecolor('white') 
label_max = "Highs of 2015 "
label_min = "Lows of 2015 "
count=0
for idx, rows in max_temp_df_2015.iterrows():
   if rows[d_v] > max_temp.loc[idx]:
       count+=1
       if count==1:
          plt.scatter(rows[d_t], rows[d_v], c = '#ff00fb', marker = '.', label = label_max)
       else:
          plt.scatter(rows[d_t], rows[d_v], c = '#ff00fb', marker = '.')
       my_label_max = "_nolegend_"
count=0
for idx, rows in min_temp_df_2015.iterrows():
   if rows[d_v] < min_temp.loc[idx]:
       count+=1
       if count==1:
          plt.scatter(rows[d_t], rows[d_v], c = '#bbbbbf', marker = '.', label = label_min)
       else :
          plt.scatter(rows[d_t], rows[d_v], c = '#bbbbbf', marker = '.')
       my_label_min = "_nolegend_"
ax.legend(loc = 1).get_frame().set_edgecolor('white')
x_min, x_max = date_range[0], date_range[-1]


# In[18]:





# In[19]:


ax.set_xlim(x_min, x_max)
ax.xaxis.set_major_locator(dates.MonthLocator())
ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))
ax.xaxis.set_major_formatter(ticker.NullFormatter())
ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
xticks = ax.xaxis.get_minor_ticks()


# In[20]:


for xtick in xticks:
    xtick.tick1line.set_markersize(0)
    xtick.tick2line.set_markersize(0)
    xtick.label1.set_horizontalalignment('center')
y_min, y_max = -10, 50
ax.set_ylim(y_min, y_max) 
yticks = ax.yaxis.get_major_ticks()

for temp in range(2):
    yticks[temp].label1.set_visible(False)

    


# In[21]:


ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax2 = ax.twinx()
ax2.set_ylabel('Temperatures in  $(^{\circ}$F)')


# In[22]:


def C_to_F(temp_c): 
    return 9/5 *temp_c + 32


# In[23]:


ax2.set_ylim(C_to_F(y_min), C_to_F(y_max))
ax2.yaxis.set_major_locator(ticker.MultipleLocator(20))
ax2.yaxis.set_minor_locator(ticker.MultipleLocator(5))
fig.tight_layout()


# In[24]:


plt.show()

