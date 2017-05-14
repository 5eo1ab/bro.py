# -*- coding: utf-8 -*-
"""
Created on Thu May 11 23:03:45 2017

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
fpath = r'C:\Users\SERVER1\bro.py\dataset_competition\colnames.json'
colname_dic = json.load(open(fpath))
colnames = colname_dic['G_IDX_CLOSE'][:6]

## Import Y_IDX_CLOSE from Database
query = "SELECT " + ", ".join(colnames) + " FROM Y_IDX_CLOSE"
cursor = cnx.cursor()
cursor.execute(query)
table_rows = cursor.fetchall()
cursor.close()
y_df = df(table_rows, columns=colnames)
cnx.close()

