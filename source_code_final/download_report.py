import pandas as pd
import os
import numpy as np
import dart_fss as dart
import zipfile
from zipfile import ZipFile

# Open DART API KEY 설정
api_key='f500347222aa08270de912e213facf6b8e2cb58c'
dart.set_api_key(api_key=api_key)

# DART 에 공시된 회사 리스트 불러오기
corp_list = dart.get_corp_list()


def corp_info(stock_code, bsns_year):     # api 호출할때마다 필요한 정보(stock_code, bsns_year, reprt_code)를 반환
  if corp_list.find_by_stock_code(stock_code):
    corp_code = corp_list.find_by_stock_code(stock_code).corp_code
    reprt_code = 11011 # 사업보고서를 의미하는 보고서 코드
    return str(corp_code) , str(bsns_year), str(reprt_code)
  else :
    return np.NaN


def download_report(PATH, SAVE_ZIP_PATH,SAVE_UNZIP_PATH, train):
    if train == 1:
        file_name = 'train'
    else:
        file_name = 'test'
  
    df= pd.read_excel(PATH+"/"+file_name+".xlsx")
    df.rename(columns = {'종목코드':"CODE", '종목명':"CO_NM"},inplace=True)    
    df_rcept_no = pd.read_csv(PATH+"/rcept_no_"+file_name+".csv")
    df['CODE'] = df['CODE'].apply(lambda x : str(x).zfill(6))
    df_rcept_no['CODE'] = df_rcept_no['CODE'].apply(lambda x : str(x).zfill(6))

    # 압축된 형태로 사업보고서 다운
    for rcept_no in df_rcept_no["rcept_no"]:
        dart.api.filings.download_document(SAVE_ZIP_PATH, rcept_no)
        
    # zip 파일 모두 선택
    os.chdir(SAVE_ZIP_PATH )
    zipfiles = [ file for file in os.listdir() if file.endswith('zip')]
    
    # 압축 해제 , 파일 선택
    for file in zipfiles:
        with ZipFile(file, 'r') as zipObj:
            listOfFileNames = zipObj.namelist()
            for fileName in listOfFileNames:
                if len(fileName)==18:
                    zipObj.extract(fileName, SAVE_UNZIP_PATH)
                    
        
    unzipfiles = os.listdir(SAVE_UNZIP_PATH)
    # 종목코드.xml 으로 파일명 일괄변경
    for src in unzipfiles:
        dst = list(df_rcept_no["CODE"][df_rcept_no["rcept_no"]==int(src[:-4])])[0]
        dst = os.path.join(SAVE_UNZIP_PATH, str(dst)+".xml")
        os.rename(SAVE_UNZIP_PATH+src, dst)
        
        
    return 1
        
    

def xml_to_txt(PATH,XML_PATH, TXT_PATH, train):
    if train == 1:
        file_name = 'train'
    else:
        file_name = 'test'
    
    df= pd.read_excel(PATH+"/"+file_name+".xlsx")
    df.rename(columns = {'종목코드':"CODE", '종목명':"CO_NM"},inplace=True)
    df['CODE'] = df['CODE'].apply(lambda x : str(x).zfill(6))
    corplist = df['CODE']
    utf_error = []
    error=[]
    
    
    while(len(corplist)>0):    # 오류난 기업들을 대상으로 계속 시도하기 
        # utf-8 로 인코딩된 파일 시도
        for code in corplist:
            xml = open(XML_PATH+'/'+code+'.xml', "rt", encoding='utf8')
            txt = open(TXT_PATH+'/'+code+'.txt', 'wt') 
            try:
                txt.write(xml.read())
            except:
                utf_error.append(code)
                continue
            
        # euc-kr 로 인코딩된 파일 시도 (둘 중 하나는 해당됨)
        for code in utf_error:
            xml = open(XML_PATH+code+'.xml', "rt", encoding='euc-kr')
            txt = open(TXT_PATH+code+'.txt', 'wt') 
            try:
                txt.write(xml.read())
            except:
                error.append(code)
                continue  
            
        corplist = error
        error=[]
        utf_error = []
        
    return len(error)>0
        
    
    
##########################
FILE_PATH = '/Users/jeeho/lab/miraeasset/mirae_env/최종/data' # train.xlsx, test.xlsx , 코스피.xlsx 

XML_PATH_train = "/Users/jeeho/lab/miraeasset/mirae_env/최종/dataout/report/train/xml"# 사업보고서 원본 파일 (압축된 형태)이 저장된 경로
TXT_PATH_train = "/Users/jeeho/lab/miraeasset/mirae_env/최종/dataout/report/train/txt"# 사업보고서 텍스트 파일이 저장된 경로

download_report(FILE_PATH, XML_PATH_train+"/zip",XML_PATH_train+"/unzip", 1) 
xml_to_txt(FILE_PATH,XML_PATH_train+"/unzip",TXT_PATH_train,1 )

XML_PATH_test = "/Users/jeeho/lab/miraeasset/mirae_env/최종/dataout/report/test/xml"# 사업보고서 원본 파일 (압축된 형태)이 저장된 경로
TXT_PATH_test = "/Users/jeeho/lab/miraeasset/mirae_env/최종/dataout/report/test/txt"# 사업보고서 텍스트 파일이 저장된 경로
download_report(FILE_PATH, XML_PATH_test+"/zip",XML_PATH_test+"/unzip", 0) 
xml_to_txt(FILE_PATH,XML_PATH_test+"/unzip",TXT_PATH_test,0 )





