# -*- coding: utf-8 -*-
"""
Created on Wed May 10 13:25:40 2017

@author: yeohyeongyu

각 기업별로 close, volume, beta 값 으로 구성 된 테이블 만들기

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
         #for the modified
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


#디렉토리 관련
directory = r"C:\Users\User\Documents\bro_py" #default directory
index_list = ['DAX30', 'kospi200_all', 'nikkei225', 'SnP500', 'SSE50']

#생성 상관 계수 관련
skip_cf = 48 #기업 데이터가 4년 미만일 경우 skip


#################################################################
#############    실제 연산 부분      ###################
#################################################################
#default 디렉토리 설정
os.chdir(directory)


rd_dir = 'Preprocessed_dataset\\Network_Data_all\\Net_raw_data\\'
wt_dir = 'Preprocessed_dataset\\Network_Data_all\\Corr_Mat'



if not os.path.exists(wt_dir):
        os.makedirs(wt_dir )


corp_df = {}

for indexnm in os.listdir(rd_dir):
    if indexnm[-3:] == 'csv':
        col_list = []
        #print(indexnm[18:-4])
        data_org = pd.read_csv(rd_dir+'\\'+indexnm)
        data_org.index = data_org.iloc[:,0]
        data =data_org.drop(data_org.columns[0],1)
        #        colnms = data_org.columns[1:]
        #        
        #        for col in colnms:
        #             col_list.extend([col.replace(rm,'') for rm in rm_list if rm in col])
        #             cnt = Counter(col_list)
        #        corp_list =[ k for k,v in cnt.items() if v>1]
        #        corp_list_dict[indexnm[18:-4]] = corp_list 
        corp_df[indexnm[18:-4]] = data
        
        
        

for indexnm in os.listdir(rd_dir):

    skip_corp_list = []
    
    if indexnm[-3:] == 'csv': #csv 파일 아니면 continue
        print(indexnm[18:-4])
        data = corp_df[indexnm[18:-4]]
        num_comp = np.shape(data)[1]
        pre_cursor = 0        
        X_comp_dict = dict()
        while pre_cursor<  num_comp -6: 
            
            Y_comp_list = []
            post_cursor = pre_cursor +6
            print(pre_cursor, post_cursor)
            while post_cursor < num_comp :
                #print(pre_cursor, post_cursor)
                
                #두 기업의 row 수를 맞춰야함
                X = data.iloc[:,list(range(pre_cursor,pre_cursor+6 ))]
                Y = data.iloc[:,list(range(post_cursor, post_cursor +6))]
                
                too_many_nan = False
               
    
                intersection_date = set(X.index[list(~np.isnan(X.iloc[:,5]))]).intersection(Y.index[list(~np.isnan(Y.iloc[:,5]))])
               
                
                inter_X = X.loc[intersection_date ,]
                inter_Y = Y.loc[intersection_date ,]
                
                
                X_index = inter_X.columns[0][:-6]
                Y_index = inter_Y.columns[0][:-6]
                
                if len(intersection_date) < skip_cf:
                    too_many_nan = True
                    post_cursor += 6
                    continue
                
                rv_coef = RV(inter_X, inter_Y )
                
                if not too_many_nan:
                    Y_comp_list.append((Y_index,  rv_coef))
                else:
                    skip_corp_list.append(Y_index)
                post_cursor +=6   
            
            
    
            X_comp_dict[X_index] = Y_comp_list
    
            pre_cursor +=6
            
            
            if len(list(X_comp_dict.keys())) ==0 :
                continue
            
            all_comp = [list(X_comp_dict.keys())[0]]
            all_comp.extend([comp[0] for comp in Y_comp_list])         
        all_comp =  list(set(all_comp))
        
    
        rv_coef_df = pd.DataFrame(index=all_comp, columns=all_comp)
           
        for X_comp in X_comp_dict.keys():
            for Y_comp in X_comp_dict[X_comp]:
                rv_coef_df.loc[X_comp,Y_comp[0]] = Y_comp[1]
    
            
        if not os.path.exists(wt_dir ):
                os.makedirs(wt_dir )
                
                
        skip_corp_txt = ''
        skip_corp_list = list(set(skip_corp_list))
        for skip_corp in skip_corp_list:
            skip_corp_txt += str(skip_corp) + '\n'
        
        with open(wt_dir +"\\skip_corp_list_"+ indexnm[18:-4]+ "_.txt", "w", encoding = 'utf-8') as err:
            err.write(skip_corp_txt)            
            
        rv_coef_df.to_csv(wt_dir  + "\\RV_Coeff_" + indexnm[18:])
        
