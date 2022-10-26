import pandas as pd

origin = pd.read_excel("List.xlsx", sheet_name='Origin').fillna(0)
result = pd.read_excel("List.xlsx", sheet_name='Result').fillna(0)

for i in range(len(origin['Species'])):
    origin['Species'][i] = origin['Species'][i].replace('\'', '')

for i in range(len(origin['Species'])):
    if origin['AMBI'][i] == 0.0:
        result['Status'][i] = 'Not Assinged'
    else:
        result['AMBI'][i] = int(origin['AMBI'][i])

for i in range(len(origin['Species'])):
    if result['AMBI'][i] == 0.0 and result['Status'][i] != 'Not Assinged':
        result['Status'][i] = 'Not Existed'

result.to_excel('Result.xlsx')