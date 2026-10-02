import pandas as pd, numpy as np, warnings, logging; warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.tsa.statespace.mlemodel as _m
warnings.warn = lambda *a, **k: None
a = pd.read_csv('CONSUMO SEVILLA CON MESES.csv', sep=';', decimal=',', encoding='latin-1')
a['Fecha']=pd.to_datetime(a.Timestamp.str.split().str[0], format='%d/%m/%y')
print('Diario:', a.Fecha.min().date(), '->', a.Fecha.max().date(), len(a), 'filas; NAs por columna:', a.isna().sum().to_dict())
aguaSinNA = a.dropna(); print('Tras dropna():', len(aguaSinNA))
g = aguaSinNA.copy(); g['dow']=g.Fecha.dt.dayofweek; g['doy']=g.Fecha.dt.dayofyear; g['t']=(g.Fecha-g.Fecha.min()).dt.days
g=g.sort_values('Fecha'); g['lag7']=g.CONSUMO.shift(7); g=g.dropna()
corte = g.Fecha.max()-pd.DateOffset(months=3)
tr,te = g[g.Fecha<=corte], g[g.Fecha>corte]
F=['dow','doy','t','LLUVIA','TEMPERATURA','MES','lag7']
m=GradientBoostingRegressor(n_estimators=400,learning_rate=0.05,max_depth=3,random_state=1).fit(tr[F],tr.CONSUMO); p=m.predict(te[F])
mae_d=mean_absolute_error(te.CONSUMO,p); rmse_d=mean_squared_error(te.CONSUMO,p)**.5
print(f'DIARIO  test={te.Fecha.min().date()}..{te.Fecha.max().date()} ({len(te)} días)  MAE={mae_d:.2f}  RMSE={rmse_d:.2f}  MAPE={np.mean(abs(te.CONSUMO-p)/te.CONSUMO)*100:.2f}%')
fig,ax=plt.subplots(figsize=(10,4)); ax.plot(te.Fecha,te.CONSUMO,label='real'); ax.plot(te.Fecha,p,label='forecast GBR'); ax.set_title('Consumo diario de agua Sevilla - test 3 meses'); ax.legend(); plt.tight_layout(); plt.savefig('fig/a4_diario.png',dpi=110)
mm = pd.read_csv('CONSUMO SEVILLA MENSUAL.csv', sep=';', decimal=',').dropna()
mes={'ene':1,'feb':2,'mar':3,'abr':4,'may':5,'jun':6,'jul':7,'ago':8,'sep':9,'oct':10,'nov':11,'dic':12}
mm['Fecha']=[pd.Timestamp(2000+int(x.split('-')[1]), mes[x.split('-')[0].lower()[:3]], 1) for x in mm.mes]
s=mm.set_index('Fecha').consumo.asfreq('MS')
print('Mensual:', s.index.min().date(), '->', s.index.max().date(), len(s), 'meses')
tr,te=s.iloc[:-6],s.iloc[-6:]
mod=SARIMAX(tr,order=(1,0,1),seasonal_order=(0,1,1,12)).fit(disp=False, warn_convergence=False); fc=mod.get_forecast(6).predicted_mean
mae_m=mean_absolute_error(te,fc); rmse_m=mean_squared_error(te,fc)**.5
print(pd.DataFrame({'real':te.round(1),'forecast':fc.round(1),'error%':((fc-te)/te*100).round(2)}).to_string())
print(f'MENSUAL SARIMA(1,0,1)x(0,1,1,12)  MAE={mae_m:.1f}  RMSE={rmse_m:.1f}  MAPE={np.mean(abs(te-fc)/te)*100:.2f}%')
fig,ax=plt.subplots(figsize=(10,4)); s.iloc[-36:].plot(ax=ax,label='real'); fc.plot(ax=ax,label='forecast (test 6 meses)',marker='o'); ax.legend(); ax.set_title('Consumo mensual de agua Sevilla'); plt.tight_layout(); plt.savefig('fig/a4_mensual.png',dpi=110)
