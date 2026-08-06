# AGENTS.md — flext-observability

> **Parent workspace law** lives in [`../AGENTS.md`](../AGENTS.md) — read it first.
> Universal engineering core: `~/.agents/UNIVERSAL_CORE.md`. Composition: global skills + parent/root `AGENTS.md` + this scope delta. Do not re-embed universal law.
>
> **Standalone / independent mode:** when `../AGENTS.md` does not resolve, pin the parent raw `AGENTS.md` URL to the same branch/release as this package (never `main`).

<!-- AIHUB-AGENTS-SCOPE-LOCAL-BEGIN -->
**Package:** `flext_observability` · deps: `flext-cli`, `flext-core`

## Overview

Enterprise monitoring, metrics & telemetry. Used by the Singer taps/targets for run telemetry.

## Structure

```text
src/flext_observability/
├── api.py            # FlextObservability facade
├── services/         # monitoring, performance, logging integration, custom metrics,
│                     #   context, sampling, health, error handling, HTTP instrumentation
├── constants.py typings.py protocols.py models.py utilities.py   # AUTO-GENERATED facets
└── _config.py _settings.py
```

## Code Map

| Symbol | Kind | Location | Role |
|--------|------|----------|------|
| `FlextObservability` | class | `api.py` | facade: `flext_metric`, `flext_trace`, `flext_alert`, `flext_health_check`, `flext_log_entry` |
| nested models | classes | `_models` | `Metric`, `Trace`, `Alert`, `HealthCheck`, `LogEntry` |

## Conventions (specific to this package)

- Metric type/ID/labels are normalized by private helpers **before** model creation — construct through the facade, not the models directly.
- Structured logging flows through the `flext-core` logger factory; never call `structlog.get_logger` directly.
- Config/settings canonical pattern: ADR-012.
- Codemod governance (ast-grep + make mod): ADR-014.

## Commands

```bash
make check PROJECT=flext-observability
make test  PROJECT=flext-observability       # tests/{unit,integration,e2e,fixtures}
```
<!-- AIHUB-AGENTS-SCOPE-LOCAL-END -->
