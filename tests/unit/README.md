# Unit Tests Directory

**Fast, isolated unit tests for individual FLEXT Observability components.**

## Purpose

This directory is designated for unit tests that:

- Test individual functions, classes, and methods in isolation
- Execute quickly (< 1 second per test)
- Have no external dependencies (databases, networks, file systems)
- Use mocking for all external interactions
- Focus on business logic and domain validation

## Organization

### Planned Structure

```
unit/
├── README.md                    # This file
├── test_entities_unit.py        # Domain entity unit tests
├── test_services_unit.py        # Service layer unit tests
├── test_factory_unit.py         # Factory pattern unit tests
├── test_validation_unit.py      # Domain validation unit tests
├── test_simple_api_unit.py
└── test_utilities_unit.py       # Utility function unit tests
```

## Test Patterns

### Domain Entity Testing

```python
def test_flext_metric_domain_validation():
    """Test domain validation in isolation."""
    metric = FlextMetric(name="test_metric", value=42.0, unit="count")
    validation_result = metric.validate_business_rules()
    assert validation_result.success
```

### Service Layer Testing

```python
@pytest.fixture
def mock_container():
    """Mock container for service testing."""
    return Mock(spec=FlextContainer)

def test_metrics_service_record_metric(mock_container):
    """Test service logic without external dependencies."""
    service = FlextMetricsService(mock_container)
    # Test logic here
```

## Execution

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run unit tests with coverage
pytest tests/unit/ --cov=src/flext_observability --cov-report=term-missing

# Run specific unit test file
pytest tests/unit/test_entities_unit.py -v
```

## Current Status

**Status**: Directory created, tests to be organized from main test directory · 1.0.0 Release Preparation
**Next Steps**: Move isolated unit tests from root test directory to maintain proper separation

---

**Note**: This directory is currently empty as unit tests are located in the root tests directory. As part of test organization improvements, relevant unit tests will be moved here to maintain proper separation of test types.
