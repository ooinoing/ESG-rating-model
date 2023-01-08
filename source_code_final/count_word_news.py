from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os 

# 뉴스 타이틀에서 키워드를 검색해서 등장 횟수를 카운트해주는 함수 
# 아래 함수에서 키워드 추가/삭제 가능
# PATH 에 포함되어야할 것: 뉴스 크롤링 결과가 저장된 폴더 경로
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 

def keyword_rate(PATH, df):
    e_rates=[]
    s_rates=[]
    g_rates=[]
    
    for i in df['CODE']:
        news= pd.read_csv(PATH+'/'+str(i)+'.csv')

        e_count=0
        s_count=0
        g_count=0
        
        for t in news['기사제목']:

            s_list=['담합','불법파견','불매운동','불법고용','불공정거래','하도급문제','논란','골목상권 위협']
            g_list=['갑질','비리','뇌물','분식회계','비자금','일감몰아주기','배임','횡령','탈세','밀어내기','차명계좌','주가조작','성과급 잔치','구속','조세회피','내부자거래']
            
            
            if '환경' in t:  #환경이 들어간 단어 카운트
                if ( '근무 환경' or '근무환경' or '수주환경' or'수주 환경'or '금융환경' or'금융 환경'or'주거환경'or '주거 환경'or'대외환경'or'대외 환경' or '반부패 환경' or
                    '경영환경'or'경영 환경'or '외부환경'or '외부 환경' or'시장환경'or'시장 환경'or'투자환경'or '투자 환경'or'성장환경'or'성장 환경'or
                    '환경개선'or'환경 개선'or'안전 환경'or '안전환경' or '비우호적 환경'or'영업환경' or'영업 환경'or '실증환경' '불리한 환경'or '우호적 환경'or
                    '극한환경'or '매크로 환경' or '악화한 환경' or'수면 환경' or '불확실한 환경'or'환경 변화'or'몰입 환경'or'작업 환경'or'교육 환경' or
                    '대외 환경'or'업무환경'or'업무 환경'or'사무환경'or'인터넷 환경'or'클라우드 환경'or'방송환경'or'방송 환경'or'훈련환경'or'훈련 환경'or '교통'or'산업환경' or '산업 환경') in t:
                    pass
            
                else:
                    e_count += 1
                
            elif ('담합'in t or '불법파견'in t or'불매운동' in t or'불법고용' in t or '불공정거래' in t or '하도급문제' in t or '논란'in t or '골목상권 위협' in t):
                s_count+=1
            elif ('갑질' in t or '비리'in t or '뇌물'in t or '분식회계' in t or '비자금' in t or '일감몰아주기' in t or '배임' in t or '횡령' in t or '탈세' in t or '밀어내기' in t or '차명계좌' in t or '주가조작' in t or '성과급 잔치' in t or '구속' in t or '조세회피' in t or '내부자거래'in t):
                g_count+=1
            e_rate= e_count / len(news['기사제목'])
            s_rate= s_count / len(news['기사제목'])
            g_rate= g_count / len(news['기사제목'])
            
        e_rates.append(e_rate)
        s_rates.append(s_rate)
        g_rates.append(g_rate)

    df['e_pos_news'] = e_rates
    df['s_neg_news'] = s_rates
    df['g_neg_news'] = g_rates
    
    return df
    