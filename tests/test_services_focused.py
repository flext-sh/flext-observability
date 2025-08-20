"""Focused test to push services.py coverage over 90% threshold.

Target specific uncovered lines to reach 90%+ total coverage.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_observability import FlextMetricsService, flext_create_metric


class TestServicesFocused:
    """Focused tests to reach 90%+ coverage."""

    def test_metrics_service_reset_metrics(self) -> None:
        """Test reset_metrics method (covers lines 226-241)."""
        service = FlextMetricsService()

        # Record some metrics first
        metric_result = flext_create_metric("test_metric", 100.0)
        assert metric_result.success
        service.record_metric(metric_result.data)

        # Reset metrics
        result = service.reset_metrics()

        assert result.success

    def test_metrics_service_export_prometheus_simple(self) -> None:
        """Test export_prometheus_format method (covers lines 193-224)."""
        service = FlextMetricsService()

        # Record a simple metric
        metric_result = flext_create_metric("simple_metric", 42.0)
        assert metric_result.success
        service.record_metric(metric_result.data)

        # Export in Prometheus format
        result = service.export_prometheus_format()

        assert result.success
        prometheus_output = result.data
        assert "simple_metric" in prometheus_output

    def test_metrics_service_get_value_paths(self) -> None:
        """Test get_metric_value method paths (covers lines 140-162)."""
        service = FlextMetricsService()

        # Test with recorded metric
        metric_result = flext_create_metric("test_gauge", 75.0)
        assert metric_result.success
        service.record_metric(metric_result.data)

        # Get metric value
        result = service.get_metric_value("test_gauge")
        assert result.success

        # Test with non-existent metric
        result = service.get_metric_value("nonexistent")
        assert result.is_failure

    def test_metrics_service_summary_with_data(self) -> None:
        """Test get_metrics_summary with actual data (covers lines 164-191)."""
        service = FlextMetricsService()

        # Record multiple metrics
        for i in range(3):
            metric_result = flext_create_metric(f"metric_{i}", float(i * 10))
            assert metric_result.success
            service.record_metric(metric_result.data)

        # Get summary
        result = service.get_metrics_summary()

        assert result.success
        summary = result.data
        assert isinstance(summary, dict)
        assert "service_info" in summary
        service_info = summary["service_info"]
        assert isinstance(service_info, dict)
        assert service_info["metrics_recorded"] == 3
