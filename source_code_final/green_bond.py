import os
import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


# 녹색채권 발행한 기업 목록을 끌어오는 크롤러  
# 기업명 중 일치하는 기업에 대해서는 1, 0로 데이터 프레임에 기록함
# PATH 에 포함되어야 할 것 : chromedriver.exe , data.csv(녹색채권 정리한 파일)
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0

def GREEN_BOND(PATH, df, train = 1):

    driver = webdriver.Chrome(PATH+"/chromedriver") 
    driver.get('https://www.gmi.go.kr/gb/pblcnSttusList.do')
    table = driver.find_element('xpath','//*[@id="contents"]/form/div/div[2]/table/tbody')
    green=[]
    for tr in table.find_elements(By.TAG_NAME,'tr'):
        td = tr.find_elements(By.TAG_NAME,"td")
        green.append(td[0].text)                        # 녹색채권 발행한 기업 뽑아오기 
        
    green=list(set(green))
    corp = list(df['CODE'])
    name=list(df['CO_NM'])
    set1 = set(green)
    set2 = set(name)
    green= set1 & set2
    
    table2 = pd.read_csv(PATH + "/data.csv")    # 녹색채권 정리한 파일 불러오기 
    green1 = set(list(table2['발행기관']))       # 발행기업 가져오기 
    green1 = list(green & green1)              # 합치기 
    green_bond=pd.DataFrame({'CODE': corp, 'green_bond': green1})
    #green_bond.to_csv(SAVE_PATH + 'green_bond_train.csv',index=False)
    return green_bond

