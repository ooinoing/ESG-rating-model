import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests
import pandas as pd
import numpy as np
import os
from bs4 import BeautifulSoup


# 네이버 금융 사이트로 부터 CR(부채비율) 수집하는 크롤러, 
# 유동자산, 유동부채 값 함께 출력하도록 설정했습니다
# PATH에 포함되어야할 것 : chromedriver.exe
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0

flow_asset = []
flow_debt = []
error=[]

def CR(PATH, SAVE_PATH, df,train):
    
    corplist = df["CODE"]

    driver = webdriver.Chrome(PATH+"/chromedriver") # xattr -d com.apple.quarantine chromedriver
    wait = WebDriverWait(driver, 10)
            
    for stock_code in corplist:
        try:
            driver.get('https://finance.naver.com/')
            search_box = driver.find_element('xpath','//*[@id="stock_items"]')
            search_box.send_keys(stock_code)
            search_start = driver.find_element('xpath','//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/button').click()
            time.sleep(4)
            search_start = driver.find_element('xpath','//*[@id="content"]/ul/li[6]/a/span').click()
            time.sleep(3)
            driver.switch_to.frame('coinfo_cp')
            time.sleep(1)
            search_start = driver.find_element('xpath','//*[@id="header-menu"]/div[1]/dl/dt[3]').click()
            time.sleep(2)
            search_start = driver.find_element('xpath','//*[@id="rpt_tab2"]').click()
            time.sleep(2)
            search_box = driver.find_element('xpath','/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[2]/td[6]')
            flow_asset.append((stock_code,search_box.text))
            search_box = driver.find_element('xpath','/html/body/div/form/div[1]/div/div[2]/div[3]/div/div/div[5]/table[2]/tbody/tr[128]/td[6]')
            flow_debt.append((stock_code,search_box.text))
                
        except:
            error.append(stock_code)
            continue
            
            
        df["flow_asset"]=np.NaN
        df["flow_debt"]=np.NaN
        df['CR']=np.NaN
        
        for i in flow_asset:
            try:
                df["flow_asset"][df["CODE"]==i[0]] = i[1].replace(',','')
            except:
                continue
            
        for i in flow_debt:
            try:
                df["flow_debt"][df["CODE"]==i[0]] = i[1].replace(',','')
            except:
                continue
            
        
        for i in range(len(df)):
            try:
                df['flow_asset'][i] = float(df['flow_asset'][i])
            except:
                df['flow_asset'][i]= np.NaN
                
        for i in range(len(df)):
            try:
                df['flow_debt'][i] = float(df['flow_debt'][i])
            except:
                df['flow_debt'][i]= np.NaN
        
        for i in range(len(df)):
            try:
                df['CR'][i] = (df['flow_asset'][i] / df['flow_debt'][i])*100
            except:
                df['CR'][i]=np.NaN
                
        df = df[["CR"]]
            
    #df.to_csv(SAVE_PATH+'/CR_train_error.csv',index=False)
    return df
                
                
                    
