# Prediccion de incumplimiento crediticio - demo academica

Proyecto de continuidad de la evaluacion de modelos. Datos **sinteticos**, 12 variables abstractas, sin interpretacion financiera. No usar en decisiones bancarias.

## Arquitectura
Navegador (HTML/JS) -> `POST /predict` (FastAPI) -> RandomForest entrenado offline -> JSON.

## Ejecucion local sin Docker
```bash
python -m venv .venv
# Activar entorno: Windows .venv\Scripts\activate | Linux/macOS source .venv/bin/activate
pip install -r requirements-dev.txt
python -m model.train
python -m pytest -q
uvicorn app.main:app --host 127.0.0.1 --port 8080
```
Abrir http://localhost:8080 y documentacion http://localhost:8080/docs

## Docker
```bash
docker build -t riesgo-crediticio-demo:1.0 .
docker run --rm -p 8080:8080 --name riesgo-crediticio riesgo-crediticio-demo:1.0
```
En otra terminal:
```bash
curl http://localhost:8080/health
curl http://localhost:8080/model-info
curl -X POST http://localhost:8080/predict -H 'Content-Type: application/json' -d '{"features":[0,0,0,0,0,0,0,0,0,0,0,0]}'
```
En PowerShell puede usarse `Invoke-RestMethod` o Swagger `/docs`.

## Endpoints
- `GET /` interfaz HTML
- `GET /health` estado de archivos
- `GET /model-info` metadatos y AUC demostrativo
- `POST /predict` JSON con 12 numeros finitos; devuelve probabilidad, clase y aviso
- `GET /docs` Swagger UI

## Reproducibilidad y limitaciones
La receta de datos sinteticos replica `make_classification` y Random Forest del ejercicio previo. El umbral 0.5 es **demostrativo** y NO representa necesariamente el umbral optimizado en el reporte anterior. No se reutiliza un artefacto entrenado previamente: el Dockerfile lo vuelve a entrenar durante la construccion. No hay autenticacion, monitoreo ni controles de gobierno de modelo aptos para produccion.

## Evidencias
Guardar capturas de `docker build`, `docker ps`, pagina principal, Swagger, `/health`, respuesta de `/predict`, `pytest` y errores 422. No afirmar que Docker o nube se validaron si no se ejecutaron.

## Nube
Ver `Manual_despliegue_nube.docx` y `Documento_validacion_pruebas.docx` incluidos en el paquete de entrega.

## Entrega fase II y rubrica
La lista de evidencias que debes capturar esta en `evidencias/GUIA_EVIDENCIAS.md`.
Se incluye GitHub Actions en `.github/workflows/tests.yml` para ejecutar pruebas en cada push.

### Publicacion en GitHub (despues de verificar que no hay secretos ni datos personales)
```bash
git init
git add .
git commit -m "Proyecto fase II: API, frontend, Docker y pruebas"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```
Primero crea un repositorio vacio en GitHub; reemplaza los marcadores por tu usuario y nombre real del repositorio. No se ha publicado automaticamente.
