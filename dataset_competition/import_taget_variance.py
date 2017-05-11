# -*- coding: utf-8 -*-
"""
Created on Thu May 11 16:16:05 2017

@author: SERVER1
"""

import pandas as pd
from pandas import DataFrame as df
import numpy as np
import mysql.connector

## database connection
cnx = mysql.connector.connect(
        user = 'seo',
        password = '0000',
        host = '192.168.0.4',
        database = 'bropy')
print("Success Connection.")

cursor = cnx.cursor()
query = "SELECT TimeLog, SPX, SSEC, GDAXI, N225, KOSPI FROM G_IDX_CLOSE"
cursor.execute(query)
table_rows = cursor.fetchall()
cursor.close()

tg_idx_df = df(table_rows)
tg_idx_df.columns = ['TimeLog','SPX','SSEC','GDAXI','N225','KOSPI']


