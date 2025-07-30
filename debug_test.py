#!/usr/bin/env python3

"""Debug script to understand test failure."""

from unittest.mock import Mock

from flext_core import FlextContainer, FlextResult

from flext_observability import FlextMetricsService


def test_debug() -> None:
    """Debug the test failure."""
    # Create container and service
    container = FlextContainer()
    metrics_service = FlextMetricsService(container=container)

    # Create mock metric
    sample_metric = Mock()
    sample_metric.name = "test_metric"
    sample_metric.value = 42.0
    sample_metric.unit = "count"

    # Create mock repository
    mock_repository = Mock()
    mock_repository.save.return_value = FlextResult.ok(sample_metric)

    # Register repository
    container.register("metrics_repository", mock_repository)

    # Verify registration worked
    container.get("metrics_repository")

    # Test domain service (should not exist)
    container.get("metrics_domain_service")

    # Execute the service method
    metrics_service.record_metric(sample_metric)

    # Check if save was called


if __name__ == "__main__":
    test_debug()
