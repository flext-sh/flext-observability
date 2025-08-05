# Python Module Organization & Semantic Patterns

**FLEXT Observability Module Architecture & Standards for Ecosystem Observability Patterns**

---

## 🏗️ **Module Architecture Overview**

FLEXT Observability implements a **layered observability module architecture** that supports Clean Architecture, Domain-Driven Design, and railway-oriented programming specifically for monitoring, metrics, and telemetry concerns. This structure serves as the observability foundation for all 33 projects in the FLEXT ecosystem.

### **Core Design Principles**

1. **Observability-First**: Every pattern designed for monitoring and telemetry
2. **Explicit Dependencies**: Clear import paths with minimal coupling to flext-core
3. **Type-Safe Observability**: Comprehensive type hints for all observability entities
4. **Railway-Oriented Telemetry**: FlextResult[T] threading through all observability operations
5. **Ecosystem Consistency**: Observability patterns work identically across 33 projects

---

## 📁 **Module Structure & Responsibilities**

### **Foundation Layer**

```python
# Core observability foundation
src/flext_observability/
├── __init__.py              # 🎯 Public API gateway - observability exports
├── constants.py             # 🎯 Observability constants and defaults
├── exceptions.py            # 🎯 Observability-specific exceptions
└── validation.py            # 🎯 Domain validation utilities
```

**Responsibility**: Establish the foundational observability contracts that all other modules depend on.

**Import Pattern**:

```python
# All ecosystem projects start with observability patterns here
from flext_observability import FlextMetric, FlextTrace, flext_create_metric
```

### **Domain Entity Layer**

```python
# Core observability domain models
├── entities.py              # 🏛️ FlextMetric, FlextTrace, FlextAlert entities
```

**Responsibility**: Provide rich observability domain models with business rules validation.

**Entity Architecture**:

```python
from flext_core import FlextEntity, FlextResult
from flext_observability.entities import FlextMetric, FlextTrace

class FlextMetric(FlextEntity):
    """Observability metric with domain validation."""
    name: str
    value: float | Decimal
    unit: str = ""
    tags: dict[str, str] = field(default_factory=dict)
    metric_type: str = "gauge"

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate metric domain rules."""
        if not self.name or not isinstance(self.name, str):
            return FlextResult.fail("Invalid metric name")
        try:
            float(self.value)
        except (ValueError, TypeError):
            return FlextResult.fail("Invalid metric value")
        return FlextResult.ok(None)
```

### **Application Services Layer**

```python
# Observability business logic services
├── services.py              # 🚀 FlextMetricsService, FlextTracingService
├── obs_platform.py          # 🚀 FlextObservabilityPlatformV2 orchestration
└── health.py                # 🚀 Health check coordination services
```

**Responsibility**: Provide observability business logic coordinating entities with external systems.

**Service Pattern**:

```python
from flext_core import FlextContainer, FlextResult
from flext_observability.services import FlextMetricsService

class FlextMetricsService:
    """Application service for metrics operations."""

    def __init__(self, container: FlextContainer) -> None:
        self._container = container
        self._metrics_store: dict[str, FlextMetric] = {}

    def record_metric(self, metric: FlextMetric) -> FlextResult[FlextMetric]:
        """Record metric with business validation."""
        validation_result = metric.validate_business_rules()
        if validation_result.is_failure:
            return FlextResult.fail(f"Metric validation failed: {validation_result.error}")

        self._metrics_store[metric.id] = metric
        return FlextResult.ok(metric)

    def export_prometheus_format(self) -> FlextResult[str]:
        """Export metrics in Prometheus format."""
        # Business logic for Prometheus export
        return FlextResult.ok(prometheus_output)
```

### **Factory & Creation Layer**

```python
# Entity creation and factory patterns
├── factory.py               # 🏭 FlextObservabilityMasterFactory
```

**Responsibility**: Provide consistent observability entity creation with validation.

**Factory Pattern**:

```python
from flext_observability.factory import FlextObservabilityMasterFactory

class FlextObservabilityMasterFactory:
    """Central factory for all observability entities."""

    def create_metric(self, name: str, value: float, unit: str = "") -> FlextResult[FlextMetric]:
        """Create validated metric with domain rules."""
        try:
            metric = FlextMetric(
                name=name,
                value=value,
                unit=unit,
                timestamp=datetime.now(UTC)
            )

            validation_result = metric.validate_business_rules()
            if validation_result.is_failure:
                return validation_result

            return FlextResult.ok(metric)
        except Exception as e:
            return FlextResult.fail(f"Metric creation failed: {str(e)}")

    def create_trace(self, operation_name: str, service_name: str) -> FlextResult[FlextTrace]:
        """Create validated trace span."""
        try:
            trace = FlextTrace(
                operation_name=operation_name,
                service_name=service_name,
                start_time=datetime.now(UTC)
            )
            return FlextResult.ok(trace)
        except Exception as e:
            return FlextResult.fail(f"Trace creation failed: {str(e)}")
```

### **Interface Adapters Layer**

```python
# External interface adaptation
├── flext_simple.py          # 🎛️ Simple API functions (flext_create_*)
├── flext_monitor.py         # 🎛️ Monitoring decorators (@flext_monitor_function)
└── flext_structured.py      # 🎛️ Structured logging adapters
```

**Responsibility**: Provide easy-to-use interfaces adapting complex services for common use cases.

**Simple API Pattern**:

```python
from flext_observability.flext_simple import flext_create_metric, flext_create_trace

def flext_create_metric(name: str, value: float, unit: str = "") -> FlextResult[FlextMetric]:
    """Simple API for metric creation."""
    factory = get_global_factory()
    return factory.create_metric(name, value, unit)

def flext_create_trace(operation_name: str, service_name: str) -> FlextResult[FlextTrace]:
    """Simple API for trace creation."""
    factory = get_global_factory()
    return factory.create_trace(operation_name, service_name)
```

**Monitoring Decorator Pattern**:

```python
from flext_observability.flext_monitor import flext_monitor_function

@flext_monitor_function("user_processing")
def process_user_data(user_data: dict) -> dict:
    """Function automatically monitored for execution time and errors."""
    # Business logic here
    return {"status": "processed", "user": user_data}

# Decorator automatically:
# - Creates execution time metrics
# - Creates trace spans with operation context
# - Handles success/failure tracking
# - Logs structured entries with correlation IDs
```

### **Infrastructure & Utilities Layer**

```python
# Supporting infrastructure
├── repos.py                 # 🗄️ Repository patterns (in-memory implementations)
├── metrics.py               # 🗄️ Metrics collection utilities
└── flext_metrics.py         # 🗄️ Advanced metrics collector patterns
```

**Responsibility**: Provide infrastructure support and utility functions for observability operations.

**Repository Pattern**:

```python
from flext_observability.repos import FlextObservabilityRepository

class FlextObservabilityRepository:
    """Repository for observability data access."""

    def __init__(self) -> None:
        self._metrics: dict[str, FlextMetric] = {}
        self._traces: dict[str, FlextTrace] = {}
        self._alerts: dict[str, FlextAlert] = {}

    def store_metric(self, metric: FlextMetric) -> FlextResult[None]:
        """Store metric with validation."""
        if not metric.id:
            return FlextResult.fail("Metric must have ID")

        self._metrics[metric.id] = metric
        return FlextResult.ok(None)

    def find_metrics_by_name(self, name: str) -> FlextResult[list[FlextMetric]]:
        """Find metrics by name pattern."""
        matching_metrics = [
            metric for metric in self._metrics.values()
            if metric.name == name
        ]
        return FlextResult.ok(matching_metrics)
```

---

## 🎯 **Semantic Naming Conventions**

### **Public API Naming (FlextXxx)**

All public observability exports use the `Flext` prefix for namespace separation:

```python
# Observability entities
FlextMetric                 # Metrics collection entity
FlextTrace                  # Distributed tracing span entity
FlextAlert                  # Alert management entity
FlextHealthCheck            # Health monitoring entity
FlextLogEntry               # Structured logging entry

# Observability services
FlextMetricsService         # Metrics collection and management
FlextTracingService         # Distributed tracing coordination
FlextAlertService           # Alert processing and routing
FlextHealthService          # Health check coordination
FlextLoggingService         # Structured logging management

# Factory patterns
FlextObservabilityMasterFactory         # Central factory for all entities
FlextObservabilityPlatformV2           # Platform orchestration service
FlextObservabilityMonitor              # Advanced monitoring coordination

# Utility patterns
FlextStructuredLogger       # Structured logging with correlation IDs
FlextMetricsCollector      # Advanced metrics collection patterns
```

**Rationale**: Clear namespace separation prevents conflicts with application domain entities across 33 projects.

### **Module-Level Naming**

```python
# Module names focus on observability concerns
entities.py                 # Contains FlextMetric, FlextTrace, FlextAlert entities
services.py                 # Contains FlextMetricsService, FlextTracingService
factory.py                  # Contains FlextObservabilityMasterFactory
flext_simple.py            # Contains flext_create_* simple API functions
flext_monitor.py           # Contains @flext_monitor_function decorators
flext_structured.py        # Contains structured logging with correlation IDs
obs_platform.py            # Contains FlextObservabilityPlatformV2 orchestration
```

**Pattern**: One primary observability concern per module with related utilities.

### **Function Naming Patterns**

```python
# Simple API functions use flext_create_ prefix
def flext_create_metric(name: str, value: float, unit: str = "") -> FlextResult[FlextMetric]
def flext_create_trace(operation_name: str, service_name: str) -> FlextResult[FlextTrace]
def flext_create_alert(name: str, severity: str, message: str) -> FlextResult[FlextAlert]
def flext_create_health_check(name: str, status: str) -> FlextResult[FlextHealthCheck]
def flext_create_log_entry(level: str, message: str) -> FlextResult[FlextLogEntry]

# Monitoring functions use flext_monitor_ prefix
def flext_monitor_function(operation_name: str) -> Callable
def flext_get_correlation_id() -> str
def flext_set_correlation_id(correlation_id: str) -> None

# Factory access functions
def get_global_factory() -> FlextObservabilityMasterFactory
def reset_global_factory() -> None
```

**Pattern**: Consistent prefixing for easy discoverability and namespace protection.

---

## 📦 **Import Patterns & Best Practices**

### **Recommended Import Styles**

#### **1. Primary Pattern (Recommended for Ecosystem)**

```python
# Import from main package - gets essential observability tools
from flext_observability import (
    flext_create_metric,
    flext_create_trace,
    flext_monitor_function,
    FlextMetricsService
)

# Use patterns directly in business logic
@flext_monitor_function("order_processing")
def process_order(order_data: dict) -> FlextResult[dict]:
    # Create business metrics
    flext_create_metric("orders_processed", 1, "count")

    # Business logic here
    return FlextResult.ok({"status": "processed"})
```

#### **2. Service Integration Pattern (For FLEXT Services)**

```python
# Import services for advanced integration
from flext_observability import (
    FlextMetricsService,
    FlextTracingService,
    FlextObservabilityMasterFactory
)
from flext_core import FlextContainer

class UserAPIService:
    def __init__(self, container: FlextContainer) -> None:
        self.metrics = FlextMetricsService(container)
        self.tracing = FlextTracingService(container)
        self.factory = FlextObservabilityMasterFactory()

    def handle_user_request(self, request: dict) -> FlextResult[dict]:
        # Create request trace
        trace_result = self.factory.create_trace("user_request", "user-api")
        if trace_result.is_failure:
            return trace_result

        # Record request metric
        metric_result = self.factory.create_metric("api_requests", 1, "count",
                                                  tags={"endpoint": "/users"})

        # Process with observability
        return self._process_user_request(request, trace_result.data)
```

#### **3. Infrastructure Integration Pattern (For Infrastructure Services)**

```python
# Import for infrastructure monitoring
from flext_observability import (
    FlextHealthService,
    flext_create_health_check,
    flext_create_metric
)

class DatabaseConnectionService:
    def __init__(self, container: FlextContainer) -> None:
        self.health_service = FlextHealthService(container)

    def check_database_connectivity(self) -> FlextResult[dict]:
        """Monitor database health with observability."""
        try:
            # Test connection
            connection_time = self._test_connection()

            # Create health check
            health_result = flext_create_health_check(
                name="postgresql_connection",
                status="healthy",
                message=f"Connection successful in {connection_time}ms"
            )

            # Create performance metric
            metric_result = flext_create_metric(
                name="db_connection_time",
                value=connection_time,
                unit="milliseconds",
                tags={"database": "postgresql", "host": self.host}
            )

            return FlextResult.ok({"status": "healthy", "metrics": [metric_result.data]})

        except Exception as e:
            # Create failure health check
            health_result = flext_create_health_check(
                name="postgresql_connection",
                status="unhealthy",
                message=f"Connection failed: {str(e)}"
            )
            return FlextResult.fail(f"Database health check failed: {str(e)}")
```

### **Anti-Patterns (Forbidden)**

```python
# ❌ Don't import everything
from flext_observability import *

# ❌ Don't import internal implementations
from flext_observability.validation import _internal_validation_function

# ❌ Don't bypass simple API without reason
from flext_observability.factory import FlextObservabilityMasterFactory
factory = FlextObservabilityMasterFactory()
metric = factory.create_metric("test", 1.0)  # Use flext_create_metric instead

# ❌ Don't create custom observability types
class MyCustomMetric:  # Use FlextMetric instead
    pass

# ❌ Don't ignore FlextResult error handling
result = flext_create_metric("test", 1.0)
metric = result.data  # Should check result.success first
```

---

## 🏛️ **Architectural Patterns**

### **Layer Separation**

```python
# Observability architecture with clear boundaries
┌─────────────────────────────────────┐
│       Interface Adapters            │  # flext_simple.py, flext_monitor.py
│   (Simple API, Decorators, Export)  │  # flext_structured.py
├─────────────────────────────────────┤
│       Application Services          │  # services.py, obs_platform.py
│   (Business Logic, Coordination)    │  # health.py
├─────────────────────────────────────┤
│         Domain Layer                │  # entities.py (FlextMetric, FlextTrace)
│   (Observability Entities)          │  # validation.py (Domain rules)
├─────────────────────────────────────┤
│       Infrastructure Layer          │  # repos.py, metrics.py
│   (Storage, Utilities, Collection)  │  # flext_metrics.py
├─────────────────────────────────────┤
│         Foundation Layer            │  # constants.py, exceptions.py
│   (Constants, Base Patterns)        │  # validation.py (Base validation)
└─────────────────────────────────────┘
```

### **Dependency Direction**

```python
# Dependencies flow inward (Clean Architecture)
Interface Adapters  →  Application Services  →  Domain Layer
        ↓                      ↓                   ↓
Infrastructure Layer  →  Foundation Layer  →  flext-core
```

**Rule**: Higher layers can depend on lower layers and flext-core, never the reverse.

### **Cross-Cutting Observability Concerns**

```python
# Handled via decorators and context management
from flext_observability import flext_monitor_function, flext_get_correlation_id

@flext_monitor_function("critical_business_operation")
def process_payment(payment_data: dict) -> FlextResult[dict]:
    """Function automatically gets observability patterns."""
    correlation_id = flext_get_correlation_id()

    # Business logic with automatic:
    # - Execution time metrics
    # - Success/failure tracing
    # - Structured logging with correlation ID
    # - Error capture and categorization

    return FlextResult.ok({"status": "processed", "correlation_id": correlation_id})
```

---

## 🔄 **Observability-Specific Patterns**

### **Metric Creation Patterns**

```python
# Basic metric creation
def create_business_metrics(operation: str, duration: float, success: bool) -> None:
    """Create comprehensive business metrics."""

    # Performance metric
    duration_result = flext_create_metric(
        name=f"{operation}_duration",
        value=duration,
        unit="seconds",
        tags={"operation": operation, "service": "payment-service"}
    )

    # Success/failure metric
    status_result = flext_create_metric(
        name=f"{operation}_status",
        value=1,
        unit="count",
        tags={"operation": operation, "status": "success" if success else "failure"},
        metric_type="counter"
    )

    # Business KPI metric
    kpi_result = flext_create_metric(
        name="business_transactions",
        value=1,
        unit="count",
        tags={"type": operation, "outcome": "success" if success else "failure"},
        metric_type="counter"
    )

# Advanced metric patterns with validation
def create_validated_metric(name: str, value: float) -> FlextResult[None]:
    """Create metric with comprehensive validation."""
    metric_result = flext_create_metric(name, value, "count")

    if metric_result.is_failure:
        # Log metric creation failure
        log_result = flext_create_log_entry(
            level="error",
            message=f"Failed to create metric {name}: {metric_result.error}",
            context={"metric_name": name, "metric_value": str(value)}
        )
        return FlextResult.fail(f"Metric creation failed: {metric_result.error}")

    return FlextResult.ok(None)
```

### **Distributed Tracing Patterns**

```python
# Parent-child trace correlation
def process_order_with_tracing(order_data: dict) -> FlextResult[dict]:
    """Process order with distributed tracing."""

    # Create parent trace
    parent_trace_result = flext_create_trace("process_order", "order-service")
    if parent_trace_result.is_failure:
        return parent_trace_result

    parent_trace = parent_trace_result.data

    # Create child operations with parent correlation
    validate_result = validate_order_with_trace(order_data, parent_trace.id)
    if validate_result.is_failure:
        return validate_result

    payment_result = process_payment_with_trace(order_data, parent_trace.id)
    if payment_result.is_failure:
        return payment_result

    return FlextResult.ok({"order_id": "order123", "trace_id": parent_trace.id})

def validate_order_with_trace(order_data: dict, parent_trace_id: str) -> FlextResult[dict]:
    """Validate order with child trace."""
    child_trace_result = flext_create_trace(
        operation_name="validate_order",
        service_name="validation-service",
        context={"parent_trace_id": parent_trace_id, "order_size": str(len(order_data))}
    )

    if child_trace_result.is_failure:
        return child_trace_result

    # Validation logic with trace context
    return FlextResult.ok({"status": "valid", "trace_id": child_trace_result.data.id})
```

### **Health Monitoring Patterns**

```python
# Comprehensive health monitoring
def monitor_service_health() -> FlextResult[dict]:
    """Comprehensive service health monitoring."""

    health_checks = []

    # Database health
    db_health = check_database_health()
    if db_health.success:
        health_checks.append(db_health.data)

    # Cache health
    cache_health = check_cache_health()
    if cache_health.success:
        health_checks.append(cache_health.data)

    # External API health
    api_health = check_external_api_health()
    if api_health.success:
        health_checks.append(api_health.data)

    # Aggregate health status
    overall_status = "healthy" if all(
        check.status == "healthy" for check in health_checks
    ) else "degraded"

    # Create overall health metric
    health_metric = flext_create_metric(
        name="service_health_score",
        value=len([c for c in health_checks if c.status == "healthy"]) / len(health_checks),
        unit="ratio",
        tags={"service": "order-service"}
    )

    return FlextResult.ok({
        "overall_status": overall_status,
        "checks": health_checks,
        "health_score": health_metric.data if health_metric.success else None
    })

def check_database_health() -> FlextResult[FlextHealthCheck]:
    """Check database connectivity and performance."""
    try:
        start_time = time.time()
        # Test database query
        connection_time = (time.time() - start_time) * 1000

        status = "healthy" if connection_time < 100 else "degraded"

        return flext_create_health_check(
            name="postgresql_database",
            status=status,
            message=f"Database responding in {connection_time:.2f}ms",
            details={
                "response_time": f"{connection_time:.2f}ms",
                "connection_pool": "available",
                "last_backup": "2025-08-03T10:00:00Z"
            }
        )
    except Exception as e:
        return flext_create_health_check(
            name="postgresql_database",
            status="unhealthy",
            message=f"Database connection failed: {str(e)}",
            details={"error": str(e), "retry_count": "3"}
        )
```

### **Alert Management Patterns**

```python
# Business rule-based alerting
def create_business_alert(metric_name: str, current_value: float, threshold: float) -> FlextResult[None]:
    """Create business rule alert based on metric thresholds."""

    if current_value <= threshold:
        return FlextResult.ok(None)  # No alert needed

    # Determine severity based on threshold breach
    severity_ratio = current_value / threshold
    if severity_ratio > 2.0:
        severity = "critical"
    elif severity_ratio > 1.5:
        severity = "error"
    else:
        severity = "warning"

    # Create contextual alert
    alert_result = flext_create_alert(
        name=f"{metric_name}_threshold_breach",
        severity=severity,
        message=f"{metric_name} exceeded threshold: {current_value} > {threshold}",
        details={
            "metric_name": metric_name,
            "current_value": str(current_value),
            "threshold": str(threshold),
            "breach_ratio": str(severity_ratio),
            "timestamp": datetime.now(UTC).isoformat()
        }
    )

    if alert_result.is_failure:
        return FlextResult.fail(f"Failed to create alert: {alert_result.error}")

    # Create alert metric for monitoring
    alert_metric_result = flext_create_metric(
        name="alerts_created",
        value=1,
        unit="count",
        tags={"severity": severity, "metric": metric_name},
        metric_type="counter"
    )

    return FlextResult.ok(None)

# Alert escalation patterns
def escalate_alert_if_needed(alert: FlextAlert, duration_minutes: int) -> FlextResult[None]:
    """Escalate alert based on duration and severity."""

    escalation_thresholds = {
        "warning": 60,    # 1 hour
        "error": 30,      # 30 minutes
        "critical": 15    # 15 minutes
    }

    threshold = escalation_thresholds.get(alert.severity, 60)

    if duration_minutes >= threshold:
        escalated_alert_result = flext_create_alert(
            name=f"{alert.name}_escalated",
            severity="critical",
            message=f"Alert escalated: {alert.message} (duration: {duration_minutes}m)",
            details={
                "original_alert_id": alert.id,
                "original_severity": alert.severity,
                "escalation_duration": str(duration_minutes),
                "escalation_threshold": str(threshold)
            }
        )

        return escalated_alert_result.map(lambda _: None)

    return FlextResult.ok(None)
```

---

## 🧪 **Testing Patterns**

### **Test Organization**

```python
# Test structure mirrors observability structure
tests/
├── unit/                           # Unit tests (isolated)
│   ├── test_entities.py           # Tests for entities.py (FlextMetric, FlextTrace)
│   ├── test_services.py           # Tests for services.py (FlextMetricsService)
│   ├── test_factory.py            # Tests for factory.py (FlextObservabilityMasterFactory)
│   └── test_simple_api.py          # Tests for flext_simple.py (flext_create_ functions)
├── integration/                    # Integration tests
│   ├── test_service_integration.py # Service layer integration
│   ├── test_monitoring_integration.py # Decorator integration
│   └── test_platform_integration.py # Platform orchestration
├── e2e/                           # End-to-end tests
│   └── test_observability_workflows.py # Complete observability workflows
├── conftest.py                    # Test configuration and fixtures
└── test_complete_coverage.py      # Comprehensive coverage validation
```

### **FlextResult Testing Patterns for Observability**

```python
import pytest
from flext_observability import flext_create_metric, flext_create_trace

def test_metric_creation_success():
    """Test successful metric creation."""
    result = flext_create_metric("api_requests", 42.0, "count")

    assert result.success
    assert result.data.name == "api_requests"
    assert result.data.value == 42.0
    assert result.data.unit == "count"
    assert result.error is None

def test_metric_creation_failure():
    """Test metric creation validation failure."""
    result = flext_create_metric("", 42.0, "count")  # Empty name

    assert result.is_failure
    assert result.data is None
    assert "Invalid metric name" in result.error

def test_observability_chaining():
    """Test railway-oriented chaining of observability operations."""
    def create_observability_data(operation: str) -> FlextResult[dict]:
        return (
            flext_create_metric(f"{operation}_requests", 1, "count")
            .flat_map(lambda metric:
                flext_create_trace(operation, "test-service")
                .map(lambda trace: {"metric": metric, "trace": trace})
            )
        )

    result = create_observability_data("user_login")

    assert result.success
    assert "metric" in result.data
    assert "trace" in result.data
    assert result.data["metric"].name == "user_login_requests"
    assert result.data["trace"].operation_name == "user_login"

def test_observability_failure_propagation():
    """Test failure propagation in observability chains."""
    def create_invalid_observability() -> FlextResult[dict]:
        return (
            flext_create_metric("", 1, "count")  # Invalid metric name
            .flat_map(lambda metric:
                flext_create_trace("operation", "service")  # Should not execute
                .map(lambda trace: {"metric": metric, "trace": trace})
            )
        )

    result = create_invalid_observability()

    assert result.is_failure
    assert "Invalid metric name" in result.error
```

### **Observability Entity Testing Patterns**

```python
from flext_observability.entities import FlextMetric, FlextTrace
from decimal import Decimal

class TestFlextMetric:
    """Test observability metric entity behavior."""

    def test_metric_validation_success(self):
        """Test successful metric validation."""
        metric = FlextMetric(
            name="response_time",
            value=150.5,
            unit="milliseconds",
            tags={"service": "api", "endpoint": "/users"}
        )

        validation_result = metric.validate_business_rules()

        assert validation_result.success
        assert metric.name == "response_time"
        assert metric.value == 150.5
        assert metric.unit == "milliseconds"
        assert metric.tags["service"] == "api"

    def test_metric_validation_invalid_name(self):
        """Test metric validation with invalid name."""
        metric = FlextMetric(name="", value=100.0, unit="count")

        validation_result = metric.validate_business_rules()

        assert validation_result.is_failure
        assert "Invalid metric name" in validation_result.error

    def test_metric_decimal_value_support(self):
        """Test metric with Decimal value for financial precision."""
        metric = FlextMetric(
            name="transaction_amount",
            value=Decimal("1234.56"),
            unit="USD"
        )

        validation_result = metric.validate_business_rules()

        assert validation_result.success
        assert metric.value == Decimal("1234.56")
        assert isinstance(metric.value, Decimal)

class TestFlextTrace:
    """Test observability trace entity behavior."""

    def test_trace_creation_with_context(self):
        """Test trace creation with operation context."""
        trace = FlextTrace(
            operation_name="process_payment",
            service_name="payment-service",
            context={"user_id": "123", "amount": "100.00"}
        )

        assert trace.operation_name == "process_payment"
        assert trace.service_name == "payment-service"
        assert trace.context["user_id"] == "123"
        assert trace.context["amount"] == "100.00"
        assert trace.start_time is not None

    def test_trace_parent_child_relationship(self):
        """Test parent-child trace relationships."""
        parent_trace = FlextTrace(
            operation_name="api_request",
            service_name="api-gateway"
        )

        child_trace = FlextTrace(
            operation_name="database_query",
            service_name="user-service",
            parent_trace_id=parent_trace.id
        )

        assert child_trace.parent_trace_id == parent_trace.id
        assert child_trace.operation_name == "database_query"
        assert child_trace.service_name == "user-service"
```

### **Service Testing Patterns**

```python
from flext_observability import FlextMetricsService, FlextObservabilityMasterFactory
from flext_core import FlextContainer

@pytest.fixture
def clean_container():
    """Provide clean container for each test."""
    return FlextContainer()

@pytest.fixture
def metrics_service(clean_container):
    """Provide metrics service with clean container."""
    return FlextMetricsService(clean_container)

@pytest.fixture
def observability_factory():
    """Provide fresh observability factory."""
    return FlextObservabilityMasterFactory()

def test_metrics_service_record_metric(metrics_service, observability_factory):
    """Test metrics service metric recording."""
    # Create metric using factory
    metric_result = observability_factory.create_metric("test_metric", 100.0, "count")
    assert metric_result.success

    # Record metric using service
    record_result = metrics_service.record_metric(metric_result.data)

    assert record_result.success
    assert record_result.data.name == "test_metric"
    assert record_result.data.value == 100.0

def test_metrics_service_prometheus_export(metrics_service, observability_factory):
    """Test Prometheus format export."""
    # Create and record multiple metrics
    metrics_data = [
        ("api_requests", 150.0, "count"),
        ("response_time", 250.5, "milliseconds"),
        ("error_rate", 0.05, "ratio")
    ]

    for name, value, unit in metrics_data:
        metric_result = observability_factory.create_metric(name, value, unit)
        assert metric_result.success

        record_result = metrics_service.record_metric(metric_result.data)
        assert record_result.success

    # Export to Prometheus format
    export_result = metrics_service.export_prometheus_format()

    assert export_result.success
    prometheus_output = export_result.data

    # Verify Prometheus format
    assert "# TYPE api_requests gauge" in prometheus_output
    assert "api_requests 150.0" in prometheus_output
    assert "# TYPE response_time gauge" in prometheus_output
    assert "response_time 250.5" in prometheus_output

def test_metrics_service_memory_management(metrics_service, observability_factory):
    """Test metrics service memory management."""
    # Create metrics beyond memory limit to test cleanup
    for i in range(1200):  # Exceeds default limit of 1000
        metric_result = observability_factory.create_metric(f"test_metric_{i}", float(i), "count")
        assert metric_result.success

        record_result = metrics_service.record_metric(metric_result.data)
        assert record_result.success

    # Verify memory management kicked in
    total_metrics = len(metrics_service._metrics_store)
    assert total_metrics <= 1000  # Should have cleaned up to stay within limits
```

### **Monitoring Decorator Testing Patterns**

```python
from flext_observability import flext_monitor_function
import time

def test_function_monitoring_decorator():
    """Test automatic function monitoring."""

    @flext_monitor_function("test_operation")
    def monitored_function(x: int, y: int) -> int:
        """Test function with monitoring."""
        time.sleep(0.1)  # Simulate work
        return x + y

    # Execute monitored function
    result = monitored_function(5, 3)

    # Verify function result
    assert result == 8

    # Verify monitoring data was created (in a real implementation,
    # you would check the metrics service or factory for created metrics)

def test_function_monitoring_with_exception():
    """Test monitoring decorator with function exceptions."""

    @flext_monitor_function("error_prone_operation")
    def failing_function() -> int:
        """Function that raises an exception."""
        raise ValueError("Test error")

    # Execute function and expect exception
    with pytest.raises(ValueError, match="Test error"):
        failing_function()

    # In a real implementation, verify that error metrics were created
    # and failure traces were recorded
```

---

## 📏 **Code Quality Standards**

### **Type Annotation Requirements**

```python
# ✅ Complete type annotations for observability functions
def create_business_metric(
    operation: str,
    value: float | Decimal,
    tags: dict[str, str] | None = None
) -> FlextResult[FlextMetric]:
    """Create business metric with complete type safety."""
    return flext_create_metric(
        name=f"business_{operation}",
        value=value,
        unit="count",
        tags=tags or {}
    )

# ✅ Generic type usage for observability utilities
from typing import TypeVar, Generic, Callable

T = TypeVar('T')
U = TypeVar('U')

def map_observability_result(
    result: FlextResult[T],
    func: Callable[[T], U]
) -> FlextResult[U]:
    """Generic result mapping for observability operations."""
    if result.success:
        return FlextResult.ok(func(result.data))
    return FlextResult.fail(result.error)

# ✅ Protocol definitions for observability interfaces
from typing import Protocol

class ObservabilityCollector(Protocol):
    """Protocol for observability data collectors."""

    def collect_metric(self, metric: FlextMetric) -> FlextResult[None]:
        """Collect metric data."""
        ...

    def collect_trace(self, trace: FlextTrace) -> FlextResult[None]:
        """Collect trace data."""
        ...

# ❌ Missing type annotations
def create_metric(name, value, unit):  # Missing types
    return flext_create_metric(name, value, unit)
```

### **Error Handling Standards**

```python
# ✅ Always use FlextResult for observability error handling
def create_comprehensive_observability(operation: str) -> FlextResult[dict[str, Any]]:
    """Create comprehensive observability data with error handling."""

    # Chain observability operations with proper error handling
    metric_result = flext_create_metric(f"{operation}_requests", 1, "count")
    if metric_result.is_failure:
        return FlextResult.fail(f"Failed to create metric: {metric_result.error}")

    trace_result = flext_create_trace(operation, "main-service")
    if trace_result.is_failure:
        return FlextResult.fail(f"Failed to create trace: {trace_result.error}")

    return FlextResult.ok({
        "metric": metric_result.data,
        "trace": trace_result.data,
        "correlation_id": trace_result.data.id
    })

# ✅ Chain observability operations safely
def monitor_business_operation(operation_data: dict) -> FlextResult[dict]:
    """Monitor business operation with comprehensive observability."""
    return (
        flext_create_trace("business_operation", "business-service")
        .flat_map(lambda trace:
            flext_create_metric("operations_started", 1, "count")
            .map(lambda metric: {"trace": trace, "metric": metric})
        )
        .flat_map(lambda obs_data:
            process_operation(operation_data, obs_data["trace"].id)
            .map(lambda result: {**result, **obs_data})
        )
    )

# ❌ Never raise exceptions for observability failures
def create_metric_bad(name: str, value: float) -> FlextMetric:
    """Bad example - raises exceptions."""
    if not name:
        raise ValueError("Name is required")  # Breaks railway pattern
    return FlextMetric(name=name, value=value)
```

### **Documentation Standards**

```python
def create_business_observability_dashboard(
    service_name: str,
    metrics_config: dict[str, Any],
    trace_config: dict[str, Any]
) -> FlextResult[dict[str, Any]]:
    """
    Create comprehensive business observability dashboard.

    This function implements the complete observability setup for a business
    service including metrics collection, distributed tracing, and health
    monitoring. It follows FLEXT observability patterns for consistent
    monitoring across the ecosystem.

    Args:
        service_name: Name of the service to monitor (e.g., "user-api", "payment-service")
        metrics_config: Configuration for metrics collection including names,
            types, and collection intervals. Example:
            {
                "response_time": {"type": "histogram", "unit": "seconds"},
                "request_count": {"type": "counter", "unit": "count"}
            }
        trace_config: Configuration for distributed tracing including sampling
            rates and context propagation. Example:
            {
                "sampling_rate": 0.1,
                "propagate_context": True,
                "trace_external_calls": True
            }

    Returns:
        FlextResult[dict[str, Any]]: Success contains dashboard configuration
        with metric definitions, trace setup, and health check configuration.
        Failure contains detailed error message explaining setup failure.

    Example:
        >>> metrics = {"api_requests": {"type": "counter", "unit": "count"}}
        >>> traces = {"sampling_rate": 0.1}
        >>> result = create_business_observability_dashboard("user-api", metrics, traces)
        >>> if result.success:
        ...     dashboard = result.data
        ...     print(f"Created dashboard with {len(dashboard['metrics'])} metrics")
        ... else:
        ...     print(f"Dashboard creation failed: {result.error}")

    Integration:
        - Uses FlextMetricsService for metrics collection coordination
        - Integrates with FlextTracingService for distributed tracing
        - Coordinates with FlextHealthService for health monitoring
        - Built on flext-core FlextResult patterns for error handling
    """
    try:
        # Create service-specific observability components
        dashboard_config = {
            "service_name": service_name,
            "metrics": [],
            "traces": [],
            "health_checks": []
        }

        # Setup metrics based on configuration
        for metric_name, config in metrics_config.items():
            metric_result = flext_create_metric(
                name=f"{service_name}_{metric_name}",
                value=0,  # Initial value
                unit=config.get("unit", "count"),
                metric_type=config.get("type", "gauge")
            )

            if metric_result.is_failure:
                return FlextResult.fail(f"Failed to create metric {metric_name}: {metric_result.error}")

            dashboard_config["metrics"].append(metric_result.data)

        # Setup tracing based on configuration
        trace_result = flext_create_trace(
            operation_name=f"{service_name}_operations",
            service_name=service_name,
            context=trace_config
        )

        if trace_result.is_failure:
            return FlextResult.fail(f"Failed to create trace setup: {trace_result.error}")

        dashboard_config["traces"].append(trace_result.data)

        return FlextResult.ok(dashboard_config)

    except Exception as e:
        return FlextResult.fail(f"Unexpected error creating observability dashboard: {str(e)}")
```

---

## 🌐 **Ecosystem Integration Guidelines**

### **Cross-Project Observability Standards**

```python
# ✅ Standard observability imports across ecosystem
from flext_core import FlextResult, FlextContainer
from flext_observability import (
    flext_create_metric,
    flext_create_trace,
    flext_monitor_function,
    FlextMetricsService
)

# ✅ Consistent observability patterns across FLEXT projects
class FlextUserService:
    """User service with standardized observability."""

    def __init__(self, container: FlextContainer) -> None:
        self.container = container
        self.observability = FlextMetricsService(container)

    @flext_monitor_function("user_creation")
    def create_user(self, user_data: dict) -> FlextResult[dict]:
        """Create user with automatic observability."""

        # Business metrics
        flext_create_metric("users_created", 1, "count",
                           tags={"service": "user-service"})

        # Business logic
        result = self._create_user_impl(user_data)

        # Success/failure metrics
        status = "success" if result.success else "failure"
        flext_create_metric("user_creation_status", 1, "count",
                           tags={"status": status, "service": "user-service"})

        return result

# ✅ Cross-service observability correlation
def sync_user_between_services(user_id: str) -> FlextResult[dict]:
    """Sync user data between services with trace correlation."""

    # Create correlation trace
    correlation_trace = flext_create_trace("user_sync", "integration-service")
    if correlation_trace.is_failure:
        return correlation_trace

    trace_id = correlation_trace.data.id

    # LDAP service call with trace context
    ldap_result = fetch_user_from_ldap(user_id, trace_id)
    if ldap_result.is_failure:
        return ldap_result

    # Oracle service call with trace context
    oracle_result = update_user_in_oracle(user_id, ldap_result.data, trace_id)
    if oracle_result.is_failure:
        return oracle_result

    # Success metrics
    flext_create_metric("user_sync_completed", 1, "count",
                       tags={"correlation_id": trace_id})

    return FlextResult.ok({
        "user_id": user_id,
        "correlation_id": trace_id,
        "status": "synchronized"
    })

# ❌ Don't create service-specific observability types
class UserMetric:  # Use FlextMetric instead
    pass

class OracleTrace:  # Use FlextTrace instead
    pass
```

### **Configuration Integration Across Services**

```python
# ✅ Extend observability configuration patterns
from flext_core import FlextBaseSettings

class ObservabilitySettings(FlextBaseSettings):
    """Observability configuration extending core patterns."""
    metrics_enabled: bool = True
    tracing_enabled: bool = True
    log_level: str = "INFO"
    correlation_id_header: str = "X-Correlation-ID"

    class Config:
        env_prefix = "OBSERVABILITY_"

class UserServiceSettings(FlextBaseSettings):
    """User service configuration with observability."""
    service_name: str = "user-service"
    database_url: str = "postgresql://localhost/users"
    observability: ObservabilitySettings = field(default_factory=ObservabilitySettings)

    class Config:
        env_prefix = "USER_SERVICE_"
        env_nested_delimiter = "__"

# Usage in service initialization
class UserService:
    def __init__(self, settings: UserServiceSettings) -> None:
        self.settings = settings

        # Initialize observability based on configuration
        if settings.observability.metrics_enabled:
            self.metrics_service = FlextMetricsService(container)

        if settings.observability.tracing_enabled:
            self.tracing_service = FlextTracingService(container)
```

### **Monitoring Integration Patterns**

```python
# ✅ Consistent monitoring across ecosystem services
from flext_observability import flext_monitor_function

class FlextAPIService:
    """API service with ecosystem-standard monitoring."""

    @flext_monitor_function("api_endpoint")
    def handle_user_request(self, request_data: dict) -> FlextResult[dict]:
        """Handle API request with automatic monitoring."""
        # Automatically gets:
        # - Request latency metrics
        # - Success/failure tracking
        # - Distributed tracing
        # - Structured logging with correlation IDs

        return self._process_request(request_data)

    @flext_monitor_function("database_operation")
    def query_user_data(self, user_id: str) -> FlextResult[dict]:
        """Database query with monitoring."""
        # Database-specific observability patterns
        return self._execute_database_query(user_id)

class FlextOracleService:
    """Oracle service with ecosystem-standard monitoring."""

    @flext_monitor_function("oracle_query")
    def execute_wms_query(self, query: str) -> FlextResult[list[dict]]:
        """Execute Oracle WMS query with monitoring."""
        # Oracle-specific observability patterns
        return self._execute_oracle_query(query)

class FlextLDAPService:
    """LDAP service with ecosystem-standard monitoring."""

    @flext_monitor_function("ldap_operation")
    def search_users(self, search_filter: str) -> FlextResult[list[dict]]:
        """LDAP search with monitoring."""
        # LDAP-specific observability patterns
        return self._execute_ldap_search(search_filter)
```

---

## 📋 **Checklist for New Observability Modules**

### **Module Creation Checklist**

- [ ] **Naming**: Uses `flext_` prefix and clear observability-focused name
- [ ] **Location**: Placed in appropriate observability architectural layer
- [ ] **Imports**: Only imports from flext-core and same/lower observability layers
- [ ] **Types**: Complete type annotations with MyPy compliance for observability entities
- [ ] **Error Handling**: Uses FlextResult for all observability error conditions
- [ ] **Documentation**: Comprehensive docstrings with observability examples
- [ ] **Tests**: 95% coverage with observability-specific test patterns
- [ ] **Exports**: Added to `__init__.py` if part of public observability API
- [ ] **Examples**: Working examples in observability example files
- [ ] **Ecosystem Impact**: Validated across FLEXT ecosystem projects

### **Observability Quality Gate Checklist**

- [ ] **Linting**: `make lint` passes (Ruff with all rules)
- [ ] **Type Check**: `make type-check` passes (strict MyPy with observability types)
- [ ] **Tests**: `make test` passes (95% coverage for observability components)
- [ ] **Security**: `make security` passes (Bandit + pip-audit)
- [ ] **Format**: `make format` passes (consistent formatting)
- [ ] **Integration**: Works with existing FLEXT ecosystem observability
- [ ] **Documentation**: Updated observability documentation
- [ ] **Examples**: Added working observability examples

### **Observability-Specific Standards**

- [ ] **FlextResult Integration**: All observability operations return FlextResult[T]
- [ ] **Entity Validation**: All observability entities implement `validate_business_rules()`
- [ ] **Factory Support**: Entities can be created via FlextObservabilityMasterFactory
- [ ] **Simple API**: Core functionality available via `flext_create_*` functions
- [ ] **Monitoring Support**: Functions can be decorated with `@flext_monitor_function`
- [ ] **Service Integration**: Services use FlextContainer dependency injection
- [ ] **Correlation IDs**: Tracing supports correlation ID propagation
- [ ] **Ecosystem Consistency**: Patterns match other FLEXT observability implementations

---

**Last Updated**: August 3, 2025  
**Target Audience**: FLEXT ecosystem developers implementing observability  
**Scope**: Python module organization for observability across 33-project ecosystem  
**Version**: 0.9.0 → 1.0.0 observability development guidelines
