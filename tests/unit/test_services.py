"""Unit tests for flext_observability.services module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_observability import FlextObservabilityServices


class TestFlextObservabilityServices:
    """Test the unified FlextObservabilityServices class."""

    def test_inherits_from_flext_utilities(self) -> None:
        """Test that FlextObservabilityServices inherits from FlextUtilities."""
        from flext_core import FlextUtilities

        assert issubclass(FlextObservabilityServices, FlextUtilities)

    def test_domain_constants(self) -> None:
        """Test domain constants are properly defined."""
        assert FlextObservabilityServices.MAX_TRACE_DURATION == 3600.0
        assert FlextObservabilityServices.MAX_METRIC_NAME_LENGTH == 255
        assert FlextObservabilityServices.MAX_ALERT_MESSAGE_LENGTH == 1000
        assert FlextObservabilityServices.DEFAULT_HEALTH_CHECK_INTERVAL == 30.0
        assert FlextObservabilityServices.MAX_SPAN_COUNT_PER_TRACE == 1000
        assert FlextObservabilityServices.MIN_PERCENTILE == 0.0
        assert FlextObservabilityServices.MAX_PERCENTILE == 100.0

    def test_metrics_storage_initialization(self) -> None:
        """Test metrics storage is initialized."""
        assert isinstance(FlextObservabilityServices._metrics_counters, dict)
        assert isinstance(FlextObservabilityServices._metrics_gauges, dict)
        assert isinstance(FlextObservabilityServices._metrics_histograms, dict)
        assert isinstance(FlextObservabilityServices._metrics_metadata, dict)

    def test_thread_safety_storage(self) -> None:
        """Test thread safety mechanisms are in place."""
        # Test that storage attributes exist for thread safety
        assert hasattr(FlextObservabilityServices, "_metrics_lock")
        assert hasattr(FlextObservabilityServices, "_traces_lock")
        assert hasattr(FlextObservabilityServices, "_alerts_lock")
        assert hasattr(FlextObservabilityServices, "_health_lock")

    def test_metrics_operations_exist(self) -> None:
        """Test key metrics operations are available."""
        operations = [
            "record_metric",
            "get_metric",
            "list_metrics",
            "delete_metric",
            "update_metric",
            "increment_counter",
            "set_gauge",
            "observe_histogram",
        ]
        for operation in operations:
            assert hasattr(FlextObservabilityServices, operation)
            assert callable(getattr(FlextObservabilityServices, operation))

    def test_tracing_operations_exist(self) -> None:
        """Test key tracing operations are available."""
        operations = [
            "start_trace",
            "complete_trace",
            "fail_trace",
            "add_span",
            "get_trace",
            "list_traces",
            "delete_trace",
        ]
        for operation in operations:
            assert hasattr(FlextObservabilityServices, operation)
            assert callable(getattr(FlextObservabilityServices, operation))

    def test_alerting_operations_exist(self) -> None:
        """Test key alerting operations are available."""
        operations = [
            "create_alert",
            "process_alert",
            "escalate_alert",
            "resolve_alert",
            "get_alert",
            "list_alerts",
            "delete_alert",
        ]
        for operation in operations:
            assert hasattr(FlextObservabilityServices, operation)
            assert callable(getattr(FlextObservabilityServices, operation))

    def test_health_operations_exist(self) -> None:
        """Test key health operations are available."""
        operations = [
            "execute_health_check",
            "register_health_check",
            "unregister_health_check",
            "get_health_status",
            "list_health_checks",
            "update_health_check",
        ]
        for operation in operations:
            assert hasattr(FlextObservabilityServices, operation)
            assert callable(getattr(FlextObservabilityServices, operation))

    def test_logging_operations_exist(self) -> None:
        """Test key logging operations are available."""
        operations = [
            "log_entry",
            "get_log_entries",
            "search_logs",
            "delete_logs",
            "export_logs",
        ]
        for operation in operations:
            assert hasattr(FlextObservabilityServices, operation)
            assert callable(getattr(FlextObservabilityServices, operation))

    def test_utility_operations_exist(self) -> None:
        """Test utility operations are available."""
        operations = [
            "calculate_percentile",
            "aggregate_metrics",
            "validate_trace_duration",
            "sanitize_metric_name",
            "format_timestamp",
        ]
        for operation in operations:
            assert hasattr(FlextObservabilityServices, operation)
            assert callable(getattr(FlextObservabilityServices, operation))


class TestFlextObservabilityUtilities:
    """Test the nested FlextObservabilityUtilities class."""

    def test_utilities_class_exists(self) -> None:
        """Test that FlextObservabilityUtilities class exists."""
        assert hasattr(FlextObservabilityServices, "FlextObservabilityUtilities")

    def test_utilities_inherits_from_flext_utilities(self) -> None:
        """Test that FlextObservabilityUtilities inherits from FlextUtilities."""
        from flext_core import FlextUtilities

        assert issubclass(
            FlextObservabilityServices.FlextObservabilityUtilities, FlextUtilities
        )


class TestFlextObservabilityService:
    """Test the FlextObservabilityService alias."""

    def test_service_alias_exists(self) -> None:
        """Test that FlextObservabilityService alias exists."""
        # This should be an alias to FlextObservabilityServices
        assert FlextObservabilityServices.FlextObservabilityService is not None
