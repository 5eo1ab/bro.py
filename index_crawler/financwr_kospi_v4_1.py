# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 13:58:38 2017

@author: User
"""
#한번 이상 등장한 기업
#최신

from selenium import webdriver
import os
import time
import pandas as pd 
import shutil

###################################################################
####################    필요한 함수 정의 부분      #################
###################################################################

def file_copy_move(old, new):
    shutil.copy2(old, new)
#
#def code_dup_check(comp_code_dict):
#    code_dup_temp = list(comp_code_dict.values())
#    dup_list = list()
#    for i in comp_code_dict.values():
#        if code_dup_temp.count(i) >=2:
#            dup_list.append(i)
#    return list(set(dup_list))
# 
#def find_dup_code_comp_dict(code_dup_list, comp_code_dict):
#    dup_code_comp_dict  = dict()
#    for dup_code in code_dup_list:
#        temp_dup_comp =[]
#        for code, comp in comp_code_dict.items():
#            if code== dup_code:
#                temp_dup_comp.append(comp)
#        dup_code_comp_dict[dup_code]=temp_dup_comp
#    return dup_code_comp_dict


def get_ccode(comp_code):
    lenstr = len(str(comp_code))
    if lenstr < 6:
        comp_code='0'*(6-lenstr)+ str(comp_code)   
    return str(comp_code)


def get_url(baseurl, ccode, startdate, enddate):
    all_list = []
    all_list.append(ccode)
    all_list.extend(startdate)
    all_list.extend(enddate)
    return baseurl.format(*all_list)


def get_google_comp_nm(driver, comp_code_dict, key):
    comp_name = driver.find_element_by_class_name('appbar-snippet-primary').text #google finance에 있는 기업 이름
    return comp_name


def data_down(driver):
    down_url = driver.find_element_by_class_name('nowrap').get_attribute('href')    
    driver.get(down_url)


#입력한 폴더에 파일에서 한번이라도 등장한 종목과 코드 반환(key가 종목명이므로 같은 기업이 여러번 나올 경우 최근에 사용한 코드로 할거임(파일명 역순으로 해서....) )
def mk_comp_code_dict(folder_nm):
    comp_code_dict = dict()
    for file_name in sorted(os.listdir(folder_nm), reverse=True):
        list_file =pd.read_excel(folder_nm + '//'+file_name)
        for code, comp in list_file.loc[:,['종목코드', '종목명']].values:
            comp_code_dict[code] = comp
    return comp_code_dict


###################################################################
#############    변수 및 파라미터 설정 부분      ###################
###################################################################
directory = r"C:\Users\yeohyeongyu\Desktop\finance_data"

baseurl = 'https://www.google.com/finance/historical?q=KRX%3A{}&&startdate={}+{}%2C+{}&enddate={}+{}%2C+{}'
startdate = ['Jan', 1, 1995]
enddate = ['Apr', 1, 2017]

#############################################################
####################    실행 부분      #######################
#############################################################
os.chdir(directory)



# 한번이라도 등장한 기업 목록 뽑기(code 기준으로 중복되는 기업명 제거, 남기는 기업명은 최근에 사용된 기업명)
org_comp_code_dict = mk_comp_code_dict('kospi200_data')    

# key : google finanace에서 검색가능한 형태의 코드 , value : 기업명
mode_code_dict = dict()
for key in org_comp_code_dict.keys():
    mode_code_dict[str(get_ccode(key))] = org_comp_code_dict[key]





#driver 실행 
driver = webdriver.Chrome(r"Chromdriver\chromedriver.exe")
driver.implicitly_wait(4)



krgog_comp_code_dict = dict() #key : 한글이름_영어이름, value : code
not_found_code = []
for key in mode_code_dict.keys():
    URL =get_url(baseurl, key, startdate, enddate)
    driver.get(URL)
    time.sleep(0.7)
    try:
        data_down(driver)
        comp_nm = get_google_comp_nm(driver, mode_code_dict, key)
        krgog_comp_code_dict[key] = str(mode_code_dict[key]) + '(' + str(comp_nm) + ')'
    except:
        not_found_code.append(str(key)+ ':'+ str(mode_code_dict[key]))
    time.sleep(0.5)

print("----------------코드가 검색되지 않는 기업들 ---------------------")
for i in not_found_code:
    print(i)  

time.sleep(2) # 다 받아 질 때 까지 기다려




err_text = '--------------------error message------------------------\n'
#데이터 수집 053000기준일로 된 폴더 없으면 만들어라
for key in krgog_comp_code_dict.keys():
    try:
        old = r'C:\Users\yeohyeongyu\Downloads'+'\\'+str(key)+'.csv'
        new =  r'C:\Users\yeohyeongyu\Desktop\finance_data\kospi200_a'+'\\'+str(krgog_comp_code_dict[key])+'_'+str(key)+'.csv'
        file_copy_move(old, new)
    except KeyError:
        err_text += str('google finance 검색 안된 기업 code: %s, name: %s\n'%(key, str(mode_code_dict[key]))) 
    except FileNotFoundError:
        err_text += str('google finance 검색은 됐지만, 자료 다운 못한 기업 code: %s, name: %s\n'%(key, str(krgog_comp_code_dict[key])))
err_text += '-----------------------------------------------------\n\n'
print(err_text)
with open('kospi200_a\\err_text.txt', "w") as err:
    err.write(err_text)
    