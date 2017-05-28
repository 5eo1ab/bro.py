# -*- coding: utf-8 -*-
"""
Created on Fri May 26 23:51:27 2017

@author: User
"""

## 변환률 변환 코드
def get_diff_df(df_in) :
    import numpy as np
    from pandas import DataFrame as df
    diff_df = []
    arr_tl = df_in['TimeLog'][1:]
    df_in = df_in[list(df_in.columns.values)[1:]]
    for i in range(1, len(df_in)):
        row = (np.array(df_in[df_in.index==i]) 
            - np.array(df_in[df_in.index==i-1]))
        row = (row/(np.array(df_in[df_in.index==i-1]))*100)[0]
        row = [100 if np.isinf(row[j]) or np.isnan(row[j]) else row[j] 
                for j in range(len(row))]        
        diff_df.append([arr_tl[i]]+row)
    df_out = df(diff_df, columns=['TimeLog']+list(df_in.columns.values))
    return df_out


import os
import pandas as pd




for trd in os.listdir():
    data_org = pd.read_csv(trd_dir+'\\' +trd[:-4]+ '.csv')
    
    diff_data = get_diff_df(data_org) 
    lag_diff_data = get_modeling_input(diff_data, 3)
    
    
    if not os.path.exists(directory+"\\Modeling_RawData_all\\Lag_diff_gog_trd"):
            os.makedirs(directory+"\\Modeling_RawData_all\\Lag_diff_gog_trd")
    
    lag_diff_data.to_csv(directory+"\\Modeling_RawData_all\\Lag_diff_gog_trd\\Lag_diff_" +trd[:-4] + '.csv', index = False)
            
    
    
#################################################################
#############    변수 및 파라미터 설정 부분      ###################
#################################################################
#디렉토리 관련
directory = r"C:\Users\User\Documents\bro_py" #default directory
ctr_nm = ['DE', 'KR', 'JP', 'US', 'CH']
#################################################################
#############    실제 연산 부분      ###################
#################################################################
#default 디렉토리 설정
os.chdir(directory)


for ctr in ctr_nm:
    data_org = pd.read_csv(directory+"\\Modeling_RawData_all\\Lag_diff_corp\\Lag_ModelingSet_"+ctr + '.csv')
    
    diff_data = get_diff_df(data_org) 
    
    if not os.path.exists(directory+"\\Modeling_RawData_all\\Lag_diff"):
            os.makedirs(directory+"\\Modeling_RawData_all\\Lag_diff")
    
    diff_data.to_csv(directory+"\\Modeling_RawData_all\\Lag_diff\\Lag_Diff_ModelingSet_"+ctr + '.csv', index = False)
            