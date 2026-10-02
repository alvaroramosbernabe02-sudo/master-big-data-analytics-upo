from comun import *
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
v = cargar(); X, y = v[NUM + CAT], v.RETRASO
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
pipe = Pipeline([('pre', prepro()), ('clf', RandomForestClassifier(class_weight='balanced', n_jobs=-1, random_state=42))])
espacio = {'clf__n_estimators': [200, 400], 'clf__max_depth': [10, 14, 18, 24, None], 'clf__min_samples_leaf': [1, 3, 5, 10, 20],
           'clf__max_features': ['sqrt', 0.3]}
bus = RandomizedSearchCV(pipe, espacio, n_iter=12, scoring='roc_auc', cv=StratifiedKFold(3, shuffle=True, random_state=1),
                         return_train_score=True, random_state=7, n_jobs=1, verbose=0).fit(Xtr, ytr)
r = pd.DataFrame(bus.cv_results_)[['param_clf__max_depth','param_clf__min_samples_leaf','param_clf__max_features','param_clf__n_estimators','mean_train_score','mean_test_score']]
r.columns = ['max_depth','min_leaf','max_feat','n_est','AUC_train_cv','AUC_val_cv']; r['brecha'] = r.AUC_train_cv - r.AUC_val_cv
print(r.sort_values('AUC_val_cv', ascending=False).round(4).to_string(index=False))
print('\nMejores hiperparámetros:', {k.replace('clf__',''): v for k, v in bus.best_params_.items()})
best = bus.best_estimator_
atr, ate = roc_auc_score(ytr, best.predict_proba(Xtr)[:,1]), roc_auc_score(yte, best.predict_proba(Xte)[:,1])
print(f'Modelo óptimo -> AUC train={atr:.4f}  AUC test={ate:.4f}  brecha={atr-ate:.4f}')
libre = Pipeline([('pre', prepro()), ('clf', RandomForestClassifier(n_estimators=200, max_depth=None, min_samples_leaf=1, class_weight='balanced', n_jobs=-1, random_state=42))]).fit(Xtr, ytr)
a1, a2 = roc_auc_score(ytr, libre.predict_proba(Xtr)[:,1]), roc_auc_score(yte, libre.predict_proba(Xte)[:,1])
print(f'Árboles sin límite (max_depth=None, min_leaf=1) -> AUC train={a1:.4f}  AUC test={a2:.4f}  brecha={a1-a2:.4f}  <- sobreajuste')
