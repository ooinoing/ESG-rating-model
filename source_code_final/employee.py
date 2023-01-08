import os
import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup
import regex
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


# 정규직수, 근속연수, 평균급여 모두 한 번에 크롤링해서 각각 텍스트 파일로 저장
def get_employee(PATH,SAVE_PATH, df,train):

  driver = webdriver.Chrome(PATH+"/chromedriver") # xattr -d com.apple.quarantine chromedriver
  wait = WebDriverWait(driver, 10)
        
  corplist = df['CODE'][:20]#[:3]
  per_emp = []    # (종목코드 , 정규직 직원수) 로 구성된 list
  work_year=[]    # (종목코드 , 평균근속연수 ) 로 구성된 list
  salary=[]   # (종목코드 , 1인평균급여) 로 구성된 list
  error=[]
  
  i=0
  while(i<3):  
      if i==0:
          report,year = '사업보고서','2021' # 첫 시도 -> 직전 연도 사업보고서
      if i==1:
          report,year = '반기보고서','2021' # 두번쨰 시도 -> 직전 연도 반기보고서
      if i==2:
          report,year = '사업보고서', '2020' # 마지막 -> 이전 연도 사업보고서
                      
      
      url = 'https://opendart.fss.or.kr/disclosureinfo/biz/main.do'
      for stock_code in corplist:
          try:
              print(stock_code, year, report)
              driver.get('https://opendart.fss.or.kr/disclosureinfo/biz/main.do')
              element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="contents"]/div[4]/h3')))
              time.sleep(1)
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
              #time.sleep(2)    
              element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layerPop01"]/div[3]/button[1]'))) 
              driver.find_element(By.XPATH,'//*[@id="layerPop01"]/div[3]/button[1]').click()    # 확인 버튼
              time.sleep(1)    
              select = Select(driver.find_element(By.XPATH,'//*[@id="selectYear"]'))   # 사업연도 선택
              select.select_by_value(year)  
              select = Select(driver.find_element(By.XPATH,'//*[@id="reportCode"]'))   # 보고서명 선택
              select.select_by_visible_text(report)
              element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gubun_b"]'))) 
              driver.find_element(By.XPATH,'//*[@id="gubun_b"]').click() #직원 현황
              #time.sleep(1)    
              element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contents"]/div[8]/span/button'))) 
              driver.find_element(By.XPATH,'//*[@id="contents"]/div[8]/span/button').click()    # 검색
              time.sleep(1)    
              element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="listContents"]/div[1]/table/tbody/tr[1]/td[11]')))
              table = driver.find_element(By.XPATH,'//*[@id="listContents"]/div[1]/table/tbody')   # 표 선택
                
              for tr in table.find_elements(By.TAG_NAME,'tr'):
                td = tr.find_elements(By.TAG_NAME,"td")
                per_emp.append((stock_code, td[6].text))
                work_year.append((stock_code,td[10].text, td[11].text)) # (종목코드 , 직원수, 1인 평균급여) -> 가중평균 구하기 위함
                salary.append((stock_code, td[10].text, td[13].text))
                            
          except: 
            error.append(stock_code)
            continue
            
      i+=1
                
      corplist = error 
      
      error=[]
      
      
  if train == 1:
      file_name = 'train'
  else:
      file_name = 'test'

  filePath = SAVE_PATH+'/정규직수_'+file_name+'.txt'
  with open(filePath, 'w',encoding="utf-8") as f:
    for i in per_emp:
      line = str(i[0])+'\t'+str(i[1])+'\n'
      f.write(line)
    
  filePath = SAVE_PATH+'/근속연수_'+file_name+'.txt'
  with open(filePath, 'w',encoding="utf-8") as f:
    for i in work_year:
      line = str(i[0])+'\t'+str(i[1])+'\t'+str(i[2])+'\n'
      f.write(line)
  
  filePath = SAVE_PATH+'/평균급여_'+file_name+'.txt'
  with open(filePath, 'w',encoding="utf-8") as f:
    for i in salary:
      line = str(i[0])+'\t'+str(i[1])+'\t'+str(i[2])+'\n'
      f.write(line)
      
  return per_emp, work_year, salary 


# 근속연수를 저장하기 위한 텍스트 전처리 함수
def clean(x):
  #if re.match(r"[^가-힣]+",'10.83')==x:
  #  return float(x)
  if x.find('(')>0:
    x = x[:x.find('(')]
  if x.find(' ')>0:
    x = x.replace(' ','')
  if x.find('ㅐ')>0:
    x = x.replace('ㅐ','')
  if x.find('약')>=0:
    x = x.replace('약','')
  if x.find('Y')>=0:
    x = x.replace('Y','년')
  if x.find('M')>=0:
    x = x.replace('M','월')
  if x.find('일')>0:
    x = x[:x.find('개월')]
  if x.find('-')>=0:
    return np.NaN
  elif re.match('[0-9]+[.]+[0-9]*(년)',x):
    x = x.replace('년','')
    #x = x.replace('개월','')
    return float(x)
  elif re.match('[0-9]+[.]+[0-9]*[개월]+',x):
    x = x.replace('개월','')
    return float(x.split('.')[0])+round(int(x.split('.')[1])/12,2)
  elif re.match('[0-9]+(년)\s*[0-9]+(개월)+',x):
    x = x.replace('년','.')
    x = x.replace('개월','')
    return int(x.split('.')[0])+round(int(x.split('.')[1])/12,2)
  elif re.match('[0-9]+(년)\s*[0-9]+(월)+',x):
    x = x.replace('년','.')
    x = x.replace('월','')
    return int(x.split('.')[0])+round(int(x.split('.')[1])/12,2)
  elif re.match('[0-9]+(개월)+',x):
    x = x.replace('개월','')
    return round(int(x)/12,2)
  elif re.match('[0-9]+(월)+',x):
    x = x.replace('월','')
    return round(int(x)/12,2)
  elif re.match('[0-9]+[.]+[0-9]+(년)+',x):
    x = x.replace('년','')
    return float(x)
  elif re.match('[0-9]+(년)+',x):
    #print(x)
    x = x.replace('년','.')
    return float(x)
  elif re.match('[0-9]+[.]+[0-9]+(년)+',x):
    x = x.replace('년','')
    return float(x)

  return float(x)


########## 아래 함수들은 총직원수 결측치 채우고 실행해야함 ##############

# PATH에 포함되어야할 것 : 근속연수_train/test.txt 
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0

def WORK_YEAR(PATH, df,train):
  if train ==1:
    with open(PATH+'/근속연수_train.txt', "r") as f:  # 근속연수 저장된 파일 불러오기 
      data = f.readlines()      
  else:
    with open(PATH+'/근속연수_test.txt', "r") as f:
      data = f.readlines()

  data_split = [x.strip().split('\t') for x in data[0:]]  # 텍스트 파일로 정리된 정규직수 불러오기 
  tmp = pd.DataFrame(data_split, columns = ["CODE","emp","work_year"]) # 직원수, 근속연수
    
  tmp["emp"]= tmp["emp"].apply(lambda x : int(str(x).replace(',','')) if x!='-' else 0)
  tmp["work_year"]= tmp["work_year"].apply(clean)
  tmp = pd.merge(train, tmp, on="CODE", how='left')
  
  work_year_aver=[]
  sum= float(tmp["work_year"][0]) * (int(tmp["emp"][0]) / int(tmp["total_emp"][0]))
  
  for i in range(1,len(tmp["CODE"])):   #### 하나의 기업에 대해 근속연수 계산 (직원수 데이터를 이용해서 가중평균을 적용함)
      if not(tmp["emp"][i]) or not(tmp["work_year"][i]):  # 결측치 또는 0에 대해서는 계산을 하지 않음
          continue
      if (tmp["CODE"][i-1] == tmp["CODE"][i]):
          sum += tmp["work_year"][i] * tmp["emp"][i] / tmp["total_emp"][i]
      else :
          work_year_aver.append((tmp["CODE"][i-1] ,sum))
          sum = tmp["work_year"][i]* tmp["emp"][i] / tmp["total_emp"][i]
          
          
  tmp = pd.DataFrame(work_year_aver, columns = ["CODE","work_year"]) # 코드, 근속연수
  df = pd.merge(df, tmp, on="CODE", how='left') # 기존 데이터 프레임과 합치기
  df=df[['CODE','work_year']]

  return df

# PATH에 포함되어야할 것 : 평균급여_train/test.txt 
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0    
def SALARY(PATH,df,train):
      
  if train ==1:
    with open(PATH+'/평균급여_train.txt', "r") as f:  # 근속연수 저장된 파일 불러오기 
      data = f.readlines()    
  else:
    with open(PATH+'/평균급여_test.txt', "r") as f:
      data = f.readlines()
      
  data_split = [x.strip().split('\t') for x in data[0:]]  # 텍스트 파일로 정리된 근속연수 불러오기 
  tmp = pd.DataFrame(data_split, columns = ["CODE","emp","salary"]) # 직원수, 평균급여
  tmp["emp"]= tmp["emp"].apply(lambda x : int(str(x).replace(',','')) if x!='-' else 0)
  tmp["salary"]= tmp["salary"].apply(lambda x : int(str(x).replace(',','')) if x!='-' else 0)

  tmp = pd.merge(train, tmp, on="CODE", how='left')

  salary_aver=[]

  sum= float(tmp["salary"][0]) * (int(tmp["emp"][0]) / int(tmp["total_emp"][0]))

  for i in range(1,len(tmp["CODE"])):   #### 하나의 기업에 대해 근속연수 계산 (직원수 데이터를 이용해서 가중평균을 적용함)
      if not(tmp["emp"][i]) or not(tmp["salary"][i]):  # 결측치 또는 0에 대해서는 계산을 하지 않음
          continue
      if (tmp["CODE"][i-1] == tmp["CODE"][i]):
          sum += tmp["salary"][i] * tmp["emp"][i] / tmp["total_emp"][i]
      else :
          salary_aver.append((tmp["CODE"][i-1] ,sum))
          sum = tmp["salary"][i]* tmp["emp"][i] / tmp["total_emp"][i]

            
  tmp = pd.DataFrame(salary_aver, columns = ["CODE","salary"]) # 코드, 근속연수
  df = pd.merge(df, tmp, on="CODE", how='left') # 기존 데이터 프레임과 합치기
  df=df[['CODE','salary']]
        
  return df
                           
# PATH에 포함되어야할 것 : 정규직수_train/test.txt 
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0      
def RE_EMP_RATIO(PATH,df,train):
  if train ==1 :
    with open(PATH+'/정규직수_train.txt', 'r') as f:
      data = f.readlines()
  else:
    with open(PATH+'/정규직수_train.txt', 'r') as f:
      data = f.readlines()
           
  re_emp_sum=[]
      
  data_split = [x.strip().split('\t') for x in data[0:]]  # 텍스트 파일로 정리된 정규직수 불러오기 
  tmp = pd.DataFrame(data_split, columns = ["CODE","re_emp"]) # 코드, 정규직수
      
  tmp["re_emp"]= tmp["re_emp"].apply(lambda x : int(str(x).replace(',','')) if x!='-' else 0)
  sum = tmp["re_emp"][0]
  
  for i in range(1,len(tmp)): 
    if (tmp["CODE"][i-1] == tmp["CODE"][i]):
      sum = sum+ tmp["re_emp"][i]
    else :
      re_emp_sum.append((tmp["CODE"][i-1] ,sum))
      sum=0
              
  tmp = pd.DataFrame(re_emp_sum, columns = ["CODE","re_emp"]) # 코드, 정규직수
  df = pd.merge(df, tmp, on="CODE", how='left')
  df['re_emp_ratio'] = df['re_emp']/df['total_emp']
  df=df[['CODE','re_emp_ratio']]
  
  return df
    
      