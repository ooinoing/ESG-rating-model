import pandas as pd
import numpy as np

def map_service_type(type):
  if type in ['화학', '전기가스업']:
    return 0
  elif type in ['증권','은행','기타금융','보험','금융']:
    return 1
  elif type in ['제약','의약품', '의료정밀','의료.정밀기기']:
    return 2
  elif type in ['서비스업','통신업','컴퓨터서비스','디지털 컨텐츠','오락.문화','소프트웨어', '방송서비스', '인터넷' , '기타서비스']:
    return 3
  elif type in ['전기전자', '기계', '반도체', 'it부품','일반전기전자', '통신장비' ,'기계장비' ]:
    return 4
  elif type in ['운수장비','유통업','운수창고업','유통' ]:
    return 5
  elif type in ['농업, 임업 및 어업','음식료품','기타제조업','섬유의복','숙박.음식', '음식료.담배']:
    return 6
  elif type in ['철강금속', '비금속광물','종이목재','종이.목재','비금속','금속']:
    return 7
  elif type in ['건설업','건설']:
    return 8
  else:
    return -1
    
# 기업별 업종을 매칭시키고, 비슷한 업종끼리 묶어서 그룹화 시키는 함수 
# 업종은 추후에 결측치를 채울 때 중요하므로 미리 함수 내에서 결측치를 처리해 주었음
# PATH에 포함되어야할 것 : "코스피.xlsx", 코스닥.xlsx

def TYPE(PATH, df, train):
  
  service_type_kospi= pd.read_excel(PATH+"/코스피.xlsx")
  service_type_kosdaq= pd.read_excel(PATH+"/코스닥.xlsx")
    
  service_type= pd.concat([service_type_kospi,service_type_kosdaq])
  service_type.drop(["시장구분","종가","대비","등락률","시가총액",'종목명'],axis=1, inplace=True)
  service_type.rename(columns = {'종목코드':"CODE", "업종명":'type'},inplace=True)
  service_type['CODE'] = service_type['CODE'].apply(lambda x : str(x).zfill(6).strip())

  if train ==1: 
    
    df=pd.merge(df,service_type, on=["CODE"],how="left")
    df["type"]=df["type"].apply(map_service_type)
    
    ##
    df["type"][df['CO_NM']=='펄어비스'] = 3
    df["type"][df['CO_NM']=='스튜디오드래곤'] = 3
    df["type"][df['CO_NM']=='위메이드'] = 3
    df["type"][df['CO_NM']=='JYP Ent.'] = 3
    df["type"][df['CO_NM']=='에스엠'] = 3
    df["type"][df['CO_NM']=='오스템임플란트'] = 2
    df["type"][df['CO_NM']=='동화기업'] = 7
    df["type"][df['CO_NM']=='파라다이스'] = 6
    df["type"][df['CO_NM']=='피엔티'] = 4
    df["type"][df['CO_NM']=='고영'] = 4
    df["type"][df['CO_NM']=='컴투스'] = 3
    df["type"][df['CO_NM']=='와이지엔터테인먼트'] = 3
    df["type"][df['CO_NM']=='이녹스첨단소재'] = 4
    df["type"][df['CO_NM']=='웹젠'] = 3
    df["type"][df['CO_NM']=='아난티'] = 6
    df["type"][df['CO_NM']=='파트론'] = 4
    df["type"][df['CO_NM']=='아미코젠'] = 6
    df["type"][df['CO_NM']=='신흥에스이씨'] = 0
    df["type"][df['CO_NM']=='국일제지'] = 7
    df["type"][df['CO_NM']=='원익홀딩스'] = 4
    df["type"][df['CO_NM']=='인터플렉스'] = 4
    df["type"][df['CO_NM']=='톱텍'] = 4
    df["type"][df['CO_NM']=='노바렉스'] = 6
    df["type"][df['CO_NM']=='비츠로셀'] = 0
    df["type"][df['CO_NM']=='에스티큐브'] = 4
    df["type"][df['CO_NM']=='멀티캠퍼스'] = 3
    df["type"][df['CO_NM']=='슈피겐코리아'] = 6
    df["type"][df['CO_NM']=='알서포트'] = 3
    df["type"][df['CO_NM']=='지니뮤직'] = 3
    df["type"][df['CO_NM']=='에이치엘사이언스'] = 6
    df["type"][df['CO_NM']=='현대에버다임'] = 5
    df["type"][df['CO_NM']=='영풍정밀'] = 6
    df["type"][df['CO_NM']=='SBS콘텐츠허브'] = 3
    df["type"][df['CO_NM']=='나노엔텍'] = 2
    df["type"][df['CO_NM']=='신화인터텍'] = 4
    df["type"][df['CO_NM']=='에스엠코어'] = 4
    df["type"][df['CO_NM']=='넥스트사이언스'] = 7
    df["type"][df['CO_NM']=='롯데푸드'] = 6
    df["type"][df['CO_NM']=='SBS미디어홀딩스'] = 3
    df["type"][df['CO_NM']=='폴루스바이오팜'] = 3
    df["type"][df['CO_NM']=='SK머티리얼즈'] = 1
    df["type"][df['CO_NM']=='넥슨지티'] = 3
    df["type"][df['CO_NM']=='디피씨'] = 1
    df["type"][df['CO_NM']=='HDC'] = 1
    df["type"][df['CO_NM']=='우리들휴브레인'] = 5
    
    
    #df.to_csv(SAVE_PATH+"/type_train.csv", index= False,mode='w')
    return df


  else: 

    df=pd.merge(df,service_type, on=["CODE"],how="left")
    df["type"]=df["type"].apply(map_service_type)


    df["type"][df['CO_NM']=='엘앤에프'] = 0
    df["type"][df['CO_NM']=='에스에프에이'] = 4
    df["type"][df['CO_NM']=='대주전자재료'] = 4
    df["type"][df['CO_NM']=='씨아이에스'] = 4
    df["type"][df['CO_NM']=='클래시스'] = 2
    df["type"][df['CO_NM']=='비에이치'] = 4
    df["type"][df['CO_NM']=='다원시스'] = 0
    df["type"][df['CO_NM']=='매일유업'] = 6
    df["type"][df['CO_NM']=='서부T&D'] = 6
    df["type"][df['CO_NM']=='KH바텍'] = 4
    df["type"][df['CO_NM']=='하림'] = 6
    df["type"][df['CO_NM']=='이지홀딩스'] = 6
    df["type"][df['CO_NM']=='드림어스컴퍼니'] = 3
    df["type"][df['CO_NM']=='로보스타'] = 4
    #df["type"][df['CO_NM']=='부산가스'] = 0
    #df["type"][df['CO_NM']=='엔에스쇼핑'] = 3
    df["type"][df['CO_NM']=='에이치엘비'] = 2

  
    #df.to_csv(SAVE_PATH+"/type_train.csv", index= False,mode='w')    
    return df