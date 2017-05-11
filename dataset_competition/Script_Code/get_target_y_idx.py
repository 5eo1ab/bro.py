# -*- coding: utf-8 -*-
"""
Created on Thu May 11 16:16:05 2017

@author: 5eo1ab
"""

################################
## Get target_Y_Index
################################

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

## Execute Query
cursor = cnx.cursor()
query = "SELECT TimeLog, SPX, SSEC, GDAXI, N225, KOSPI FROM G_IDX_CLOSE"
cursor.execute(query)
table_rows = cursor.fetchall()
cursor.close()
tg_df = df(table_rows)

## Load column names
import json
fpath = r'C:\Users\SERVER1\bro.py\dataset_competition\colnames.json'
colname_dic = json.load(open(fpath))
colnames = colname_dic['G_IDX_CLOSE'][:6]
tg_df.columns = colnames

## Get Y result(index up or down)
y_idx_li = []
for i in range(1, len(tg_df)) :
    tmp = ((np.array(tg_df[tg_df.index==i]) > np.array(tg_df[tg_df.index==i-1]))*1)[0][1:]
    tmp_ = [tg_df[colnames[0]][i]] + list(tmp)
    y_idx_li.append(tmp_)
y_result = df(y_idx_li, columns=colnames)

## Export to CSV format
fpath0 = '/'.join(fpath.split('\\')[:-1])+'/IMPORTED_CSV/Y_IDX_CLOSE.csv'
y_result.to_csv(fpath0, index=False)

