# Simple API Reference

## Table of Contents

- [Simple API Reference](#simple-api-reference)
  - [📋 API Overview](#-api-overview)
  - [🔍 Core Functions](#-core-functions)
    - [`flext_create_metric()`](#flext_create_metric)
      - [Parameters](#parameters)
      - [Returns](#returns)
      - [Examples](#examples)
- [Basic metric](#basic-metric)
- [Business metric with tags](#business-metric-with-tags)
- [High-precision financial metric](#high-precision-financial-metric) - [Error Scenarios](#error-scenarios)
- [Invalid metric name](#invalid-metric-name)
- [Invalid value type](#invalid-value-type)
  - [`flext_create_trace()`](#flext_create_trace)
    - [Parameters](#parameters)
    - [Returns](#returns)
    - [Examples](#examples)
- [Basic trace](#basic-trace)
- [Trace with context](#trace-with-context)
- [Child trace with parent correlation](#child-trace-with-parent-correlation)
  - [`flext_create_alert()`](#flext_create_alert)
    - [Parameters](#parameters)
    - [Returns](#returns)
    - [Examples](#examples)
- [Basic alert](#basic-alert)
- [Alert with detailed context](#alert-with-detailed-context)
- [Business logic alert](#business-logic-alert)
  - [`flext_create_health_check()`](#flext_create_health_check)
    - [Parameters](#parameters)
    - [Returns](#returns)
    - [Examples](#examples)
- [Basic health check](#basic-health-check)
- [Unhealthy service check](#unhealthy-service-check)
- [Degraded performance check](#degraded-performance-check)
  - [`flext_create_log_entry()`](#flext_create_log_entry)
    - [Parameters](#parameters)
    - [Returns](#returns)
    - [Examples](#examples)
- [Basic log entry](#basic-log-entry)
- [Log with context](#log-with-context)
- [Correlated log entry](#correlated-log-entry)
  - [🔄 Common Usage Patterns](#-common-usage-patterns)
    - [Pattern 1: Error Handling with Railway-Oriented Programming](#pattern-1-error-handling-with-railway-oriented-programming)
    - [Pattern 2: Batch Observability Creation](#pattern-2-batch-observability-creation)
    - [Pattern 3: Observability Context Propagation](#pattern-3-observability-context-propagation)
  - [🚨 Error Reference](#-error-reference)
    - [Common Validation Errors](#common-validation-errors)
    - [Type Safety Errors](#type-safety-errors)
- [❌ MyPy will catch these type errors](#-mypy-will-catch-these-type-errors)
- [✅ Correct usage](#-correct-usage)
  - [🔗 Related APIs](#-related-apis)

**Quick-Start Functions for FLEXT Observability Integration**

The Simple API provides the fastest way to integrate observability into FLEXT ecosystem projects. These functions offer a streamlined interface for creating observability entities with automatic validation and FlextResult error handling.

## 📋 API Overview

All Simple API functions follow consistent patterns:

- **Return Type**: `FlextResult[Entity]` for railway-oriented programming
- **Error Handling**: Domain validation with descriptive error messages
- **Type Safety**: Full type annotations with MyPy compatibility
- **Zero Dependencies**: No external configuration required

## 🔍 Core Functions

### `flext_create_metric()`

Create metrics for performance monitoring and business intelligence.

```python
def flext_create_metric(
    name: str,
    value: float | Decimal,
    unit: str = "",
    tags: t.StringDict | None = None,
    metric_type: str = "gauge"
) -> FlextResult[FlextMetric]
```

#### Parameters

- **`name`** (str, required): Metric identifier following naming conventions
- **`value`** (float | Decimal, required): Numeric measurement value
- **`unit`** (str, optional): Unit of measurement (e.g., "seconds", "bytes", "count")
- **`tags`** (t.StringDict, optional): Key-value pairs for metric categorization
- **`metric_type`** (str, optional): Metric type ("gauge", "counter", "histogram")

#### Returns

`FlextResult[FlextMetric]` - Success contains FlextMetric entity, failure contains validation error.

#### Examples

```python
from flext_observability import flext_create_metric

# Basic metric
result = flext_create_metric("response_time", 150.5, "milliseconds")
if result.success:
    print(f"Created: {result.data.name} = {result.data.value}")

# Business metric with tags
result = flext_create_metric(
    name="orders_processed",
    value=42,
    unit="count",
    tags={"service": "order-api", "region": "us-east"},
    metric_type="counter"
)

# High-precision financial metric
from decimal import Decimal
result = flext_create_metric(
    name="transaction_amount",
    value=Decimal("1234.56"),
    unit="USD",
    tags={"account_type": "premium"}
)
```

#### Error Scenarios

```python
# Invalid metric name
result = flext_create_metric("", 100.0)
assert not result.success
assert "Invalid metric name" in result.error

# Invalid value type
result = flext_create_metric("test", "not_a_number")
assert not result.success
assert "Invalid metric value" in result.error
```

---

### `flext_create_trace()`

Create distributed tracing spans for request correlation and performance analysis.

```python
def flext_create_trace(
    operation_name: str,
    service_name: str,
    context: t.StringDict | None = None,
    parent_trace_id: str | None = None
) -> FlextResult[FlextTrace]
```

#### Parameters

- **`operation_name`** (str, required): Name of the operation being traced
- **`service_name`** (str, required): Name of the service performing the operation
- **`context`** (t.StringDict, optional): Additional context information
- **`parent_trace_id`** (str, optional): Parent trace ID for span correlation

#### Returns

`FlextResult[FlextTrace]` - Success contains FlextTrace entity, failure contains validation error.

#### Examples

```python
from flext_observability import flext_create_trace

# Basic trace
result = flext_create_trace("user_login", "authentication-service")
if result.success:
    trace = result.data
    print(f"Started trace: {trace.operation_name} in {trace.service_name}")

# Trace with context
result = flext_create_trace(
    operation_name="process_payment",
    service_name="payment-service",
    context={
        "user_id": "user123",
        "order_id": "order456",
        "payment_method": "credit_card"
    }
)

# Child trace with parent correlation
parent_result = flext_create_trace("api_request", "user-api")
if parent_result.success:
    child_result = flext_create_trace(
        operation_name="database_query",
        service_name="user-api",
        parent_trace_id=parent_result.data.id
    )
```

---

### `flext_create_alert()`

Create alerts for system monitoring and incident management.

```python
def flext_create_alert(
    name: str,
    severity: str,
    message: str,
    details: t.StringDict | None = None
) -> FlextResult[FlextAlert]
```

#### Parameters

- **`name`** (str, required): Alert identifier/name
- **`severity`** (str, required): Alert severity ("info", "warning", "error", "critical")
- **`message`** (str, required): Human-readable alert description
- **`details`** (t.StringDict, optional): Additional alert context

#### Returns

`FlextResult[FlextAlert]` - Success contains FlextAlert entity, failure contains validation error.

#### Examples

```python
from flext_observability import flext_create_alert

# Basic alert
result = flext_create_alert(
    name="high_cpu_usage",
    severity="warning",
    message="CPU usage exceeded 80% threshold"
)

# Alert with detailed context
result = flext_create_alert(
    name="database_connection_failure",
    severity="critical",
    message="Unable to connect to primary database",
    details={
        "host": "db-primary.example.com",
        "port": "5432",
        "database": "production",
        "error_code": "CONNECTION_TIMEOUT"
    }
)

# Business logic alert
result = flext_create_alert(
    name="payment_processing_delay",
    severity="error",
    message="Payment processing taking longer than expected",
    details={
        "queue_size": "1500",
        "avg_processing_time": "45s",
        "threshold": "30s"
    }
)
```

---

### `flext_create_health_check()`

Create health check entries for service monitoring and dependency validation.

```python
def flext_create_health_check(
    name: str,
    status: str,
    message: str = "",
    details: t.StringDict | None = None
) -> FlextResult[FlextHealthCheck]
```

#### Parameters

- **`name`** (str, required): Health check identifier
- **`status`** (str, required): Health status ("healthy", "unhealthy", "degraded")
- **`message`** (str, optional): Status description
- **`details`** (t.StringDict, optional): Additional health information

#### Returns

`FlextResult[FlextHealthCheck]` - Success contains FlextHealthCheck entity, failure contains validation error.

#### Examples

```python
from flext_observability import flext_create_health_check

# Basic health check
result = flext_create_health_check(
    name="database_connection",
    status="healthy",
    message="PostgreSQL connection active and responsive"
)

# Unhealthy service check
result = flext_create_health_check(
    name="external_api",
    status="unhealthy",
    message="Third-party API returning 503 errors",
    details={
        "endpoint": "https://api.external.com/v1/status",
        "last_success": "2025-08-03T10:30:00Z",
        "error_rate": "95%"
    }
)

# Degraded performance check
result = flext_create_health_check(
    name="cache_performance",
    status="degraded",
    message="Redis cache showing increased latency",
    details={
        "avg_latency": "150ms",
        "threshold": "50ms",
        "hit_rate": "85%"
    }
)
```

---

### `flext_create_log_entry()`

Create structured log entries with correlation ID support.

```python
def flext_create_log_entry(
    level: str,
    message: str,
    context: t.StringDict | None = None,
    correlation_id: str | None = None
) -> FlextResult[FlextLogEntry]
```

#### Parameters

- **`level`** (str, required): Log level ("debug", "info", "warning", "error", "critical")
- **`message`** (str, required): Log message content
- **`context`** (t.StringDict, optional): Additional context information
- **`correlation_id`** (str, optional): Request correlation ID for distributed tracing

#### Returns

`FlextResult[FlextLogEntry]` - Success contains FlextLogEntry entity, failure contains validation error.

#### Examples

```python
from flext_observability import flext_create_log_entry

# Basic log entry
result = flext_create_log_entry(
    level="info",
    message="User authentication successful"
)

# Log with context
result = flext_create_log_entry(
    level="warning",
    message="Database query taking longer than expected",
    context={
        "query": "SELECT * FROM users WHERE active = true",
        "duration": "5.2s",
        "threshold": "2.0s"
    }
)

# Correlated log entry
result = flext_create_log_entry(
    level="error",
    message="Payment processing failed",
    context={
        "user_id": "user123",
        "order_id": "order456",
        "error": "INSUFFICIENT_FUNDS"
    },
    correlation_id="req_789xyz"
)
```

---

## 🔄 Common Usage Patterns

### Pattern 1: Error Handling with Railway-Oriented Programming

```python
from flext_observability import flext_create_metric, flext_create_trace

def process_business_operation(data: dict) -> FlextResult[t.Dict]:
    """Example of chaining observability operations."""

    # Create metric - handle potential failure
    metric_result = flext_create_metric("operations_started", 1, "count")
    if not metric_result.success:
        return FlextResult[None].fail(f"Failed to create metric: {metric_result.error}")

    # Create trace - handle potential failure
    trace_result = flext_create_trace("business_operation", "main-service")
    if not trace_result.success:
        return FlextResult[None].fail(f"Failed to create trace: {trace_result.error}")

    # Business logic here
    result_data = {"status": "processed", "data": data}

    # Success metric
    success_metric = flext_create_metric("operations_completed", 1, "count")
    # Note: In production, you might want to handle this error too

    return FlextResult[None].ok(result_data)
```

### Pattern 2: Batch Observability Creation

```python
def create_system_metrics() -> list[FlextResult[FlextMetric]]:
    """Create multiple metrics with error handling."""

    metrics_to_create = [
        ("cpu_usage", 75.2, "percent"),
        ("memory_usage", 1024, "MB"),
        ("disk_usage", 85.5, "percent"),
        ("active_connections", 42, "count")
    ]

    results = []
    for name, value, unit in metrics_to_create:
        result = flext_create_metric(name, value, unit)
        results.append(result)

        if not result.success:
            print(f"⚠️  Failed to create {name}: {result.error}")

    return results
```

### Pattern 3: Observability Context Propagation

```python
def handle_user_request(user_id: str, operation: str) -> FlextResult[t.Dict]:
    """Example of propagating context through observability."""

    # Create base context
    context = {"user_id": user_id, "operation": operation}

    # Create trace with context
    trace_result = flext_create_trace(
        operation_name=operation,
        service_name="user-service",
        context=context
    )

    if not trace_result.success:
        return FlextResult[None].fail(f"Tracing failed: {trace_result.error}")

    trace_id = trace_result.data.id

    # Create metric with tags from context
    metric_result = flext_create_metric(
        name="user_operations",
        value=1,
        unit="count",
        tags={"operation": operation, "user_id": user_id}
    )

    # Create log entry with correlation
    log_result = flext_create_log_entry(
        level="info",
        message=f"Processing {operation} for user {user_id}",
        context=context,
        correlation_id=trace_id
    )

    return FlextResult[None].ok({
        "trace_id": trace_id,
        "status": "success",
        "context": context
    })
```

## 🚨 Error Reference

### Common Validation Errors

| Error Message            | Cause                    | Solution                                   |
| ------------------------ | ------------------------ | ------------------------------------------ |
| "Invalid metric name"    | Empty or non-string name | Provide non-empty string name              |
| "Invalid metric value"   | Non-numeric value        | Use float, int, or Decimal                 |
| "Invalid severity level" | Unknown severity         | Use: info, warning, error, critical        |
| "Invalid health status"  | Unknown status           | Use: healthy, unhealthy, degraded          |
| "Invalid log level"      | Unknown log level        | Use: debug, info, warning, error, critical |

### Type Safety Errors

```python
# ❌ MyPy will catch these type errors
flext_create_metric(123, "not_a_number")  # Wrong parameter types
flext_create_trace(None, "service")       # None not allowed for required params

# ✅ Correct usage
flext_create_metric("cpu_usage", 75.5, "percent")
flext_create_trace("operation", "service")
```

## 🔗 Related APIs

- **[Factory API](factory-api.md)**: Advanced entity creation patterns
- **[Service API](service-api.md)**: Full service layer capabilities
- **[Monitoring API](monitoring-api.md)**: Automatic instrumentation decorators

---

**Next Steps**: For more advanced usage patterns,
see the [Factory API Reference](factory-api.md) or explore [Basic Usage Examples](../examples/basic-usage.md).
