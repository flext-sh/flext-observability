# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLEXT Observability is a foundation library within the FLEXT ecosystem providing monitoring, metrics, tracing, and health check capabilities. Built with Python 3.13+ implementing Clean Architecture patterns, it serves as the centralized observability layer for all FLEXT ecosystem components.

**Current Status**: Core observability patterns are functional but the project has dependency issues preventing normal operations (Poetry/requests import errors).

## Core Architecture

### Key Components

- **FlextObservabilityMasterFactory**: Central factory for creating observability entities
- **FlextMetric, FlextTrace, FlextAlert, FlextHealthCheck**: Core observability domain entities
- **FlextMetricsService, FlextTracingService, FlextAlertService**: Application services with business logic
- **Simple API**: Easy-to-use factory functions (flext_create_metric, flext_create_trace)
- **Monitoring Decorators**: @flext_monitor_function for automatic instrumentation

### Module Organization

- `src/flext_observability/observability_models.py` - Core domain entities
- `src/flext_observability/observability_services.py` - Application services
- `src/flext_observability/observability_factory.py` - Factory patterns
- `src/flext_observability/observability_api.py` - Simple API functions
- `src/flext_observability/observability_monitor.py` - Monitoring decorators

### Dependencies

- **flext-core**: Foundation library (FlextEntity, FlextResult, FlextContainer patterns)
- **OpenTelemetry**: Distributed tracing and metrics collection
- **Prometheus**: Metrics client library
- **Pydantic**: Runtime validation and type safety

## Development Commands

**⚠️ Critical Issue**: All Poetry-based commands currently fail due to requests library import errors. Direct Python execution may work for some operations.

### Essential Commands (Currently Broken)

```bash
# These commands are defined but fail due to dependency issues:
make check                  # Lint + type check (FAILS - Poetry error)
make validate               # Complete validation (FAILS - Poetry error)
make test                   # Run tests with coverage (FAILS - Poetry error)
make lint                   # Ruff linting (FAILS - Poetry error)
make type-check             # MyPy type checking (FAILS - Poetry error)

# Direct alternatives when Poetry is broken:
python -m ruff check src tests               # Direct linting
python -m mypy src --strict                  # Direct type checking
python -m pytest tests/test_simple.py -v    # Direct test execution
```

### Working Commands

```bash
# Information and diagnostics
make help                   # Show available commands
make info                   # Show project information
make clean                  # Clean build artifacts

# Build operations (if Poetry works)
make build                  # Build package
```

### Testing Strategy

When dependency issues are resolved:

```bash
# Test categories available
make test-unit              # Unit tests only
make test-integration       # Integration tests only
make test-fast              # Tests without coverage
make coverage-html          # HTML coverage report

# Direct test execution
python -m pytest tests/test_entities_simple.py -v
python -m pytest tests/test_factory_complete.py -v
python -m pytest tests/test_services_comprehensive.py -v
```

## Architecture Patterns

### Simple API Usage (Primary Interface)

```python
# Basic metric creation
from flext_observability import flext_create_metric, flext_create_trace

metric_result = flext_create_metric("cpu_usage", 85.2, "percent")
trace_result = flext_create_trace("user_request", "processing_order")

# Check results using FlextResult pattern
if metric_result.success:
    print(f"Metric created: {metric_result.data.name}")
```

### Factory Pattern (Advanced Usage)

```python
from flext_observability import get_global_factory, FlextObservabilityMasterFactory
from flext_core import FlextContainer

# Use global factory
factory = get_global_factory()
metric_result = factory.create_metric("memory_usage", 1024, "MB")

# Or create custom factory with dependency injection
container = FlextContainer()
custom_factory = FlextObservabilityMasterFactory(container)
```

### Service Integration

```python
from flext_observability import FlextMetricsService
from flext_core import FlextContainer

# Initialize with dependency injection
container = FlextContainer()
metrics_service = FlextMetricsService(container)

# All operations return FlextResult
result = metrics_service.record_metric(metric)
if result.success:
    print(f"Recorded: {result.data.name}")
```

### Monitoring Decorators

```python
from flext_observability import flext_monitor_function

@flext_monitor_function("data_processing")
def process_data(data):
    # Automatically monitored with execution metrics and tracing
    return processed_data
```

## Testing Organization

The test suite is organized in `/tests/` with comprehensive coverage:

- **Test Files**: Multiple test files covering entities, services, factories, and API functions
- **Coverage Target**: 90% minimum coverage (when tests can run)
- **Test Fixtures**: `conftest.py` provides OpenTelemetry and Prometheus setup
- **Test Types**: Unit tests for individual components, integration tests for service interactions

### Key Test Files

- `test_entities_simple.py` - Core entity validation
- `test_services_comprehensive.py` - Service layer business logic
- `test_factory_complete.py` - Factory pattern verification
- `test_flext_simple.py` - Simple API functionality
- `test_true_100_coverage.py` - Comprehensive coverage validation

## Quality Standards

- **Type Safety**: Python 3.13 with strict MyPy configuration
- **Linting**: Ruff with comprehensive rule sets
- **Security**: Bandit security scanning
- **Validation**: Pydantic models for runtime type checking

## FLEXT Ecosystem Integration

### Role in Architecture

This library provides observability foundation for all FLEXT ecosystem components:

- **Services**: FlexCore (Go), FLEXT Service (Python), web interfaces
- **Infrastructure**: Oracle, LDAP, gRPC, monitoring integration
- **Singer Ecosystem**: Taps, targets, and DBT transformers monitoring

### Integration Patterns

```python
# Basic integration in FLEXT services
from flext_observability import flext_create_metric, flext_monitor_function

@flext_monitor_function("service_operation")
def service_function():
    # Automatically instrumented
    result = do_work()
    flext_create_metric("operation_count", 1, "count")
    return result
```

## Known Issues & Troubleshooting

### Critical Dependency Issue

**Issue**: Poetry and pytest fail with requests library import errors
**Impact**: All Poetry-based commands (make check, make test, etc.) are currently broken
**Workaround**: Use direct Python execution when possible

### Monitoring Stack Integration

The Makefile includes monitoring stack commands but implementation is incomplete:

- `make setup-prometheus`, `make setup-grafana` - Show placeholder messages
- `make start-monitoring` - Requires `docker-compose.monitoring.yml` (not exists)
- Monitoring stack integration needs to be implemented

### Architecture Gaps

1. **Cross-Service Tracing**: Distributed tracing between Go and Python services not implemented
2. **Metrics Standardization**: Ecosystem-wide metric naming conventions not defined
3. **Monitoring Integration**: Full monitoring stack not integrated with FLEXT workspace

### Development Notes

- Core observability patterns are functional when dependencies work
- Test coverage is comprehensive when tests can execute
- Focus on fixing dependency issues before major feature development
- Consider using direct tool execution until Poetry issues resolved
