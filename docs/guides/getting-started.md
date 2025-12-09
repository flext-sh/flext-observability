# Getting Started with FLEXT Observability

## Table of Contents

- [Getting Started with FLEXT Observability](#getting-started-with-flext-observability)
  - [🎯 Prerequisites](#-prerequisites)
    - [FLEXT Ecosystem Requirements](#flext-ecosystem-requirements)
    - [Development Environment](#development-environment)
- [Verify Python version](#verify-python-version)
- [Verify Poetry installation](#verify-poetry-installation)
- [Verify you're in a FLEXT ecosystem project](#verify-youre-in-a-flext-ecosystem-project)
  - [🚀 Installation](#-installation)
    - [Via Poetry (Recommended for FLEXT Projects)](#via-poetry-recommended-for-flext-projects)
- [Add flext-observability to your FLEXT project](#add-flext-observability-to-your-flext-project)
- [Install development dependencies if contributing](#install-development-dependencies-if-contributing)
- [Verify installation](#verify-installation)
  - [Via pip (Alternative)](#via-pip-alternative)
- [Direct installation](#direct-installation)
- [Verify installation](#verify-installation)
  - [🏁 First Observability Integration](#-first-observability-integration)
    - [1. Basic Metric Creation](#1-basic-metric-creation)
- [Create a simple metric](#create-a-simple-metric)
  - [2. Basic Trace Creation](#2-basic-trace-creation)
- [Create a trace for an operation](#create-a-trace-for-an-operation)
  - [3. Function Monitoring Decorator](#3-function-monitoring-decorator)
- [Use the function normally - monitoring happens automatically](#use-the-function-normally---monitoring-happens-automatically)
  - [🏛️ Service Layer Integration](#-service-layer-integration)
    - [Using Services with Dependency Injection](#using-services-with-dependency-injection)
- [Initialize dependency injection container](#initialize-dependency-injection-container)
- [Create observability services](#create-observability-services)
- [Create and record a metric](#create-and-record-a-metric)
  - [🔧 Integration Patterns](#-integration-patterns)
    - [Pattern 1: FLEXT Service Integration](#pattern-1-flext-service-integration)
- [In your FLEXT service initialization](#in-your-flext-service-initialization)
  - [Pattern 2: Infrastructure Service Integration](#pattern-2-infrastructure-service-integration)
  - [Pattern 3: Singer Ecosystem Integration](#pattern-3-singer-ecosystem-integration)
  - [🧪 Testing Your Integration](#-testing-your-integration)
    - [Create Test File](#create-test-file)
    - [Run Tests](#run-tests)
- [Run your integration test](#run-your-integration-test)
- [Expected output:](#expected-output)
- [✅ All observability integration tests passed!](#-all-observability-integration-tests-passed)
  - [📊 Verify Integration](#-verify-integration)
    - [Check Quality Gates](#check-quality-gates)
- [Ensure your integration passes FLEXT quality standards](#ensure-your-integration-passes-flext-quality-standards)
  - [Monitor Integration](#monitor-integration)
  - [🔄 Next Steps](#-next-steps)
    - [For Basic Usage](#for-basic-usage)
    - [For Advanced Integration](#for-advanced-integration)
    - [For FLEXT Ecosystem Integration](#for-flext-ecosystem-integration)
  - [🚨 Common Issues & Solutions](#-common-issues--solutions)
    - [ImportError: No module named 'flext_observability'](#importerror-no-module-named-flext_observability)
- [Solution: Verify installation](#solution-verify-installation)
- [or](#or)
  - [Type checking errors with MyPy](#type-checking-errors-with-mypy)
- [Solution: Ensure proper type imports](#solution-ensure-proper-type-imports)
- [Use proper typing](#use-proper-typing)
  - [FlextResult pattern confusion](#flextresult-pattern-confusion)
- [❌ Wrong: Directly accessing data without checking success](#-wrong-directly-accessing-data-without-checking-success)
- [✅ Correct: Always check success first](#-correct-always-check-success-first)

**Quick Start Guide for Integrating Observability Patterns in FLEXT Projects**

This guide will walk you through the essential steps to integrate FLEXT Observability into your FLEXT ecosystem project,
from installation to your first working observability implementation.

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
def process_user_data(user_id: str, data: dict) -> dict[str, object]:
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

class UserService:
    @flext_monitor_function("user_service_create")
    def create_user(self, user_data: dict) -> FlextResult[t.Dict]:
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

class DatabaseConnectionService:
    def __init__(self):
        self.container = FlextContainer()
        self.health_service = FlextHealthService(self.container)

    def check_database_health(self) -> FlextResult[t.Dict]:
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

class FlextMeltanoTapOracle:
    @flext_monitor_function("tap_oracle_extract")
    def extract_records(self, table_name: str) -> list[t.Dict]:
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

- **Basic Usage Examples**: More comprehensive examples (_Documentation coming soon_)

### For Advanced Integration

- **Service Layer Guide**: Deep dive into service patterns (_Documentation coming soon_)
- **Factory Patterns**: Advanced entity creation patterns (_Documentation coming soon_)

### For FLEXT Ecosystem Integration

- **Ecosystem Integration**: Cross-project patterns (_Documentation coming soon_)
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

**Next recommended reading**: Entity Patterns Guide (_Documentation coming soon_) for detailed entity usage patterns.
