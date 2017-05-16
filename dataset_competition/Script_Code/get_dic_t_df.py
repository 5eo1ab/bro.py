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
fpath = 'C:/Users/SERVER1/bro.py/dataset_competition/'
dic_t_cols = json.load(open(fpath+'colnames.json'))

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
"""
############################
## Export to CSV format
############################
nationals = ['KR_INDEX', 'US_INDEX', 'CN_INDEX', 'JP_INDEX', 'DE_INDEX']

ex_dir = 'C:/Users/SERVER1/bro.py/dataset_competition/EXPORTED_CSV/'
for n in nationals :
    dic_t_df[n].to_csv(dirs+"{}.csv".format(n), index=False)
"""


############################
## Get pearson cor.
############################
from scipy.stats import pearsonr
def has_missing(ar) :
    if False in list(ar[:2]==pd.Series([0,0])) :
        return False
    return True
def get_idx_missing(ar) :
    if has_missing(ar) is False :
        return 0
    return ar[ar>0].index[0]-1
fpath = 'C:/Users/SERVER1/bro.py/dataset_competition/'
dic_n_idx = json.load(open(fpath+'nationals.json'))
nationals = list(dic_n_idx.keys())

dic_n_corr = {}
for n in nationals :
    cols = list(dic_t_df[n].columns.values)[1:]
    corr_li = []
    tmp_n_df = dic_t_df[n][dic_t_df[n]['TimeLog']>=dic_t_df['G_IDX_CLOSE']['TimeLog'][0]]
    tmp_n_df = tmp_n_df.reset_index(drop=True)
    for c0 in cols :
        tmp_li = [dic_n_idx[n], c0]
        s_idx = get_idx_missing(tmp_n_df[c0])
        corr, p_v = pearsonr(dic_t_df['G_IDX_CLOSE'][dic_n_idx[n]][s_idx:],
                             tmp_n_df[c0][s_idx:])
        corr_li.append(tmp_li+[corr, p_v])
    for c0 in cols[:-1] :
        c0_idx = get_idx_missing(dic_t_df[n][c0])
        for c1 in cols[cols.index(c0)+1:] :
            #print(c0,c1)
            tmp_li = [c0, c1]
            if c0_idx > get_idx_missing(dic_t_df[n][c1]):
                s_idx = get_idx_missing(dic_t_df[n][c1])
            else :
                s_idx = c0_idx
            corr, p_v = pearsonr(dic_t_df[n][c0][s_idx:],dic_t_df[n][c1][s_idx:])
            corr_li.append(tmp_li+[corr, p_v])
    dic_n_corr[n] = df(corr_li, columns=['c0', 'c1', 'corr', 'p-value'])
    print(n)

## Export to CSV format
ex_dir = 'C:/Users/SERVER1/bro.py/dataset_competition/EXPORTED_CSV/'
for n in nationals :
    dic_n_corr[n].to_csv(ex_dir+"{}.csv".format("corr_{}".format(n)), index=False)
