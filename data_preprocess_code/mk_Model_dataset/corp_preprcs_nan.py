# -*- coding: utf-8 -*-
"""
Created on Thu May 25 23:53:44 2017

@author: User
"""

import os
import pandas as pd
import numpy as np


#################################################################
#############    변수 및 파라미터 설정 부분      ###################
#################################################################
#beta 연산 관련
period_list = [1,3,6,12]  #beta 연산 기간(달 단위)
cal_list = ['Close', 'Volume', 'Beta']
#price_colnm = ['Open', 'High', 'Low', 'Close', 'Volume'] #price 목록


#null 값 비율이 null_ratio_cutoff 이상인 기업 데이터 삭제 (참고로 2003.1 ~2016.12 까지 168개)
null_ratio_cutoff_by_corp = 0.3
latest_period = 36
null_ratio_cutoff_by_date = 0.9

#디렉토리 관련
directory = r"C:\Users\User\Documents\bro_py" #default directory
index_file = ['Close_Volume_Beta_DAX30.csv', 'Close_Volume_Beta_kospi200_all.csv', 'Close_Volume_Beta_nikkei225.csv', 'Close_Volume_Beta_SnP500.csv', 'Close_Volume_Beta_SSE50.csv']

#################################################################
#############    실제 연산 부분      ###################
#################################################################
#default 디렉토리 설정
os.chdir(directory)
rd_dir = 'Preprocessed_dataset\\Close_Volume_all_Beta\\'
wt_dir = 'Preprocessed_dataset\\Modeling_Data_all\\'

for indexnm in index_file:
    count = 0

    print(indexnm, 1)

    data_org = pd.read_csv(rd_dir+indexnm)
    data_org.index = data_org.iloc[:,0]
    data_org =data_org.drop(data_org.columns[0],1)
    data= data_org[data_org.index <= "2016-12"]
    
        

    
    #---------------------------------------------
    #-------------결측 처리 1차 제거 부분----------
    #---------------------------------------------
    

    
    #가장 최근 달 부터  한번이라도 일자에 null 값이 있는 컬럼 drop
    latest_null_list = []
    for p in range(1, latest_period+1):
        data  = data.drop(list(data.columns[data.iloc[len(data)-p].isnull()]), axis=1)

        
    #가장 과거에서 부터 한달 씩 확인 했을 때, 해당 달에 null 값의 비율이 90%이상인 달(row index)삭제
    rm_date_list = []
    p= 0
    num_col = data.shape[1]
    while True:
        if (sum(data.iloc[p].isnull()) /num_col )> null_ratio_cutoff_by_date:
            rm_date_list.append(data.index[p])
        else :
            break
        p +=1
    data = data.drop(rm_date_list, axis=0)
    
    #null 값의 비율이 정해진 값 이상으로 높을 때 drop        
    ovr_nullcf_list =  data.columns[list(data.isnull().sum() /len(data) > null_ratio_cutoff_by_corp )]
    rm_data = data.copy()
    rm_data =  rm_data.drop(ovr_nullcf_list, axis=1)
    
    #---------------------------------------------
    #-------------결측 처리 2차 대체 부분----------
    #---------------------------------------------
    print(indexnm, 2)
    
    #중간이 아닌, 가장 과거 데이터에서 연속으로 null 값이 있는 부분은 그 기업의 평균값으로 대체
    fcol_nan_list = list(rm_data.columns[list(rm_data.iloc[0].isnull())])
    for i in range(rm_data.shape[0]):
        nan_co_list = list(rm_data.columns[list(rm_data.iloc[i].isnull())])
        complt_repce_list = set(fcol_nan_list) - set(nan_co_list)
        for j in complt_repce_list : fcol_nan_list.remove(j)
        
        for col in fcol_nan_list:
            rm_data.ix[i, fcol_nan_list]= np.mean(rm_data.loc[:,fcol_nan_list])
            #rm_data.iloc[i][fcol_nan_list] 
            
            
    #중간 중간에 있는 null 값은 앞뒤 값의 평균으로 대체(앞 뒤로 가장 가까운 한개(만약 바로 인접 값이 null이면 그 다은 인접값으로 계산))
    for i in range(1,rm_data.shape[0]):
        nan_co_list = list(rm_data.columns[list(rm_data.iloc[i].isnull())])
        for col in nan_co_list:
            r = 1
            while r < rm_data.shape[0]:
                r+=1
                if not np.isnan(rm_data.iloc[r][col]):
                    ajc_rcnt = rm_data.iloc[r][col]
                    break
            p =i
            while p >= 1:
                p-=1
                if not np.isnan(rm_data.iloc[p][col]):
                    ajc_past = rm_data.iloc[p][col]
                    break    
            rm_data.ix[i, col] = (ajc_past + ajc_rcnt)/2

    print(indexnm, 3)
    if not os.path.exists(wt_dir):
            os.makedirs(wt_dir )
    
    rm_data.to_csv(wt_dir + 'preprocess_nan_' + indexnm[18:-4] + '_all.csv')


