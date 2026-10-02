from comun import *
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score
v = cargar(); X, y = v[NUM + CAT], v.RETRASO
modelos = {'RandomForest': lambda: RandomForestClassifier(n_estimators=300, max_depth=18, min_samples_leaf=5, class_weight='balanced', n_jobs=-1, random_state=42),
           'Red densa MLP': lambda: MLPClassifier(hidden_layer_sizes=(128,64,32), alpha=1e-3, batch_size=256, max_iter=60, early_stopping=True, n_iter_no_change=6, random_state=42)}
filas = []
for n, f in modelos.items():
    for test in [0.2, 0.3]:
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=test, stratify=y, random_state=42)
        m = Pipeline([('pre', prepro()), ('clf', f())]).fit(Xtr, ytr); pr = m.predict_proba(Xte)[:,1]; p = m.predict(Xte)
        filas.append([n, f'hold-out {int((1-test)*100)}-{int(test*100)}', accuracy_score(yte,p), f1_score(yte,p), roc_auc_score(yte,pr), '-'])
    cv = cross_validate(Pipeline([('pre', prepro()), ('clf', f())]), X, y, cv=StratifiedKFold(5, shuffle=True, random_state=42),
                        scoring=['accuracy','f1','roc_auc'], n_jobs=1)
    filas.append([n, 'CV 5-fold (media)', cv['test_accuracy'].mean(), cv['test_f1'].mean(), cv['test_roc_auc'].mean(), f"±{cv['test_roc_auc'].std():.4f}"])
r = pd.DataFrame(filas, columns=['modelo','evaluación','accuracy','F1','AUC','desv. AUC'])
print(r.round(4).to_string(index=False))
