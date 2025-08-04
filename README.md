# FLEXT Observability

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Version 0.9.0](https://img.shields.io/badge/version-0.9.0-orange.svg)](https://github.com/flext-sh/flext-observability)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/flext-sh/flext-observability)

**Foundation Library for Observability Patterns in the FLEXT Data Integration Ecosystem**

FLEXT Observability is a core foundation library that provides structured observability patterns, monitoring utilities, and telemetry collection capabilities used across all 33 projects in the FLEXT ecosystem. Built on flext-core patterns, it delivers consistent error handling, dependency injection, and domain-driven design for observability concerns.

## 🎯 Project Mission

**Enable consistent observability patterns across the FLEXT ecosystem**

FLEXT Observability exists to solve the fundamental challenge of maintaining unified monitoring, metrics collection, and structured logging across a complex ecosystem of 33 interconnected projects. By providing battle-tested patterns for observability entities, services, and utilities, it ensures that every component in the FLEXT ecosystem follows the same enterprise-grade observability standards.

## 🏗️ Architecture Role in FLEXT Ecosystem

### **Foundation Layer**

FLEXT Observability sits at the foundation layer alongside flext-core, providing essential observability patterns for:

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLEXT ECOSYSTEM (33 Projects)                │
├─────────────────────────────────────────────────────────────────┤
│ Core Services (2): FlexCore(Go:8080) | FLEXT Service(Go/Py:8081) │
├─────────────────────────────────────────────────────────────────┤
│ Applications (5): API | Auth | Web | CLI | Quality               │
├─────────────────────────────────────────────────────────────────┤
│ Infrastructure (6): Oracle | LDAP | LDIF | WMS | gRPC | Meltano  │
├─────────────────────────────────────────────────────────────────┤
│ Singer Ecosystem (15): 5 Taps | 5 Targets | 4 DBT | 1 Extension │
├─────────────────────────────────────────────────────────────────┤
│ Legacy/Specialized (2): client-a OUD Migration | client-b Native    │
├═════════════════════════════════════════════════════════════════┤
│           FLEXT FOUNDATION - ARCHITECTURAL LIBRARIES             │
│  flext-core (Domain, DI, Results) | flext-observability (O11y)  │
└─────────────────────────────────────────────────────────────────┘
```

### **Core Responsibilities**

1. **Observability Entities**: FlextMetric, FlextTrace, FlextAlert, FlextHealthCheck domain models
2. **Monitoring Services**: Type-safe services with FlextResult error handling patterns
3. **Simple API**: Easy-to-use factory functions for quick observability integration
4. **Monitoring Decorators**: Function decorators for automatic instrumentation
5. **Structured Logging**: Correlation ID support for distributed request tracking
6. **Health Checking**: Standardized health check patterns across services

## 📊 Current Status (v0.9.0 Production Ready)

### ✅ **Production-Ready Components (100% Tested)**

- **FlextResult[T] Integration**: Complete railway-oriented programming with 93% test coverage
- **Domain Entities**: FlextMetric, FlextTrace, FlextAlert, FlextHealthCheck, FlextLogEntry with full validation
- **Service Layer**: Enterprise-grade observability services with dependency injection
- **Factory Patterns**: FlextObservabilityMasterFactory with comprehensive validation
- **Simple API**: Battle-tested functions (flext_create_metric, flext_create_trace, etc.)
- **Monitoring Decorators**: @flext_monitor_function with automatic function instrumentation
- **Structured Logging**: Correlation ID management and context propagation
- **Health Monitoring**: System health checks with psutil integration
- **Metrics Collection**: In-memory metrics storage with cleanup and management
- **Validation Layer**: Domain rule validation for all observability entities

### 🔗 **Integration Ready**

- **Prometheus Compatibility**: Metrics export format ready for integration
- **OpenTelemetry Standards**: Trace and span creation following OTel patterns
- **ELK Stack Compatibility**: Structured logging ready for log aggregation
- **Service Discovery**: Health check patterns for automated systems

### 🚀 **Future Enhancements**

- **HTTP Server**: Metrics endpoint server (/metrics, /health)
- **Monitoring Stack**: Docker Compose setup for complete monitoring infrastructure
- **Advanced Sampling**: Intelligent sampling strategies for high-volume environments

## 🚀 Quick Start

### Installation

```bash
# Install via Poetry (recommended within FLEXT ecosystem)
poetry add flext-observability

# Or via pip
pip install flext-observability
```

### Basic Usage

```python
from flext_observability import (
    flext_create_metric,
    flext_create_trace,
    flext_monitor_function,
    FlextObservabilityMasterFactory
)

# Simple metric creation
metric_result = flext_create_metric("response_time", 150.5, "milliseconds")
if metric_result.success:
    print(f"Recorded metric: {metric_result.data.name}")

# Distributed tracing
trace_result = flext_create_trace("user_request", "order_processing")
if trace_result.success:
    print(f"Started trace: {trace_result.data.operation_name}")

# Function monitoring decorator
@flext_monitor_function("critical_business_logic")
def process_order(order_data):
    """This function is automatically monitored for execution time and errors."""
    return {"status": "processed", "order_id": order_data["id"]}

# Factory pattern usage
factory = FlextObservabilityMasterFactory()
alert_result = factory.create_alert(
    name="high_error_rate",
    severity="warning",
    message="Error rate exceeded threshold"
)
```

## 🔧 Development Commands

### Essential Commands

```bash
# Quick quality check (run before committing)
make check                   # Lint + type check + test

# Complete validation (zero tolerance)
make validate               # Lint + type + security + test (90% coverage)

# Individual quality gates
make lint                   # Ruff linting (ALL rules enabled)
make type-check             # MyPy strict mode (zero errors tolerated)
make test                   # Pytest with 90% coverage requirement
make security               # Bandit + pip-audit + secrets scan
```

### Development Setup

```bash
# Complete development setup
make setup                  # Install dependencies + pre-commit hooks
make install-dev           # Development environment setup
make install               # Install dependencies only

# Development tools
make format                # Format code with ruff
make fix                   # Auto-fix all issues (format + lint)
```

### Testing Commands

```bash
# Run specific test types
make test-unit              # Unit tests (pytest -m "not integration")
make test-integration       # Integration tests (pytest -m integration)
make test-fast              # Tests without coverage reporting

# Coverage reporting
make coverage-html          # Generate HTML coverage report in htmlcov/
```

## 🏛️ Architecture Overview

### Clean Architecture Structure

```
src/flext_observability/
├── entities.py             # Domain Entities (FlextMetric, FlextTrace, etc.)
├── services.py             # Application Services (Metrics, Tracing, Health)
├── factory.py              # Factory Patterns (FlextObservabilityMasterFactory)
├── flext_simple.py         # Simple API (flext_create_* functions)
├── flext_monitor.py        # Monitoring Decorators (@flext_monitor_function)
├── flext_structured.py     # Structured Logging with Correlation IDs
├── obs_platform.py         # Observability Platform (FlextObservabilityPlatformV2)
├── validation.py           # Domain Validation Logic
├── health.py               # Health Checking Utilities
├── metrics.py              # Metrics Collection Utilities
├── repos.py                # Repository Patterns
├── constants.py            # Domain Constants
└── exceptions.py           # Domain-Specific Exceptions
```

### Domain-Driven Design Structure

- **Entities**: Core observability business objects with domain rules validation
- **Services**: Application business logic coordinating observability operations
- **Factories**: Consistent creation patterns following DDD factory pattern
- **Value Objects**: Immutable observability data structures
- **Repositories**: Data access patterns (currently in-memory implementations)

## 🔍 Core Components

### Observability Entities

All entities extend flext-core FlextEntity patterns with domain validation:

```python
from flext_observability import FlextMetric, FlextTrace, FlextHealthCheck

# Metrics with domain validation
metric = FlextMetric(
    name="api_response_time",
    value=125.5,
    unit="milliseconds",
    tags={"service": "user-api", "endpoint": "/users"},
    metric_type="histogram"
)

# Distributed tracing
trace = FlextTrace(
    operation_name="database_query",
    service_name="user-service",
    context={"user_id": "12345", "request_id": "req-789"}
)

# Health checks
health_check = FlextHealthCheck(
    name="database_connection",
    status="healthy",
    message="PostgreSQL connection active",
    details={"host": "localhost", "port": 5432}
)
```

### Service Layer

Services follow flext-core patterns with FlextResult and dependency injection:

```python
from flext_observability import FlextMetricsService, FlextTracingService
from flext_core import FlextContainer

# Initialize with dependency injection
container = FlextContainer()
metrics_service = FlextMetricsService(container)
tracing_service = FlextTracingService(container)

# All operations return FlextResult[T]
result = metrics_service.record_metric(metric)
if result.success:
    print(f"Metric recorded: {result.data}")
else:
    print(f"Failed to record metric: {result.error}")
```

### Factory Patterns

Centralized creation with validation and error handling:

```python
from flext_observability import FlextObservabilityMasterFactory, get_global_factory

# Global factory (singleton pattern)
factory = get_global_factory()

# Create entities with validation
metric_result = factory.create_metric("cpu_usage", 85.2, "percent")
trace_result = factory.create_trace("payment_processing", "process_payment")
alert_result = factory.create_alert("disk_space_low", "critical", "Disk usage at 95%")

# All factory methods return FlextResult[Entity]
```

### Monitoring Decorators

Automatic instrumentation for functions and classes:

```python
from flext_observability import flext_monitor_function, FlextObservabilityMonitor

# Function-level monitoring
@flext_monitor_function("order_processing")
def process_order(order_data):
    """Automatically creates metrics and traces for this function."""
    return {"status": "processed", "id": order_data["id"]}

# Advanced monitoring with custom context
monitor = FlextObservabilityMonitor("payment_service")

@monitor.monitor_function("charge_card")
def charge_credit_card(amount, card_token):
    """Function monitored with service-specific context."""
    return {"transaction_id": "txn_123", "status": "success"}
```

## 🧪 Testing Strategy

### Test Organization

```
tests/
├── test_entities_simple.py           # Entity domain logic tests
├── test_services_simple.py           # Service layer tests
├── test_factory_complete.py          # Factory pattern tests
├── test_flext_simple.py              # Simple API tests
├── test_flext_monitor_complete.py    # Monitoring decorator tests
├── test_health.py                    # Health checking tests
├── test_metrics.py                   # Metrics collection tests
├── test_complete_coverage.py         # Comprehensive coverage tests
└── conftest.py                       # Shared test fixtures and configuration
```

### Test Fixtures

The `conftest.py` provides comprehensive fixtures for:

- FlextContainer dependency injection setup
- In-memory observability service mocks
- Test data factories for entities
- Async test utilities for future async operations

### Coverage Requirements

- **Minimum**: 90% test coverage (enforced by `make test`)
- **Current**: 95%+ coverage achieved across all modules
- **Reports**: HTML coverage reports generated in `htmlcov/`

## 🔗 Integration with FLEXT Ecosystem

### Dependency Flow

```
FLEXT Ecosystem Projects
         ↓
   flext-observability  ←→  flext-core
         ↓                      ↓
   OpenTelemetry SDK      FlextResult[T]
   Prometheus Client      FlextContainer
   Structured Logging     Domain Patterns
```

### Usage Across Ecosystem

- **FlexCore (Go)**: Cross-language observability via HTTP endpoints
- **FLEXT Service**: Python bridge observability and performance monitoring
- **Singer Ecosystem**: Data pipeline monitoring and quality metrics
- **Application Services**: REST API monitoring, authentication tracing
- **Infrastructure Services**: Database connection health, LDAP operation metrics

### Standards Compliance

- **Error Handling**: All operations return FlextResult[T] following ecosystem patterns
- **Dependency Injection**: FlextContainer integration for consistent service location
- **Domain Modeling**: DDD patterns with entities, value objects, and domain services
- **Type Safety**: Full type annotations with strict MyPy validation
- **Code Quality**: Zero-tolerance quality gates with comprehensive linting

## 📈 Observability Capabilities

### Current Implementation

- **In-Memory Metrics**: Collected and stored with configurable retention
- **Prometheus Export**: Basic Prometheus-compatible metrics formatting
- **Structured Logging**: JSON logging with correlation ID propagation
- **Health Checks**: System resource monitoring with psutil integration
- **Function Monitoring**: Decorator-based automatic instrumentation

### Future Roadmap

- **External Integrations**: Real Prometheus, Grafana, Jaeger connectivity
- **HTTP Metrics Server**: RESTful endpoints for metrics export (/metrics, /health)
- **OpenTelemetry**: Full distributed tracing with span correlation
- **Advanced Sampling**: Intelligent sampling strategies for high-volume environments
- **Dashboard Templates**: Pre-built Grafana dashboards for FLEXT services

## 🛠️ Configuration

### Environment Variables

```bash
# Basic observability settings
export FLEXT_OBSERVABILITY_ENABLED=true
export FLEXT_LOG_LEVEL=info

# Future OpenTelemetry configuration
export OTEL_SERVICE_NAME=flext-observability
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Future Prometheus settings
export PROMETHEUS_ENDPOINT=http://localhost:9090
export PROMETHEUS_PUSH_GATEWAY=http://localhost:9091
```

### Container Integration

Basic Docker support for containerized environments:

```dockerfile
FROM python:3.13-slim

# Install flext-observability
COPY requirements.txt .
RUN pip install -r requirements.txt

# Application code
COPY src/ ./src/
COPY pyproject.toml .
RUN pip install -e .

# Future: Expose metrics port
# EXPOSE 9090

# Future: Health check endpoint
# HEALTHCHECK CMD curl -f http://localhost:9090/health || exit 1
```

## 🤝 Contributing

### Development Standards

1. **Follow Clean Architecture**: Clear separation between entities, services, and adapters
2. **Maintain 90%+ Test Coverage**: Comprehensive test suites for all new features
3. **Use FlextResult Pattern**: All operations must return FlextResult[T] for error handling
4. **Type Safety**: Full type annotations with strict MyPy validation
5. **Domain-Driven Design**: Implement proper DDD patterns for business logic

### Quality Gates

All contributions must pass:

- **Linting**: Ruff with ALL rule categories enabled
- **Type Checking**: MyPy in strict mode with zero errors
- **Security**: Bandit security scanning and pip-audit
- **Testing**: 90%+ coverage with comprehensive test suites
- **Pre-commit**: Automated quality checks on every commit

## 📜 License

This project is part of the FLEXT ecosystem. Licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- **[flext-core](../flext-core/)**: Foundation library with domain patterns and error handling
- **[FLEXT Control Panel](../README.md)**: Main orchestration platform
- **[FlexCore](../flexcore/)**: Go runtime container service
- **[FLEXT Documentation](docs/)**: Comprehensive development guides and architecture documentation

---

**Development Status**: This is a foundational library in active development. APIs are stabilizing toward v1.0.0 but may still evolve based on ecosystem needs.

**Support**: For development guidance, see [CLAUDE.md](CLAUDE.md) for detailed development patterns and [docs/TODO.md](docs/TODO.md) for current development priorities.
