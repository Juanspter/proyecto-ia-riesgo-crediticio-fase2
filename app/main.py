from pathlib import Path
import json
import numpy as np
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, ConfigDict
ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/'model'/'credit_model.joblib'
META=ROOT/'model'/'metadata.json'
app=FastAPI(title='API de riesgo crediticio (demostracion)',version='1.0.0',description='Solo datos sinteticos; no usar para decisiones crediticias reales.')
class PredictRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    features:list[float]=Field(min_length=12,max_length=12,description='12 variables numericas sinteticas, orden feature_01..feature_12')
@app.get('/')
def index():
    return FileResponse(ROOT/'app'/'index.html')
@app.get('/health')
def health():
    return {'status':'ok' if MODEL.exists() and META.exists() else 'not_ready'}
@app.get('/model-info')
def info():
    if not META.exists():raise HTTPException(503,'Modelo no disponible')
    return json.loads(META.read_text(encoding='utf-8'))
@app.post('/predict')
def predict(payload:PredictRequest):
    x=np.asarray(payload.features,dtype=float)
    if not np.isfinite(x).all():raise HTTPException(422,'Todos los valores deben ser finitos')
    if not MODEL.exists() or not META.exists():raise HTTPException(503,'Modelo no disponible')
    m=joblib.load(MODEL)
    meta=json.loads(META.read_text(encoding='utf-8'))
    probability=float(m.predict_proba(x.reshape(1,-1))[0,1])
    threshold=meta['umbral_demo']
    return {'probabilidad_incumplimiento':round(probability,6),'clasificacion':int(probability>=threshold),'umbral':threshold,'aviso':'Resultado didactico con variables sinteticas; no es una evaluacion bancaria real.'}
