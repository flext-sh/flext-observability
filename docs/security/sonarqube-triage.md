# Triagem SonarCloud — flext-sh/flext-observability

Gerado do dump da plataforma SonarCloud (2026-08-06).

Bead: `mro-2wjm.12`

## Resumo

**13 issues** — BLOCKER 0, CRITICAL 3, MAJOR 6, MINOR 4
Tipos: VULNERABILITY 4, BUG 2, CODE_SMELL 7 · **Debt total: 85min**

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
| `python:S1940` | 1 |

## Como usar

Cada issue traz a **mensagem do SonarQube** (descreve o problema e o impacto), o **código real** (linha `>>>`), o tipo e o effort estimado.
**Decisão**: `corrigir` / `falso-positivo` (marcar na plataforma com justificativa) / `risco-aceito`. Ordem: BLOCKER → CRITICAL → VULNERABILITY → MAJOR. CODE_SMELL em volume pede correção de padrão.

## Issues

### 1 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_observability/api.py:99` · **Effort**: 6min

> Define a constant instead of duplicating this literal "create metric" 3 times.

```python
       95          """Create a metric entity directly."""
       96          try:
       97              return FlextObservability._flext_metric_entity(name, value, unit, kwargs)
       98          except (c.ValidationError, ValueError, TypeError, AttributeError) as e:
>>>    99              return r[FlextObservability.Metric].fail_op("create metric", e)
      100  
      101      @staticmethod
      102      def _flext_metric_entity(
      103          name: str, value: float, unit: str, kwargs: t.MappingKV[str, t.JsonPayload]
```

**Decisão**: 

### 2 · 🟠 CRITICAL · CODE_SMELL · `python:S1192`
**Local**: `src/flext_observability/api.py:244` · **Effort**: 6min

> Define a constant instead of duplicating this literal "create health check" 3 times.

```python
      240          _ = health_check_id
      241          try:
      242              if not component:
      243                  return r[FlextObservability.HealthCheck].fail_op(
>>>   244                      "create health check", "Component name cannot be empty"
      245                  )
      246              if status not in c.Observability.HealthStatus:
      247                  return r[FlextObservability.HealthCheck].fail_op(
      248                      "create health check", f"Invalid health status: {status}"
```

**Decisão**: 

### 3 · 🟠 CRITICAL · CODE_SMELL · `python:S3776`
**Local**: `src/flext_observability/services/http_client_instrumentation.py:101` · **Effort**: 26min

> Refactor this function to reduce its Cognitive Complexity from 36 to the 15 allowed.

```python
       97  
       98          instrumented_clients: ClassVar[set[int]] = set()
       99  
      100          @staticmethod
>>>   101          def _apply_httpx_instrumentation(
      102              client: t.RegisterableService,
      103          ) -> p.Result[bool]:
      104              """Apply httpx instrumentation to a validated client.
      105  
```

**Decisão**: 

### 4 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8264`
**Local**: `.github/workflows/docs.yml:18` · **Effort**: 5min

> Move this read permission from workflow level to job level.

```yaml
       14        - ".github/workflows/docs.yml"
       15    workflow_dispatch:
       16  
       17  permissions:
>>>    18    contents: read
       19    pages: write
       20    id-token: write
       21  
       22  concurrency:
```

**Decisão**: 

### 5 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:19` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       15    workflow_dispatch:
       16  
       17  permissions:
       18    contents: read
>>>    19    pages: write
       20    id-token: write
       21  
       22  concurrency:
       23    group: pages
```

**Decisão**: 

### 6 · 🟡 MAJOR · VULNERABILITY · `githubactions:S8233`
**Local**: `.github/workflows/docs.yml:20` · **Effort**: 5min

> Move this write permission from workflow level to job level.

```yaml
       16  
       17  permissions:
       18    contents: read
       19    pages: write
>>>    20    id-token: write
       21  
       22  concurrency:
       23    group: pages
       24    cancel-in-progress: false
```

**Decisão**: 

### 7 · 🟡 MAJOR · BUG · `python:S2201`
**Local**: `examples/01_functional.py:109` · **Effort**: 5min

> The return value of "dict.get" must be used.

```python
      105                  "warning": "[WARN]",
      106                  "error": "[ERROR]",
      107                  "critical": "[CRIT]",
      108              }
>>>   109              icons.get(level, "[UNKNOWN]")
      110  
      111  
      112  def demonstrate_global_factory() -> None:
      113      """Demonstrate repeated facade usage without factory indirection."""
```

**Decisão**: 

### 8 · 🟡 MAJOR · BUG · `python:S2201`
**Local**: `examples/02_solid_observability_demo.py:124` · **Effort**: 5min

> The return value of "__getitem__" must be used.

```python
      120                  "warning": "[WARN]",
      121                  "error": "[ERROR]",
      122                  "critical": "[CRIT]",
      123              }
>>>   124              icons[level]
      125  
      126  
      127  def demonstrate_function_monitoring() -> None:
      128      """Demonstrate automatic function monitoring."""
```

**Decisão**: 

### 9 · 🟡 MAJOR · VULNERABILITY · `text:S8565`
**Local**: `pyproject.toml:-` · **Effort**: 5min

> Dependency versions are not predictable if the lock file (uv.lock, poetry.lock, pdm.lock or pylock.toml) is missing.


**Decisão**: 

### 10 · ⚪ MINOR · CODE_SMELL · `python:S7504`
**Local**: `conftest.py:20` · **Effort**: 5min

> Remove this unnecessary `list()` call on an already iterable object.

```python
       16      if (
       17          existing_package is None
       18          or Path(getattr(existing_package, "__file__", "")).resolve() != init_file
       19      ):
>>>    20          for module_name in list(sys.modules):
       21              if module_name == package_name or module_name.startswith(
       22                  f"{package_name}."
       23              ):
       24                  sys.modules.pop(module_name, None)
```

**Decisão**: 

### 11 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_observability/services/custom_metrics.py:70` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
       66              """Initialize metric registry."""
       67              self._metrics: MutableMapping[
       68                  str, m.Observability.CustomMetricDefinition
       69              ] = {}
>>>    70              self._metric_instances: t.MutableScalarMapping = dict[str, t.Scalar]()
       71              self._namespaces: t.MutableStrMapping = dict[str, str]()
       72  
       73          def clear_metrics(self, namespace: str | None = None) -> p.Result[bool]:
       74              """Clear metrics from registry.
```

**Decisão**: 

### 12 · ⚪ MINOR · CODE_SMELL · `python:S7498`
**Local**: `src/flext_observability/services/custom_metrics.py:71` · **Effort**: 5min

> Replace this constructor call with a literal.

```python
       67              self._metrics: MutableMapping[
       68                  str, m.Observability.CustomMetricDefinition
       69              ] = {}
       70              self._metric_instances: t.MutableScalarMapping = dict[str, t.Scalar]()
>>>    71              self._namespaces: t.MutableStrMapping = dict[str, str]()
       72  
       73          def clear_metrics(self, namespace: str | None = None) -> p.Result[bool]:
       74              """Clear metrics from registry.
       75  
```

**Decisão**: 

### 13 · ⚪ MINOR · CODE_SMELL · `python:S1940`
**Local**: `src/flext_observability/services/error_handling.py:269` · **Effort**: 2min

> Use the opposite operator (">=") instead.

```python
      265              last_alert = self._last_alert_time.get(error.fingerprint, 0)
      266              if time.time() - last_alert < self._alert_cooldown_sec:
      267                  return False
      268              count = self._error_counts.get(error.fingerprint, 0)
>>>   269              return not count < self._escalation_threshold
      270  
      271          def _run_with_result[TResult](
      272              self, operation: Callable[[], TResult], *, error_prefix: str
      273          ) -> p.Result[TResult]:
```

**Decisão**: 

