import math
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():
 r=client.get('/health');assert r.status_code==200;assert r.json()['status']=='ok'
def test_frontend():
 r=client.get('/');assert r.status_code==200;assert 'Consultar prediccion' in r.text
def test_model_info():
 r=client.get('/model-info');assert r.status_code==200;assert len(r.json()['features'])==12
def test_prediction():
 r=client.post('/predict',json={'features':[0.0]*12});assert r.status_code==200
 data=r.json();assert 0<=data['probabilidad_incumplimiento']<=1;assert data['clasificacion'] in (0,1)
def test_missing_features():
 assert client.post('/predict',json={'features':[0]*11}).status_code==422
def test_extra_features():
 assert client.post('/predict',json={'features':[0]*13}).status_code==422
def test_invalid_type():
 assert client.post('/predict',json={'features':['texto']+[0]*11}).status_code==422
def test_extra_field():
 assert client.post('/predict',json={'features':[0]*12,'secret':'x'}).status_code==422
def test_null_payload():
 assert client.post('/predict',json=None).status_code==422
def test_extreme_finite_values():
 r=client.post('/predict',json={'features':[1e6,-1e6]*6});assert r.status_code==200
