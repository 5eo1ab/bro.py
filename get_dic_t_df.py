# -*- coding: utf-8 -*-
"""
Created on Sun May 14 21:08:26 2017

@author: SERVER1
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
fpath = r'C:\Users\SERVER1\bro.py\dataset_competition\colnames.json'
dic_t_cols = json.load(open(fpath))

## Load data to DataFrame and set dictioary
dic_t_df = {}
for t, cols in dic_t_cols.items() :
    cursor = cnx.cursor()
    query = "SELECT {} FROM {}".format(", ".join(cols), t)
    cursor.execute(query)
    dic_t_df[t] = df(cursor.fetchall(), columns=cols)
    cursor.close()
    
#dic_t_df['G_IDX_CLOSE'].head()
#dic_t_df['MATERIALS'].head()


############################
## Export to CSV format
############################
nationals = ['KR_INDEX', 'US_INDEX', 'CN_INDEX', 'JP_INDEX', 'DE_INDEX']
"""
dirs = 'C:/Users/SERVER1/bro.py/dataset_competition/EXPORTED_CSV/'
for n in nationals :
    dic_t_df[n].to_csv(dirs+"{}.csv".format(n), index=False)
"""

from scipy.stats import pearsonr
pearsonr(dic_t_df['G_IDX_CLOSE']['SPX'], dic_t_df['G_IDX_CLOSE']['KOSPI'])

cols = dic_t_df[n].columns.values
dic_t_df[n]['ahBDMAHS'][0:3]
dic_t_df[n][cols[1]]

if False in list(dic_t_df[n]['ahBDMAHS'][0:3]==pd.Series([1,0,0])) :
    print(1)
has_null(dic_t_df[n][cols[1]])

dic_t_df[n]['ahBDMAHS'][64]
dic_t_df[n]['ahBDMAHS'][dic_t_df[n]['ahBDMAHS']>0].index[0]-1
dic_t_df[n][cols[1]][dic_t_df[n][cols[1]]>0].index[0]
get_idx_missing(dic_t_df[n][cols[1]])
pearsonr(dic_t_df[n]['ahBDMAHS'][65:], dic_t_df[n][cols[1]][65:])

############################
## Get pearson cor.
############################
def has_missing(ar) :
    if False in list(ar[:3]==pd.Series([0,0,0])) :
        return False
    return True
def get_idx_missing(ar) :
    if has_missing(ar) is False :
        return 0
    return ar[ar>0].index[0]-1

cols = list(cols[1:])
for c0 in cols :
    for c1 in cols[cols.index(c0)+1:] :
        

#for n in nationals :
#    cols = dic_t_df[n].columns.values
