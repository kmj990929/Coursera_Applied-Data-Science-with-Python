
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[2]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[2]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[8]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    result_state = []
    result_region = []
    state_name = " "
    with open("university_towns.txt") as txt:
        origin = txt.read()
        lst1 = origin.splitlines()
        for i in range(len(lst1)):
            current = lst1[i]
            if(current.find('(') != -1):
                idx = current.find("(")            
                region_name = current[:idx].strip()
                result_state.append(state_name)
                result_region.append(region_name)
            elif(current.find("[") != -1):
                idx = current.find("[")
                state_name = current[:idx]


                
    dataframe_set = {"State":result_state, "RegionName":result_region}
    
    result_df = pd.DataFrame(dataframe_set, columns= ['State', 'RegionName'])
    
    return result_df

get_list_of_university_towns()


# In[6]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', skiprows = 7)
    gdp = gdp[[4,6]]
    gdp.columns = ['Quarterly', 'GDP in billions of chained 2009 dollars']
    gdp = gdp.where('2000q1' <= gdp['Quarterly']).dropna().reset_index(drop=True)
    
    check = 0
    for i in range(1,len(gdp)):
        if (gdp['GDP in billions of chained 2009 dollars'][i] < gdp['GDP in billions of chained 2009 dollars'][i-1]):
            if(check == 1):
                return gdp['Quarterly'][i-1]
            else:
                check = 1
        else:
            check = 0
            
    return 0

get_recession_start()


# In[7]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', skiprows = 7)
    gdp = gdp[[4,6]]
    gdp.columns = ['Quarterly', 'GDP in billions of chained 2009 dollars']
    gdp = gdp.where(get_recession_start() <= gdp['Quarterly']).dropna().reset_index(drop=True)
    
    check = 0
    for i in range(1,len(gdp)):
        if (gdp['GDP in billions of chained 2009 dollars'][i] > gdp['GDP in billions of chained 2009 dollars'][i-1]):
            if(check == 1):
                return gdp['Quarterly'][i]
            else:
                check = 1
        else:
            check = 0
            
    return 0

get_recession_end()


# In[8]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel('gdplev.xls', skiprows = 7)
    gdp = gdp[[4,6]]
    gdp.columns = ['Quarterly', 'GDP in billions of chained 2009 dollars']
    gdp = gdp.where(get_recession_start() <= gdp['Quarterly']).dropna().reset_index(drop=True)
    gdp = gdp.where(get_recession_end() >= gdp['Quarterly']).dropna().reset_index(drop=True)
    
    for i in range(1,len(gdp)):
        if (gdp['GDP in billions of chained 2009 dollars'][i] > gdp['GDP in billions of chained 2009 dollars'][i-1]):
            return gdp['Quarterly'][i-1]
    
get_recession_bottom()


# In[9]:


def quarter(date:str):
    date = date.split('-')
    month = int(date[1])
    quarter = int((month-1)/3)+1
    return date[0] + 'q' + str(quarter)
    

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    # Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
    housing_data = pd.read_csv("City_Zhvi_AllHomes.csv")
    
    column_name = ['State', 'RegionName']
    column_name += list(housing_data.columns[list(housing_data.columns).index('2000-01'):])
    
    housing_data = housing_data[column_name]
    housing_data = housing_data.replace(states)
    
    housing_data = housing_data.set_index(['State','RegionName']).sort_index()
    
    housing_data = housing_data.groupby(quarter, axis = 1).mean()
    
    return housing_data
            

convert_housing_data_to_quarters()


# In[26]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    start_point = get_recession_start()
    end_point = get_recession_bottom()
    
    housing_data = convert_housing_data_to_quarters()
    
    for i in range(len(housing_data)):
        housing_data = np.divide(housing_data.ix[:,before_rec],housing_data.ix[:,rec_bottom]).to_frame().dropna()

    university = get_list_of_university_towns()
    housing_data = housing_data.reset_index().dropna()

    university_true = []
    university_false = []
    
    university_true= housing_data.merge(university, how = 'inner', left_on = ['State', 'RegionName'], right_on = ['State', 'RegionName'])
    university_false = housing_data.merge(university, how = 'left', left_on = ['State', 'RegionName'], right_on = ['State', 'RegionName'])

    print(university_true)
    p = ttest_ind(university_true['price_ratio'], university_false['price_ratio'])
    
    if (p.pvalue < 0.01):
        ttest_bool = True
    else:
        ttest_bool = False
        
    mean_true = university_true['price_ratio'].mean()
    mean_false = university_false['price_ratio'].mean()
    better = "university town" if mean_true < mean_false else "non-university town"
    
    return (ttest_bool, p.pvalue, better)
    #return university_true, university_false

run_ttest()


# In[24]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    df = convert_housing_data_to_quarters()
    
    # Start position is the quarter BEFORE the recession starts!
    before_rec = (df.columns.get_loc(get_recession_start())-1)
    rec_bottom = df.columns.get_loc(get_recession_bottom())
    
    uni = get_list_of_university_towns().set_index(['State', 'RegionName'])
    
    # Turn the divided values into a DataFrame!
    df = np.divide(df.ix[:,before_rec],df.ix[:,rec_bottom]).to_frame().dropna()
    
    # Merge university and GDP data.
    uni_df = df.merge(uni, right_index=True, left_index=True, how='inner')
    
    # Drop the indices of uni towns to get data only for non uni towns.
    nonuni_df = df.drop(uni_df.index)
    
    # A t-test is commonly used to determine whether the mean of a population significantly
    # differs from a specific value (called the hypothesized mean) or from the mean of another population.
    p_value = ttest_ind(uni_df.values, nonuni_df.values).pvalue
    
    if p_value < 0.01:
        different=True
    else:
        different=False
        
    # Better depending on which one is LOWER! Remember prices go up during a recession so lower is better.
    if uni_df.mean().values < nonuni_df.mean().values:
        better='university town'
    else:
        better='non-university town'

    return (different, p_value[0], better)
    
run_ttest()

