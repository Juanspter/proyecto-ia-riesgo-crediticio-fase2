"""Prueba E2E: formulario HTML -> POST /predict -> respuesta visible."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = 'http://127.0.0.1:8080'
OUT = Path('evidencias_frontend')
OUT.mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 900}, device_scale_factor=1)
    page.goto(BASE + '/', wait_until='networkidle', timeout=30000)
    page.locator('#values').fill(', '.join(['0'] * 12))
    with page.expect_response(lambda r: r.url.endswith('/predict') and r.request.method == 'POST', timeout=30000) as event:
        page.locator('#run').click()
    response = event.value
    assert response.status == 200, f'POST /predict: HTTP {response.status}: {response.text()}'
    payload = response.json()
    assert isinstance(payload['probabilidad_incumplimiento'], (int, float))
    assert 0 <= payload['probabilidad_incumplimiento'] <= 1
    assert payload['clasificacion'] in (0, 1)
    assert payload['clasificacion'] == int(payload['probabilidad_incumplimiento'] >= payload['umbral'])
    page.wait_for_function("() => document.querySelector('#out').textContent.includes('probabilidad_incumplimiento')")
    visible = json.loads(page.locator('#out').inner_text())
    assert visible == payload, f'Frontend no muestra la respuesta exacta: {visible} vs {payload}'
    page.screenshot(path=str(OUT / 'formulario_con_prediccion.png'), full_page=True)
    (OUT / 'respuesta_frontend_api.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT / 'resultado.txt').write_text('PASS: formulario -> POST /predict HTTP 200 -> respuesta visible y coincidente\n', encoding='utf-8')
    print('PASS: formulario -> API -> resultado mostrado; captura guardada')
    browser.close()
