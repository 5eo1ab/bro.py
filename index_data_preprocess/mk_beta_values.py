# -*- coding: utf-8 -*-
"""
Created on Wed May 10 13:25:40 2017

@author: yeohyeongyu

beta 값 구하기 위한 클래스
이 클래스에서 최종적으로 출력 되는 데이터는 각 기업
Date(매달 말일) Beta


"""


import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta
import scipy 

directory = r"C:\Users\User\Documents\bro_py"
#directory1 = r'C:\Users\User\Documents\bro_py\kospi200_all'
os.chdir(directory)
#index_list = ['DAX30', 'kospi200_all', 'nikkei225', 'SnP500', 'SSE50']

#일단은 코스피 기업에 대해서만
indexnm= 'kospi200_all'


#start_index에서 ~ peirod_m 만큼 앞 시간 만큼에 index 반환
#ex) start_index = 3498이고 이날이 2014-01-31, period_m이 1이면 2014-01-데이터상 첫 일에 index 34xx 
#-> range( 34xx, 3498) 반환
def cal_index(data,start_index, period_m):
    pre_month = data.iloc[start_index]['Month']
    cur_index = start_index   
    count=0
    while True:  
        if pre_month != data.iloc[cur_index]['Month']: 
            pre_month = data.iloc[cur_index]['Month']
            count +=1
            if count == period_m:
                break   
        if cur_index <0: #or( count <= period_m):
            result = None
            break
        cur_index -=1
        result = range(cur_index+1, start_index)
    return result

#입력한 index에 날짜의 그 달에 마지막날 index 반환
#ex) index 1000일때의 date 값이 2014-01-05라면 2014-01-31에 해당하는 index 10xx  반환
def end_date_index(data, start_index):
    pre_month = data.iloc[start_index]['Month']
    cur_index = start_index
    while True:  
        if pre_month != data.iloc[cur_index]['Month']: 
            break   
        cur_index -=1
    return cur_index, data.iloc[cur_index]['Date']

#data와 index범위 입력하면 x축 시간에 대한 index(1~i까지), y축 price로 해서 회기식의 기울기 값 반환
#이때 회귀 모델 자체에 대한 F 검정과, beta 값에대한 t 검정해서 유의하지 않으면 beta =0 반환
def cal_bata(sorted_data, target_nm, time_range, reg, signct = 0.05):
    X = (np.array(time_rng) -time_rng[0]+1).reshape(-1,1) #들어온 index 값이 X값이 된다.
    y = np.array(sorted_data[target_nm])[time_rng]
    reg.fit(X,y)  
    y_pred = reg.predict(X)
    
    beta = reg.coef_[0]
    n = len(X)
    
    SSE = sum((y - y_pred)**2)
    MSR= sum((np.mean(y) - y_pred)**2)
    MSE = SSE /(n-2)
    F_val = MSR / MSE
    
    
    SE_beta_i = np.sqrt( MSE / sum((X- np.mean(X))**2)[0])
    t_val = beta / SE_beta_i
    
    M_p_val = 1- scipy.stats.f.cdf(F_val,1, n-2)
    beta_p_val = 1- scipy.stats.t.cdf(abs(t_val), n-2)
    
    #모델 자체가 의미가 없거나, beta 값이 의미가 없는 경우 beta값을 0으로 한다.
    #모델 의미 없는데 beta 값만 의미 있다 나올 수도 있으므로 순서는 아래처럼
    if (M_p_val > signct) :
        beta = 0
    if (beta_p_val > signct/2):
        beta = 0
    return beta
    

   

reg = LinearRegression(fit_intercept=True)
period = 1


price_colnm = ['Open', 'High', 'Low', 'Close', 'Volume']
data_period = ''

price = 'Close'
cal_list = ['Date_org']
cal_list.append(price)





for compnm in os.listdir(indexnm)[0:2]:
    #아래 --- 표시한 부분 까지는 데이터 타입 정리하고, 날짜 순으로 sort 하는 부분임(데이터 정제)
    data_org = pd.read_csv(indexnm+'\\'+compnm)
    data_org.columns = ['Date_org', 'Open', 'High', 'Low', 'Close', 'Volume']
   
    data = data_org[cal_list].copy()
    
    data['Date'] = pd.to_datetime(data['Date_org'])
    data[price] = pd.to_numeric(data[price])
    data = data.drop('Date_org', axis =1) 

    data['Month'] = data['Date'].dt.month       
    
    sorted_data = data.sort(columns = 'Date', ascending=1).copy()
    sorted_data.index = range(len(sorted_data)-1,-1,-1)

    print('--------------------',compnm,'-----------------------')
    cursor = len(sorted_data)-1 
    time_beta_dict = dict()
    while True:
        time_rng  =cal_index(sorted_data, cursor, period)
        if time_rng ==None or len(time_rng) <10:
            break
        cal_bata(sorted_data, price, time_rng, reg)
        cursor, end_day = end_date_index(sorted_data,cursor)
        if cursor <=0:
            break        
        time_beta_dict[end_day] = cal_bata(sorted_data, price, time_rng, reg)




        



