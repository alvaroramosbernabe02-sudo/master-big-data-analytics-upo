from comun import *
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score, accuracy_score
v = cargar()
print('Vuelos no cancelados ni desviados:', len(v), '| % retrasados (>15 min):', round(v.RETRASO.mean()*100, 2))
X, y = v[NUM + CAT], v.RETRASO
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
for nombre, clf in [('LogisticRegression (baseline)', LogisticRegression(max_iter=2000, class_weight='balanced')),
                    ('RandomForestClassifier', RandomForestClassifier(n_estimators=300, max_depth=18, min_samples_leaf=5, class_weight='balanced', n_jobs=-1, random_state=42))]:
    m = Pipeline([('pre', prepro()), ('clf', clf)]).fit(Xtr, ytr)
    p = m.predict(Xte); pr = m.predict_proba(Xte)[:, 1]
    print(f'\n== {nombre} ==  accuracy={accuracy_score(yte,p):.4f}  F1={f1_score(yte,p):.4f}  AUC={roc_auc_score(yte,pr):.4f}')
    print('Matriz de confusión [[TN FP],[FN TP]]:', confusion_matrix(yte, p).tolist())
    print(classification_report(yte, p, digits=3, target_names=['puntual', 'retrasado']))
import joblib; joblib.dump((m, Xte, yte), 'rf.joblib')
