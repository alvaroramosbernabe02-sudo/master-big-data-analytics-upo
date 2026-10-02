"""Ejercicio 4. Herramientas adicionales: predicción de churn con el modelo entrenado del workshop,
ranking de clientes en riesgo y detección de outliers (IQR)."""
import warnings, joblib, pandas as pd
from langchain_core.tools import tool
from typing import Any, Dict
warnings.filterwarnings("ignore")
_churn = joblib.load("models/churn_predictor.pkl")
for _t in _churn.estimators_:            # compatibilidad: modelo guardado con scikit-learn 1.3
    if not hasattr(_t, "monotonic_cst"): _t.monotonic_cst = None
FEATS = list(_churn.feature_names_in_)
import numpy as np
def _proba(X):
    """Probabilidad de churn promediando hojas normalizadas (el pickle de sklearn 1.3 guarda recuentos, no proporciones)."""
    Xv = X[FEATS].to_numpy(dtype=np.float32); ps = []
    for t in _churn.estimators_:
        v = t.tree_.value[t.tree_.apply(Xv)][:, 0, :]
        ps.append(v[:, 1] / v.sum(axis=1))
    return np.mean(ps, axis=0)

@tool("predict_churn_customer")
def predict_churn_customer(customer_id: int) -> Dict[str, Any]:
    """Predice la probabilidad de abandono (churn) de un cliente concreto de customer_data a partir de su customer_id."""
    df = pd.read_csv("data/customer_data.csv")
    fila = df[df.customer_id == int(customer_id)]
    if fila.empty: return {"error": f"No existe el cliente {customer_id}"}
    p = float(_proba(fila)[0])
    return {"customer_id": int(customer_id), "probabilidad_churn": round(p, 3), "riesgo": "alto" if p >= 0.6 else "medio" if p >= 0.35 else "bajo",
            **{k: float(v) for k, v in fila[FEATS].iloc[0].items()},
            "segmento": fila.segment.iloc[0]}

@tool("top_churn_risk")
def top_churn_risk(n: int = 10, segment: str = "") -> Dict[str, Any]:
    """Devuelve los n clientes con mayor probabilidad de churn (opcionalmente filtrando por segmento Bronze/Silver/Gold/Platinum)."""
    df = pd.read_csv("data/customer_data.csv")
    if segment: df = df[df.segment.str.lower() == segment.lower()]
    df = df.assign(prob_churn=_proba(df)).sort_values("prob_churn", ascending=False).head(int(n))
    return {"clientes": df[["customer_id", "segment", "total_spent", "days_since_last_purchase", "prob_churn"]].round(3).to_dict(orient="records"),
            "prob_media_top": round(float(df.prob_churn.mean()), 3)}

@tool("detect_outliers")
def detect_outliers(dataset_name: str, column: str) -> Dict[str, Any]:
    """Detecta valores atípicos de una columna numérica con la regla de Tukey (1,5·IQR)."""
    s = pd.read_csv(f"data/{dataset_name}.csv")[column].dropna()
    q1, q3 = s.quantile(.25), s.quantile(.75); iqr = q3 - q1; lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    out = s[(s < lo) | (s > hi)]
    return {"columna": column, "limite_inferior": round(float(lo), 2), "limite_superior": round(float(hi), 2), "n_outliers": int(len(out)),
            "pct_outliers": round(100 * len(out) / len(s), 2), "ejemplos": out.head(8).round(2).tolist()}
