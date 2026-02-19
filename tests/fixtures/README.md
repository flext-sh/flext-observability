# Test Fixtures Directory


<!-- TOC START -->
- [Purpose](#purpose)
- [Organization](#organization)
  - [Planned Structure](#planned-structure)
- [Fixture Categories](#fixture-categories)
  - [Entity Test Fixtures](#entity-test-fixtures)
  - [Service Mock Fixtures](#service-mock-fixtures)
  - [Test Data Factories](#test-data-factories)
- [Usage Patterns](#usage-patterns)
  - [Using Fixtures in Tests](#using-fixtures-in-tests)
  - [Fixture Composition](#fixture-composition)
- [Test Environment Setup](#test-environment-setup)
  - [Shared Configuration](#shared-configuration)
  - [Cleanup Fixtures](#cleanup-fixtures)
- [Current Status](#current-status)
<!-- TOC END -->

**Shared test fixtures and utilities for FLEXT Observability testing.**

## Purpose

This directory is designated for shared test fixtures that:

- Provide consistent test data across all test types (unit, integration, e2e)
- Create reusable mock objects and test doubles
- Setup common test environments and configurations
- Maintain test data consistency and reduce duplication

## Organization

### Planned Structure

```
fixtures/
├── README.md                    # This file
├── observability_fixtures.py    # Core observability test fixtures
├── entity_fixtures.py           # Test data for domain entities
├── service_fixtures.py          # Mock services and dependencies
├── container_fixtures.py        # FlextContainer test configurations
├── mock_external_systems.py     # External system mocks
└── test_data_factories.py       # Test data factory functions
```

## Fixture Categories

### Entity Test Fixtures

```python
# Example entity fixtures
@pytest.fixture
def sample_metric() -> FlextMetric:
    """Provide consistent test metric."""
    return FlextMetric(
        name="test_metric",
        value=42.0,
        unit="count",
        tags={"environment": "test"}
    )

@pytest.fixture
def sample_trace() -> FlextTrace:
    """Provide consistent test trace."""
    return FlextTrace(
        operation_name="test_operation",
        service_name="test_service",
        context={"test": True}
    )
```

### Service Mock Fixtures

```python
# Example service mocks
@pytest.fixture
def mock_metrics_service() -> Mock:
    """Mock metrics service for testing."""
    mock_service = Mock(spec=FlextMetricsService)
    mock_service.record_metric.return_value = FlextResult[bool].ok(sample_metric())
    return mock_service

@pytest.fixture
def mock_container() -> Mock:
    """Mock FlextContainer for service testing."""
    mock_container = Mock(spec=FlextContainer)
    return mock_container
```

### Test Data Factories

```python
# Example test data factories
class MetricsTestDataFactory:
    """Factory for creating test metrics data."""

    @staticmethod
    def create_api_metric(value: float = 1.0) -> FlextMetric:
        """Create API request metric for testing."""
        return FlextMetric(
            name="api_requests",
            value=value,
            unit="count",
            tags={"service": "test-api"}
        )

    @staticmethod
    def create_performance_metric(response_time: float = 100.0) -> FlextMetric:
        """Create performance metric for testing."""
        return FlextMetric(
            name="response_time",
            value=response_time,
            unit="milliseconds",
            tags={"endpoint": "/test"}
        )
```

## Usage Patterns

### Using Fixtures in Tests

```python
def test_metric_processing(sample_metric, mock_metrics_service):
    """Test using shared fixtures."""
    result = mock_metrics_service.record_metric(sample_metric)
    assert result.success
    assert result.data.name == "test_metric"

def test_with_factory_data():
    """Test using factory-created data."""
    metric = MetricsTestDataFactory.create_api_metric(value=5.0)
    assert metric.value == 5.0
    assert metric.name == "api_requests"
```

### Fixture Composition

```python
@pytest.fixture
def configured_observability_platform(mock_container):
    """Compose fixtures for complex testing scenarios."""
    platform = FlextObservabilityPlatformV2(mock_container)
    return platform
```

## Test Environment Setup

### Shared Configuration

```python
@pytest.fixture(scope="session")
def test_config():
    """Shared test configuration."""
    return {
        "metrics_retention": "1h",
        "trace_sampling": 1.0,  # 100% sampling for tests
        "log_level": "DEBUG"
    }
```

### Cleanup Fixtures

```python
@pytest.fixture(autouse=True)
def cleanup_test_state():
    """Automatic cleanup after each test."""
    yield
    # Cleanup code here
    clear_test_metrics()
    reset_test_state()
```

## Current Status

**Status**: Directory created, fixtures to be organized from conftest.py · 1.0.0 Release Preparation
**Next Steps**: Move shared fixtures from conftest.py to organized fixture modules

---

**Note**: This directory is currently empty. Shared fixtures and test utilities will be organized here to improve test maintainability and reduce duplication across the test suite.
