import os
import requests
from bs4 import BeautifulSoup
import dart_fss as dart
import pandas as pd
import numpy as np


#######################################################3
# 경로 지정
# SAVE_PATH = 완성된 데이터셋을 저장할 경로
# FILE_PATH = train.xlsx test.xlsx가 포함되어있어야함
FILE_PATH = '/Users/jeeho/lab/miraeasset/mirae_env/최종/data' # train.xlsx, test.xlsx 가 저장된 폴더
SAVE_PATH = '/Users/jeeho/lab/miraeasset/mirae_env/최종/dataout'
#######################################################

# train, test set에서 기업코드, 기업명만 저장해놓은 데이터 프레임을 불러오는 과정

train= pd.read_excel(FILE_PATH+"/train.xlsx")
train.rename(columns = {'종목코드':"CODE", '종목명':"CO_NM"},inplace=True)
train['CODE'] = train['CODE'].apply(lambda x : str(x).zfill(6))
train=train[['CODE','CO_NM']]
train[["PER", "PBR", "DVR"]] = np.NaN


test= pd.read_excel(FILE_PATH+"/test.xlsx")
test.rename(columns = {'종목코드':"CODE", '종목명':"CO_NM"},inplace=True)
test['CODE'] = test['CODE'].apply(lambda x : str(x).zfill(6))
test=test[['CODE','CO_NM']]
test[["PER", "PBR", "DVR"]] = np.NaN



def corp_info(stock_code, bsns_year, corp_list):     # api 호출할때마다 필요한 정보(stock_code, bsns_year, reprt_code)를 반환
  if corp_list.find_by_stock_code(stock_code):
    corp_code = corp_list.find_by_stock_code(stock_code).corp_code # corp_code : 기업코드 -> 따로 조회해야해서 corp_info 함수를 사용
    reprt_code = 11011 # 사업보고서를 의미하는 보고서 코드
    return str(corp_code) , str(bsns_year), str(reprt_code)
  else :
    return np.NaN


# 하나의 기업에 대해 per, pbr, dvr 크롤링해오는 함수 
# df : 데이터 프레임 (test 혹은 train)
def get_per_pbr_dvr(df, stock_code, corp_code, bsns_year, reprt_code, idx):
    try:
        per_selector = "#_per"
        pbr_selector = "#_pbr"
        dividend_yield_selector = "#_dvr"
        url = "https://finance.naver.com/item/main.naver?code="+stock_code
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html5lib")
        per = soup.select(per_selector)
        pbr = soup.select(pbr_selector)
        dividend_yield = soup.select(dividend_yield_selector)

        fin_per = per[0].text if per else np.NaN
        fin_pbr = pbr[0].text if pbr else np.NaN
        fin_dvr = dividend_yield[0].text if dividend_yield else np.NaN
        
    except:    
        fin_per = np.NaN
        fin_pbr = np.NaN
        fin_dvr = np.NaN

    try:
        idx=list(df["CODE"]==stock_code).index(True)
        df["PER"][idx]=fin_per
        df["PBR"][idx]=fin_pbr
        df["DVR"][idx]=fin_dvr
    except:
        pass

    return df


################################################
def PER_PBR_DVR(df):
    api_key='f500347222aa08270de912e213facf6b8e2cb58c'      # Open DART API KEY 설정
    dart.set_api_key(api_key=api_key)
    corp_list = dart.get_corp_list()        # DART 에 공시된 회사 리스트 불러오기

    for stock_code in df["CODE"]:
        try:
            corp_code, bsns_year, reprt_code = corp_info(stock_code, 2021,corp_list)
        except:
            continue
        try:
            idx=list(df["CODE"]==stock_code).index(True)
            df = get_per_pbr_dvr(df,stock_code,corp_code, bsns_year, reprt_code, idx)
        except:
            pass
        try:
            df = get_per_pbr_dvr(df,stock_code,corp_code, bsns_year, reprt_code, idx)
        except:
            pass
    return df


#######################################################
# 실제 크롤링 진행 및 결과 저장

train = PER_PBR_DVR(train)
train.to_csv(SAVE_PATH+"/PER_PBR_DVR_train.csv", index= False,mode='w')

test = PER_PBR_DVR(test)
test.to_csv(SAVE_PATH+"/PER_PBR_DVR_test.csv", index= False,mode='w')

