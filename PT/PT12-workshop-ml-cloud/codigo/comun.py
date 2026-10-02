import pandas as pd, numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
def cargar():
    v = pd.read_csv('flights_subsampling.csv', low_memory=False)
    v = v[(v.CANCELLED == 0) & (v.DIVERTED == 0) & v.ARRIVAL_DELAY.notna()].copy()
    v['RETRASO'] = (v.ARRIVAL_DELAY > 15).astype(int)          # criterio FAA: retraso > 15 min
    v['HORA_SALIDA'] = v.SCHEDULED_DEPARTURE // 100
    v['HORA_LLEGADA'] = v.SCHEDULED_ARRIVAL // 100
    for c in ['ORIGIN_AIRPORT', 'DESTINATION_AIRPORT']:            # top-40 aeropuertos, resto -> OTRO
        top = v[c].value_counts().index[:40]; v[c] = v[c].where(v[c].isin(top), 'OTRO').astype(str)
    return v
NUM = ['MONTH', 'DAY', 'DAY_OF_WEEK', 'HORA_SALIDA', 'HORA_LLEGADA', 'SCHEDULED_TIME', 'DISTANCE']
CAT = ['AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT']
def prepro():
    return ColumnTransformer([('num', StandardScaler(), NUM), ('cat', OneHotEncoder(handle_unknown='ignore'), CAT)])
