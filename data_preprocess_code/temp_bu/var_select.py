# -*- coding: utf-8 -*-
"""
Created on Sat May 27 12:56:03 2017

@author: User
"""



import os
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

###################################################################
####################    필요한 함수 정의 부분      #################
###################################################################



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

#df_in = dic_n_t_df[n]
def get_diff_df(df_in) :
    from pandas import DataFrame as df
    diff_df = []
    arr_tl = df_in['TimeLog'][1:]
    df_in = df_in[list(df_in.columns.values)[1:]]
    for i in range(1, len(df_in)):
        row = (np.array(df_in[df_in.index==i])[0] 
                - np.array(df_in[df_in.index==i-1])[0])[0]
        row = (row/(np.array(df_in[df_in.index==i-1]))*100)[0]
        row = [0 if np.isinf(row)[j] else row[j] 
                for j in range(len(row))]        
        diff_df.append([arr_tl[i]]+row)
    df_out = df(diff_df, columns=['TimeLog'] + list(df_in.columns.values))
    return df_out

#################################################################
#############    변수 및 파라미터 설정 부분      ###################
#################################################################

#디렉토리 관련
directory = r"C:\Users\User\Documents\bro_py" #default directory


os.chdir(directory)






cntry_nm= ['DE', 'KR', 'JP', 'CH', 'US']
target_index_nm= [ 'GDAXI','KOSPI', 'N225', 'SSEC', 'SPX']
input_files =['Modeling_dataset_DAX30_all.csv', 'Modeling_dataset_kospi200_all_all.csv', 'Modeling_dataset_nikkei225_all.csv', 'Modeling_dataset_SSE50_all.csv']#, 'Modeling_dataset_SnP500_all.csv'



target_data = pd.read_csv('dataset_competition\\IMPORTED_CSV\\G_IDX_CLOSE.csv')
target_data_cls = pd.read_csv('dataset_competition\\Y_IDX_CLOSE.csv')


#Lag 부분
dic_n_t_df = {} # t lag append table
dic_n_tgt = {}
dic_n_tgt_cls = {}
lag_t =3
for i in range(len(input_files)):
    
    input_data = pd.read_csv('Modeling_RawData_all\\'+input_files[i])         
    input_data['TimeLog'] = input_data[input_data.columns[0]]
    input_data.index = input_data['TimeLog'] 
    input_data= input_data.drop(input_data.columns[0], 1)
    
    
    
    target_temp = target_data.copy()
    target_temp = target_temp.loc[:,['TimeLog',target_index_nm[i]] ]
    target_temp.index =np.array( [tm[:7] for tm in  target_temp['TimeLog']])
    target_temp = target_temp.drop('TimeLog', 1)

    target_temp_cls = target_data_cls.copy()
    target_temp_cls = target_temp_cls.loc[:,['TimeLog',target_index_nm[i]] ]
    target_temp_cls.index =np.array( [tm[:7] for tm in  target_temp_cls['TimeLog']])
    target_temp_cls = target_temp_cls.drop('TimeLog', 1)


    intersection_date = (input_data.index).intersection(target_temp.index)  

    input_df = input_data.loc[input_data.index,]
    target_df =target_temp.loc[intersection_date,]
    target_df_cls =target_temp_cls.loc[intersection_date,]
    
    dic_n_t_df[cntry_nm[i]] =get_modeling_input(input_df, lag_t )
    dic_n_tgt[cntry_nm[i]] = target_df[lag_t:]
    dic_n_tgt_cls[cntry_nm[i]] = target_df_cls[lag_t:]
    



#상관계수
dic_n_corr_df = {} # variable selection by corr.
cutoff = 0.3

for i in range(len(input_files)):

    corr_li = []
    for c in dic_n_t_df[cntry_nm[i]].columns.values[1:]:
        
        input_df = dic_n_t_df[cntry_nm[i]] 
        tg_arr  = dic_n_tgt[cntry_nm[i]]
        corr, p_v = pearsonr(tg_arr[target_index_nm[i]][:-48], input_df[c][:-48])
        if p_v < 0.05 and abs(corr) > cutoff:
            corr_li.append(c)
            

    dic_n_corr_df[cntry_nm[i]] = input_df[corr_li]




#변화량-------------------------------------------------------
dic_n_diff_df = {} # t lag, diff table
for i in range(len(input_files)):
    cols = list(dic_n_corr_df[cntry_nm[i]].columns.values)
    dic_n_diff_df[cntry_nm[i]] = get_diff_df(dic_n_t_df[cntry_nm[i]])[cols]




###########################
# l1 penalty variable selection
###########################


from sklearn.linear_model import LogisticRegression
dic_n_cols_l1 = {} # selected by logistic regression l1 penalty
for i in range(len(input_files)):
    
    X = dic_n_corr_df[cntry_nm[i]][:-48]
    y = dic_n_tgt_cls[cntry_nm[i]][:-48]
    # C 값을 조정하여 coefficient값이 0인 변수 수를 조절 할 수 있음
    model = LogisticRegression(penalty='l1',C=0.1)
    model.fit(X,y)
    cols = X.columns.values[np.where(model.coef_ != 0)[1]]
    dic_n_cols_l1[cntry_nm[i]] = cols
###########################
# Random Forest variable selection
###########################    
from sklearn.ensemble import RandomForestClassifier
dic_n_cols_rf = {} # selected by random forest
for i in range(len(input_files)):
    X = dic_n_corr_df[cntry_nm[i]][:-48]
    y = dic_n_tgt_cls[cntry_nm[i]][:-48]
    # C 값을 조정하여 coefficient값이 0
    model = RandomForestClassifier()
    model.fit(X,y)
    cols = X.columns.values[np.where(model.feature_importances_ != 0)[0]]
    dic_n_cols_rf[cntry_nm[i]] = cols

dic_union = {}
dic_intersection = {}
for i in range(len(input_files)):
    dic_union[cntry_nm[i]] = list(set(dic_n_cols_l1[cntry_nm[i]]) | set(dic_n_cols_rf[cntry_nm[i]]))
    dic_intersection[cntry_nm[i]] = list(set(dic_n_cols_l1[cntry_nm[i]]) & set(dic_n_cols_rf[cntry_nm[i]]))

#fpath    
var_counts = []
for i in range(len(input_files)):
    var_counts.append([ cntry_nm[i],
            len(dic_n_diff_df[cntry_nm[i]].columns.values),
            len(dic_n_cols_l1[cntry_nm[i]]),
            len(dic_n_cols_rf[cntry_nm[i]]),
            len(dic_union[cntry_nm[i]]),
            len(dic_intersection[cntry_nm[i]])
            ])
    print("{}\tunion: {}\tintersection:{}".format(cntry_nm[i], len(dic_union[cntry_nm[i]]), len(dic_intersection[cntry_nm[i]])))
    
from pandas import DataFrame as df
var_counts = df(var_counts, columns=['national', 'corr', 'l1', 'RF', 'union', 'intersection'])

if not os.path.exists('Modeling_RawData_all\\Sltd_in_var_data\\result_report'):
        os.makedirs('Modeling_RawData_all\\Sltd_in_var_data\\result_report')
var_counts.to_csv('Modeling_RawData_all\\Sltd_in_var_data\\result_report\\'+"var_counts.csv", index=False)





if not os.path.exists('Modeling_RawData_all\\Sltd_in_var_data\\Input_CSV\\'):
        os.makedirs('Modeling_RawData_all\\Sltd_in_var_data\\Input_CSV\\')

for i in range(len(input_files)):
    dic_n_diff_df[cntry_nm[i]][dic_union[cntry_nm[i]]].to_csv('Modeling_RawData_all\\Sltd_in_var_data\\Input_CSV\\union_{}_total.csv'.format(cntry_nm[i]), index='TimeLog')
    dic_n_diff_df[cntry_nm[i]][dic_union[cntry_nm[i]]][:-48].to_csv('Modeling_RawData_all\\Sltd_in_var_data\\Input_CSV\\union_{}_train.csv'.format(cntry_nm[i]), index='TimeLog')
    dic_n_diff_df[cntry_nm[i]][dic_union[cntry_nm[i]]][-48:].to_csv('Modeling_RawData_all\\Sltd_in_var_data\\Input_CSV\\union_{}_test.csv'.format(cntry_nm[i]), index='TimeLog')


dic_n_tgt_cls[cntry_nm[i]]

## Export TEST TABLE
temp_dict = {}
for i in range(len(input_files)):
    a = dic_n_tgt_cls[cntry_nm[i]].reset_index(drop=True)


for i in range(len(input_files)):
    if i ==0:
        merged_df = dic_n_tgt_cls[cntry_nm[i]].copy()
    else:
        merged_df  = pd.concat([merged_df, dic_n_tgt_cls[cntry_nm[i]]], axis=1)


merged_df.to_csv('Modeling_RawData_all\\Sltd_in_var_data\\'+"Y_bin_total.csv", index='TimeLog')
merged_df[:-48].to_csv('Modeling_RawData_all\\Sltd_in_var_data\\'+"Y_bin_train.csv", index='TimeLog')
merged_df[-48:].to_csv('Modeling_RawData_all\\Sltd_in_var_data\\'+"Y_bin_test.csv", index='TimeLog')
