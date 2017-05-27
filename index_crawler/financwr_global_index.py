# -*- coding: utf-8 -*-
"""
Created on Tue May  9 18:42:36 2017

@author: yeohyeongyu
"""


import os
import pandas as pd
import time
from bs4 import BeautifulSoup
import requests
import numpy as np

#import numpy as np

###################################################################
####################    필요한 함수 정의 부분      #################
###################################################################

def get_url(baseurl, ccode =111, startdate = ['Jan', 1, 1995], enddate = ['Apr', 1, 2017], start_pg = 0):
    all_list = []
    all_list.append(str(ccode))
    all_list.extend(startdate)
    all_list.extend(enddate)
    all_list.append(str(start_pg))
    return baseurl.format(*all_list)


def mk_comp_code_dict(file_nm):
    comp_code_dict = dict()
    list_file =pd.read_excel('SSE50_data\\'+file_nm)
    for code, comp in list_file.loc[:,['SSE number', 'Constituent']].values:
        comp_code_dict[code] = comp
    return comp_code_dict


def get_soup(url, params=None):
    r = requests.get(url, params=params).text
    return BeautifulSoup(r, 'html.parser')
    
#################################################################
#############    변수 및 파라미터 설정 부분      ###################
#################################################################

directory = r"C:\Users\User\Documents\bro_py"
startdate = ['Jan', 1, 1995]
enddate = ['Apr', 1, 2017]


os.chdir(directory)

# 한번이라도 등장한 기업 목록 뽑기(code 기준으로 중복되는 기업명 제거, 남기는 기업명은 최근에 사용된 기업명)


global_idx = {'DAX' : 14199910, 'SnP500' : 626307, 'KOSPI200' : 542029859096076, 'NIKKEI225':15513676,  'SSE50' :3147530}

base_url = 'https://www.google.com/finance/historical?cid={}&&startdate={}+{}%2C+{}&enddate={}+{}%2C+{}&start={}&num=200'

prd_cor = []





for key in global_idx.keys():
    price_info= []  
    start = 0
    while True:
        URL =get_url(base_url, global_idx[key], startdate, enddate, start)
        print(start)
    
        soup = get_soup(URL)
        time.sleep(np.random.randint(2,6))
        temp_data = []
        table_data = soup.find('table', class_='gf-table historical_price').text.split('\n\n')
        temp_data = [ i.split('\n') for i in table_data] 
    
        if len(temp_data) <200:
            break
        start += 200
        if start == 200:
            price_info.extend(temp_data[1:])
        else:
            price_info.extend(temp_data[2:])

    price_info_df = pd.DataFrame(price_info).iloc[1:,0:6]
    price_info_df.columns = price_info[0]

    if not os.path.exists(directory +'\\global_idx'):
        os.makedirs(directory +'\\global_idx')
    
    price_info_df.to_csv(directory +'\\' + 'global_idx\\'+key+'.csv', index=False)


        
print('end')
