# -*- coding: utf-8 -*-
"""
Created on Sun May 21 15:17:37 2017

@author: hyeongyu
"""



import os
import pandas as pd
import numpy as np

###################################################################
####################    필요한 함수 정의 부분      #################
###################################################################
#RV coeff 분모 구하는 부분
def cal_RVDenom(data, type_set="orig"):
    p = range(np.shape(data)[1])
    n = np.shape(data)[0]

    abs_cov = abs(np.cov(data.T)) 
    cov_sqr = [(abs_cov[(i,j)])**2 for i in p for j in p]  
    r = sum(cov_sqr)
    if type_set == 'mod':
        mod_cal = [sum(np.square(data)[:,i] * np.square(data)[:,j] / np.square(n-1))  for i in p for j in p]  
        cov_sqr_m =[cov_sqr[i] - mod_cal[i]  for i in range(len(cov_sqr))]  
        r = sum(cov_sqr_m)
    return r

#RV coeff 구하는 부분
def RV(X, Y, type_set="orig"):
    
    data1 = np.array(X)
    data2 = np.array(Y)
    
    #각 컬럼 별 표준화 
    data1 = (data1 - data1.mean(axis=0))/(data1.std(axis=0))
    data2 = (data2 - data2.mean(axis=0))/(data2.std(axis=0))

    n = np.shape(data1)[0]
    p1 = range(np.shape(data1)[1])
    p2 = range(np.shape(data2)[1])
  
    comb = [(i,j) for i in p1 for j in p2]
    
    #calculate numerator    
    vecnum = []   
    for i in comb:   
         elemnum = np.square(np.cov(data1[:,i[0]], data2[:,i[1]])[0,1])
         # for the modified
         if type_set=="mod":
             elemnum -=  sum((data1[:,i[0]] ** 2) * (data2[:,i[1]]) **2)/np.square(n-1)           
         vecnum.append(elemnum)
    num = sum(vecnum)
 
   #calculate denominator   
    denom1 = cal_RVDenom(data1, type_set)
    denom2 = cal_RVDenom(data2, type_set)

    RV = num/np.sqrt(denom1*denom2)
 
    return RV

#################################################################
#############    변수 및 파라미터 설정 부분      ###################
#################################################################
#beta 연산 관련
period_list = [1,3,6,12]  #beta 연산 기간(달 단위)

directory = r"C:\Users\User\Documents\bro_py" #default directory
index_list = ['preprocess_nan_DAX30_all.csv', 'preprocess_nan_kospi200_all_all.csv', 'preprocess_nan_nikkei225_all.csv', 'preprocess_nan_SnP500_all.csv', 'preprocess_nan_SSE50_all.csv']

skip_cf = 48 #기업 데이터가 4년 미만일 경우 skip
#################################################################
#############    실제 연산 부분      ###################
#################################################################
#default 디렉토리 설정
os.chdir(directory)

rd_dir = 'Preprocessed_dataset\\Modeling_Data_all\\'
wt_dir = 'Preprocessed_dataset\\Network_Data_all\\'



if not os.path.exists(wt_dir):
        os.makedirs(wt_dir )


for period in period_list:
    #코드 실행 결과 출력 관련 
    #생성 파일 저장 directory 
    read_directory = 'Close_Volume_Beta_'+str(period) +'_v2'
    for indexnm in index_list:    
        skip_corp_list = []

        data_org = pd.read_csv(read_directory+'\\'+indexnm)
        data_org.index = data_org.iloc[:,0]
        data =data_org.drop(data_org.columns[0],1)

        num_comp = np.shape(data)[1]

        #두 기업의 row 수를 맞춰야함
        X = data.iloc[:,list(range(num_comp-3,num_comp ))]
        Y = data.iloc[:,list(range(num_comp-6,num_comp-3 ))]
        
        X.columns
        Y.columns                
        
        too_many_nan = False

        intersection_date = set(X.index[list(~np.isnan(X.iloc[:,2]))]).intersection(Y.index[list(~np.isnan(Y.iloc[:,2]))])
       
        inter_X = X.loc[intersection_date ,]
        inter_Y = Y.loc[intersection_date ,]
        
        X_index = inter_X.columns[0][:-6]
        Y_index = inter_Y.columns[0][:-6]
        
        if len(intersection_date) < skip_cf:
            too_many_nan = True
            continue
        
        rv_coef = RV(inter_X, inter_Y )
      
            
        print(str(period), indexnm[18:-4], '\t', X_index,'\t', Y_index, '\t',rv_coef)
            
            