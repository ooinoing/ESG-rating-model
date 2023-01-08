import numpy as np
import pandas as pd
import re

def OPOS(PATH, SAVE_PATH, df):
    
    finance = pd.read_csv(PATH+'/finance.csv')
    finance=finance.drop_duplicates(['CO_NM'], keep = 'last')
    finance=finance.reset_index(drop=True)     
    for i in range(len(finance)):
        finance.loc[i,'CODE'] = re.sub('A','',finance.loc[i,'CODE'])
            
    idx=finance[finance['BIZ_PROFIT'] == ' - '].index     # 결측치인 값들의 인덱스 찾기
    finance=finance.drop(idx)                             # 결측치 값 제거 
    idx2=finance[finance['SALE_COST'] ==' - '].index     
    finance=finance.drop(idx2)
    finance=finance.reset_index(drop=True)
        
    for i in range(0,len(finance)):
        finance.loc[i,'BIZ_PROFIT']=finance.loc[i,'BIZ_PROFIT'].replace(',','').strip()     # 쉼표 지우기 
    for i in range(0,len(finance)):
        finance.loc[i,'SALE_COST']=finance.loc[i,'SALE_COST'].replace(',','').strip() 
            
    finance = finance.astype({'BIZ_PROFIT': 'float'})  #object -> float 데이터 타입 수정 
    finance = finance.astype({'SALE_COST': 'float'})        
    finance['OPOS'] = finance['BIZ_PROFIT'] /finance['SALE_COST']   #OPOS 값 구하기 
    
    opos=finance[['CODE','OPOS']]
    df=pd.merge(df,opos, on='CODE', how='inner')
    return df 


def NOE(PATH, SAVE_PATH, df):
        
    finance = pd.read_csv(PATH+'/finance.csv')
    finance=finance.drop_duplicates(['CO_NM'], keep = 'last')
    finance=finance.reset_index(drop=True)     
    for i in range(len(finance)):
        finance.loc[i,'CODE'] = re.sub('A','',finance.loc[i,'CODE'])
    
    idx=finance[finance['THIS_TERM_PROFIT'] == ' - '].index     # 결측치인 값들의 인덱스 찾기
    finance=finance.drop(idx)                             # 결측치 값 제거 
    idx2=finance[finance['CAPITAL_AMT'] ==' - '].index     
    finance=finance.drop(idx2)
    finance=finance.reset_index(drop=True)
    for i in range(0,len(finance)):
         finance.loc[i,'THIS_TERM_PROFIT']=finance.loc[i,'THIS_TERM_PROFIT'].replace(',','').strip()     # 쉼표 지우기 
    for i in range(0,len(finance)):
        finance.loc[i,'CAPITAL_AMT']=finance.loc[i,'CAPITAL_AMT'].replace(',','').strip() 
    finance = finance.astype({'THIS_TERM_PROFIT': 'float'})  #object -> float 데이터 타입 수정 
    finance = finance.astype({'CAPITAL_AMT': 'float'})
    finance['NOE'] = finance['THIS_TERM_PROFIT'] / finance['CAPITAL_AMT']   #NOE 값 구하기 
    
    noe=finance[['CODE','NOE']]   
    df=pd.merge(df,noe, on='CODE', how='inner')
    
    return df
    

def CR(PATH, SAVE_PATH, df):
            
    finance = pd.read_csv(PATH+'/finance.csv')
    finance=finance.drop_duplicates(['CO_NM'], keep = 'last')
    finance=finance.reset_index(drop=True)     
    for i in range(len(finance)):
        finance.loc[i,'CODE'] = re.sub('A','',finance.loc[i,'CODE'])
    
    idx=finance[finance['FLOW_ASSET'] == ' - '].index     # 결측치인 값들의 인덱스 찾기
    finance=finance.drop(idx)                             # 결측치 값 제거 
    idx2=finance[finance['FLOW_DEBT'] ==' - '].index     
    finance=finance.drop(idx2)
    finance=finance.reset_index(drop=True)
    for i in range(0,len(finance)):
        finance.loc[i,'FLOW_ASSET']=finance.loc[i,'FLOW_ASSET'].replace(',','').strip()    # 쉼표 지우기 
    for i in range(0,len(finance)):
        finance.loc[i,'FLOW_DEBT']=finance.loc[i,'FLOW_DEBT'].replace(',','').strip() 
    finance = finance.astype({'FLOW_ASSET': 'float'})  #object -> float 데이터 타입 수정 
    finance = finance.astype({'FLOW_DEBT': 'float'})
    finance['CR'] = finance['FLOW_ASSET'] / finance['FLOW_DEBT']   #CR 값 구하기 
    cr=finance[['CODE','CR']]   
    df=pd.merge(df,cr, on='CODE', how='inner')
    
    return df
        
        
        
def DR(PATH, SAVE_PATH, df):
    
    finance = pd.read_csv(PATH+'/finance.csv')
    finance=finance.drop_duplicates(['CO_NM'], keep = 'last')
    finance=finance.reset_index(drop=True)     
    for i in range(len(finance)):
        finance.loc[i,'CODE'] = re.sub('A','',finance.loc[i,'CODE'])
        
    idx=finance[finance['DEBT_SUM'] == ' - '].index     # 결측치인 값들의 인덱스 찾기
    finance=finance.drop(idx)                             # 결측치 값 제거 
    idx2=finance[finance['CAPITAL_AMT'] ==' - '].index     
    finance=finance.drop(idx2)
    finance=finance.reset_index(drop=True)
    for i in range(0,len(finance)):
        finance.loc[i,'DEBT_SUM']=finance.loc[i,'DEBT_SUM'].replace(',','').strip()     # 쉼표 지우기 
    for i in range(0,len(finance)):
        finance.loc[i,'CAPITAL_AMT']=finance.loc[i,'CAPITAL_AMT'].replace(',','').strip() 
    finance = finance.astype({'DEBT_SUM': 'float'})  #object -> float 데이터 타입 수정 
    finance = finance.astype({'CAPITAL_AMT': 'float'})
    finance['DR'] = finance['DEBT_SUM'] / finance['CAPITAL_AMT']   #DR 값 구하기    
    dr=finance[['CODE','DR']]  
    df=pd.merge(df,dr, on='CODE', how='inner')
    
    return df

