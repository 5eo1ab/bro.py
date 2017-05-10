# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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

def get_url(baseurl, ccode = 5631, startdate = ['Jan', 1, 1995], enddate = ['Apr', 1, 2017], start_pg = 0):
    all_list = []
    all_list.append(ccode)
    all_list.extend(startdate)
    all_list.extend(enddate)
    all_list.append(str(start_pg))
    return baseurl.format(*all_list)


def mk_comp_code_dict(file_nm):
    comp_code_dict = dict()
    list_file =pd.read_excel('nikkei225_data\\'+file_nm)
    for code, comp in list_file.loc[:,['code', 'company_name']].values:
        comp_code_dict[code] = comp
    return comp_code_dict


def get_soup(url, params=None):
    r = requests.get(url, params=params).text
    return BeautifulSoup(r, 'html.parser')
    
#################################################################
#############    변수 및 파라미터 설정 부분      ###################
#################################################################

directory = r"C:\Users\yeohyeongyu\Desktop\finance_data"
startdate = ['Jan', 1, 1995]
enddate = ['Apr', 1, 2017]


os.chdir(directory)

# 한번이라도 등장한 기업 목록 뽑기(code 기준으로 중복되는 기업명 제거, 남기는 기업명은 최근에 사용된 기업명)
comp_code_dict = mk_comp_code_dict('nikkei225_official.xlsx')    

base_url = 'https://www.google.com/finance/historical?q=TYO%3A{}&&startdate={}+{}%2C+{}&enddate={}+{}%2C+{}&start={}&num=200'

prd_cor = []

t1 = prd_cor # 
t2 = prd_cor # 
t3 = prd_cor
t4 = prd_cor
not_ched_list = []

for i in comp_code_dict.keys():
    if i not in t3:
        not_ched_list.append(i)

err_text = '-------------------- 오류가 있는 부분 ------------------------\n'

for key in not_ched_list:
    print('---------------------', comp_code_dict[key], ', ', key, '---------------------')
    price_info= []  
    start = 0
    while True:
        URL =get_url(base_url, key, startdate, enddate, start)
        print(start)
        try:
            soup = get_soup(URL)
            time.sleep(np.random.randint(2,6))
            temp_data = []
            table_data = soup.find('table', class_='gf-table historical_price').text.split('\n\n')
            temp_data = [ i.split('\n') for i in table_data] 
        except KeyError:
            err_text += str('google finance 검색 안된 기업 code: %s, name: %s\n'%(key, str(comp_code_dict[key]))) 
            break
        except AttributeError:
            err_text += str('AttributeError, code: %s, name: %s\n'%(key, str(comp_code_dict[key]))) 
        
        if len(temp_data) <200:
            break
        start += 200
        if start == 200:
            price_info.extend(temp_data[1:])
        else:
            price_info.extend(temp_data[2:])
    
        price_info_df = pd.DataFrame(price_info).iloc[1:,0:6]
        price_info_df.columns = price_info[0]
    
        price_info_df.to_csv('nikkei225'+'\\'+str(comp_code_dict[key])+'_'+str(key)+'.csv', index=False)
    prd_cor.append(key)


print(err_text)
with open('nikkei225\\err_text.txt', "w") as err:
    err.write(err_text)
    
print('end')