#%%%
import decimal
import io
import json


import pandas as pd

import requests



def WallexData():
    r = requests.get('https://wallex.ir/markets')
    content = r.content
    content = str(content, 'utf-8')
    start = content.find(' type="application/json">{"props":{"pageProps":{"dehydratedState"')
    end = content.find('"message":"عملیات با موفقیت انجام شد","success":true}')
    content_cropped = content[start+110:end-1] + '}'
    wallexDict = json.loads(content_cropped)
    symbols = wallexDict['result']['symbols']
    df = pd.DataFrame(symbols).T
    statsData = df.stats.apply(pd.Series)
    df.drop('stats', axis=1, inplace=True)
    direction = statsData.direction.apply(pd.Series)
    statsData.drop('direction', axis=1, inplace=True)
    statsdata = pd.concat([statsData, direction], axis=1)
    df = pd.concat([statsData,df], axis=1)
    df.loc[df['24h_ch'] =='-', '24h_ch'] =0
    df.loc[df['lastPrice'] =='-' , 'lastPrice'] =0
    df.loc[df['24h_quoteVolume'] =='-', '24h_quoteVolume'] =0
    df['24h_quoteVolume']= df['24h_quoteVolume'].astype(float)
    df['lastPrice'] = df['lastPrice'].apply(lambda x: float(decimal.Decimal(x)))
    return df
# %%

df = WallexData()
df.to_csv('wallexData.csv')
# %%
