# Triagem SonarCloud — flext-sh/flext-observability

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead de rastreio: `mro-2wjm.12`

## Resumo

**13 issues** — BLOCKER 0, CRITICAL 3, MAJOR 6, MINOR 4
Tipos: VULNERABILITY 4, BUG 2, CODE_SMELL 7

| regra | issues |
|---|---|
| `python:S1192` | 2 |
| `githubactions:S8233` | 2 |
| `python:S2201` | 2 |
| `python:S7498` | 2 |
| `python:S3776` | 1 |
| `githubactions:S8264` | 1 |
| `text:S8565` | 1 |
| `python:S7504` | 1 |

## Issues

Coluna **Decisão**: `corrigir` / `falso-positivo` / `risco-aceito`.

| # | sev | tipo | regra | componente | linha | Decisão |
|---|---|---|---|---|---|---|
| 1 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_observability/api.py` | 99 | |
| 2 | CRITICAL | CODE_SMELL | `python:S1192` | `src/flext_observability/api.py` | 244 | |
| 3 | CRITICAL | CODE_SMELL | `python:S3776` | `src/flext_observability/services/http_client_instrumentation.py` | 101 | |
| 4 | MAJOR | VULNERABILITY | `githubactions:S8264` | `.github/workflows/docs.yml` | 18 | |
| 5 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 19 | |
| 6 | MAJOR | VULNERABILITY | `githubactions:S8233` | `.github/workflows/docs.yml` | 20 | |
| 7 | MAJOR | BUG | `python:S2201` | `examples/01_functional.py` | 109 | |
| 8 | MAJOR | BUG | `python:S2201` | `examples/02_solid_observability_demo.py` | 124 | |
| 9 | MAJOR | VULNERABILITY | `text:S8565` | `pyproject.toml` | - | |
| 10 | MINOR | CODE_SMELL | `python:S7504` | `conftest.py` | 20 | |
| 11 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_observability/services/custom_metrics.py` | 70 | |
| 12 | MINOR | CODE_SMELL | `python:S7498` | `src/flext_observability/services/custom_metrics.py` | 71 | |
| 13 | MINOR | CODE_SMELL | `python:S1940` | `src/flext_observability/services/error_handling.py` | 269 | |

## Como triar

1. **BLOCKER e CRITICAL primeiro**, e todo VULNERABILITY independente de severidade.
2. Classificar: **corrigir**, **falso-positivo** (marcar na plataforma SonarCloud com justificativa), **risco-aceito** (com prazo).
3. CODE_SMELL em volume alto sugere padrão — corrigir a causa raiz, não issue a issue.

Dados brutos: `~/sonarqube-violations/by-repo/flext-sh__flext-observability.json`

