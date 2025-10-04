# Getting Started with FLEXT Observability

**Quick Start Guide for Integrating Observability Patterns in FLEXT Projects**

This guide will walk you through the essential steps to integrate FLEXT Observability into your FLEXT ecosystem project, from installation to your first working observability implementation.

## 🎯 Prerequisites

### FLEXT Ecosystem Requirements

- **flext-core**: Foundation library (automatically included as dependency)
- **Python 3.13+**: Required for all FLEXT ecosystem projects
- **Poetry**: Package management (recommended for FLEXT projects)

### Development Environment

```bash
# Verify Python version
python --version  # Should be 3.13+

# Verify Poetry installation
poetry --version

# Verify you're in a FLEXT ecosystem project
ls pyproject.toml  # Should exist with FLEXT project configuration
```

## 🚀 Installation

### Via Poetry (Recommended for FLEXT Projects)

```bash
# Add flext-observability to your FLEXT project
poetry add flext-observability

# Install development dependencies if contributing
poetry add --group dev flext-observability

# Verify installation
poetry run python -c "import flext_observability; print('Success!')"
```

### Via pip (Alternative)

```bash
# Direct installation
pip install flext-observability

# Verify installation
python -c "import flext_observability; print('Success!')"
```

## 🏁 First Observability Integration

### 1. Basic Metric Creation

Create your first metric using the Simple API:

```python
from flext_observability import flext_create_metric

# Create a simple metric
result = flext_create_metric("api_response_time", 150.5, "milliseconds")

if result.success:
    metric = result.data
    print(f"✅ Created metric: {metric.name} = {metric.value} {metric.unit}")
    print(f"📊 Metric ID: {metric.id}")
else:
    print(f"❌ Failed to create metric: {result.error}")
```

**Expected Output**:

```
✅ Created metric: api_response_time = 150.5 milliseconds
📊 Metric ID: flext_metric_abc123...
```

### 2. Basic Trace Creation

Create distributed tracing spans:

```python
from flext_observability import flext_create_trace

# Create a trace for an operation
result = flext_create_trace("user_authentication", "validate_credentials")

if result.success:
    trace = result.data
    print(f"🔍 Started trace: {trace.operation_name}")
    print(f"🏷️  Service: {trace.service_name}")
    print(f"📋 Trace ID: {trace.id}")
else:
    print(f"❌ Failed to create trace: {result.error}")
```

### 3. Function Monitoring Decorator

Automatically monitor function execution:

```python
from flext_observability import flext_monitor_function

@flext_monitor_function("user_data_processing")
def process_user_data(user_id: str, data: dict) -> dict:
    """This function is automatically monitored."""
    # Your business logic here
    processed_data = {"user_id": user_id, "status": "processed"}
    return processed_data

# Use the function normally - monitoring happens automatically
result = process_user_data("user123", {"name": "John", "email": "john@example.com"})
print(f"📈 Processed data: {result}")
```

## 🏛️ Service Layer Integration

### Using Services with Dependency Injection

For more advanced scenarios, use the service layer with flext-core patterns:

```python
from flext_observability import FlextMetricsService, FlextObservabilityMasterFactory
from flext_core import FlextContainer

# Initialize dependency injection container
container = FlextContainer()

# Create observability services
metrics_service = FlextMetricsService(container)
factory = FlextObservabilityMasterFactory()

# Create and record a metric
metric_result = factory.create_metric("database_connections", 42, "connections")

if metric_result.success:
    # Record the metric using the service
    record_result = metrics_service.record_metric(metric_result.data)

    if record_result.success:
        print(f"✅ Metric recorded successfully: {record_result.data.name}")
    else:
        print(f"❌ Failed to record metric: {record_result.error}")
```

## 🔧 Integration Patterns

### Pattern 1: FLEXT Service Integration

For FLEXT ecosystem services (API, Auth, Web, CLI):

```python
# In your FLEXT service initialization
from flext_observability import flext_monitor_function, flext_create_metric
from flext_core import FlextResult

class UserService:
    @flext_monitor_function("user_service_create")
    def create_user(self, user_data: dict) -> FlextResult[FlextTypes.Dict]:
        """Create user with automatic monitoring."""

        # Record custom metric
        metric_result = flext_create_metric("users_created", 1, "count")

        # Your business logic
        user = {"id": "user123", "email": user_data["email"]}

        return FlextResult[None].ok(user)
```

### Pattern 2: Infrastructure Service Integration

For FLEXT infrastructure services (Oracle, LDAP, LDIF):

```python
from flext_observability import FlextHealthService, flext_create_health_check
from flext_core import FlextContainer

class DatabaseConnectionService:
    def __init__(self):
        self.container = FlextContainer()
        self.health_service = FlextHealthService(self.container)

    def check_database_health(self) -> FlextResult[FlextTypes.Dict]:
        """Monitor database connection health."""

        # Create health check
        health_result = flext_create_health_check(
            name="postgresql_connection",
            status="healthy",
            message="Database responding normally"
        )

        if health_result.success:
            # Process health check through service
            return self.health_service.process_health_check(health_result.data)

        return health_result
```

### Pattern 3: Singer Ecosystem Integration

For Singer taps, targets, and DBT projects:

```python
from flext_observability import flext_monitor_function, flext_create_metric

class FlextTapOracle:
    @flext_monitor_function("tap_oracle_extract")
    def extract_records(self, table_name: str) -> list[FlextTypes.Dict]:
        """Extract records with monitoring."""

        # Your extraction logic
        records = self._query_oracle_table(table_name)

        # Record extraction metrics
        flext_create_metric("records_extracted", len(records), "count")
        flext_create_metric("extraction_table", 1, "count", tags={"table": table_name})

        return records
```

## 🧪 Testing Your Integration

### Create Test File

Create `test_observability_integration.py`:

```python
from flext_observability import (
    flext_create_metric,
    flext_create_trace,
    flext_monitor_function
)

def test_basic_metric_creation():
    """Test basic metric creation works."""
    result = flext_create_metric("test_metric", 100.0, "count")

    assert result.success
    assert result.data.name == "test_metric"
    assert result.data.value == 100.0
    assert result.data.unit == "count"

def test_basic_trace_creation():
    """Test basic trace creation works."""
    result = flext_create_trace("test_operation", "test_service")

    assert result.success
    assert result.data.operation_name == "test_operation"
    assert result.data.service_name == "test_service"

@flext_monitor_function("test_function")
def monitored_test_function():
    """Test function with monitoring."""
    return {"status": "success"}

def test_function_monitoring():
    """Test function monitoring works."""
    result = monitored_test_function()
    assert result["status"] == "success"

if __name__ == "__main__":
    test_basic_metric_creation()
    test_basic_trace_creation()
    test_function_monitoring()
    print("✅ All observability integration tests passed!")
```

### Run Tests

```bash
# Run your integration test
python test_observability_integration.py

# Expected output:
# ✅ All observability integration tests passed!
```

## 📊 Verify Integration

### Check Quality Gates

```bash
# Ensure your integration passes FLEXT quality standards
make check    # Lint + type check + test
make validate # Complete validation including security
```

### Monitor Integration

Create a simple monitoring dashboard:

```python
from flext_observability import FlextObservabilityMasterFactory

def display_observability_status():
    """Display current observability status."""
    factory = FlextObservabilityMasterFactory()

    # Create some sample observability data
    metrics = [
        factory.create_metric("cpu_usage", 75.2, "percent"),
        factory.create_metric("memory_usage", 1024, "MB"),
        factory.create_metric("active_connections", 15, "connections")
    ]

    print("📊 FLEXT Observability Status:")
    print("=" * 40)

    for metric_result in metrics:
        if metric_result.success:
            m = metric_result.data
            print(f"📈 {m.name}: {m.value} {m.unit}")
        else:
            print(f"❌ Failed to create metric: {metric_result.error}")

if __name__ == "__main__":
    display_observability_status()
```

## 🔄 Next Steps

### For Basic Usage

- **[Entity Patterns](entity-patterns.md)**: Learn detailed entity usage patterns
- **[Basic Usage Examples](../examples/basic-usage.md)**: More comprehensive examples

### For Advanced Integration

- **[Service Layer Guide](service-layer.md)**: Deep dive into service patterns
- **[Factory Patterns](factory-patterns.md)**: Advanced entity creation patterns

### For FLEXT Ecosystem Integration

- **[Ecosystem Integration](../examples/ecosystem-integration.md)**: Cross-project patterns
- **[Architecture Overview](../architecture/README.md)**: Understand the full architecture

## 🚨 Common Issues & Solutions

### ImportError: No module named 'flext_observability'

```bash
# Solution: Verify installation
poetry show flext-observability
# or
pip list | grep flext-observability
```

### Type checking errors with MyPy

```bash
# Solution: Ensure proper type imports
from flext_observability import FlextMetric
from flext_core import FlextResult

# Use proper typing
def create_metric() -> FlextResult[FlextMetric]:
    return flext_create_metric("test", 1.0, "count")
```

### FlextResult pattern confusion

```python
# ❌ Wrong: Directly accessing data without checking success
result = flext_create_metric("test", 1.0, "count")
metric = result.data  # May fail if result contains error

# ✅ Correct: Always check success first
result = flext_create_metric("test", 1.0, "count")
if result.success:
    metric = result.data  # Safe to access
else:
    print(f"Error: {result.error}")
```

---

**Congratulations!** You've successfully integrated FLEXT Observability into your project. You're now ready to implement comprehensive monitoring patterns across your FLEXT ecosystem service.

**Next recommended reading**: [Entity Patterns Guide](entity-patterns.md) for detailed entity usage patterns.
