# FLEXT Observability Package

**Core observability implementation providing monitoring, metrics, tracing, and health check capabilities for the FLEXT ecosystem.**

This package implements Clean Architecture and Domain-Driven Design patterns specifically for observability concerns, delivering monitoring solutions that integrate seamlessly across all 33 FLEXT ecosystem projects.

## Package Architecture

### Domain Layer

Core business entities with domain validation and business logic:

#### [models.py](models.py) - Domain Models (FlextObservabilityModels)

- **FlextMetric**: Metrics collection entity with domain validation
- **FlextTrace**: Distributed tracing span entity with context propagation
- **FlextAlert**: Alert management entity with severity handling
- **FlextHealthCheck**: Health monitoring entity with dependency validation
- **FlextLogEntry**: Structured logging entity with correlation ID support
- **u.Generators**: Utility functions for ID generation and timestamps

### Application Layer

Business logic and service coordination:

#### [services.py](services.py) - Application Services

- **FlextMetricsService**: Metrics collection, validation, and export
- **FlextTracingService**: Distributed tracing coordination
- **FlextAlertService**: Alert processing and routing
- **FlextHealthService**: Health check coordination and reporting
- **FlextLoggingService**: Structured logging management

#### [obs_platform.py](obs_platform.py) - Platform Orchestration

- **FlextObservabilityPlatformV2**: Central platform coordinating all services

### Interface Adapters Layer

External interfaces and API adaptations:

#### [factory.py](factory.py) - Factory Patterns

- **FlextObservabilityMasterFactory**: Central entity creation with validation

#### [flext_simple.py](flext_simple.py) - Simple API

- **flext_create_metric()**: Easy metric creation
- **flext_create_trace()**: Simple trace creation
- **flext_create_alert()**: Alert creation interface
- **flext_create_health_check()**: Health check creation
- **flext_create_log_entry()**: Log entry creation

#### [flext_monitor.py](flext_monitor.py) - Monitoring Decorators

- **@flext_monitor_function**: Automatic function monitoring
- **FlextObservabilityMonitor**: Advanced monitoring coordination

#### [flext_structured.py](flext_structured.py) - Structured Logging

- **FlextStructuredLogger**: JSON structured logging
- **Correlation ID management**: Context-local correlation tracking

### Infrastructure Layer

Supporting utilities and cross-cutting concerns:

#### [repos.py](repos.py) - Repository Patterns

- **FlextObservabilityRepository**: Data access patterns (in-memory)

#### [health.py](health.py) - Health Utilities

- **HealthChecker**: Basic health check coordination

#### [metrics.py](metrics.py) - Metrics Utilities

- **MetricsCollector**: Utility metrics collection patterns

#### [flext_metrics.py](flext_metrics.py) - Advanced Metrics

- **FlextMetricsCollector**: Advanced metrics collection with type safety

### Foundation Layer

Base patterns and cross-cutting concerns:

#### [validation.py](validation.py) - Domain Validation

- **create_observability_result_error()**: Standardized error creation
- Domain validation utilities and patterns

#### [constants.py](constants.py) - Domain Constants

- Health check thresholds and system limits
- Metrics collection configuration defaults

#### [exceptions.py](exceptions.py) - Domain Exceptions

- Observability-specific exception types and error handling

## Usage Examples

### Basic Entity Creation

```python
from flext_observability import FlextMetric, FlextTrace

# Create metric with validation
metric = FlextMetric(
    name="api_response_time",
    value=150.5,
    unit="milliseconds",
    tags={"service": "user-api"}
)

validation = metric.validate_business_rules()
if validation.success:
    print(f"Valid metric: {metric.name}")
```

### Service Layer Usage

```python
from flext_observability.services import FlextMetricsService
from flext_core import FlextBus
from flext_core import FlextSettings
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
```

### Factory Pattern Usage

```python
from flext_observability.factory import FlextObservabilityMasterFactory

factory = FlextObservabilityMasterFactory()
metric_result = factory.create_metric("cpu_usage", 75.2, "percent")

if metric_result.success:
    metric = metric_result.data
    print(f"Created metric: {metric.name}")
```

### Simple API Usage

```python
from flext_observability.flext_simple import flext_create_metric, flext_create_trace

# Quick metric creation
metric_result = flext_create_metric("requests_total", 1, "count")

# Quick trace creation
trace_result = flext_create_trace("user_login", "auth-service")
```

### Monitoring Decorator Usage

```python
from flext_observability.flext_monitor import flext_monitor_function

@flext_monitor_function("order_processing")
def process_order(order_data: dict) -> dict[str, object]:
    # Automatically monitored for execution time, success/failure
    return {"status": "processed", "order_id": order_data["id"]}
```

## Integration Patterns

### FLEXT Ecosystem Integration

All modules follow FLEXT ecosystem standards:

- **FlextResult[T]** for railway-oriented programming
- **FlextContainer** for dependency injection
- **FlextModels.Entity** base patterns for domain entities
- **Type safety** with comprehensive annotations

### Cross-Service Observability

```python
# Consistent observability across services
@flext_monitor_function("api_endpoint")
def handle_user_request(request: dict) -> FlextResult[t.Dict]:
    # Automatic metrics, tracing, and logging
    return FlextResult[bool].ok({"status": "processed"})
```

## Quality Standards

All modules in this package maintain:

- **100% Type Coverage**: Complete type annotations
- **95% Test Coverage**: Comprehensive test suites
- **Domain Validation**: Business rule enforcement
- **Error Handling**: FlextResult patterns throughout
- **Documentation**: Enterprise-grade docstrings

## Development Guidelines

1. **Follow Clean Architecture**: Maintain clear layer separation
2. **Use FlextResult**: All operations return FlextResult[T]
3. **Domain Validation**: Implement validate_business_rules() for entities
4. **Type Safety**: Complete type annotations required
5. **Test Coverage**: 95% minimum coverage for all new code

---

**For detailed module documentation, see individual module files with comprehensive docstrings and usage examples.**
