import pandas as pd
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from selenium import webdriver

# PATH 에 포함되어야 할 것 : chromedriver.exe
# dart에서 기업별 여성의 1인 평균급여를 끌어오는 크롤러
# PATH에 포함되어야할 것 : chromedriver.exe
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0


def FEMALE_SALARY(PATH, df,train):
    
    driver = webdriver.Chrome(PATH+"/chromedriver") 
    wait = WebDriverWait(driver, 10)
    
    corplist = df['CODE']
    total_per=[]
    total_money=[]
    error=[]    

    i=0
    
    while(i<3): # 사업보고서가 없거나, 올해 공시자료 없는 기업들은 반기보고서나 이전 연도 자료로 대체하기 위한 설정
        if i==0:
            report,year = '사업보고서','2021' # 첫 시도 -> 직전 연도 사업보고서
        if i==1:
            report,year = '반기보고서','2021' # 두번쨰 시도 -> 직전 연도 반기보고서
        if i==2:
            report,year = '사업보고서', '2020' # 마지막 -> 이전 연도 사업보고서
        
        i+=1  

        for stock_code in corplist:
            try:
                driver.get('https://opendart.fss.or.kr/disclosureinfo/biz/main.do')
                time.sleep(2)
                search_box = driver.find_element('xpath','//*[@id="searchForm"]/table[1]/tbody/tr[1]/td/span[2]/button').click()
                element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="corpSearchForm"]/div[1]/ul/li[3]/button')))
                time.sleep(1)
                search_box = driver.find_element('xpath','//*[@id="textCrpNm"]')
                search_box.send_keys(stock_code)
                search_box = driver.find_element('xpath','//*[@id="corpSearchForm"]/div[1]/ul/li[3]/button').click()
                time.sleep(1)
                element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="allCheckSel"]')))
                search_start = driver.find_element('xpath','//*[@id="allCheckSel"]').click()
                search_start = driver.find_element('xpath','//*[@id="layerPop01"]/div[2]/div[2]/button[1]/span').click()
                time.sleep(1)
                search_start = driver.find_element('xpath','//*[@id="layerPop01"]/div[3]/button[1]').click()
                select = Select(driver.find_element('xpath','//*[@id="selectYear"]'))
                select.select_by_value(year)
                select = Select(driver.find_element('xpath','//*[@id="reportCode"]'))
                select.select_by_visible_text(report)
                search_start = driver.find_element('xpath','//*[@id="gubun_b"]').click()
                search_start = driver.find_element('xpath','//*[@id="contents"]/div[8]/span/button').click()
                element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="listContents"]/div[1]/table/tbody/tr[1]/td[11]')))
                table = driver.find_element('xpath','//*[@id="listContents"]/div[1]/table/tbody')
                per_sum=[]
                money_sum=[]
                for tr in table.find_elements(By.TAG_NAME,'tr'):
                    td = tr.find_elements(By.TAG_NAME,"td")
                    if td[2].text == '여': 
                        per_sum.append(td[10].text)
                        money_sum.append(td[13].text)
                total_per.append(per_sum)
                total_money.append(money_sum)
                for i in range(len(total_per)):      #per 계산을 위한 처리 
                    if total_money[i] == []:
                        total_money[i] = [0]
                for i in range(len(total_per)):
                    for j in range(len(total_per[i])):
                        if total_per[i][j] != '-':
                            total_per[i][j] = total_per[i][j].replace(',','')
                for i in range(len(total_per)):
                    for j in range(len(total_per[i])):
                        if total_per[i][j] != '-':
                            total_per[i][j]= int(total_per[i][j])
                for i in range(len(total_money)):                    # money 계산을 위한 처리 
                    if total_money[i] == 0:
                        total_money[i] = [0]
                for i in range(len(total_money)):
                    for j in range(len(total_money[i])):
                        if total_money[i][j] != '-':
                            total_money[i][j] = total_money[i][j].replace(',','')
                for i in range(len(total_money)):
                    for j in range(len(total_money[i])):
                        if total_money[i][j] != '-':
                            total_money[i][j]= int(total_money[i][j])
                for i in range(len(total_money)):
                    for j in range(len(total_money[i])):
                        if total_money[i][j] == '-':
                            total_money[i][j] = 0
                            total_per[i][j] = 0
                            
                female_salary=[]
                
                for i in range(len(total_money)):
                    if len(total_money[i]) == 1 :
                        female_salary.append(total_money[i][0])
                        
                    else : 
                        girl = 0
                        for j in range(len(total_money[i])):
                            girl+= total_money[i][j] * total_per[i][j]
                        if sum(total_per[i]) != 0:
                            girl /=  sum(total_per[i])
                        else : 
                            girl = 0 
                        female_salary.append(girl)
                        
            except: 
                error.append(stock_code)
                continue    
        
        corplist = error 
        error=[]
    
    
    df["female_salary"] = np.NaN
    #for i in female_salary:
    #    df["female_salary"][df["CODE"]==stock_code] =  female_salary
    for i in female_salary:
        df["female_salary"][df["CODE"]==i[0]] = i[1]        
    #female_aver_salary=pd.DataFrame({'CODE': df['CODE'], 'female_salary':female_salary})
        
    return df 

