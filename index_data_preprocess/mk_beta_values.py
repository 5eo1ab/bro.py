# -*- coding: utf-8 -*-
"""
Created on Wed May 10 13:25:40 2017

@author: yeohyeongyu

beta 값 구하기 위한 클래스
이 클래스에서 최종적으로 출력 되는 데이터는 각 기업
Date(매달 말일) Beta


"""


import os
import pandas as pd
import numpy as np


directory = r"r'C:\Users\User\Documents\bro_py\kospi200_all"

os.chdir(directory)
#index_list = ['DAX30', 'kospi200_all', 'nikkei225', 'SnP500', 'SSE50']

#일단은 코스피 기업에 대해서만
indexnm= 'kospi200_all'


data = pd.read_csv('BGF리테일(BGF Retail Co Ltd)_027410.csv' )

for compnm in os.listdir(indexnm):
    print(compnm)
    data = pd.read_csv(indexnm+'\\'+compnm)
    #        data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    #        data['Date'] = pd.to_datetime(data['Date'])
    



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

