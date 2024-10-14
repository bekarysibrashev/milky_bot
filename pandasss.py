import pandas as pd
import numpy as np

# file_path = '/home/ftpuser/баллы.xlsx'
file_path = '/home/ftpuser/Остатки бонусных баллов (XLSX).xlsx'
# file_path = "C:/Users/User/Desktop/milky bot tg/баллы.xlsx"
df1= pd.read_excel(file_path)

# df = df.iloc[5:]
# df.columns = df.iloc[0]
# df1 = df.iloc[4:]
# df1['Штрихкод'] = df1['Штрихкод'].fillna(0)

# df1['Штрихкод'] = df1['Штрихкод'].fillna(0).str.replace(' ', '').astype(np.int64)



bonus = df1.iloc[3,4] 
df1.iloc[4,4] = bonus
df1.columns = df1.iloc[4]





hashcode = df1['Штрихкод']# Series штрих кодов которые потом будут списком

codes = hashcode.tolist() # Список всех существующих штрих кодов. Нужно чтоб убедиться код который отправил пользователь есть в базе  

# print(codes)
# code = int(input())

def bonus_amount(code):
   
    filtered_data = df1.loc[df1['Штрихкод'] == code, 'Накоплено баллов']
    owner = df1.loc[df1['Штрихкод'] == code,'Дисконтная карта']
    if not filtered_data.empty:
        respond = filtered_data.values[0]
        respond1 = owner.values[0]
        # print(respond)
    else:
        respond = 'Непарвильный штриход'
        respond1 = None
        # print(respond)
    return respond, respond1


# print(df1.loc[df1['Штрихкод'] == "2551000050109"])
# print(df1['Штрихкод'].dropna())
# print(df1)
