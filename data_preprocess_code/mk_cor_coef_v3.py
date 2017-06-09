# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 21:23:28 2017

@author: User
"""


import os
import pandas as pd
import numpy as np
#from sklearn.linear_model import LinearRegression
#import scipy 



#############################################################################################
#####################    필요한 파라미터 및 디렉토리 설정 부분      ###########################
#############################################################################################

#래 두개 변수만 수정하면 실행은 된다.
#작업 디렉토리
directory = r"C:\Users\User\Documents\bro_py\Preprocessed_dataset\Close_Volume_all_Beta" #default directory



############################################################################################
#################################      연산 부분      #######################################
#############################################################################################
#=================================================================================
#==================== 데이터 불러와 사용 가능한 형태로 변환  =======================
#=================================================================================
#saeron
#analysis_comp = '3128135376'
#fb = 'f'
###comp_list_df= pd.read_csv(rd_dir+'\\behind_saeron.csv')
###dl_comp_list = list(set([str(int(i))  for i in comp_list_df.SUP_RGNO[~np.isnan(comp_list_df.SUP_RGNO)]]))
##
#comp_list_df= pd.read_csv(rd_dir+'\\front_saeron.csv')
#dl_comp_list = list(set([str(int(i))  for i in comp_list_df.BYR_RGNO[~np.isnan(comp_list_df.BYR_RGNO)]]))

#sangshin
#analysis_comp = '5148103617'
#fb = 'f'
####comp_list_df= pd.read_csv(rd_dir+'\\behind_sangshin.csv')
####dl_comp_list = list(set([str(int(i))  for i in comp_list_df.SUP_RGNO[~np.isnan(comp_list_df.SUP_RGNO)]]))
##
#comp_list_df= pd.read_csv(rd_dir+'\\front_sangshin.csv')
#dl_comp_list = list(set([str(int(i))  for i in comp_list_df.BYR_RGNO[~np.isnan(comp_list_df.BYR_RGNO)]]))
#

##KB
analysis_comp = '2048112301'
fb='f'
##comp_list_df= pd.read_csv(rd_dir+'\\behind_KB.csv')
##dl_comp_list = list(set([str(int(i))  for i in comp_list_df.SUP_RGNO[~np.isnan(comp_list_df.SUP_RGNO)]]))
#
comp_list_df= pd.read_csv(rd_dir+'\\front_KB.csv')
dl_comp_list = list(set([str(int(i))  for i in comp_list_df.BYR_RGNO[~np.isnan(comp_list_df.BYR_RGNO)]]))




#분석 대상 기업과 거래한 기업 목록 불러오기
#comp_list_df= pd.read_csv(rd_dir+'com_list\\suppliers_list.csv')
#dl_comp_list= comp_list_df.loc[:,analysis_comp][1:].dropna()



#입력한 기업 목록 전체, 코드가 10 자리 넘어가는 기업 목록은 버림 
comp_list_org = []
comp_list_org.append(analysis_comp)
comp_list_org.extend(dl_comp_list)
comp_list = [ str(int(comp)) for comp in comp_list_org if len(str(int(comp)))==10 ]


#생성한 데이터 출력하는 디렉토리 없으면 만들기 
if not os.path.exists(mk_dir):
        os.makedirs(mk_dir)


#매출액 데이터 
sales_data_org = pd.read_csv(rd_dir+ raw_data_file_nm)

rd_list = ['Date']
rd_list.extend(comp_list)
sales_data_org = sales_data_org.loc[:, rd_list]

#거래액이 0인 데이터는 모두 결측으로 바꿈(수치형이기 때문에 0으로 계산하면 의미를 가짐)
#=>결측값으로 바꿔서 상관계수나 beta 구하는데 의미 갖지 않게함.
sales_data_org ['Date'] = pd.to_numeric(sales_data_org ['Date'])
sales_data = sales_data_org .sort_values(by= ['Date'], ascending=1).copy()
sales_data.index = range(len(sales_data ))
sales_data = sales_data .replace(0, np.nan)
sales_data.index= sales_data.Date
sales_data =sales_data.drop('Date',1)

sales_data.index
#매출액 raw data에서 대부분의 기업이 4월 데이터의 매출이 급격히 떨어지는 것으로 보아 아직 집계가 안된 것 같음 => 마지막 달 빼고 연산
#sales_data = sales_data.drop([201704],0)
#2017년 전체 뺄 경우
sales_data = sales_data.drop([201701, 201702, 201703, 201704],0)



###########################################################################################################################
#########  아래 연산하는부분에서 dtw 계산하는 부분과 다중 산관관계 계산하는 부분은 완전 독립적으로 계산됨  #####################
###########################################################################################################################

##################################################
#########   다중 상관관계 계산 부분   #############
#################################################

#================================================================================
#======================= beta , diff 추가한 데이터 생성  ========================
#================================================================================
#입력 파라미터
#   data:  위에서 전처리한 raw 데이터
#   comp_list : 분석 대상 기업 + VC 기업 목록
#   period_list : beta 값 구할 때 정해 준 기간
#   mk_dir : 생성한 데이터 출력 디렉토리
#   wrt_file : False면 파일 출력안하고, True면 함
#출력 값
#   add_beta_df : beta 추가한 데이터셋(ex ) A_corp  -> A_corp| A_corp_beta_3 | A_corp_beta_6 ...
#   var_list : 새로 생성된 데이터 셋에서 기업명 뒤에 붙는 변수 이름 목록(ex) sales, beta_1, beta_2 ...) 나중에 연산에서 쓴다. 
    
    
#파라미터 설정
period_list = [1, 3, 6,12]  #beta 연산 기간(달 단위)
add_beta_df, var_list = mkbt.mk_beta_diff_val(analysis_comp, fb, sales_data, comp_list, period_list, mk_dir, True)



#================================================================================
#===== 데이터와 lag time 입력하면 원래 데이터에 lag한 데이터 추가해서 반환  ========
#================================================================================
#입력 파라미터
#   add_beta_df: beta값이 추가된 데이터(위에서 출력한 데이터)
#   lag_time : lag 적용할 개월 수 (ex) t=3일 경우 lag 1 ~ lag 3까지 적용된 데이터가 추가 됨
#출력 값
#   beta_lag_df  : 입력 한  데이터에 lag된 컬럼이 추가 된 데이터 셋

#파라미터 설정
lag_time = 12
beta_lag_df = mkbt.mk_lag_data(add_beta_df, lag_time) 
beta_lag_df.columns

beta_lag_df.to_csv( mk_dir + "\\Sales_Diff_Beta_lag.csv")
#================================================================================
#======================== 상관관계 행렬 만들기  ==================================
#================================================================================
#입력 파라미터
#   beta_lag_df: lag된 컬럼이 추가 된 데이터 셋
#   comp_list : 분석 대상 기업 + VC 기업 목록
#   skip_cf : 다중상관계수 계산할 때 두 기업의 데이터가 모두 있는 개월 수가 skip_cf 보다 작을 경우 상관관계가 0으로 계산
#   var_list :컬럼 명(기업명+변수)형태에서 기업명 뒤에 붙는 변수 이름 목록 (lag_n은 빠져 있음 )
#   mk_dir : 생성한 데이터 저장 디렉토리
#   analysis_comp : 분석 대상 기업
#   lag_time : lag 적용할 개월 수
#   wrt_file :상관계수 csv로  출력할 지 여부
#출력 값
#   cor_mat : 상관계수 
#
#파라미터 설정
skip_cf = 12

#cor_mat = mkcor.mk_analysis_comp_mcor(beta_lag_df, comp_list, skip_cf, var_list ,mk_dir, analysis_comp, fb, lag_time, wrt_file=True, only_lag =True, type_set = 'orig')
#cor_mat = mkcor.mk_analysis_comp_mcor(beta_lag_df, comp_list, skip_cf, var_list ,mk_dir, analysis_comp, fb, lag_time, wrt_file=True, only_lag =True, type_set = 'mod')
cor_mat = mkcor.mk_analysis_comp_mcor(beta_lag_df, comp_list, skip_cf, var_list ,mk_dir, analysis_comp, fb, lag_time, wrt_file=True, only_lag =True, type_set = 'adj')

sortd_cor_mat = cor_mat.sort_values(by= [alalysis_comp], ascending=1).copy()


#################################################################################################
##############   DTW와 상관관계로 뽑힌 기업들의 매출액 추이가 실제 비슷한지 확인   ##################
#################################################################################################
comp1_code = analysis_comp #분석 대상 기업
comp2_code = '3128135376' #매출액 추이 비교 할 기업
s2_lag = 12#comp2의 lag time
#분석 비교 기간
period =24
print('========== last date : ',  sales_data.index[-1],'===============')
s12 = sales_data.loc[:,[comp1_code, comp2_code]].dropna().copy()
s1 = s12.iloc[:,0]
s2 = s12.iloc[:,1]



ck_pt.mk_diff_plot(comp1_code, comp2_code,s1, s2, s2_lag, period, print_s2 = True)

#s2.loc[s1.index[40:45],]

