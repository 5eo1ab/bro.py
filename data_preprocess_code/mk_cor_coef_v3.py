# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 21:23:28 2017

@author: User
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
    elif  type_set == 'adj':
        cov_sqr_adj =[1-(n-1)/(n-2)*(1-cov_sqr[i])  for i in range(len(cov_sqr))]  
        r = sum(cov_sqr_adj)
        
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
         
         elif type_set == 'adj':
             elemnum = 1- (n-1)/(n-2) * (1-elemnum)
             
         vecnum.append(elemnum)    
    num = sum(vecnum)
 
   #calculate denominator   
    denom1 = cal_RVDenom(data1, type_set)
    denom2 = cal_RVDenom(data2, type_set)
    
    RV = num/np.sqrt(denom1*denom2)
    #print(RV, denom1, denom2)
    return RV

#############################################################################################
#####################    필요한 파라미터 및 디렉토리 설정 부분      ###########################
#############################################################################################

#래 두개 변수만 수정하면 실행은 된다.
#작업 디렉토리
directory = r"C:\Users\User\Documents\bro_py\Preprocessed_dataset" #default directory
read_cvb_directory = 'Close_Volume_all_Beta'

############################################################################################
#################################      연산 부분      #######################################
#############################################################################################
os.chdir(directory)


skip_cf = 36

var_list = ['_Close', '_Volume', '_Beta_1', '_Beta_3', '_Beta_6', '_Beta_12']


temp = ['Close_Volume_Beta_DAX30.csv',
 #'Close_Volume_Beta_NIKKEI225.csv',
 #'Close_Volume_Beta_SnP500.csv',
 'Close_Volume_Beta_KOSPI200.csv',
 'Close_Volume_Beta_SSE50.csv',
 'date_period.txt',
 'err_text.txt']

index_nm_list = ['NIKKEI225', 'SnP500', 'SSE50', 'DAX30']
index_list= [] 
for indexnm in temp:
    skip_corp_list = []
    if indexnm[-4:] == '.txt': #csv 파일 아니면 continue
        continue
    if indexnm[-4:] == '.csv': #csv 파일 아니면 continue
        data_org = pd.read_csv(read_cvb_directory+'\\'+indexnm)
        index= indexnm[18:-4]
        index_list.append(index)
        data_org.index = data_org.iloc[:,0]
        data =data_org.drop(data_org.columns[0],1)
        
        f = open(index+"_Union_sltd_corp.txt", 'r')#, encoding = 'utf-8')
        corp_list = [corp.replace('\n','') for corp in f]
        f.close()
        corp_list.append(index)
        corp_list = list(set(corp_list))
        print(index)
        corp_var_list = [corp + '_' +var for corp in corp_list for var in var_list]
        rv_coef_df = pd.DataFrame(index=[corp_list], columns=[corp_list])
        
        X_comp_dict = dict()
        for i in range(len(corp_list)):
            print(corp_list[i])
            for j in range(i, len(corp_list)):

                
                corp1 = corp_list[i]
                corp2 = corp_list[j]
                
                
                Y_comp_list = []
                
                corp1_var_list = [corp1 + var for var in var_list]
                corp2_var_list = [corp2 + var for var in var_list]
                
                X = data.loc[:,corp1_var_list]
                Y = data.loc[:,corp2_var_list]

                too_many_nan = False
               

                intersection_beta12 = set(X.index[list(~np.isnan(X.loc[:,corp1+var_list[-1]]))]).intersection(Y.index[list(~np.isnan(Y.loc[:,corp2+var_list[-1]]))])
                intersection_volume = set(X.index[list(~np.isnan(X.loc[:,corp1+var_list[1]]))]).intersection(Y.index[list(~np.isnan(Y.loc[:,corp2+var_list[1]]))])
                
                
                if (len(intersection_volume) <= skip_cf) & (corp1 in index_nm_list) :
                    volume_list = [corp + '_Volume'for corp in corp_list]
                    X.loc[intersection_beta12, corp1+ '_Volume'] = data.loc[intersection_beta12, volume_list].sum(1)
                    
                elif (len(intersection_volume) <= skip_cf) & (corp2 in index_nm_list) :
                    volume_list = [corp + '_Volume'for corp in corp_list]
                    Y.loc[intersection_beta12, corp2+ '_Volume'] = data.loc[intersection_beta12, volume_list].sum(1)
                    
                    
                intersection_volume1 = set(X.index[list(~np.isnan(X.loc[:,corp1+var_list[1]]))]).intersection(Y.index[list(~np.isnan(Y.loc[:,corp2+var_list[1]]))])
                intersection_date = intersection_beta12.intersection(intersection_volume1)
                
                
                inter_X = X.loc[intersection_date ,]
                inter_Y = Y.loc[intersection_date ,]
                
                rv_coef = RV(inter_X, inter_Y )
                


                rv_coef_df.loc[corp1,corp2] =rv_coef

        if not os.path.exists(directory+"\\RV_coeff"+read_cvb_directory[-5:-2]+ "v3"):
                os.makedirs(directory+"\\RV_coeff"+read_cvb_directory[-5:-2]+ "v3")
                
                
        skip_corp_txt = ''
        skip_corp_list = list(set(skip_corp_list))
              
        rv_coef_df.to_csv(directory+"\\RV_coeff"+read_cvb_directory[-5:-2]+ "v3\\RV_Coeff_" + indexnm[18:])
        


