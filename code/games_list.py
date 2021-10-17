#!/usr/bin/env python
# coding: utf-8

"""
Created on Fri Oct 15 18:52:24 2021

@author: Jeroen Mahieu
"""

# ## Games List
# This program downloads all the app ids from Steamspy and converts them to a csv file

# ### Import Libraries

# standard library imports
import csv
import datetime as dt
import json
import os
import statistics
import time
import glob

# third-party imports
import numpy as np
import pandas as pd
import requests

# customisations - ensure tables show all columns
pd.set_option("max_columns", 100)

#change wd
os.chdir("C:/Users/jeroe/Dropbox/SteamGames/data/")


# ### Define Request Function

# In[2]:


def get_request(url, parameters=None):
    """Return json-formatted response of a get request using optional parameters.
    
    Parameters
    ----------
    url : string
    parameters : {'parameter': 'value'}
        parameters to pass as part of get request
    
    Returns
    -------
    json_data
        json-formatted response (dict-like)
    """
    try:
        response = requests.get(url=url, params=parameters)
    except SSLError as s:
        print('SSL Error:', s)
        
        for i in range(5, 0, -1):
            print('\rWaiting... ({})'.format(i), end='')
            time.sleep(1)
        print('\rRetrying.' + ' '*10)
        
        # recusively try again
        return get_request(url, parameters)
    
    if response:
        return response.json()
    else:
        # response is none usually means too many requests. Wait and try again 
        print('No response, waiting 60 seconds...')
        time.sleep(60)
        print('Retrying.')
        return get_request(url, parameters)


# ### Download App IDs
# Steamspy does not allow to bulk download all app ids simultaneously. Only 1000 per page. So we need to loop over the different pages to extract all ids and export them to one single csv file. There seem to be currently 49 pages (0-48).

# In[5]:

app_list={}
url = "https://steamspy.com/api.php"
for i in range(0,49):
    parameters = {"request": "all", "page": str(i)}

    # request 'all' from steam spy and parse into dataframe
    json_data = get_request(url, parameters=parameters)
    steam_spy_all = pd.DataFrame.from_dict(json_data, orient='index')

    # generate sorted app_list from steamspy data
    app_list[i] = steam_spy_all[['appid', 'name']].sort_values('appid').reset_index(drop=True)
    
    #concatenate dataframes
    apps = pd.concat(app_list)

    # export to csv
    apps.to_csv('app_list.csv', index=False)




