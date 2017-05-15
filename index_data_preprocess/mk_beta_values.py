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
import scipy 


###################################################################
####################    필요한 함수 정의 부분      #################
###################################################################


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
            result = -1
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
def cal_bata(sorted_data, target_nm, time_range, signct = 0.05):
    reg = LinearRegression(fit_intercept=True)
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
    

#################################################################
#############    변수 및 파라미터 설정 부분      ###################
#################################################################
#beta 연산 관련
period_list = [1,3,6,12]  #beta 연산 기간(달 단위)
price = 'Close'#beta값 계산 할 price 기준
#price_colnm = ['Open', 'High', 'Low', 'Close', 'Volume'] #price 목록

#디렉토리 관련
directory = r"C:\Users\User\Documents\bro_py" #default directory
index_list = ['DAX30', 'kospi200_all', 'nikkei225', 'SnP500', 'SSE50']




#################################################################
#############    실제 연산 부분      ###################
#################################################################
#default 디렉토리 설정
os.chdir(directory)


cal_list = ['Date_org']
cal_list.append(price)

#------------------------------------
#아래 부분은 각 국가별 테이블을 csv 파일로 만들기위한 부분임
#(기존에는 한 기업 당 하나의 csv 파일이기 때문에 이후에 불러 쓰기가 번거로움 => 국 국가 내에 여러 기업에 대한 beta 값을 한 테이블에 붙임)

for period in period_list:
    #코드 실행 결과 출력 관련 
    err_msg='오류 발생한 회사들\n오류 내용 : 지수 이름, 회사 이름 \n'
    date_period = '각 회사 별 데이터에 날짜 범위'
    mk_directory = price+'_beta_each_index_'+str(period)  + '_v1'
        #아래 있는 코드는 각 기업 별 하나의 csv 파일
    for indexnm in index_list:
        count = 0
        if not os.path.exists(directory+"\\"+mk_directory):
                os.makedirs(directory+"\\"+mk_directory)
        print('#################################################################')
        print('===========================',indexnm,'===========================')
        date_period += '===============================' + indexnm  +'===============================\n'
        
        each_index_df = pd.DataFrame()
        for compnm in os.listdir(indexnm):
            try:
                data_org = pd.read_csv(indexnm+'\\'+compnm)
            except BaseException as e:
                mod_compnm = compnm.replace(' ','_')
                mod_compnm = mod_compnm.replace(' ', '_')
                try:
                    os.rename(indexnm+'\\'+compnm, indexnm+'\\' + mod_compnm)
                    data_org = pd.read_csv(indexnm+'\\' + mod_compnm)
                except BaseException as e:
                    err_msg +=  str(e) + " : " + indexnm + ', ' + compnm + '\n'
                    continue
    
    
    
            #아래 --- 표시한 부분 까지는 데이터 타입 정리하고, 날짜 순으로 sort 하는 부분임(데이터 정제)
            data_org.columns = ['Date_org', 'Open', 'High', 'Low', 'Close', 'Volume']
           
            data = data_org[cal_list].copy()
            
            data['Date'] = pd.to_datetime(data['Date_org'])
            try:
                data[price] = pd.to_numeric(data[price]) #수치 형으로 변환
            except ValueError:
                data[price] = pd.to_numeric(data[price].str.replace(',',''))
            
            data = data.drop('Date_org', axis =1) 
        
            data['Month'] = data['Date'].dt.month       
            
            sorted_data = data.sort(columns = 'Date', ascending=1).copy()
            sorted_data.index = range(len(sorted_data)-1,-1,-1)
           
            
            
            
            date_period += compnm + ' : ' + str(sorted_data.iloc[0]['Date'])[0:10] + ', ' + str(sorted_data.iloc[len(sorted_data)-1]['Date'])[0:10] + '\n'       
            print('--------------------',compnm,'-----------------------')
            
            cursor = len(sorted_data)-1 
            time_beta_dict = dict()
            #한 지수에 포함 되는 모든 기업에 대한 정보를 하나의 dict 안에 넣고, 한번에 dataframe으로 전환한다.
            while True:
                time_rng  =cal_index(sorted_data, cursor, period)
                
                if time_rng ==-1: 
                    break
                
                if len(time_rng) <10:#beta 구하는데 데이터 수가 너무 적을 경우(10보다 작은 경우) beta 값을 0으
                    cursor, end_day = end_date_index(sorted_data,cursor)
                    beta =0
                    continue
                                
                beta = cal_bata(sorted_data, price, time_rng)
                cursor, end_day = end_date_index(sorted_data,cursor)
                if cursor <=0:
                    break        
                time_beta_dict[str(end_day)[0:7]] =  beta #월 단위 까
                
            if time_beta_dict == {}:
                err_msg +=  '데이터 수가 10개 미만 이거나 데이터 기간이 period보다 짧음' + " : " + indexnm + ', ' + compnm + '\n'
                continue
            temp_df = pd.DataFrame.from_dict(time_beta_dict, orient= 'index')
            temp_df.columns = [compnm[0:-4].replace(' ','_')]
            if count ==0:
                each_index_df =  temp_df.copy()
            else:
                #temp_each_index_df = each_index_df.copy()
                each_index_df = pd.concat([each_index_df, temp_df], axis=1)
            count +=1

        each_index_df.to_csv(directory+"\\"+mk_directory+ "\\beta_" + indexnm + '.csv')
    with open(directory+"\\"+mk_directory+"\\"+'\\date_period.txt', "w", encoding = 'utf-8') as date_prod:
        date_prod.write(date_period) 
    
    with open(directory+"\\"+mk_directory+'\\err_text.txt', "w", encoding = 'utf-8') as err:
        err.write(err_msg)                                                      
        


