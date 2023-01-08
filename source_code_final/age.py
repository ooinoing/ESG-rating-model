import pandas as pd
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.ui import Select
from selenium import webdriver

# krx 사이트로부터 기업상장일을 수집하는 크롤러
# 상장일 - 오늘 날짜 = 기업 연령을 계산하는 함수

# PATH에 포함되어야할 것 : chromedriver.exe
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0

def AGE(PATH, df ,train=1):
    
    driver = webdriver.Chrome(PATH+"/chromedriver") 
    wait = WebDriverWait(driver, 10)

    corplist = df['CODE']
    age=[]
    error=[]

    for stock_code in corplist:
            
        driver.get('http://data.krx.co.kr/contents/MMC/ISIF/isif/MMCISIF001.cmd')
        search_start = driver.find_element('xpath','//*[@id="header"]/div[1]/button[3]').click()
        search_box = driver.find_element('xpath','//*[@id="jsStockSearchLayerWord"]')
        search_box.send_keys(stock_code)
        element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="jsStockSearchLayerContent"]/ul/li[2]/a/p')))
        search_start = driver.find_element('xpath','//*[@id="jsStockSearchLayerExecute"]').click()
        element = wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="jsStockSearchLayerContent"]/ul/li[2]/a/p')))
        search_click =driver.find_element('xpath','//*[@id="jsStockSearchLayerContent"]/ul/li/a/span[1]').click()
        element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="jsCard"]/div/div[1]/strong')))
        search_box = driver.find_element('xpath','//*[@id="jsTotalInfoTable02"]/tbody/tr[8]/td[1]')
        age.append((stock_code,search_box.text))
        
        
    # 기업 연령 산출 (일수)
    corp_year=[]
    for i in age:
        young= i[1].split('/')
        time1= datetime(list(map(int,young))[0],list(map(int,young))[1],list(map(int,young))[2])
        time2= datetime.now()
        corp_year.append((i[0],(time2-time1).days))
        
    
    for i in corp_year:
        df["age"][df["CODE"]==i[0]] = i[1]        
        
    return df
