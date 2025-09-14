# FLEXT Observability - Source Code

**Foundation library source code implementing observability patterns for the FLEXT ecosystem.**

This directory contains the complete implementation of FLEXT Observability, organized following Clean Architecture and Domain-Driven Design principles. All modules implement observability patterns with type safety, domain validation, and railway-oriented programming error handling.

## Module Organization

### [flext_observability/](flext_observability/) - Core Package

Complete observability implementation with layered architecture:

- **Domain Layer**: Core entities and business logic
- **Application Layer**: Services and business operations
- **Interface Layer**: APIs and external adapters
- **Infrastructure Layer**: Utilities and cross-cutting concerns

## Architecture Overview

```
src/flext_observability/
├── entities.py              # Domain entities (FlextMetric, FlextTrace, etc.)
├── services.py              # Application services (business logic)
├── factory.py               # Factory patterns for entity creation
├── flext_simple.py
├── flext_monitor.py         # Monitoring decorators and utilities
├── obs_platform.py          # Platform orchestration services
├── validation.py            # Domain validation logic
├── repos.py                 # Repository patterns
├── health.py                # Health check utilities
├── metrics.py               # Metrics collection utilities
├── flext_metrics.py         # Advanced metrics patterns
├── flext_structured.py      # Structured logging coordination
├── constants.py             # Domain constants
└── exceptions.py            # Domain-specific exceptions
```

## Key Design Principles

1. **Clean Architecture**: Clear separation between domain, application, and infrastructure layers
2. **Domain-Driven Design**: Rich domain models with business logic encapsulation
3. **Railway-Oriented Programming**: FlextResult[T] patterns throughout
4. **Type Safety**: MyPy strict mode adoption; aiming for complete annotations
5. **Enterprise Standards**: Professional code quality and documentation

## Integration Points

- **flext-core**: Foundation patterns (FlextModels.Entity, FlextResult, FlextContainer)
- **OpenTelemetry**: Industry-standard telemetry (future integration)
- **Prometheus**: Metrics export and collection compatibility
- **Structured Logging**: JSON logging with correlation ID support

## Development Standards

- **100% Type Coverage**: All public APIs fully typed
- **95% Test Coverage**: Comprehensive test suites
- **Zero Tolerance Quality**: All quality gates must pass
- **Documentation Standards**: Enterprise-grade docstrings
- **Railway-Oriented**: All operations return FlextResult[T]

## Usage Patterns

```python
# Import core observability functionality
from flext_observability import (
    flext_create_metric,
    flext_create_trace,
    flext_monitor_function,
    FlextMetricsService
)

# Create observability data
metric_result = flext_create_metric("api_requests", 42, "count")
trace_result = flext_create_trace("user_login", "auth-service")

# Use monitoring decorators
@flext_monitor_function("business_operation")
def process_order(order_data: dict) -> dict:
    return {"status": "processed"}
```

## Quality Assurance

All source code passes:

- **Ruff linting** with ALL rules enabled
- **MyPy type checking** in strict mode
- **Bandit security scanning**
- **95% test coverage** minimum
- **Documentation standards** compliance

---

**Next Steps**: Explore the [flext_observability/](flext_observability/) package for detailed module documentation and implementation patterns.
