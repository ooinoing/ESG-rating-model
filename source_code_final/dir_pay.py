import os
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import regex
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
# 이사 보수 수집하는 크롤링 코드
# PATH에 포함되어야할 것 : train.xlsx , test.xlsx , chromedriver.exe
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0

def get_dir_pay(PATH, df, train):
    corplist = df['CODE']
    dir_pay = []
    error=[]
    
    i=0
    while(i<3):
        
        if i==0:
            report,year = '사업보고서','2021' # 첫 시도 -> 직전 연도 사업보고서
        if i==1:
            report,year = '반기보고서','2021' # 두번쨰 시도 -> 직전 연도 반기보고서
        if i==2:
            report,year = '사업보고서', '2020' # 마지막 -> 이전 연도 사업보고서
                        
        driver = webdriver.Chrome(PATH+"/chromedriver") # xattr -d com.apple.quarantine chromedriver
        wait = WebDriverWait(driver, 10)
        url = 'https://opendart.fss.or.kr/disclosureinfo/biz/main.do'

        for stock_code in corplist:
            try:
                driver.get('https://opendart.fss.or.kr/disclosureinfo/biz/main.do')
                time.sleep(1)    
                element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="contents"]/div[4]/h3')))
                search_box = driver.find_element(By.XPATH,'//*[@id="searchForm"]/table[1]/tbody/tr[1]/td/span[2]/button') # 회사명 찾기 버튼
                search_box.click()
                element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="corpSearchForm"]/div[1]/ul/li[3]/button')))  # 검색 버튼
                search_box = driver.find_element(By.XPATH,'//*[@id="textCrpNm"]') # 회사명 입력 칸   
                search_box.send_keys(stock_code)   

                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="corpSearchForm"]/div[1]/ul/li[3]/button'))) 
                driver.find_element(By.XPATH,'//*[@id="corpSearchForm"]/div[1]/ul/li[3]/button').click()
                time.sleep(1)    

                element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="allCheckSel"]'))) 
                driver.find_element(By.XPATH,'//*[@id="allCheckSel"]').click() # 전체선택 
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layerPop01"]/div[2]/div[2]/button[1]/span'))) 
                driver.find_element(By.XPATH,'//*[@id="layerPop01"]/div[2]/div[2]/button[1]/span').click()  # 아래 화살표 클릭
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layerPop01"]/div[3]/button[1]'))) 
                driver.find_element(By.XPATH,'//*[@id="layerPop01"]/div[3]/button[1]').click()    # 확인 버튼
                time.sleep(1)    
                select = Select(driver.find_element(By.XPATH,'//*[@id="selectYear"]'))   # 사업연도 선택
                select.select_by_value(year)  
                
                select = Select(driver.find_element(By.XPATH,'//*[@id="reportCode"]'))   # 보고서명 선택
                select.select_by_visible_text(report)
                    
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gubun_o"]'))) 
                driver.find_element(By.XPATH,'//*[@id="gubun_o"]').click() #직원 현황
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contents"]/div[8]/span/button'))) 
                driver.find_element(By.XPATH,'//*[@id="contents"]/div[8]/span/button').click()    # 검색
                time.sleep(1)    
                #element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="listContents"]/div[1]/table/tbody/tr[1]/td[11]')))
                table = driver.find_element(By.XPATH,'//*[@id="listContents"]/div[1]/table/tbody')   # 표 선택
        
                for tr in table.find_elements(By.TAG_NAME,'tr'):
                    td = tr.find_elements(By.TAG_NAME,"td")
                    dir_pay.append( (stock_code, td[3].text.replace(',','')))
                            
            except: 
                error.append(stock_code)
                continue
            
        i+=1
                
        corplist = error 
        error=[]
            
    
    return dir_pay
        
        
# 크롤링 결과를 기업별로 합계 내는 함수 
# A : (종목코드, 이사보수) 로 이루어진 리스트 , 한 기업에 대해 여러개의 튜플이 존재함
# B : {종목코드:이사보수} 형태의 딕셔너리. 한 기업에 대해 이사 보수를 최종 산출한 결과
def list2dict(A, B):
  tmp=A[0][0]
  sum=0
  for i in A: 
    if (tmp == i[0]):
      if i[1]!='-':
        sum = sum + float(i[1].replace(',',''))
    else :
      B[tmp] = sum
      tmp = i[0]
      sum = float(i[1].replace(',','')) if i[1]!='-' else 0
  return B    