"""Pytest configuration and shared fixtures for FLEXT-Observability.

Modern test configuration for observability with metrics, tracing, and logging.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

import pytest
import pytest_asyncio

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from _pytest.config import Config
    from _pytest.nodes import Item
    from prometheus_client import CollectorRegistry


# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


# ============================================================================
# Pytest Configuration
# ============================================================================


def pytest_configure(config: Config) -> None:
    """Configure pytest with custom markers and settings."""
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
    """Automatically mark tests based on their location."""
    for item in items:
        # Auto-mark based on test location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)


# ============================================================================
# Event Loop Configuration
# ============================================================================


@pytest.fixture(scope="session")
def event_loop_policy() -> asyncio.AbstractEventLoopPolicy:
    """Use the default asyncio event loop policy."""
    return asyncio.DefaultEventLoopPolicy()


# ============================================================================
# Metrics Fixtures
# ============================================================================


@pytest.fixture
def metrics_registry() -> CollectorRegistry:
    """Create isolated metrics registry for testing."""
    from prometheus_client import CollectorRegistry

    return CollectorRegistry()


@pytest.fixture
def metrics_collector(metrics_registry: CollectorRegistry) -> Any:
    """Create metrics collector with test registry."""
    from flext_observability.metrics import MetricsCollector

    return MetricsCollector(registry=metrics_registry)


@pytest.fixture
def counter_metric(metrics_registry: CollectorRegistry) -> Any:
    """Create test counter metric."""
    from prometheus_client import Counter

    return Counter(
        "test_counter",
        "Test counter for unit tests",
        ["label1", "label2"],
        registry=metrics_registry,
    )


@pytest.fixture
def histogram_metric(metrics_registry: CollectorRegistry) -> Any:
    """Create test histogram metric."""
    from prometheus_client import Histogram

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
async def tracer_provider() -> AsyncIterator[Any]:
    """Create test tracer provider."""
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

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
def tracer(tracer_provider: Any) -> Any:
    """Create test tracer."""
    return tracer_provider.get_tracer("test-tracer")


@pytest.fixture
def span_context() -> Any:
    """Create test span context."""
    from opentelemetry import trace

    return trace.SpanContext(
        trace_id=0x123456789ABCDEF0123456789ABCDEF0,
        span_id=0x123456789ABCDEF0,
        is_remote=False,
    )


# ============================================================================
# Logging Fixtures
# ============================================================================


@pytest.fixture
def structured_logger() -> Any:
    """Create structured logger for testing."""
    from flext_observability.logging import create_structured_logger

    return create_structured_logger(
        name="test-logger",
        level="DEBUG",
        testing=True,
    )


@pytest.fixture
def log_context() -> dict[str, Any]:
    """Provide standard log context."""
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
async def health_checker() -> AsyncIterator[Any]:
    """Create health checker for testing."""
    from flext_observability.health import HealthChecker

    checker = HealthChecker()
    yield checker

    # Cleanup
    await checker.shutdown()


@pytest.fixture
def health_check_config() -> dict[str, Any]:
    """Health check configuration."""
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
def mock_prometheus_client(mocker: Any) -> Any:
    """Mock Prometheus client."""
    mock = mocker.Mock()
    mock.push_to_gateway.return_value = None
    return mock


@pytest.fixture
def mock_otel_exporter(mocker: Any) -> Any:
    """Mock OpenTelemetry exporter."""
    mock = mocker.Mock()
    mock.export.return_value = mocker.Mock(success=True)
    return mock


# ============================================================================
# Test Data Fixtures
# ============================================================================


@pytest.fixture
def sample_metric_data() -> dict[str, Any]:
    """Sample metric data."""
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
def sample_trace_data() -> dict[str, Any]:
    """Sample trace data."""
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
