# -*- coding: utf-8 -*-
"""
Created on Sat May 27 19:20:27 2017

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






import os
import pandas as pd



#################################################################
#############    변수 및 파라미터 설정 부분      ###################
#################################################################
#디렉토리 관련
directory = r"C:\Users\User\Documents\bro_py" #default directory

#################################################################
#############    실제 연산 부분      ###################
#################################################################
#default 디렉토리 설정

os.chdir(directory)

trd_dir = 'Raw_DataSet\\gog_trd\\'
wt_dir = 'Preprocessed_dataset\\Modeling_Data_all\\'

for trd in os.listdir(trd_dir):
    data_org = pd.read_csv(trd_dir + trd[:-4]+ '.csv')
    
    diff_data = get_diff_df(data_org) 
    lag_diff_data = get_modeling_input(diff_data, 3)
    
    
    if not os.path.exists(wt_dir + "Lag_diff_gog_trd"):
            os.makedirs(wt_dir + "Lag_diff_gog_trd")
    
    lag_diff_data.to_csv(wt_dir + "Lag_diff_gog_trd\\Lag_diff_" +trd[:-4] + '.csv', index = False)
            