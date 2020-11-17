#!/usr/bin/env python
# coding: utf-8

# # Cohort analysis: Customer purchase behaviour
# 
# In this exercise a time based cohort analysis has been performed to see the customers purchase activity. Customers are grouped into cohort, based on their month of their first purchase and then calculte the number of month since the first purchase. Retention are then calculated and plotted on a heatmap.
# 
# ### Table content
# * Exporatory data analysis (EDA)
# * Data cleaning and manipulation 
# * Cohort analysis
# * Conslusion

# In[1]:


import pandas as pd 
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt #import datetime as dt
import seaborn as sns


df = pd.read_excel('Online Retail.xlsx')


# In[2]:


def get_month(x):
    """
    Input parameter: Date from the InvoiceDate column
    Output parameter: Truncates a given Incoive date to first day of the month
    """
   
    return dt(x.year, x.month, 1)

def get_date_int(df,column):
    """
    Input paramter: dataframe(df) and date column(column)
    Output: Get the date parts that is year, month and day
    """
    year = df[column].dt.year
    month = df[column].dt.month
    day = df[column].dt.day
    
    return year, month, day


def size_cohort(dic,date):
    """
    Input paramter: 1st paramter: A dictionary where the keys are the dates and the values are the cohort size
                    2nd paramter: The date that will be used as a key in the dictionary
    Output paramter: The cohort size of a specific date
    """
  
    return dic.get(date)


# # Exploratory Data Analysis (EDA)

# In[3]:


df.info()


# In[4]:


df.isnull().sum()


# In[5]:


df[ df.isnull().any(axis=1)]


# In[6]:


df = df.dropna()
df.info()


# In[7]:


# Descriptive statistics
df.describe()


# In[8]:


purchase_country = df.groupby('Country')['CustomerID'].count().sort_values()
plt.figure(figsize=(8,6))
sns.barplot(x=purchase_country.values,y=purchase_country.index)
plt.title('Number of customers')
plt.show()


# In[9]:


purchase_customer = df.groupby(['CustomerID','Country'])['InvoiceNo'].count().sort_values(ascending=False)[:10]
plt.figure(figsize=(8,6))
sns.barplot(x=purchase_customer.values, y=purchase_customer.index)
plt.title('Top 10 purchase customer')
plt.xlabel('Amount of purchase')
plt.ylabel('CustomerID and Country')


# In[10]:


df_item_price = df[df['Quantity'] >0].sort_values(ascending=False, by='UnitPrice')
df_item_price.set_index('Description')['UnitPrice'][:20].plot.bar()
plt.title('Top 20 most expensive purchase')
plt.show()


# In[82]:


# Add boxplot and histogram
f, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.30, 0.5)})

sns.boxplot(df_item_price['UnitPrice'], ax=ax_box)
sns.distplot(df_item_price['UnitPrice'], ax=ax_hist,kde=False)
plt.suptitle('Boxplot and histogram')
plt.show()


# The UnitPrice range is very wide with many outliers which cause the histogram to be scewed. 

# # Data manipulation

# In[84]:


# Create two data frames, one for purchase and one for refund
# We will only use purchase

df_purchase =  df[df['Quantity'] > 0].copy()
df_refund = df[df['Quantity'] < 0].copy()


# In[85]:


# Convert object to date
df_purchase['InvoiceDate'] = pd.to_datetime(df_purchase['InvoiceDate']).dt.date


# In[86]:


# Get invoice month for every purchase

df_purchase['InvoiceMonth'] = df_purchase['InvoiceDate'].apply(get_month)
df_purchase.tail()


# In[87]:


# First purchase for respectively customer
df_purchase['StartingMonth'] = df_purchase.groupby('CustomerID')['InvoiceMonth'].transform('min')
df_purchase['StartingMonth'] = pd.to_datetime(df_purchase['StartingMonth'])
df_purchase.tail()


# In[88]:


# Get the date parts from the InvoiceMonth column
invoice_year, invoice_month, invoice_day = get_date_int(df_purchase,'InvoiceMonth')

# Get the date parts from the StartingtMonth column
cohort_year, cohort_month, cohort_day = get_date_int(df_purchase,'StartingMonth')

# Caclulate difference in year, month and day respectively
yrs_diff = invoice_year - cohort_year
mons_diff = invoice_month - cohort_month
days_diff = invoice_day - cohort_day

# Column for Number of month passed
df_purchase['MonthsPassed'] = yrs_diff * 12 + mons_diff
df_purchase.tail()


# In[104]:


#Count number of unique values in CustomerID
grouping = df_purchase.groupby(['StartingMonth','MonthsPassed'])
cohort_data = grouping['CustomerID'].nunique().reset_index() 
cohort_data


# In[105]:


# Create a dictionary of cohort size for each month,i.e. initial month, MonthsPassed = 0
cohort_sizes= cohort_data[cohort_data['MonthsPassed'] == 0].drop('MonthsPassed',axis=1).set_index('StartingMonth')
cohort_sizes.index=cohort_sizes.index.strftime('%Y-%m-%d')
dict_cohort_sizes = cohort_sizes['CustomerID'].to_dict()
dict_cohort_sizes


# In[91]:


# Number of customer for respectively StartingMonth row

# Convert the values in StartingMonth column for 
cohort_data['StartingMonth']= cohort_data['StartingMonth'].astype(str)

cohort_data['NumCustomer'] = cohort_data.apply(lambda x: 
                                               size_cohort(dict_cohort_sizes,x['StartingMonth']),
                                               axis=1)
cohort_data.tail()


# # Cohort analysis 

# In[94]:


# Create pivot table
cohort_counts = cohort_data.pivot(index=['StartingMonth','NumCustomer'],
                                  columns='MonthsPassed',
                                  values='CustomerID')


# Calculate the percentage retension
retention = cohort_counts.divide(cohort_sizes.values,axis=0)
retention = retention.round(3)*100

retention.style.background_gradient(cmap="Greens", vmax=50,vmin=0)


# In[98]:


df_purchase_uk = df_purchase[df_purchase['Country'] == 'United Kingdom'].copy()
df_purchase_uk['StartingMonth'] = df_purchase_uk.groupby('CustomerID')['InvoiceMonth'].transform('min')
df_purchase_uk['StartingMonth'] = pd.to_datetime(df_purchase_uk['StartingMonth'])

# Get the date parts from the InvoiceMonth column
invoice_year, invoice_month, invoice_day = get_date_int(df_purchase_uk,'InvoiceMonth')

# Get the date parts from the StartingtMonth column
cohort_year, cohort_month, cohort_day = get_date_int(df_purchase_uk,'StartingMonth')

# Caclulate difference in year, month and day respectively
yrs_diff = invoice_year - cohort_year
mons_diff = invoice_month - cohort_month
days_diff = invoice_day - cohort_day

# Column for Number of month passed
df_purchase_uk['MonthsPassed'] = yrs_diff * 12 + mons_diff

#Count number of unique values in CustomerID
grouping = df_purchase_uk.groupby(['StartingMonth','MonthsPassed'])
cohort_data = grouping['CustomerID'].nunique().reset_index() 


# Create a dictionary of cohort size for each month,i.e. initial month, MonthsPassed = 0
cohort_sizes= cohort_data[cohort_data['MonthsPassed'] == 0].drop('MonthsPassed',axis=1).set_index('StartingMonth')
cohort_sizes.index=cohort_sizes.index.strftime('%Y-%m-%d')
dict_cohort_sizes = cohort_sizes['CustomerID'].to_dict()

cohort_data['StartingMonth']= cohort_data['StartingMonth'].astype(str)
cohort_data['NumCustomer'] = cohort_data.apply(lambda x: 
                                               size_cohort(dict_cohort_sizes,x['StartingMonth']),
                                               axis=1)

cohort_counts = cohort_data.pivot(index=['StartingMonth','NumCustomer'],
                                  columns='MonthsPassed',
                                  values='CustomerID')


# In[100]:


# Calculate the percentage retension for UK customer
retention = cohort_counts.divide(cohort_sizes.values,axis=0)
retention
retention=retention.round(3)*100

#cm = sns.light_palette("seagreen", as_cmap=True)
retention.style.background_gradient(cmap="Greens", vmax=50,vmin=0)


# # Conclusion
# Cohort analysis have been performed on international customer and UK customer. The trend is clear for both cohort analysis, that is the churn is more than 60% after first month of purchase. EDA shows that data for UK customers are dominating in the data set. That explains also the behaviour of the two cohort analysis. Since number of purchase is much smaller for the other countries, cohort analysis have not been performed. There is no additional data that can explain this high churn rate. However, customer who purchased during december month have less churn rate compared to the other groups. It seems like these customers were more satisfied compared to the other groups and the retension rate is fairly stable compared tothe other groups as well. 
# 

# In[ ]:




