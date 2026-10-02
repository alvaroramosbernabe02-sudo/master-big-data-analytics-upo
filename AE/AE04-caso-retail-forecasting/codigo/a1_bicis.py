import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
df = pd.read_csv('day.csv')
X = df.drop(columns=['instant','dteday','casual','registered','cnt'])   # casual+registered = cnt -> fuga de información
X = pd.get_dummies(X, columns=['season','weathersit','mnth','weekday'], drop_first=True)
y = df['cnt']
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
print('train', Xtr.shape, 'test', Xte.shape)
modelos = {
 'LinearModel (Ridge)': (Ridge(), {'alpha':[0.01,0.1,1,10]}),
 'RandomForestRegressor': (RandomForestRegressor(random_state=42), {'n_estimators':[200,500],'max_depth':[None,10,20],'min_samples_leaf':[1,3]}),
 'GradientBoostingRegressor': (GradientBoostingRegressor(random_state=42), {'n_estimators':[200,500],'learning_rate':[0.03,0.1],'max_depth':[2,3,4]}),
}
res=[]
lr = LinearRegression().fit(Xtr,ytr); p=lr.predict(Xte)
res.append(['LinearRegression (sin hiperparámetros)','-',mean_absolute_error(yte,p),mean_squared_error(yte,p)**.5,r2_score(yte,p)])
for n,(m,g) in modelos.items():
    gs = GridSearchCV(m, g, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1).fit(Xtr,ytr)
    p = gs.predict(Xte)
    res.append([n, gs.best_params_, mean_absolute_error(yte,p), mean_squared_error(yte,p)**.5, r2_score(yte,p)])
r = pd.DataFrame(res, columns=['modelo','mejores_parametros','MAE','RMSE','R2'])
pd.set_option('display.width',200); pd.set_option('display.max_colwidth',80)
print(r.round(3).to_string(index=False))
print('Mejor modelo (MAE):', r.loc[r.MAE.idxmin(),'modelo'])
