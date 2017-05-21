# -*- coding: utf-8 -*-
"""
Created on Sun May 14 21:08:26 2017

@author: 5eo1ab
"""

import pandas as pd
from pandas import DataFrame as df
import numpy as np
import mysql.connector



## Connect Database
cnx = mysql.connector.connect(
        user = 'seo',
        password = '0000',
        host = '192.168.0.4',
        database = 'bropy')
print("Success Connection.")

## Load column names
import json
fpath = 'C:/Users/SERVER1/bro.py/dataset_competition/'
dic_t_cols = json.load(open(fpath+'colnames.json'))

dic_n_idx = json.load(open(fpath+'nationals.json'))
nationals = list(dic_n_idx.keys())

## Load data to DataFrame and set dictioary
dic_t_df = {}
for t, cols in dic_t_cols.items() :
    cursor = cnx.cursor()
    query = "SELECT {} FROM {}".format(", ".join(cols), t)
    cursor.execute(query)
    dic_t_df[t] = df(cursor.fetchall(), columns=cols)
    cursor.close()
 