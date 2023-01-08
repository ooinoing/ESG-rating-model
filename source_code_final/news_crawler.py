from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os 


# 뉴스 크롤링 코드 (하나의 기업에 대해)

def crawler(company_code, maxpage, PATH):
    
    page = 1 
    all_news= pd.DataFrame(columns={'날짜','언론사','기사제목','링크'})
    while page <= int(maxpage): 
        
        url = 'https://finance.naver.com/item/news_news.nhn?code=' + str(company_code) + '&page=' + str(page) 
        source_code = requests.get(url).text
        html = BeautifulSoup(source_code, "lxml")

        # 뉴스 제목 
        titles = html.select('.title')
        title_result=[]
        for title in titles: 
            title = title.get_text() 
            title = re.sub('\n','',title)
            title_result.append(title)
 
 
        # 뉴스 링크
        links = html.select('.title') 
 
        link_result =[]
        for link in links: 
            add = 'https://finance.naver.com' + link.find('a')['href']
            link_result.append(add)
 
 
        # 뉴스 날짜 
        dates = html.select('.date') 
        date_result = [date.get_text() for date in dates] 

 
        # 뉴스 매체     
        sources = html.select('.info')
        source_result = [source.get_text() for source in sources] 
 
 
        # 변수들 합쳐서 해당 디렉토리에 csv파일로 저장하기 
        result= {"날짜" : date_result, "언론사" : source_result, "기사제목" : title_result, "링크" : link_result} 
        df_result = pd.DataFrame(result)
        
        all_news=pd.concat([all_news, df_result])
        
        print("다운 받고 있습니다———")

        page += 1 
    all_news=all_news.drop_duplicates(['기사제목'])
    all_news.to_csv(PATH+"/"+str(company_code) + '.csv', mode='w', encoding='utf-8-sig') 
    print('all_news')
    print(all_news)


# train/ test set 내에 모든 기업들에 대해 크롤링한 결과를 각각 csv로 저장하는 함수
# 이 함수에서 위의 crawler를 호출
# PATH : train.xlsx, test.xlsx 있는지 확인
# SAVE_PATH : 뉴스 크롤링. csv 파일을 저장할 경로

def save2df(PATH, SAVE_PATH, train):
    
    if train ==1:
        
        train= pd.read_excel(PATH+"/train.xlsx")
        train.rename(columns = {'종목코드':"CODE", '종목명':"CO_NM"},inplace=True)
        train['CODE'] = train['CODE'].apply(lambda x : str(x).zfill(6))
        for i in train['CODE']:
            crawler(i,100, SAVE_PATH)    # SAVEPATH - 크롤링 결과 다운 받을 경로
            
    else:
        test= pd.read_excel(PATH+"/test.xlsx")
        test.rename(columns = {'종목코드':"CODE", '종목명':"CO_NM"},inplace=True)
        test['CODE'] = test['CODE'].apply(lambda x : str(x).zfill(6))
        for i in test['CODE']:
            crawler(i,100, SAVE_PATH)


