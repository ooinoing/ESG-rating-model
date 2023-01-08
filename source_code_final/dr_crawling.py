import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time



# 네이버 금융 사이트로 부터 DR(부채비율) 수집하는 크롤러

# PATH에 포함되어야할 것 : chromedriver.exe
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0

DR = []
error=[]

def DR(PATH, df,train):
    
    corplist = df["CODE"]

    driver = webdriver.Chrome(PATH+"/chromedriver") # xattr -d com.apple.quarantine chromedriver
    wait = WebDriverWait(driver, 10)
        
    for stock_code in corplist:
        try:
            driver.get('https://finance.naver.com/')
            search_box = driver.find_element('xpath','//*[@id="stock_items"]')
            search_box.send_keys(stock_code)
            search_start = driver.find_element('xpath','//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/button').click()
            time.sleep(2)
            search_box = driver.find_element('xpath','//*[@id="content"]/div[4]/div[1]/table/tbody/tr[7]/td[9]')
            DR.append((stock_code,search_box.text))

        except:
            error.append(stock_code)
            continue
        
    #OPOS_frame = pd.DataFrame(columns={})
    
    df["DR"]=np.NaN
    
    for i in DR:
        df["DR"][df["CODE"]==i[0]] = i[1].replace(',','')
        
            
    idx=df[df['DR'] == '-'].index
    df=df.drop(idx)
    idx=df[df['DR'] == ''].index
    df=df.drop(idx)
    idx=df[df['DR'] == ' '].index
    df=df.drop(idx)
        
    df = df.astype({'DR': 'float'})
    df=df[['CODE','DR']]
        
    return df
        