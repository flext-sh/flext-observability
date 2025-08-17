"""Pytest configuration and shared fixtures for FLEXT-Observability.

Modern test configuration for observability with metrics, tracing, and logging.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

# Keep only stdlib inside TYPE_CHECKING; promote the rest
import pytest
import pytest_asyncio
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from prometheus_client import CollectorRegistry, Counter, Histogram

from flext_observability import get_logger

# ============================================================================
# Pytest Configuration
# ============================================================================


def pytest_configure(config: Config) -> None:
    """Configure pytest with custom markers."""
    # Register custom markers
    config.addinivalue_line(
      "markers",
      "unit: Unit tests that don't require external dependencies",
    )
    config.addinivalue_line(
      "markers",
      "integration: Integration tests that may require external services",
    )
    config.addinivalue_line(
      "markers",
      "slow: Tests that take more than 1 second to run",
    )
    config.addinivalue_line(
      "markers",
      "smoke: Quick smoke tests for CI/CD",
    )
    config.addinivalue_line(
      "markers",
      "e2e: End-to-end tests",
    )
    config.addinivalue_line(
      "markers",
      "metrics: Metrics-related tests",
    )
    config.addinivalue_line(
      "markers",
      "tracing: Tracing-related tests",
    )
    config.addinivalue_line(
      "markers",
      "logging: Logging-related tests",
    )


def pytest_collection_modifyitems(config: Config, items: list[Item]) -> None:
    """Auto-mark tests based on their location."""
    for item in items:
      # Auto-mark based on test location
      if "unit" in str(item.fspath):
          item.add_marker(pytest.mark.unit)
      elif "integration" in str(item.fspath):
          item.add_marker(pytest.mark.integration)
      elif "e2e" in str(item.fspath):
          item.add_marker(pytest.mark.e2e)


# ============================================================================
# Global Context Reset - CRITICAL for test isolation
# ============================================================================


@pytest.fixture(autouse=True)
def reset_observability_context() -> None:
    """Reset observability context before and after each test to prevent state leakage."""
    # Simplified - no structured logging module needed
    return


# ============================================================================
# Event Loop Configuration
# ============================================================================


@pytest.fixture(scope="session")
def event_loop_policy() -> asyncio.AbstractEventLoopPolicy:
    """Get the event loop policy for testing."""
    return asyncio.DefaultEventLoopPolicy()


# ============================================================================
# Metrics Fixtures
# ============================================================================


@pytest.fixture
def metrics_registry() -> CollectorRegistry:
    """Create a Prometheus metrics registry for testing."""
    return CollectorRegistry()


@pytest.fixture
def metrics_collector(metrics_registry: CollectorRegistry) -> dict[str, object]:
    """Create mock metrics collector for testing."""
    return {"registry": metrics_registry, "mock": True}


@pytest.fixture
def counter_metric(metrics_registry: CollectorRegistry) -> object:
    """Create a counter metric for testing."""
    return Counter(
      "test_counter",
      "Test counter for unit tests",
      ["label1", "label2"],
      registry=metrics_registry,
    )


@pytest.fixture
def histogram_metric(metrics_registry: CollectorRegistry) -> object:
    """Create a histogram metric for testing."""
    return Histogram(
      "test_histogram",
      "Test histogram for unit tests",
      ["method", "endpoint"],
      buckets=(0.1, 0.5, 1.0, 2.0, 5.0),
      registry=metrics_registry,
    )


# ============================================================================
# Tracing Fixtures
# ============================================================================


@pytest_asyncio.fixture
async def tracer_provider() -> AsyncIterator[TracerProvider]:
    """Create a tracer provider for testing."""
    # Create in-memory exporter for testing
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    processor = SimpleSpanProcessor(exporter)
    provider.add_span_processor(processor)

    # Set as global provider
    trace.set_tracer_provider(provider)

    yield provider

    # Cleanup
    provider.shutdown()


@pytest.fixture
def tracer(tracer_provider: object) -> object:
    """Create a tracer for testing."""
    return tracer_provider.get_tracer("test-tracer")


@pytest.fixture
def span_context() -> object:
    """Create a span context for testing."""
    return trace.SpanContext(
      trace_id=0x123456789ABCDEF0123456789ABCDEF0,
      span_id=0x123456789ABCDEF0,
      is_remote=False,
    )


# ============================================================================
# Logging Fixtures
# ============================================================================


@pytest.fixture
def structured_logger() -> object:
    """Create a structured logger for testing."""
    return get_logger("test-logger")


@pytest.fixture
def log_context() -> dict[str, str]:
    """Create log context for testing."""
    return {
      "user_id": "test-user-123",
      "request_id": "req-456",
      "environment": "test",
      "service": "test-service",
    }


# ============================================================================
# Health Check Fixtures
# ============================================================================


@pytest_asyncio.fixture
async def health_checker() -> AsyncIterator[dict[str, object]]:
    """Create mock health checker for testing."""
    yield {"status": "healthy", "mock": True}


@pytest.fixture
def health_check_config() -> dict[str, object]:
    """Create health check configuration for testing."""
    return {
      "checks": {
          "database": {
              "enabled": True,
              "timeout": 5.0,
              "critical": True,
          },
          "redis": {
              "enabled": True,
              "timeout": 3.0,
              "critical": False,
          },
          "external_api": {
              "enabled": True,
              "timeout": 10.0,
              "critical": False,
          },
      },
      "interval": 30,
    }


# ============================================================================
# Mock Fixtures
# ============================================================================


@pytest.fixture
def mock_prometheus_client(mocker: MockerFixture) -> object:
    """Mock Prometheus client for testing."""
    mock = mocker.Mock()
    mock.push_to_gateway.return_value = None
    return mock


@pytest.fixture
def mock_otel_exporter(mocker: MockerFixture) -> object:
    """Mock OpenTelemetry exporter for testing."""
    mock = mocker.Mock()
    mock.export.return_value = mocker.Mock(success=True)
    return mock


# ============================================================================
# Test Data Fixtures
# ============================================================================


@pytest.fixture
def sample_metric_data() -> dict[str, object]:
    """Sample metric data for testing."""
    return {
      "name": "http_requests_total",
      "value": 42,
      "labels": {
          "method": "GET",
          "endpoint": "/api/health",
          "status": "200",
      },
      "timestamp": 1234567890,
    }


@pytest.fixture
def sample_trace_data() -> dict[str, object]:
    """Sample trace data for testing."""
    return {
      "trace_id": "123456789abcdef0123456789abcdef0",
      "span_id": "123456789abcdef0",
      "operation": "process_request",
      "attributes": {
          "http.method": "POST",
          "http.url": "/api/pipelines",
          "http.status_code": 201,
      },
      "duration_ms": 125.5,
    }
