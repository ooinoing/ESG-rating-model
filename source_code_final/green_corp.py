import pandas as pd
import re


# 녹색기업으로 지정된 기업 목록을 정리하여 피쳐로 저장하는 코드   
# 엑셀 파일에 포함된 기업에 대해서는 1, 0로 데이터 프레임에 기록함
# PATH 에 포함되어야 할 것 : chromedriver.exe , 녹색기업 지정현황(2021. 03. 26 기준).xlsx
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0

def GREEN_CORP(PATH, df, train =1):
    gre_corp=pd.read_excel(PATH+ "/녹색기업 지정현황(2021. 03. 26 기준).xlsx")
    gre_corp = gre_corp['Unnamed: 1']
    gre_corp = gre_corp.dropna(axis=0)
    gre_corp=gre_corp.reset_index(drop=True)


    for i in range(len(gre_corp)):                           #기업명 전처리 작업 
        if '㈜' in  gre_corp.loc[i]  :
            gre_corp.loc[i] = re.sub(r"㈜","",gre_corp.loc[i])

    abc=[]
    for i in range(len(gre_corp)):
        abc.append(gre_corp.loc[i].split(' ')[0])
    for i in range(len(abc)):
        if '(주)' in  abc[i]  :
            abc[i] = abc[i].replace('(주)',"")
        if '()' in  abc[i]  :
            abc[i] = abc[i].replace('()',"")       
        if '주식회사' in  abc[i]  :
            abc[i] = abc[i].replace('주식회사',"")
        if 'htb' in  abc[i]  :
            abc[i] = abc[i].replace('htb',"")
    abc_set = set(abc)


    green_corp = abc_set & set(df['CO_NM'])
    df['green_corp'] = 0
    for co_nm in df['CO_NM']:
        if co_nm in green_corp:
            df['green_corp'][df['CO_NM']==co_nm] = 1

    return df 
 