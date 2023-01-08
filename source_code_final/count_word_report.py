import pandas as pd

# 사업보고서에서 키워드를 검색해서 등장 횟수를 카운트해주는 함수 
# 아래 함수에서 키워드 추가/삭제 가능
# TXT_PATH : 사업보고서 파일이 모여있는 폴더
# PATH 에 포함되어야할 것: train.xlsx, test.xlsx
# df : 기업명, 기업코드로 이루어진 데이터 프레임 (train, test) 
# train : train set 이면 1, test set 이면 0


def report_word(PATH, TXT_PATH ,df,train):
    
    count_keyword=[]
    e_pos=[]
    e_neg=[]
    
    for i in df['CODE']:
        x = 0
        y = 0
        z = 0
        f = open(TXT_PATH+"/"+i+'.txt', 'r')
        data = f.read()
        x += data.count('검찰고발')
        x += data.count('과태료')
        x += data.count('과징금')
        x += data.count('징역')
        x += data.count('벌금')
        x += data.count('시정')
        x += data.count('산업안전보건')
        x += data.count('독점규제')
        x += data.count('공정거래')
        
        y += data.count('저탄소')
        y += data.count('친환경')
        y += data.count('감축')
        y += data.count('배출권')
        y += data.count('태양광')
        y += data.count('연료전지')
        y += data.count('신재생')
        y += data.count('재생에너지')
        y += data.count('한경친화적')
        y += data.count('풍력')
        y += data.count('태양광')
        y += data.count('환경개선')
        y += data.count('환경보호')
        y += data.count('지속가능')
        y += data.count('저감')
        y += data.count('기후변화대응')
        y += data.count('녹색')
        y += data.count('그린')
        
        z += data.count('화학물질관리법')
        z += data.count('악취')
        z += data.count('폐수배출')
        z += data.count('대기환경')
        z += data.count('폐기물')
        z += data.count('환경오염')
        z += data.count('환경관리')
        z += data.count('대기방지')
        z += data.count('대기배출')
        z += data.count('유해화학물질')
        z += data.count('오염물질')
        z += data.count('환경분야시험')
        f.close()
        count_keyword.append(x)
        e_pos.append(y)
        e_neg.append(z)

    df['s_negative'] = count_keyword
    df['e_positive'] = e_pos
    df['e_negative'] = e_neg

    
    return df
        
    