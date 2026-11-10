"""Reentrena el Random Forest con la MISMA receta de datos sintéticos del proyecto anterior.
No se dispone de datos bancarios reales. No es un modelo aprobado para producción.
"""
from pathlib import Path
import json
import joblib
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
ROOT=Path(__file__).resolve().parent
X,y=make_classification(n_samples=5000,n_features=12,n_informative=7,n_redundant=3,weights=[.83,.17],class_sep=.9,flip_y=.025,random_state=42)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,stratify=y,random_state=42)
model=RandomForestClassifier(n_estimators=160,min_samples_leaf=6,max_depth=10,n_jobs=1,random_state=42)
model.fit(X_train,y_train)
ROOT.mkdir(exist_ok=True)
joblib.dump(model,ROOT/'credit_model.joblib')
meta={'origen':'datos sinteticos generados con make_classification','features':[f'feature_{i:02d}' for i in range(1,13)],'umbral_demo':0.5,'auc_test':round(float(roc_auc_score(y_test,model.predict_proba(X_test)[:,1])),4),'advertencia':'No apto para decisiones crediticias reales. Variables sin significado economico.'}
(ROOT/'metadata.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
print(meta)
