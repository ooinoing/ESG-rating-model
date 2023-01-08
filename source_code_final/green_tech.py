import pandas as pd
import re


# 녹색기술 기업 목록을 정리하여 피쳐로 저장하는 코드   
# csv 파일에 포함된 기업에 대해서는 1, 0로 데이터 프레임에 기록함
# PATH 에 포함되어야 할 것 : chromedriver.exe , 녹색기술.csv
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0

def GREEN_TECH(PATH, df, train =1):
    
    gre_tech = pd.read_csv(PATH + "/녹색기술.csv")
    corp_list=gre_tech['기관명']
        
    for i in range(len(corp_list)):
        if '(주)' in  corp_list[i] :
            corp_list[i] = corp_list[i].replace("(주)","")
        if '()' in  corp_list[i] :
            corp_list[i] = corp_list[i].replace('()','')
        if '(유)' in  corp_list[i]:
            corp_list[i] = corp_list[i].replace("(유)","")
        if '주식회사' in  corp_list[i] :
            corp_list[i] = corp_list[i].replace("주식회사","")
        if '유한회사' in  corp_list[i] :
            corp_list[i] = corp_list[i].replace("유한회사","")

        corp_list[i] = corp_list[i].replace(' ','')
        
    green_tech = set(corp_list) & set(df['CO_NM'])
    df['green_corp'] = 0

    for co_nm in df['CO_NM']:
        if co_nm in green_tech:
            df['green_corp'][df['CO_NM']==co_nm] = 1
            
    return df
        