import pandas as pd, numpy as np, warnings, logging, itertools
warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.tsa.statespace.mlemodel as _m
warnings.warn = lambda *a, **k: None
s = pd.read_csv('Ventas Mensuales Fanta 33cl.csv', sep=';')
s['Fecha']=pd.to_datetime(s.Fecha, dayfirst=True); s=s.set_index('Fecha')['Unidades'].asfreq('MS')
print('Serie:', s.index.min().date(), '->', s.index.max().date(), len(s), 'meses')
best=None
for p,d,q in itertools.product(range(3),[0,1],range(3)):
    for P,D,Q in [(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,1,1)]:
        try:
            m=SARIMAX(s,order=(p,d,q),seasonal_order=(P,D,Q,12)).fit(disp=False, warn_convergence=False)
            fc_=m.get_forecast(12).predicted_mean
            if not (np.isfinite(m.aic) and np.isfinite(fc_).all() and fc_.min()>0 and m.aic>100): continue
            if best is None or m.aic<best[0]: best=(m.aic,(p,d,q),(P,D,Q,12),m)
        except Exception: pass
aic,o,so,m=best
print(f'Mejor modelo por AIC: SARIMA{o}x{so}  AIC={aic:.1f}')
fc=m.get_forecast(12); f=fc.predicted_mean.round(0); ci=fc.conf_int().round(0)
out=pd.DataFrame({'forecast':f,'li95':ci.iloc[:,0],'ls95':ci.iloc[:,1]}); out.index=out.index.strftime('%Y-%m')
print(out.to_string())
print('Total previsto 12 meses:', int(f.sum()))
# cobertura de 1000 latas
dia = f.iloc[0]/f.index[0].days_in_month
print(f'Primer mes previsto ({f.index[0]:%Y-%m}): {f.iloc[0]:.0f} uds -> {dia:.1f} latas/día')
stock=1000; dias=0; restante=stock
for fecha,v in f.items():
    diario=v/fecha.days_in_month
    if restante>=v: restante-=v; dias+=fecha.days_in_month
    else: dias+=restante/diario; break
print(f'1000 latas cubren aprox. {dias:.1f} días de venta')
ax=s.plot(figsize=(10,4),label='histórico'); f.plot(ax=ax,label='forecast'); ax.fill_between(ci.index,ci.iloc[:,0],ci.iloc[:,1],alpha=.2)
ax.legend(); ax.set_title('Fanta 33cl - forecast SARIMA 12 meses'); plt.tight_layout(); plt.savefig('fig/a2_arima.png',dpi=110)
