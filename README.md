# FLEXT-Observability


<!-- TOC START -->
- [🚀 Key Features](#-key-features)
- [📦 Installation](#-installation)
- [🛠️ Usage](#-usage)
  - [Creating Metrics](#creating-metrics)
  - [Tracing Execution](#tracing-execution)
  - [Automatic Instrumentation](#automatic-instrumentation)
- [🏗️ Architecture](#-architecture)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
<!-- TOC END -->

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**FLEXT-Observability** is the universal monitoring, tracing, and health check library for the FLEXT ecosystem. Built on **OpenTelemetry** and structured logging, it provides a unified layer for capturing performance metrics, distributed traces, and service health status across all FLEXT components.

**Reviewed**: 2026-02-17 | **Version**: 0.10.0-dev

Part of the [FLEXT](https://github.com/flext/flext) ecosystem.

## 🚀 Key Features

- **Unified Monitoring**: Centralized collection of application metrics, logs, and traces.
- **OpenTelemetry Integration**: Standardized metric and trace exports for Prometheus, Jaeger, and other OTLP-compliant backends.
- **Automatic Instrumentation**: Decorators for zero-config monitoring of function execution time and errors.
- **Structured Logging**: JSON-formatted logs with correlation IDs for request traceability.
- **Metric Entities**: Domain models for `FlextMetric`, `FlextTrace`, `FlextAlert`, and `FlextHealthCheck`.
- **Railway-Oriented**: Consistent `FlextResult[T]` responses for observability operations.

## 📦 Installation

To install `flext-observability`:

```bash
pip install flext-observability
```

Or with Poetry:

```bash
poetry add flext-observability
```

## 🛠️ Usage

### Creating Metrics

Capture custom metrics easily.

```python
from flext_observability import flext_create_metric

# 1. Record a Metric
metric_result = flext_create_metric(
    name="api_request_count",
    value=105.0,
    unit="count",
    tags={"endpoint": "/users"}
)

if metric_result.is_success:
    metric = metric_result.unwrap()
    print(f"Captured: {metric.name} = {metric.value}")
```

### Tracing Execution

Trace business transactions across services.

```python
from flext_observability import flext_create_trace

# 1. Start a Trace Span
trace_result = flext_create_trace(
    operation="process_order",
    span_id="span-12345",
    trace_id="trace-abcde"
)

if trace_result.is_success:
    span = trace_result.unwrap()
    print(f"Tracing Span: {span.operation}")
```

### Automatic Instrumentation

Monitor functions with a simple decorator.

```python
from flext_observability import flext_monitor_function

@flext_monitor_function("calculate_tax")
def calculate_tax(amount: float) -> float:
    # Execution time and success/failure automatically recorded
    return amount * 0.2

result = calculate_tax(100.0)
```

## 🏗️ Architecture

FLEXT-Observability integrates deeply with the ecosystem:

- **Domain Layer**: Definitive models for observability data (`FlextMetric`, `FlextTrace`).
- **Application Layer**: Services for managing metric collection and trace propagation.
- **Infrastructure Layer**: Adapters for OpenTelemetry, Prometheus, and logging backends.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development.md) for details on adding new metric types, enhancing tracing support, and submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
