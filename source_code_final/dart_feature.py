## div_cur 
## div_change	
## major_hldr	
## minor_hldr	
##outer_dir	
## dir_gender	
## total_emp	
## emp_gender
import pandas as pd
import os
import numpy as np
import dart_fss as dart
import requests
from bs4 import BeautifulSoup


#######################################################3
FILE_PATH = '/Users/jeeho/lab/miraeasset/mirae_env/최종/data' # train.xlsx, test.xlsx 가 저장된 폴더
SAVE_PATH = '/Users/jeeho/lab/miraeasset/mirae_env/최종/dataout'
#######################################################
train= pd.read_excel(FILE_PATH+"/train.xlsx")
train.rename(columns = {'종목코드':"CODE", '종목명':"CO_NM"},inplace=True)
train['CODE'] = train['CODE'].apply(lambda x : str(x).zfill(6))
train=train[['CODE','CO_NM']]
train[["major_hldr","minor_hldr"]] = np.NaN
#train[["div_cur","div_change","major_hldr","minor_hldr","outer_dir","dir_gender","total_emp","emp_gender"]] = np.NaN

test= pd.read_excel(FILE_PATH+"/test.xlsx")
test.rename(columns = {'종목코드':"CODE", '종목명':"CO_NM"},inplace=True)
test['CODE'] = test['CODE'].apply(lambda x : str(x).zfill(6))
test=test[['CODE','CO_NM']]
test[["major_hldr","minor_hldr"]] = np.NaN

#test[["div_cur","div_change","major_hldr","minor_hldr","outer_dir","dir_gender","total_emp","emp_gender"]] = np.NaN
#######################################################
api_key='f500347222aa08270de912e213facf6b8e2cb58c'  # Open DART API KEY 설정
dart.set_api_key(api_key=api_key)
corp_list = dart.get_corp_list()    # DART 에 공시된 회사 리스트 불러오기
#######################################################



def corp_info(stock_code, bsns_year,corp_list):     # api 호출할때마다 필요한 정보(stock_code, bsns_year, reprt_code)를 반환
  if corp_list.find_by_stock_code(stock_code):
    corp_code = corp_list.find_by_stock_code(stock_code).corp_code
    reprt_code = 11011 # 사업보고서를 의미하는 보고서 코드
    return str(corp_code) , str(bsns_year), str(reprt_code)
  else :
    return np.NaN

def clean(str, rep = np.NaN):                   # 보고서마다 표현 통일
  str = str.replace(',','')
  str = str.replace(' ','')
  str = str.replace('년','.')
  str = str.replace('개월','')
  str = str.replace('\n','\0')
  return np.NaN if str in '-.' else float(str)

def clean_0(str):                   # 보고서마다 표현 통일
  str = str.replace(',','')
  str = str.replace(' ','')
  str = str.replace('년','.')
  str = str.replace('개월','')
  str = str.replace('\n','\0')
  return 0 if str in '-.' else float(str)

def get_dart_api_feature(df, stock_code, corp_code, bsns_year, reprt_code, idx):
    ## 배당에 관한 사항 
    '''
    try:
        alot_matter = dart.api.info.alot_matter(corp_code, bsns_year, reprt_code, api_key=None)
        thstrm = alot_matter['list'][6]['thstrm'] # 당기
        frmtrm = alot_matter['list'][6]['frmtrm'] # 전기
        thstrm,frmtrm = list(map(clean, [thstrm,frmtrm]))
        df["div_cur"][idx]= thstrm/100    #현금배당성향_당기
        df["div_change"][idx]= (thstrm-frmtrm)/100 #현금배당성향_변화
        
    except:
        df["div_cur"][idx]= np.NaN
        df["div_change"][idx]= np.NaN
    '''

    ## 대주주 지분율(%) 
    try:
        hyslr=dart.api.info.hyslr_sttus(corp_code, bsns_year, reprt_code, api_key=None)
        result = [hyslr['list'][-1]['trmend_posesn_stock_qota_rt'], hyslr['list'][-2]['trmend_posesn_stock_qota_rt']] # result = [보통주, 우선주]
        major_hold_stock_ratio = sum(list(map(clean_0, result)))   # 보고서 상에 결측치 '-' 로 표시된 부분 처리
        df["major_hldr"][idx]= major_hold_stock_ratio/100
    except:
        df["major_hldr"][idx] = np.NaN

    ## 소액주주 지분율(%) 
    try:
        mrhl = dart.api.info.mrhl_sttus(corp_code, bsns_year, reprt_code, api_key=None)
        minor_hold_stock_ratio = list(map(clean_0, mrhl['list'][0]['hold_stock_rate'][:-1]))[0]
        df["minor_hldr"][idx]= minor_hold_stock_ratio/100
    except:
        df["minor_hldr"][idx]= np.NaN
    '''
    ## 사외이사 비율(%) 
    try:
        outcmpny_drctr= dart.api.info.outcmpny_drctr_nd_change_sttus(corp_code, bsns_year, reprt_code, api_key=None)
        otcmp_drctr_co, drctr_co = outcmpny_drctr['list'][0]['otcmp_drctr_co'],outcmpny_drctr['list'][0]['drctr_co']
        otcmp_drctr_co, drctr_co = list(map(clean, [otcmp_drctr_co, drctr_co]))
        otcmp_drctr_ratio = otcmp_drctr_co/drctr_co
        df["outer_dir"][idx]= otcmp_drctr_ratio
    except:
        df["outer_dir"][idx] = np.NaN

    ## 임원 성비 
    try:
        exctv=dart.api.info.exctv_sttus(corp_code, bsns_year, reprt_code, api_key=None)
        if len(exctv['list'])==0:
            exctv_ratio = np.NaN
        else :
            exctv_female = 0
            for i in range(len(exctv['list'])):
                if exctv['list'][i]['sexdstn']=='여':
                    exctv_female+=1
            exctv_ratio = exctv_female/len(exctv['list'])
            
        df["dir_gender"][idx]= exctv_ratio
    except:
        df["dir_gender"][idx] = np.NaN

    ## 직원 수, 성비
    try:
        emp=dart.api.info.emp_sttus(corp_code, bsns_year, reprt_code, api_key=None)
        sm=0
        emp_female = 0
        sector_female = 0

        for sector in emp['list']:
          sm += clean(sector['sm'])
          if sector['sexdstn']=='여':
            sector_female+=1
            emp_female += clean(sector['sm'])
            
        df["total_emp"][idx]= sm
        df["emp_gender"][idx] = emp_female/sm 

    except:   
        df["total_emp"][idx]= np.NaN
        df["emp_gender"][idx]= np.NaN
    '''

    return df

###################################################
#corp_code, bsns_year, reprt_code = corp_info('090430',2021,corp_list)

#hyslr=dart.api.info.hyslr_sttus(corp_code, bsns_year, reprt_code, api_key=None)
#result = [hyslr['list'][-1]['trmend_posesn_stock_qota_rt'], hyslr['list'][-2]['trmend_posesn_stock_qota_rt']] # result = [보통주, 우선주]

#major_hold_stock_ratio = sum(list(map(clean_0, result)))   # 보고서 상에 결측치 '-' 로 표시된 부분 처리

#mrhl = dart.api.info.mrhl_sttus(corp_code, bsns_year, reprt_code, api_key=None)
#minor_hold_stock_ratio = list(map(clean_0, mrhl['list'][0]['hold_stock_rate'][:-1]))[0]


#print(result)
#print(minor_hold_stock_ratio)
#i= list(map(clean_0, result))
#for j in i:
#    print(j)
#print(major_hold_stock_ratio)

#### 종목코드별로 채우기
for stock_code in train["CODE"]:
    try:
        corp_code, bsns_year, reprt_code = corp_info(stock_code, 2021,corp_list)
    except:
        continue
    try:
        idx=list(train["CODE"]==stock_code).index(True)
        train = get_dart_api_feature(train,stock_code,corp_code, bsns_year, reprt_code, idx)
    except:
        pass
    
for stock_code in test["CODE"]:
    try:
        corp_code, bsns_year, reprt_code = corp_info(stock_code, 2021,corp_list)
    except:
        continue
    try:
        idx=list(test["CODE"]==stock_code).index(True)
        test = get_dart_api_feature(test,stock_code,corp_code, bsns_year, reprt_code, idx)
    except:
        pass

##### 저장 
train.to_csv(SAVE_PATH+"/hldr_train.csv", index= False,mode='w')
test.to_csv(SAVE_PATH+"/hldr_test.csv", index= False,mode='w')
