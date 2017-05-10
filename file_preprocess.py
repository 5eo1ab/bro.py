# -*- coding: utf-8 -*-
"""
Created on Wed May 10 13:25:40 2017

@author: yeohyeongyu
"""


import os
import pandas as pd
import numpy as np


directory = r"C:\Users\yeohyeongyu\Desktop\finance_data\all_list"

os.chdir(directory)
index_list = os.listdir()

data_period = ''
for indexnm in index_list:
    for compnm in os.listdir(directory +'\\'+ indexnm):
        data = pd.read_csv(indexnm +'\\'+ compnm)
        data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        data['Date'] = pd.to_datetime(data['Date'])

        sorted_data = data.sort(columns = 'Date')

data_period += org_file + ' :\t' + str(max(sorted_data['Date']))[0:10] + '\t' + str(min(sorted_data['Date']))[0:10]


price_colnm = ['Open', 'High', 'Low', 'Close', 'Volume']        

sorted_data.loc[:,price_colnm ] = sorted_data.loc[:,price_colnm ].convert_objects(convert_numeric=True)

