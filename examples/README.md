# FLEXT Observability - Examples

**Comprehensive examples demonstrating observability patterns and integration within the FLEXT ecosystem.**

This directory contains practical examples showing how to integrate FLEXT Observability into real-world scenarios, from basic usage to advanced enterprise patterns. All examples are functional, tested, and demonstrate best practices for observability across the FLEXT ecosystem.

## Example Files

### [01_functional.py](01_functional.py) - Core Functionality

Comprehensive demonstration of core observability functionality including:

- **Entity Creation**: FlextMetric, FlextTrace, FlextAlert creation patterns
- **Factory Usage**: FlextObservabilityMasterFactory integration
- **Service Integration**: FlextMetricsService and other service usage
- **Monitoring Decorators**: @flext_monitor_function practical examples
- **Error Handling**: Railway-oriented programming with FlextCore.Result
- **Real-world Scenarios**: Business logic with observability integration

### [02_solid_observability_demo.py](02_solid_observability_demo.py) - SOLID Principles

Advanced demonstration of SOLID principles applied to observability:

- **Single Responsibility**: Focused observability components
- **Open/Closed**: Extensible monitoring patterns
- **Liskov Substitution**: Polymorphic observability interfaces
- **Interface Segregation**: Specialized observability contracts
- **Dependency Inversion**: Dependency injection with FlextCore.Container

## Usage Patterns Demonstrated

### Basic Observability Integration

```python
# Example from 01_functional.py
from flext_observability import flext_create_metric, flext_create_trace

def create_business_metrics():
    """Demonstrate basic metrics creation."""
    # Performance metric
    response_time = flext_create_metric(
        name="api_response_time",
        value=150.5,
        unit="milliseconds",
        tags={"service": "user-api", "endpoint": "/users"}
    )

    # Business metric
    user_count = flext_create_metric(
        name="active_users",
        value=1250,
        unit="count",
        tags={"region": "us-east", "tier": "premium"}
    )

    return response_time, user_count
```

### Service Layer Integration

```python
# Example service integration pattern
from flext_observability import FlextMetricsService, FlextObservabilityMasterFactory
from flext_core import FlextCore

class UserService:
    """Example service with integrated observability."""

    def __init__(self, container: FlextCore.Container):
        self.container = container
        self.metrics = FlextMetricsService(container)
        self.factory = FlextObservabilityMasterFactory()

    def create_user(self, user_data: dict) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Create user with comprehensive observability."""
        # Create business metrics
        metric_result = self.factory.create_metric(
            name="users_created",
            value=1,
            unit="count",
            tags={"service": "user-service"}
        )

        if metric_result.success:
            self.metrics.record_metric(metric_result.data)

        # Business logic here
        return FlextCore.Result[None].ok({"user_id": "user123", "status": "created"})
```

### Monitoring Decorator Patterns

```python
# Automatic function monitoring
from flext_observability import flext_monitor_function

@flext_monitor_function("order_processing")
def process_order(order_data: dict) -> dict:
    """Process order with automatic monitoring.

    This function automatically gets:
    - Execution time metrics
    - Success/failure tracking
    - Distributed tracing spans
    - Structured logging with correlation IDs
    """
    # Business logic
    processed_order = {
        "order_id": order_data["id"],
        "status": "processed",
        "items": len(order_data.get("items", []))
    }

    return processed_order

# Advanced monitoring with context
@flext_monitor_function("payment_processing")
def process_payment(amount: float, currency: str) -> FlextCore.Result[FlextCore.Types.Dict]:
    """Process payment with error handling and monitoring."""
    if amount <= 0:
        return FlextCore.Result[None].fail("Invalid payment amount")

    # Payment processing logic
    transaction = {
        "transaction_id": "txn_123",
        "amount": amount,
        "currency": currency,
        "status": "completed"
    }

    return FlextCore.Result[None].ok(transaction)
```

### Health Monitoring Patterns

```python
# Health check integration example
from flext_observability import flext_create_health_check, FlextHealthService

def monitor_database_health() -> FlextCore.Result[FlextCore.Types.Dict]:
    """Monitor database connectivity and performance."""
    try:
        # Test database connection
        connection_time = test_database_connection()

        if connection_time < 100:  # milliseconds
            health_check = flext_create_health_check(
                name="postgresql_database",
                status="healthy",
                message=f"Database responding in {connection_time}ms",
                details={
                    "response_time": f"{connection_time}ms",
                    "pool_size": "10/10",
                    "active_connections": "5"
                }
            )
        else:
            health_check = flext_create_health_check(
                name="postgresql_database",
                status="degraded",
                message=f"Database slow response: {connection_time}ms"
            )

        return health_check

    except Exception as e:
        error_health = flext_create_health_check(
            name="postgresql_database",
            status="unhealthy",
            message=f"Database connection failed: {str(e)}"
        )
        return error_health
```

### Distributed Tracing Patterns

```python
# Parent-child trace correlation
from flext_observability import flext_create_trace

def process_user_workflow(user_id: str) -> FlextCore.Result[FlextCore.Types.Dict]:
    """Process user workflow with distributed tracing."""

    # Create parent trace
    parent_trace_result = flext_create_trace(
        operation_name="user_workflow",
        service_name="workflow-service",
        context={"user_id": user_id}
    )

    if parent_trace_result.is_failure:
        return parent_trace_result

    parent_trace = parent_trace_result.data

    # Child operations with trace correlation
    validation_result = validate_user_data(user_id, parent_trace.id)
    if validation_result.is_failure:
        return validation_result

    processing_result = process_user_operation(user_id, parent_trace.id)
    if processing_result.is_failure:
        return processing_result

    return FlextCore.Result[None].ok({
        "user_id": user_id,
        "trace_id": parent_trace.id,
        "status": "completed"
    })

def validate_user_data(user_id: str, parent_trace_id: str) -> FlextCore.Result[FlextCore.Types.Dict]:
    """Validate user with child trace."""
    child_trace_result = flext_create_trace(
        operation_name="user_validation",
        service_name="validation-service",
        context={
            "user_id": user_id,
            "parent_trace_id": parent_trace_id
        }
    )

    if child_trace_result.is_failure:
        return child_trace_result

    # Validation logic here
    return FlextCore.Result[None].ok({
        "status": "valid",
        "trace_id": child_trace_result.data.id
    })
```

## FLEXT Ecosystem Integration Examples

### Singer Tap Integration

```python
# Example Singer tap with observability
from flext_observability import flext_monitor_function, flext_create_metric

class FlextMeltanoTapOracle:
    """Example Singer tap with integrated observability."""

    @flext_monitor_function("tap_oracle_extract")
    def extract_records(self, table_name: str) -> list[FlextCore.Types.Dict]:
        """Extract records with automatic monitoring."""

        # Extract data (business logic)
        records = self._query_oracle_table(table_name)

        # Business metrics
        flext_create_metric(
            name="records_extracted",
            value=len(records),
            unit="count",
            tags={"table": table_name, "tap": "oracle"}
        )

        flext_create_metric(
            name="extraction_time",
            value=self._last_extraction_time,
            unit="seconds",
            tags={"table": table_name}
        )

        return records
```

### FastAPI Service Integration

```python
# Example FastAPI service with observability
from flext_observability import flext_monitor_function, flext_create_metric

class FlextAPIService:
    """Example FastAPI service with observability."""

    @flext_monitor_function("api_endpoint")
    def handle_user_request(self, request_data: dict) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Handle API request with comprehensive observability."""

        # Request metrics
        flext_create_metric(
            name="api_requests",
            value=1,
            unit="count",
            tags={
                "endpoint": "/users",
                "method": "POST",
                "service": "user-api"
            }
        )

        # Business logic
        result = self._process_user_request(request_data)

        # Response metrics
        status = "success" if result.success else "error"
        flext_create_metric(
            name="api_responses",
            value=1,
            unit="count",
            tags={
                "endpoint": "/users",
                "status": status,
                "service": "user-api"
            }
        )

        return result
```

## Running Examples

### Execute Individual Examples

```bash
# Run functional examples
cd examples/
python 01_functional.py

# Run SOLID principles demo
python 02_solid_observability_demo.py

# Run with different scenarios
python 01_functional.py --scenario=metrics
python 01_functional.py --scenario=tracing
```

### Integration Testing

```bash
# Test examples as part of test suite
pytest examples/ -v

# Validate example code quality
make lint examples/
make type-check examples/
```

## Example Development Guidelines

### Creating New Examples

1. **Real-world Scenarios**: Examples should reflect actual usage patterns
2. **Complete Integration**: Show full observability integration, not just API calls
3. **Error Handling**: Demonstrate both success and failure paths
4. **Documentation**: Comprehensive docstrings explaining patterns
5. **Testing**: All examples should be testable and validated

### Example Quality Standards

- **Functional Code**: All examples must execute successfully
- **Type Safety**: Complete type annotations following project standards
- **Error Handling**: Proper FlextCore.Result usage and validation
- **Documentation**: Clear explanations of observability patterns
- **FLEXT Integration**: Demonstrate ecosystem integration patterns

## Integration Scenarios Covered

1. **Basic Usage**: Simple metric and trace creation
2. **Service Integration**: Full service layer observability
3. **Monitoring Automation**: Decorator-based automatic monitoring
4. **Health Monitoring**: Service health check patterns
5. **Distributed Tracing**: Cross-service trace correlation
6. **Business Metrics**: Domain-specific observability patterns
7. **Error Scenarios**: Comprehensive error handling examples
8. **Performance Monitoring**: Response time and throughput tracking
9. **Ecosystem Integration**: FLEXT-specific integration patterns
10. **Enterprise Patterns**: Production-ready observability implementations

---

**All examples are production-ready patterns that can be adapted for real-world FLEXT ecosystem integration scenarios.**
