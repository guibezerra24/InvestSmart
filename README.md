
# InvestSmart (Python demo) + SAST

Pequeno serviço FastAPI que recomenda uma carteira simples usando perfil de risco e horizonte.
Pipeline de **SAST** com **Semgrep** (+ Sonar opcional).

## Rodar localmente
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# Testes
pytest
```

## Endpoints
- `GET /health`
- `POST /profile/recommend`

Exemplo de request JSON:
```json
{"age":30,"risk_tolerance":"moderado","liquidity_available":5000,"goals":{"curto":6,"medio":24,"longo":60}}
```

## CI / SAST
- GitHub Actions: `.github/workflows/sast.yml`
- Semgrep pacotes: `p/ci`, `r/python`, `r/secrets`, `r/owasp-top-ten`
- Artefatos: `semgrep-results.sarif`, `semgrep-results.json`
- Sonar (opcional): configure secrets `SONAR_TOKEN`, `SONAR_HOST_URL`, `SONAR_PROJECT_KEY`


## DAST (execução dinâmica em staging local)
- **OWASP ZAP baseline** via ação oficial (`zaproxy/action-baseline`) contra `http://127.0.0.1:8000`.
- **Nikto** (Docker) para varredura complementar.
- Artefatos: `zap-baseline-report.html`, `nikto.txt`.

## SCA (análise de componentes)
- **pip-audit** (CVE em dependências Python) com saída SARIF/JSON.
- **pip-licenses** para relatório de licenças.
- Artefatos: `pip-audit.sarif`, `pip-audit.json`, `licenses.csv`.

## Integração & Monitoramento
- Jobs com *gates* (falham em críticos) bloqueando job `deploy_simulado`.
- Notificações via anotações no PR (SARIF). Pode adicionar Slack webhook fácil.
