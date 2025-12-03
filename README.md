# flext-observability

**Type**: Foundation Library | **Status**: Architecture Complete, Quality Validation Blocked | **Dependencies**: flext-core

Observability foundation library providing monitoring, metrics, tracing, and health check patterns for the FLEXT ecosystem.

> **⚠️ Development Status**: Complete observability architecture implemented, currently blocked by flext-core import compatibility issues

## Quick Start

```bash
# Install dependencies
poetry install

# Test basic functionality
python -c "from flext_observability import flext_create_metric; result = flext_create_metric('test', 42.0, 'units'); print('✅ Working')"

# Development setup
make setup
```

## Current Reality

**What Actually Works:**

- Complete domain entities (FlextMetric, FlextTrace, FlextAlert, FlextHealthCheck, FlextLogEntry) with Pydantic v2 validation
- Full service layer with dependency injection and FlextResult[T] railway patterns
- Simple API factory functions (flext*create*\*) for easy integration
- Monitoring decorators (@flext_monitor_function) for automatic instrumentation
- Clean Architecture implementation (Domain → Application → Infrastructure)
- Comprehensive test suite (481 functions across 40 files)

**Critical Blocker:**

- **Import Compatibility**: Currently blocked by flext-core T export issue
- All tests fail (33 collection errors) due to import failures
- Quality validation (type checking, coverage) cannot execute

**Next Steps (Post-Import Fix):**

- Monitoring stack integration (Prometheus, Grafana, Jaeger)
- Cross-service correlation ID propagation
- Distributed tracing between Go/Python services
- Metrics standardization across ecosystem

## Architecture Role in FLEXT Ecosystem

### **Foundation Component**

FLEXT Observability provides observability patterns for all ecosystem services:

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLEXT ECOSYSTEM (32 Projects)                 │
├─────────────────────────────────────────────────────────────────┤
│ Services: FlexCore(Go) | FLEXT Service(Go/Python) | Clients     │
├─────────────────────────────────────────────────────────────────┤
│ Applications: API | Auth | Web | CLI | Quality | Observability  │
├─────────────────────────────────────────────────────────────────┤
│ Infrastructure: Oracle | LDAP | LDIF | gRPC | Plugin | WMS      │
├─────────────────────────────────────────────────────────────────┤
│ Singer Ecosystem: Taps(5) | Targets(5) | DBT(4) | Extensions(1) │
├═════════════════════════════════════════════════════════════════┤
│ Foundation: FLEXT-CORE | [FLEXT-OBSERVABILITY] (Monitoring)     │
└─────────────────────────────────────────────────────────────────┘
```

### **Core Responsibilities**

1. **Observability Entities**: Domain models for metrics, traces, alerts, health checks
2. **Monitoring Services**: Type-safe services with FlextResult error handling
3. **Instrumentation**: Decorators and utilities for automatic monitoring

## Key Features

### **Current Capabilities**

- **Domain Entities**: FlextMetric, FlextTrace, FlextAlert, FlextHealthCheck with validation
- **Service Layer**: Enterprise-grade observability services with dependency injection
- **Simple API**: Easy-to-use factory functions (flext_create_metric, flext_create_trace)
- **Monitoring Decorators**: Function decorators for automatic instrumentation

### **FLEXT Core Integration**

- **FlextResult Pattern**: Type-safe error handling for all operations
- **FlextModels.Entity**: Domain entities with business logic validation
- **FlextContainer**: Dependency injection for service management

## Installation & Usage

### Installation

```bash
# Clone and install
cd /path/to/flext-observability
poetry install

# Development setup
make setup
```

### Basic Usage

```python
from flext_observability import flext_create_metric, flext_create_trace, flext_monitor_function

# Create metrics
metric_result = flext_create_metric("cpu_usage", 85.2, "percent")
if metric_result.success:
    print(f"Metric created: {metric_result.data.name}")

# Create traces
trace_result = flext_create_trace("user_request", "processing_order")

# Monitor functions automatically
@flext_monitor_function("data_processing")
def process_data(data):
    # Function automatically monitored for:
    # - Execution time metrics
    # - Success/failure traces
    # - Structured logging
    return processed_data
```

## Development Commands

### Quality Gates (Zero Tolerance)

```bash
# Complete validation pipeline (run before commits)
make validate              # Full validation (lint + type + security + test)
make check                 # Quick lint + type check + test
make test                  # Run all tests (90% coverage requirement)
make lint                  # Code linting
make type-check
make format                # Code formatting
make security              # Security scanning
```

### Testing

```bash
# Test categories
make test-unit             # Unit tests only
make test-integration      # Integration tests only
make test-monitoring       # Monitoring-specific tests
make coverage-html         # Generate HTML coverage report
```

## Configuration

### Environment Variables

```bash
# OpenTelemetry settings
export OTEL_SERVICE_NAME=flext-service
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus settings
export PROMETHEUS_ENDPOINT=http://localhost:9090
export PROMETHEUS_PUSH_GATEWAY=http://localhost:9091
```

## Quality Standards

### **Quality Targets**

- **Coverage**: 100% requirement (currently blocked by import issues)
- **Type Safety**: Pyrefly strict mode (currently blocked by import issues)
- **Linting**: Ruff with comprehensive rules (currently unverified)
- **Security**: Bandit + pip-audit scanning (currently blocked)

### **Current Quality Status**

- **Test Functions**: 481 ready (cannot execute due to imports)
- **Test Files**: 40 comprehensive test files prepared
- **Collection Errors**: 33 import failures preventing execution
- **Type Annotations**: Complete Python 3.13+ coverage implemented
- **Architecture**: Clean Architecture fully implemented

## Integration with FLEXT Ecosystem

### **FLEXT Core Patterns**

```python
# FlextResult for all operations
from flext_observability import FlextMetricsService
from flext_core import FlextBus
from flext_core import FlextConfig
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import FlextDecorators
from flext_core import FlextDispatcher
from flext_core import FlextExceptions
from flext_core import h
from flext_core import FlextLogger
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import FlextResult
from flext_core import FlextRuntime
from flext_core import FlextService
from flext_core import t
from flext_core import u

container = FlextContainer()
metrics_service = FlextMetricsService(container)

result = metrics_service.record_metric(metric)
if result.success:
    print(f"Recorded: {result.data.name}")
else:
    print(f"Error: {result.error}")
```

### **Service Integration**

- **All FLEXT Services**: Provides observability patterns for entire ecosystem
- **OpenTelemetry**: Distributed tracing and metrics collection
- **Prometheus**: Metrics storage and alerting
- **Structured Logging**: JSON-structured logging with correlation IDs

## Current Status

**Version**: 0.9.0 (Architecture Complete)

**Completed**:

- ✅ Domain entities with Pydantic v2 validation and business logic
- ✅ Service layer with dependency injection and FlextResult[T] patterns
- ✅ Simple API factory functions (flext*create*\*)
- ✅ Monitoring decorators (@flext_monitor_function)
- ✅ Clean Architecture implementation (Domain → Application → Infrastructure)
- ✅ Comprehensive test suite (481 functions across 40 files)

**Blocked**:

- ❌ **Import Compatibility**: flext-core T export issue blocks all validation
- ❌ **Test Execution**: 33 collection errors prevent test running
- ❌ **Quality Gates**: Cannot verify coverage, type safety, or linting

**Next Steps (Post-Import Fix)**:

- 🔄 Monitoring stack integration (Prometheus, Grafana, Jaeger)
- 🔄 Cross-service correlation ID propagation
- 🔄 Distributed tracing between Go/Python services
- 📋 Ecosystem-wide metrics standardization
- 📋 SLA/SLO tracking and alerting
- 📋 Auto-generated dashboards for services

## Contributing

### Development Standards

- **FLEXT Core Integration**: Use established patterns
- **Type Safety**: All code must pass MyPy
- **Testing**: Maintain 90%+ coverage
- **Code Quality**: Follow linting rules

### Development Workflow

```bash
# Setup and validate
make setup
make validate
make test
```

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Links

- **[flext-core](../flext-core)**: Foundation library
- **[CLAUDE.md](CLAUDE.md)**: Development guidance
- **[Documentation](docs/)**: Complete documentation

---
