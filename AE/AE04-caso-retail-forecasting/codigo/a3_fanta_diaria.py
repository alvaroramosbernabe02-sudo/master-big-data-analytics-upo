import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = pd.read_csv('Ventas diarias de Fanta 33cl.csv', sep=';', decimal=',')
d['Fecha']=pd.to_datetime(d.Fecha, format='%d/%m/%y')
print(d.describe().round(2).to_string())
X = pd.get_dummies(d[['Precio','Mes','Anno','DiaSemana','T']], columns=['DiaSemana'], drop_first=True); y=d.Unidades
Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=0.2,random_state=7)
ms={'LinearRegression':LinearRegression(),'RandomForestRegressor':RandomForestRegressor(n_estimators=400,min_samples_leaf=3,random_state=7),
    'GradientBoostingRegressor':GradientBoostingRegressor(n_estimators=300,learning_rate=0.05,max_depth=3,random_state=7)}
rows=[]
for n,m in ms.items():
    p=m.fit(Xtr,ytr).predict(Xte); rows.append([n,mean_absolute_error(yte,p),mean_squared_error(yte,p)**.5,r2_score(yte,p)])
r=pd.DataFrame(rows,columns=['modelo','MAE','RMSE','R2']); print(r.round(3).to_string(index=False))
print('Mejor:', r.loc[r.MAE.idxmin(),'modelo'])
lr=ms['LinearRegression']; print('Coeficientes LR:', {k: round(float(v),2) for k,v in zip(X.columns, lr.coef_)})
imp=pd.Series(ms['RandomForestRegressor'].feature_importances_,X.columns).sort_values(ascending=False).round(3); print('Importancias RF:', imp.head(6).to_dict())
