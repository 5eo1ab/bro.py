# -*- coding: utf-8 -*-
"""
Created on Fri May 26 23:18:59 2017

@author: User
"""



def get_modeling_input(df_in, t=1) :
    from pandas import DataFrame as df
    cols = [c for c in list(df_in.columns.values) if c!='TimeLog']
    df_out = df({'TimeLog': list(df_in['TimeLog'][t:])})
    for t0 in range(1,t+1) :
        cols_t = ["{}_{}".format(c,t0) for c in cols]
        d_range = [-t+i+(t0-1) for i in range(t)] if t!=1 else -1
        df_tmp = df(
                df_in.drop(df_in.index[d_range], axis=0)[cols].values,
                columns=cols_t)
        for c_t in cols_t :
            df_out[c_t] = df_tmp[c_t].values
        pass   
    return df_out




# -*- coding: utf-8 -*-
"""
Created on Thu May 25 23:53:44 2017

@author: User
"""

import os
import pandas as pd


#################################################################
#############    변수 및 파라미터 설정 부분      ###################
#################################################################
#디렉토리 관련
directory = r"C:\Users\User\Documents\bro_py" #default directory
index_file = ['Close_Volume_Beta_DAX30.csv', 'Close_Volume_Beta_kospi200_all.csv', 'Close_Volume_Beta_nikkei225.csv', 'Close_Volume_Beta_SnP500.csv', 'Close_Volume_Beta_SSE50.csv']
ctr_nm = ['DE', 'KR', 'JP', 'US', 'CH']
#################################################################
#############    실제 연산 부분      ###################
#################################################################
#default 디렉토리 설정
os.chdir(directory)

ctr_idx = 0
for indexnm in index_file:
    data_org = pd.read_csv("Modeling_RawData_all\\Modeling_dataset_" + indexnm[18:-4] + '_all.csv')
    
    data_org= data_org.copy()
    data_org['TimeLog']=data_org.loc[:,data_org.columns[0]]
    data_org= data_org.drop(data_org.columns[0], 1)
    
    lag_data = get_modeling_input(data_org, 3)
    
    if not os.path.exists(directory+"\\Modeling_RawData_all\\Lag"):
            os.makedirs(directory+"\\Modeling_RawData_all\\Lag")
            
    
    lag_data.to_csv(directory+"\\Modeling_RawData_all\\Lag\\Lag_ModelingSet_"+ctr_nm[ctr_idx] + '.csv', index = False)
    ctr_idx +=1


