import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


# 네이버 금융 사이트로 부터 noe(자기자본순이익률) 수집하는 크롤러

# PATH에 포함되어야할 것 : chromedriver.exe
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0
ROE = []
def NOE(PATH, df,train=1):
    
    driver = webdriver.Chrome(PATH+"/chromedriver") # xattr -d com.apple.quarantine chromedriver
    wait = WebDriverWait(driver, 10)
 
    corplist = df["CODE"] 
    error=[]

        
    for stock_code in corplist:
        try:
            driver.get('https://finance.naver.com/')
            search_box = driver.find_element('xpath','//*[@id="stock_items"]')
            search_box.send_keys(stock_code)
            search_start = driver.find_element('xpath','//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/button').click()
            time.sleep(1.5)
            search_box = driver.find_element('xpath','//*[@id="content"]/div[4]/div[1]/table/tbody/tr[6]/td[9]')
            ROE.append((stock_code,search_box.text))
        except:
            error.append(stock_code)
            continue
             
    for i in ROE:
        df["NOE"][df["CODE"]==i[0]] = i[1]
        
    return df