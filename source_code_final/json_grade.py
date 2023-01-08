import pandas as pd

def answering(json_path_e,json_path_s,json_path_g,test_path):
    #train된 모델에 test셋을 넣어 E,S,G json 파일을 불러온다.
    e_data=pd.read_json(json_path_e)
    s_data=pd.read_json(json_path_s)
    g_data=pd.read_json(json_path_g)

    e_grade=[]
    s_grade=[]
    g_grade=[]
    #json 파일에서 스코어가 가장 높게 나온 것을 등급으로 고른다. 
    for i in e_data['predicted_E_GRADE']:
        list=[]
        #predict score가 가장 높은 인덱스를 뽑는다.
        for j in i['scores']:
            list.append(float(j))
        tmp = max(list)
        index = list.index(tmp)
        #가장 높은 인덱스의 등급을 선택한다.
        x=float(i['classes'][index])
        e_grade.append(x)

    for i in s_data['predicted_S_GRADE']:
        list=[]
        for j in i['scores']:
            list.append(float(j))
        tmp = max(list)
        index = list.index(tmp)

        x=float(i['classes'][index])
        s_grade.append(x)

    for i in g_data['predicted_G_GRADE']:
        list=[]
        for j in i['scores']:
            list.append(float(j))
        tmp = max(list)
        index = list.index(tmp)

        x=float(i['classes'][index])
        g_grade.append(x)

    test_answer=pd.read_csv(test_path)
    test_answer['E_GRADE'] = e_grade
    test_answer['S_GRADE'] = s_grade
    test_answer['G_GRADE'] = g_grade

    return test_answer

    
def total_grade_answer(json_path, test_path):
    esg_data=pd.read_json(json_path)
    total_grade=[]

    for i in esg_data['predicted_ESG_GRADE']:
        list=[]
        for j in i['scores']:
            list.append(float(j))
        #predict score가 가장 높은 인덱스를 뽑는다.
        tmp = max(list)
        index = list.index(tmp)
        #가장 높은 인덱스의 등급을 선택한다.
        x=float(i['classes'][index])
        total_grade.append(x)
        
    test_df = pd.read_csv(test_path)
    test_df['ESG_GRADE']= total_grade
    return test_df
        