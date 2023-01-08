
import os
import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# krx esg 포털에서 지배구조보고서를 공시한 기업 목록을 끌어오는 크롤러  
# 기업명 중 하는 기업에 대해서는 1, 0로 데이터 프레임에 기록함
# PATH에 포함되어야할 것 : chromedriver.exe
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0


def GOV_REPORT(PATH, df, train = 1):
   # 크롤링 
    corplist=[] # 사이트 상에 올라와있는 기업명을 저장할 list
    
    PATH = os.getcwd()      # chrome창(웹드라이버) 열기
    driver = webdriver.Chrome(PATH+"/chromedriver") # xattr -d com.apple.quarantine chromedriver
    url = "https://esg.krx.co.kr/contents/02/02040000/ESG02040000.jsp"
    driver.get(url)
    time.sleep(2)
    total_data= driver.find_elements(By.CLASS_NAME, 'total-count')
    total_page = math.ceil(int(total_data[0].text.split()[1][:-1])/10)

    for cnt in range(int(total_page)):
        try:
            search = driver.find_elements(By.NAME, 'com_abbrv') # 동작 할 요소 선택
            time.sleep(1)

            for i in range(len(search)):
                #file.write(search[i].text+'\n')
                corplist.append(search[i].text)
            
            next_page = driver.find_element(By.CLASS_NAME, "next")
            next_page.click()
            time.sleep(1)
        except:
            print("데이터 수집 완료.")
            break

    driver.close()
    #file.close()
    
     
    df[["gov_report"]]= 0
    for i in corplist:
        i=i.strip()
        df["gov_report"][df["CO_NM"]==i]=1
        
    return df


    