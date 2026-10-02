from comun import *
import joblib, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, roc_auc_score, f1_score, accuracy_score, roc_curve, precision_score, recall_score
v = cargar(); X, y = v[NUM + CAT], v.RETRASO
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
red = Pipeline([('pre', prepro()), ('clf', MLPClassifier(hidden_layer_sizes=(128, 64, 32), activation='relu', solver='adam',
        alpha=1e-3, batch_size=256, learning_rate_init=1e-3, max_iter=60, early_stopping=True, validation_fraction=0.1,
        n_iter_no_change=6, random_state=42))])
red.fit(Xtr, ytr); mlp = red.named_steps['clf']
print(f'Red densa 3 capas ocultas (128-64-32, ReLU, Adam): {mlp.n_iter_} épocas, mejor val. accuracy={mlp.best_validation_score_:.4f}')
rf, _, _ = joblib.load('rf.joblib')
filas = []; plt.figure(figsize=(6, 5))
for nombre, m in [('RandomForest', rf), ('Red neuronal densa', red)]:
    pr = m.predict_proba(Xte)[:, 1]; th = y.mean()  # umbral = prevalencia (compensa el desbalanceo)
    p = (pr >= th).astype(int) if nombre != 'RandomForest' else m.predict(Xte)
    filas.append([nombre, accuracy_score(yte,p), precision_score(yte,p), recall_score(yte,p), f1_score(yte,p), roc_auc_score(yte,pr)])
    print(f'{nombre:20s} matriz confusión [[TN FP],[FN TP]] = {confusion_matrix(yte,p).tolist()}')
    fpr, tpr, _ = roc_curve(yte, pr); plt.plot(fpr, tpr, label=f'{nombre} (AUC={roc_auc_score(yte,pr):.3f})')
plt.plot([0,1],[0,1],'k--',lw=.8); plt.xlabel('FPR'); plt.ylabel('TPR'); plt.title('Curvas ROC - retraso > 15 min'); plt.legend(); plt.tight_layout(); plt.savefig('/opt/w2/shots/pt12_roc.png', dpi=110)
r = pd.DataFrame(filas, columns=['modelo','accuracy','precision','recall','F1','AUC']).round(4); print(r.to_string(index=False))
joblib.dump(red, 'red.joblib')
