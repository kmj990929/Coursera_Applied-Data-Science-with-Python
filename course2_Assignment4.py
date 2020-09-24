
# coding: utf-8

# # Assignment 4
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# This assignment requires that you to find **at least** two datasets on the web which are related, and that you visualize these datasets to answer a question with the broad topic of **sports or athletics** (see below) for the region of **Ann Arbor, Michigan, United States**, or **United States** more broadly.
# 
# You can merge these datasets with data from different regions if you like! For instance, you might want to compare **Ann Arbor, Michigan, United States** to Ann Arbor, USA. In that case at least one source file must be about **Ann Arbor, Michigan, United States**.
# 
# You are welcome to choose datasets at your discretion, but keep in mind **they will be shared with your peers**, so choose appropriate datasets. Sensitive, confidential, illicit, and proprietary materials are not good choices for datasets for this assignment. You are welcome to upload datasets of your own as well, and link to them using a third party repository such as github, bitbucket, pastebin, etc. Please be aware of the Coursera terms of service with respect to intellectual property.
# 
# Also, you are welcome to preserve data in its original language, but for the purposes of grading you should provide english translations. You are welcome to provide multiple visuals in different languages if you would like!
# 
# As this assignment is for the whole course, you must incorporate principles discussed in the first week, such as having as high data-ink ratio (Tufte) and aligning with Cairo’s principles of truth, beauty, function, and insight.
# 
# Here are the assignment instructions:
# 
#  * State the region and the domain category that your data sets are about (e.g., **Ann Arbor, Michigan, United States** and **sports or athletics**).
#  * You must state a question about the domain category and region that you identified as being interesting.
#  * You must provide at least two links to available datasets. These could be links to files such as CSV or Excel files, or links to websites which might have data in tabular form, such as Wikipedia pages.
#  * You must upload an image which addresses the research question you stated. In addition to addressing the question, this visual should follow Cairo's principles of truthfulness, functionality, beauty, and insightfulness.
#  * You must contribute a short (1-2 paragraph) written justification of how your visualization addresses your stated research question.
# 
# What do we mean by **sports or athletics**?  For this category we are interested in sporting events or athletics broadly, please feel free to creatively interpret the category when building your research question!
# 
# ## Tips
# * Wikipedia is an excellent source of data, and I strongly encourage you to explore it for new data sources.
# * Many governments run open data initiatives at the city, region, and country levels, and these are wonderful resources for localized data sources.
# * Several international agencies, such as the [United Nations](http://data.un.org/), the [World Bank](http://data.worldbank.org/), the [Global Open Data Index](http://index.okfn.org/place/) are other great places to look for data.
# * This assignment requires you to convert and clean datafiles. Check out the discussion forums for tips on how to do this from various sources, and share your successes with your fellow students!
# 
# ## Example
# Looking for an example? Here's what our course assistant put together for the **Ann Arbor, MI, USA** area using **sports and athletics** as the topic. [Example Solution File](./readonly/Assignment4_example.pdf)

# In[176]:

import pandas as pd
import matplotlib.pyplot as plt

#파일 읽기
lions = pd.read_csv('Lions.csv')
tigers = pd.read_csv('Tigers.csv')
pistons = pd.read_csv('Pistons.csv')
red_wings = pd.read_csv('Red wings.csv')


#파일 연도, 순위만 자르기
lions = lions[['NFL season', 'Regular season']][1:96]
tigers = tigers[['Season', 'Finish']]
pistons = pistons[['NBA Season', 'Finish']]
red_wings = red_wings[['NHL season', 'regular season']][1:]


#연도 형식 맞추고 index로 만들기
def index_format(group):
    group = group.dropna()
    group.columns = ['Year', 'Finish']
    group['Finish'] = group['Finish'].str.replace('[^0-9]','').astype(int)
    group = group.where(group['Finish'] <= 8).dropna()
    return group

lions = index_format(lions)
lions[['Year']] = lions[['Year']].astype(int)
tigers = index_format(tigers)
pistons = index_format(pistons)
pistons['Year'] = pistons['Year'].str[:4].astype(int)
red_wings = index_format(red_wings)
red_wings['Year'] = red_wings['Year'].str[:4].astype(int)

lions = lions.where(lions['Year'] >=1970).dropna()
tigers = tigers.where(tigers['Year'] >=1970).dropna()
pistons = pistons.where(pistons['Year'] >=1970).dropna()
red_wings = red_wings.where(red_wings['Year'] >=1970).dropna()

lions = lions.set_index('Year')
tigers = tigers.set_index('Year')
pistons = pistons.set_index('Year')
red_wings = red_wings.set_index('Year')


#그래프 그리기
plt.figure(figsize = [16,9])
plt.plot(lions,'-o')
plt.plot(tigers,'-o')
plt.plot(pistons,'-o')
plt.plot(red_wings,'-o')

plt.xlabel('Season')
plt.ylabel('Final position in division or league standings (< 8)')
plt.title('Detroit Spots Teams ranking')

plt.legend(['lions', 'tigers','pistons','red_wings'])

plt.gca().invert_yaxis()
plt.show()


# In[ ]:



