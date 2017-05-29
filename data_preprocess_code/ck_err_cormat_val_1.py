
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
#index_list = ['Close_Volume_Beta_DAX30_all.csv', 'Close_Volume_Beta_kospi200_all_all.csv', 'Close_Volume_Beta_nikkei225_all.csv', 'Close_Volume_Beta_SnP500_all.csv', 'Close_Volume_Beta_SSE50_all.csv']

skip_cf = 48 #기업 데이터가 4년 미만일 경우 skip
#################################################################
#############    실제 연산 부분      ###################
#################################################################
#default 디렉토리 설정
os.chdir(directory)

rd_dir = 'Preprocessed_dataset\\Close_Volume_all_Beta\\'
wt_dir = 'Preprocessed_dataset\\Network_Data_all\\'



if not os.path.exists(wt_dir):
        os.makedirs(wt_dir )

from collections import Counter

corp_list_dict = {}
corp_df = {}
rm_list = ['_Close', '_Volume', '_Beta_1', '_Beta_3', '_Beta_6', '_Beta_12']
for indexnm in os.listdir(rd_dir):
    if indexnm[-3:] == 'csv':
        col_list = []
        print(indexnm[18:-4])
        data_org = pd.read_csv(rd_dir+'\\'+indexnm)
        colnms = data_org.columns[1:]
        
        for col in colnms:
             col_list.extend([col.replace(rm,'') for rm in rm_list if rm in col])
             cnt = Counter(col_list)
        corp_list =[ k for k,v in cnt.items() if v>1]
        corp_list_dict[indexnm[18:-4]] = corp_list 
        corp_df[indexnm[18:-4]] = data_org
        
        