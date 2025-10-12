# Integration Tests Directory

**Integration tests for FLEXT Observability component interactions and external system integration.**

## Purpose

This directory is designated for integration tests that:

- Test interactions between multiple FLEXT Observability components
- Validate integration with external systems (flext-core, databases, etc.)
- Execute with moderate speed (< 10 seconds per test)
- Use real implementations with controlled test environments
- Focus on component interaction and data flow validation

## Organization

### Planned Structure

```
integration/
├── README.md                        # This file
├── test_service_integration.py      # Service layer integration tests
├── test_factory_service_integration.py  # Factory-Service interaction tests
├── test_platform_integration.py     # Platform orchestration tests
├── test_flext_core_integration.py   # flext-core integration tests
├── test_monitoring_integration.py   # End-to-end monitoring workflow tests
└── test_external_systems.py         # External system integration tests
```

## Test Patterns

### Service Integration Testing

```python
def test_metrics_service_with_factory_integration():
    """Test metrics service integration with factory."""
    container = FlextCore.Container()
    factory = FlextObservabilityMasterFactory(container)
    metrics_service = FlextMetricsService(container)

    # Create metric via factory
    metric_result = factory.create_metric("integration_test", 42.0)
    assert metric_result.success

    # Process via service
    record_result = metrics_service.record_metric(metric_result.data)
    assert record_result.success
```

### External System Integration

```python
def test_flext_core_container_integration():
    """Test integration with flext-core dependency injection."""
from flext_core import FlextCore

    container = FlextCore.Container()
    # Test that observability services integrate properly
    factory = FlextObservabilityMasterFactory(container)
    assert factory.container is container
```

## Test Environment Setup

### Required Dependencies

- **flext-core**: Foundation library integration
- **Test Containers**: Isolated test environments
- **Mock External Systems**: Controlled external dependencies

### Configuration

```python
@pytest.fixture(scope="module")
def integration_container():
    """Shared container for integration tests."""
    container = FlextCore.Container()
    # Setup integration-specific services
    return container
```

## Execution

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run integration tests with coverage
pytest tests/integration/ --cov=src/flext_observability --cov-report=term-missing

# Run specific integration test
pytest tests/integration/test_service_integration.py -v

# Run integration tests with slow marker
pytest tests/integration/ -m integration -v
```

## Test Data Management

### Test Data Strategy

- **Isolated Test Data**: Each test creates its own test data
- **Cleanup**: Automatic cleanup after each test
- **Reproducible**: Tests can run in any order
- **Realistic**: Test data mirrors production scenarios

## Current Status

**Status**: Directory created, tests to be organized from main test directory · 1.0.0 Release Preparation
**Next Steps**: Move integration-focused tests from root test directory and create new integration tests for component interactions

---

**Note**: This directory is currently empty as integration tests are mixed with unit tests in the root tests directory. As part of test organization improvements, relevant integration tests will be moved here to maintain proper separation of concerns.
