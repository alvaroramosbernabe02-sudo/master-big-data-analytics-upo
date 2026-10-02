"""PT12 E5 - Visualización de la capa de resultados (pt12.kpi_aerolinea exportada de BigQuery)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np
kpi = [("MQ",27568,33.5,53.3),("F9",6735,31.0,51.0),("NK",8632,26.4,52.7),("OO",46655,23.6,51.9),("B6",20482,23.3,47.5),
       ("EV",48084,22.1,49.9),("UA",37363,21.7,49.5),("AA",43074,21.3,47.1),("WN",98060,18.5,43.5),("US",32478,17.6,46.7),
       ("VX",4647,15.9,47.3),("AS",13151,14.1,43.7),("HA",6408,13.2,46.0),("DL",63676,12.2,39.6)]
imp = [("dia_mes",446.4),("hora_salida",194.8),("aerolinea",121.7),("dia_semana",90.3),("origen",48.0),("distancia",34.5),("duracion_programada",25.2),("destino",24.2)]
fig, ax = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw={"width_ratios": [1.5, 1]})
a = [k[0] for k in kpi]; x = np.arange(len(a))
ax[0].bar(x - .2, [k[2] for k in kpi], .4, label="% retraso real", color="#2a6fbb")
ax[0].bar(x + .2, [k[3] for k in kpi], .4, label="% prob. media prevista", color="#f39c34")
ax[0].set_xticks(x, a); ax[0].set_ylabel("%"); ax[0].set_title("Retraso > 15 min por aerolínea (enero 2015)")
ax[0].legend(frameon=False); ax[0].spines[["top", "right"]].set_visible(False)
f = [i[0] for i in imp][::-1]; g = [i[1] for i in imp][::-1]
ax[1].barh(f, g, color="#2a6fbb"); ax[1].set_title("Importancia de variables (ganancia)")
ax[1].spines[["top", "right"]].set_visible(False)
for i, v in enumerate(g): ax[1].text(v + 5, i, f"{v:.0f}", va="center", fontsize=9)
plt.tight_layout(); plt.savefig("/opt/w2/shots/pt12_c07_dashboard.png", dpi=130)
print("Gráfico guardado: pt12_c07_dashboard.png")
