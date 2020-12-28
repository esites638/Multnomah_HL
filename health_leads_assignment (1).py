"""Health Leads Assignment.py

Original file is located at
    https://colab.research.google.com/drive/1f_kQtB-W_3yvmybpxNEm6-WJmLBo_Hq0
"""

# SET UP

#installing libraries & importing tools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from pandas import ExcelFile
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


""" Importing data - Will need to change import paths for use on different computers """

# mount google drive to colab
from google.colab import drive
drive.mount('/content/drive')

#read in data
df_resources = pd.read_excel("/content/drive/My Drive/Health Leads/Assignment Data 2019.xlsx", sheet_name='Resources')
df_needs = pd.read_excel("/content/drive/My Drive/Health Leads/Assignment Data 2019.xlsx", sheet_name='Needs')
df_clients = pd.read_excel("/content/drive/My Drive/Health Leads/Assignment Data 2019.xlsx", sheet_name='Clients')

"""3 data sets: 

Resources: describes the resources Health Leads offers, the number of times somone has been referred to it, the zipcode of the resource, languages spoken, the type of need it addresses, and the sub-need type 

Needs: describes the needs of clients, the resources to which they were referred, and the outcome of the referral

Clients: describes clients, their demographics, insurance status, and zip code.
"""

#summarizing resources dataset
df_resources.describe(percentiles=None)
df_resources.astype('object').describe().transpose()
df_resources['Languages Spoken'].value_counts().plot(kind='bar')
df_resources['Need Type'].value_counts().plot(kind='bar')
df_resources['Languages Spoken'].value_counts().plot(kind='bar')

"""There are 282 resources across 17 zipcodes. On average, each resource receives 14.4 referrals. 53 resources reside in zipcode 97215. SNAP (Foodstamps) at Department of Human Services has the highest number of referrals (396). 

By far, the most frequent need addressed by all resources is Food, with 53 food-related resources. 

233 of the 282 resources provide services only in English.
"""

pd.crosstab(df_resources["Zipcode"], df_resources["Need Type"])
df_resources['Zipcode'].value_counts().plot(kind='bar')

# Summarizing needs dataset
df_needs.head()
df_needs.astype('object').describe().transpose()
NT_hist = df_needs['Need Type'].value_counts().plot(kind='bar')
outcome_hist = df_needs['Outcome'].str.lower().value_counts().plot(kind='bar') #recode all outcome values to lowercase to make cleaner histogram

"""There are 1102 unique needs, 13 unique need categories, and 63 sub-needs. The most frequent need that clients have is for food-related services, with 343 occurences of food-related needs in the dataset.  The most frequent sub-need is for Pantries & Soup Kitchens (146). In 99 out of 1102 needs, the resource referred to was SNAP (Foodstamps) at the Department of Human Services."""

#summarizing clients dataset
df_clients.head()
df_clients.astype('object').describe().transpose()

cleaned_clients = df_clients.dropna() 
cleaned_clients["Race"] = cleaned_clients['Race'].replace('Decline to State', 'Declined to State')
race_hist = cleaned_clients['Race'].value_counts().plot(kind='bar')

insurance_hist = df_clients["Insurance Status"].value_counts().plot(kind="bar")

"""The most frequently reported client race was White, with 25 observations. Of the 544 unique clients, 220 are Medicaid recipients (the most frequent insurance type in this dataset). 54% of clients are female."""

# what resources are having high rates of success, disconnection, and failure?
ct = pd.crosstab(df_needs.Outcome.str.lower(), df_needs["Resource Referred To"])
ct
ct.plot(kind='bar', legend=False)

"""Based on the figure and table above, SNAP (Foodstamps) at Department of Human Services has the highest disconnection rate (51 disconnections). However, SNAP (Foodstamps) at Department of Human Services also has the highest success rate, with 46 successes. Given that the most frequent client need is for food assistance, this makes sense."""

#Merge clients and needs datasets to associate client demographics with outcomes
clients_needs_merged = df_clients.merge(df_needs, on="Client ID")
clients_needs_merged.astype('object').describe().transpose()
pd.crosstab(clients_needs_merged.Outcome.str.lower(), clients_needs_merged["Preferred Language"])
pd.crosstab(clients_needs_merged.Outcome.str.lower(), clients_needs_merged["Need Type"])