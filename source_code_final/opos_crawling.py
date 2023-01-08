import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


# 네이버 금융 사이트로  부터 opos(매출액영업이익률) 수집하는 크롤러

# PATH에 포함되어야할 것 : chromedriver.exe
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0


sale_profit = []    #(종목코드,영업이익) 으로 이루어진 리스트
sell = []   #(종목코드, 매출액)으로 이루어진 리스트
error=[]

def OPOS(PATH, df,train):
    
    corplist = df["CODE"]

    driver = webdriver.Chrome(PATH+"/chromedriver") # xattr -d com.apple.quarantine chromedriver
    wait = WebDriverWait(driver, 10)
        
    for stock_code in corplist:
        try:
            driver.get('https://finance.naver.com/')
            search_box = driver.find_element('xpath','//*[@id="stock_items"]')
            search_box.send_keys(stock_code)
            search_start = driver.find_element('xpath','//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/button').click()
            time.sleep(1.5)
            search_box = driver.find_element('xpath','//*[@id="content"]/div[4]/div[1]/table/tbody/tr[1]/td[9]')
            sell.append((stock_code,search_box.text))
            search_box = driver.find_element('xpath','//*[@id="content"]/div[4]/div[1]/table/tbody/tr[2]/td[9]')
            sale_profit.append((stock_code,search_box.text))
            
        except:
            error.append(stock_code) # 디버깅 용도로 사용
            continue
        
    
    df["sell"]=np.NaN
    df["sale_profit"]=np.NaN
    
    for i in sell:
        df["sell"][df["CODE"]==i[0]] = i[1].replace(',','')
        
    for i in sale_profit:
        df["sale_profit"][df["CODE"]==i[0]] = i[1].replace(',','')
            
    idx=df[df['sale_profit'] == '-'].index
    df=df.drop(idx)
    idx=df[df['sell'] == '-'].index
    df=df.drop(idx)
    idx=df[df['sale_profit'] == ''].index
    df=df.drop(idx)
    idx=df[df['sell'] == ''].index
    df=df.drop(idx)
    idx=df[df['sale_profit'] == ' '].index
    df=df.drop(idx)
    idx=df[df['sell'] == ' '].index
    df=df.drop(idx)
        
    df = df.astype({'sale_profit': 'float'})
    df = df.astype({'sell': 'float'})
        
    df['OPOS'] = (df['sale_profit'] / df['sell'])*100
    df=df[['CODE','OPOS']]
        
    return df
        
