import pandas as pd
import numpy as np


origin = pd.read_excel("xlsx/spieces.xlsx", sheet_name=0).fillna(0)
cur = pd.read_excel("xlsx/spieces.xlsx", sheet_name=1).fillna(0)
result = pd.read_excel("xlsx/spieces.xlsx", sheet_name=2).fillna(0)

#for i in range(716):
#    if tmp[not tmp[i]][2]
#tmp.loc[tmp['AMBI 등급']==0, ['비고']] = 'Not Assinged'
#tmp[tmp['AMBI 등급']==0]

for i in range(len(origin['종명'])):
    origin['종명'][i] = origin['종명'][i].replace('\'', '')
#origin.head(3)

for i in range(len(cur['종명자료'])):
    for j in range(len(origin['종명'])):
#for i in range(50):
#    for j in range(1000):
        if cur['종명자료'][i] == origin['종명'][j]:
            #print('cur: ', cur['종명자료'][i])
            #print('origin: ', origin['종명'][j])

            if origin['AMBI'][i] == 0:
                result['비고'][i] = 'Not Assinged'
            else:
                result['AMBI'][i] = origin['AMBI'][j]
            continue
        # else:
        #    result['비고'][i] = 'Not Existed'

for i in range(len(cur['종명자료'])):
    if result['AMBI'][i] == 0.0 and result['비고'][i] != 'Not Assinged':
        result['비고'][i] = 'Not Existed'

print(result.head(20))
result.to_excel('Result.xlsx')