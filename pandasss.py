import pandas as pd
import numpy as np

# file_path = '/home/ftpuser/баллы.xlsx'
file_path = "C:/Users/User/Downloads/баллы.xlsx"
df = pd.read_excel(file_path)

df = df.iloc[5:]
df.columns = df.iloc[0]
df1 = df.iloc[4:]
# df1['Штрихкод'] = df1['Штрихкод'].fillna(0)

# df1['Штрихкод'] = df1['Штрихкод'].fillna(0).str.replace(' ', '').astype(np.int64)

hashcode = df1['Штрихкод']# Series штрих кодов которые потом будут списком

codes = hashcode.tolist() # Список всех существующих штрих кодов. Нужно чтоб убедиться код который отправил пользователь есть в базе  

# print(codes)
# code = int(input())

def bonus_amount(code):
   
    filtered_data = df1.loc[df1['Штрихкод'] == code, 'Доступный остаток']
    owner = df1.loc[df1['Штрихкод'] == code,'Дисконтная карта.Владелец карты']
    if not filtered_data.empty:
        respond = filtered_data.values[0]
        respond1 = owner.values[0]
        # print(respond)
    else:
        respond = 'Непарвильный штриход'
        respond1 = None
        # print(respond)
    return respond, respond1

# bonus_amount(code)

# print(df1.loc[df1['Штрихкод'] == "2551000050109"])
# print(df1['Штрихкод'].dropna())
# print(df1)
