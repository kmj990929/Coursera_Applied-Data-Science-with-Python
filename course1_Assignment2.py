
# coding: utf-8

# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[2]:


import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[2]:


# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 


# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[3]:


def answer_one():
    i = 0
    while df['Gold'][i] != max(df['Gold']):
        i+=1
    return df.index[i]


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[4]:


def answer_two():
    max_m = 0
    max_i = 0
    for i in range(len(df)):
        summer = df['Gold'][i]
        winter = df['Gold.1'][i]
        if(summer >= winter):
            if (max_m < summer-winter):
                max_m = summer-winter
                max_i = i
        else:
            if (max_m < winter-summer):
                max_m = winter-summer
                max_i = i
    return df.index[max_i]


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[5]:


def answer_three():
    max_result = 0
    max_i = 0
    for i in range(len(df)):
        summer = df['Gold'][i]
        winter = df['Gold.1'][i]
        total = summer+winter
        if(summer != 0 and winter != 0):
            result = (summer-winter)/total
            if (result > max_result):
                max_result = result
                max_i = i
    return df.index[max_i]


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created, with the country names as indices.
# 
# *This function should return a Series named `Points` of length 146*

# In[6]:


def answer_four():
    name = df.index
    lst = []
    for i in range(len(df)):
        result = df['Gold.2'][i]*3 + df['Silver.2'][i]*2 + df['Bronze.2'][i]
        lst.append(result)
    Points = pd.Series(lst,index=name)
    return Points


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2015/co-est2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

# In[6]:


census_df = pd.read_csv('census.csv')
census_df.head()


# In[8]:


def answer_five():
    name_lst = []
    num_lst = []
    count = 0
    for i in range(len(census_df)):
        if(census_df['SUMLEV'][i] == 40):
            if(i!=0):
                num_lst.append(count)
            name_lst.append(census_df['STNAME'][i])
            count = 0
        else:
            count += 1
    num_lst.append(count)
    
    max_m = 0
    max_j = 0
    for j in range(len(name_lst)):
        if(max_m < num_lst[j]):
            max_m = num_lst[j]
            max_j = j
    return name_lst[max_j]


# ### Question 6
# **Only looking at the three most populous counties for each state**, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 
# *This function should return a list of string values.*

# In[8]:


def answer_six():
    #초기 세팅
    lst = [0,0,0] # three most populous counties for each state (인구수)
    pop_sum = 0 # three most populous counties의 인구수 합
    result_num = [0,0,0] # three most populous states (인구수)
    result_lst = ["", "", ""] # three most populous states (이름)
    
    
    #state 행 - 해당 state에 속한 county 행 - state 행 - ... 순서로 data가 구성되어 있음
    name = census_df['STNAME'][0] # 현재 확인하고 있는 state의 이름
    
    for i in range(len(census_df)): # 전체 행에 대해,
        
        if(census_df['SUMLEV'][i] == 40): # state 행일 경우
            pop_sum = lst[0] + lst[1] + lst[2] # top 3개 county의 인구수 합 계산
            
            # 전체 state에서 pop_sum이 top3에 속하는지 검사
            if(pop_sum > result_num[2]):
                if(pop_sum > result_num[1]):
                    if(pop_sum > result_num[0]):
                        result_num = [pop_sum, result_num[0], result_num[1]]
                        result_lst = [name, result_lst[0], result_lst[1]]
                    else:
                        result_num = [result_num[0], pop_sum, result_num[1]]
                        result_lst = [result_lst[0], name, result_lst[1]]
                else:
                    result_num[2] = pop_sum
                    result_lst[2] = name
                    
            # 새로운 state에 대해 계산하기 위해 lst, name 값 초기화
            lst = [0,0,0]
            name = census_df['STNAME'][i]
            
        else: # county 행일 경우
            # 해당 state에 속하는 county 중 해당 county의 인구수가 top3에 속하는지 검사
            if(census_df['CENSUS2010POP'][i] > lst[2]):
                if(census_df['CENSUS2010POP'][i] > lst[1]):
                    if(census_df['CENSUS2010POP'][i] > lst[0]):
                        lst = [census_df['CENSUS2010POP'][i], lst[0], lst[1]]
                    else:
                        lst = [lst[0], census_df['CENSUS2010POP'][i], lst[1]]
                else:
                    lst[2] = census_df['CENSUS2010POP'][i]
                    
    # 마지막 state의 경우 top3에 속하는지 계산하지 못했으므로,(바로 for문을 빠져나와서) for문 밖에서 한 번 더 top3에 속하는지 검사
    pop_sum = lst[0] + lst[1] + lst[2]
    if(pop_sum > result_num[2]):
        if(pop_sum > result_num[1]):
            if(pop_sum > result_num[0]):
                result_num = [pop_sum, result_num[0], result_num[1]]
                result_lst = [name, result_lst[0], result_lst[1]]
            else:
                result_num = [result_num[0], pop_sum, result_num[1]]
                result_lst = [result_lst[0], name, result_lst[1]]
        else:
            result_num[2] = pop_sum
            result_lst[2] = name
            
            
    return result_lst #top3 state 이름 반환


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 
# *This function should return a single string value.*

# In[10]:


def answer_seven():
    max_result = 0
    result_name = ""
    for i in range(len(census_df)):
        if(census_df['SUMLEV'][i] == 50):
            small = census_df['POPESTIMATE2010'][i]
            big = census_df['POPESTIMATE2010'][i]
            for j in range(2011, 2016):
                title = 'POPESTIMATE'
                title += str(j)
                if(small > census_df[title][i]):
                    small = census_df[title][i]
                if(big < census_df[title][i]):
                    big = census_df[title][i]
            result = big-small
            if(max_result < result):
                max_result = result
                result_name = census_df['CTYNAME'][i]
    return result_name


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[11]:


def answer_eight():
    stname_lst = []
    ctyname_lst = []
    index_id = []
    for i in range(len(census_df)):
        if(census_df['REGION'][i] == 1 or census_df['REGION'][i] == 2):
            if(census_df['CTYNAME'][i].startswith("Washington")):
                if(census_df['POPESTIMATE2015'][i] > census_df['POPESTIMATE2014'][i]):
                    stname_lst.append(census_df['STNAME'][i])
                    ctyname_lst.append(census_df['CTYNAME'][i])
    result = {'STNAME': stname_lst,
            'CTYNAME': ctyname_lst}
    result_dataframe = pd.DataFrame(result)
    return result_dataframe

