import pandas as pd
import numpy as np
import re

# 저장한 csv 자료로부터 총자산을 수집하는 코드

# PATH에 포함되어야할 것 : finance.csv (대회에서 제공한 제무제표 데이터)
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0


def SIZE(PATH, df, train=1):
    finance = pd.read_csv(PATH+'/finance.csv')
    finance=finance.drop_duplicates(['CO_NM'], keep = 'last')
    finance=finance.reset_index(drop=True)     
    for i in range(len(finance)):
        finance.loc[i,'CODE'] = re.sub('A','',finance.loc[i,'CODE'])
        
    idx=finance[finance['ASSET_SUM'] == ' - '].index
    finance=finance.drop(idx)
    finance=finance.reset_index(drop=True)
    for i in range(len(finance)):
        finance.loc[i,'ASSET_SUM']=finance.loc[i,'ASSET_SUM'].replace(',','')
    finance = finance.astype({'ASSET_SUM': 'float'})
    finance['SIZE']= np.log10(finance['ASSET_SUM'])
    size=finance[['CODE','SIZE']]
    df = pd.merge(df,size, on='CODE', how='inner')
    
    return df 