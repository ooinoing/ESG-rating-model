import pandas as pd
import os
import numpy as np
import dart_fss as dart

# 보고서 코드 구하는 함수 
# 사업보고서 다운 받기 전, 다운 받을 보고서 정보를 따로 저장

def rcept_no(PATH, SAVE_PATH):

    train = pd.read_excel(PATH+"train.xlsx")
    test = pd.read_excel(PATH+"test.xlsx")

    train.rename(columns = {'종목코드':"CODE", '종목명':"CO_NM"},inplace=True)
    test.rename(columns = {'종목코드':"CODE", '종목명':"CO_NM"},inplace=True)
    train['CODE'] = train['CODE'].apply(lambda x : str(x).zfill(6))
    test['CODE'] = test['CODE'].apply(lambda x : str(x).zfill(6))
    train.drop(["시장",	"E_GRADE"	,"S_GRADE","G_GRADE",	"ESG_GRADE"],axis=1,inplace=True)
    test.drop(["시장",	"E_GRADE"	,"S_GRADE","G_GRADE",	"ESG_GRADE"],axis=1,inplace=True)
    train[["rcept_no"]]=np.NaN
    test[["rcept_no"]]=np.NaN


    # Open DART API KEY 설정
    api_key='f500347222aa08270de912e213facf6b8e2cb58c'
    dart.set_api_key(api_key=api_key)

    # DART 에 공시된 회사 리스트 불러오기
    corp_list = dart.get_corp_list()

    def corp_info(stock_code, bsns_year):     # api 호출할때마다 필요한 정보(stock_code, bsns_year, reprt_code)를 반환
        if corp_list.find_by_stock_code(stock_code):
            corp_code = corp_list.find_by_stock_code(stock_code).corp_code
            reprt_code = 11011 # 사업보고서를 의미하는 보고서 코드
            return str(corp_code) , str(bsns_year), str(reprt_code)
        else :
            return np.NaN



    for stock_code in train["CODE"]:
        try:
            corp_code, bsns_year, reprt_code = corp_info(stock_code, 2021)
            info = dart.api.info.alot_matter(corp_code, bsns_year, reprt_code, api_key=None)
            rcept_no = info["list"][0]['rcept_no']
            train["rcept_no"][train["CODE"]==stock_code]=rcept_no
        except:
            continue

    for stock_code in test["CODE"]:
        try:
            corp_code, bsns_year, reprt_code = corp_info(stock_code, 2021)
            info = dart.api.info.alot_matter(corp_code, bsns_year, reprt_code, api_key=None)
            rcept_no = info["list"][0]['rcept_no']
            test["rcept_no"][test["CODE"]==stock_code]=rcept_no
        except:
            continue
        
    # 오류난 회사들은 분기보고서나 이전년도 사업보고서를 직접 채워주었습니다
    try:
        train["rcept_no"][train["CO_NM"]=='롯데푸드']="20220315001228"
        train["rcept_no"][train["CO_NM"]=='SBS미디어홀딩스']="20211115000845" # 분기보고서
        train["rcept_no"][train["CO_NM"]=='보락']="20220317000649"
        train["rcept_no"][train["CO_NM"]=='폴루스바이오팜']="20220329001342"
        train["rcept_no"][train["CO_NM"]=='SK머티리얼즈']="20211115001993"  # 분기보고서
        train["rcept_no"][train["CO_NM"]=='하림지주']="20220322001028"
        train["rcept_no"][train["CO_NM"]=='넥슨지티']="20220317000812"


        test["rcept_no"][test["CO_NM"]=='메리츠증권']="20220316001144"
        test["rcept_no"][test["CO_NM"]=='부산가스']="20220322000318"
        test["rcept_no"][test["CO_NM"]=='엔에스쇼핑']="20220322000614"
        test["rcept_no"][test["CO_NM"]=='무림페이퍼']="20220315000719"
        test["rcept_no"][test["CO_NM"]=='이베스트투자증권']="20220317000673"
        
    except:
        pass

    train.to_csv(SAVE_PATH + "rcept_no_train.csv", index = False)
    test.to_csv(SAVE_PATH + "rcept_no_test.csv", index = False)
    
    return 1