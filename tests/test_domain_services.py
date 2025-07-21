"""Comprehensive tests for domain services - achieving high coverage."""

from __future__ import annotations

from typing import Any
from unittest.mock import Mock

import pytest

from flext_observability.domain.services import (
    AlertingService,
    HealthAnalysisService,
    LogAnalysisService,
    MetricsAnalysisService,
    TraceAnalysisService,
)


class MockMetric:
    """Mock metric class for testing."""

    def __init__(self, name: str, value: float) -> None:
        self.name = name
        self.value = value


class MockThreshold:
    """Mock threshold class for testing."""

    def __init__(self, value: float, operator: str = "gt") -> None:
        self.value = value
        self.operator = operator

    def compare(self, value: float) -> bool:
        """Simple comparison for testing."""
        if self.operator == "gt":
            return value > self.value
        if self.operator == "lt":
            return value < self.value
        if self.operator == "ge":
            return value >= self.value
        if self.operator == "le":
            return value <= self.value
        if self.operator == "eq":
            return value == self.value
        return False


class MockHealthCheck:
    """Mock health check class for testing."""

    def __init__(self, component_name: str, status: str = "healthy") -> None:
        self.component = Mock()
        # Use spec to create a proper mock that supports __str__
        self.component.configure_mock(**{"__str__.return_value": component_name})
        self.status = status


class MockLogEntry:
    """Mock log entry class for testing."""

    def __init__(self, level: str, message: str, is_error: bool = False) -> None:
        self.level = level
        self.message = message
        self.is_error = is_error
        self.exception: str | None = None


class MockTrace:
    """Mock trace class for testing."""

    def __init__(
        self,
        operation_name: str,
        status: str = "completed",
        duration_ms: float = 100.0,
    ) -> None:
        self.operation_name = operation_name
        self.status = status
        self.duration_ms = duration_ms
        self.logs: list[str] = []


class TestAlertingService:
    """Test AlertingService class comprehensively."""

    @pytest.fixture
    def alerting_service(self) -> Any:
        """Create AlertingService instance."""
        return AlertingService()

    def test_init(self, alerting_service: Any) -> None:
        """Test AlertingService initialization."""
        assert alerting_service._alert_rules == {}

    def test_register_alert_rule(self, alerting_service: Any) -> None:
        """Test registering an alert rule."""
        threshold = MockThreshold(80.0, "gt")
        alerting_service.register_alert_rule("cpu_usage", threshold)

        assert "cpu_usage" in alerting_service._alert_rules
        assert alerting_service._alert_rules["cpu_usage"] == threshold

    def test_register_multiple_alert_rules(self, alerting_service: Any) -> None:
        """Test registering multiple alert rules."""
        threshold1 = MockThreshold(80.0, "gt")
        threshold2 = MockThreshold(90.0, "gt")

        alerting_service.register_alert_rule("cpu_usage", threshold1)
        alerting_service.register_alert_rule("memory_usage", threshold2)

        assert len(alerting_service._alert_rules) == 2
        assert alerting_service._alert_rules["cpu_usage"] == threshold1
        assert alerting_service._alert_rules["memory_usage"] == threshold2

    def test_evaluate_metric_no_rule(self, alerting_service: Any) -> None:
        """Test evaluating a metric with no registered rule."""
        metric = MockMetric("unknown_metric", 85.0)
        result = alerting_service.evaluate_metric(metric)

        assert result.is_success
        assert result.data is None

    def test_evaluate_metric_threshold_not_exceeded(
        self,
        alerting_service: Any,
    ) -> None:
        """Test evaluating a metric where threshold is not exceeded."""
        threshold = MockThreshold(90.0, "gt")
        alerting_service.register_alert_rule("cpu_usage", threshold)

        metric = MockMetric("cpu_usage", 85.0)
        result = alerting_service.evaluate_metric(metric)

        assert result.is_success
        assert result.data is None

    def test_evaluate_metric_threshold_exceeded(self, alerting_service: Any) -> None:
        """Test evaluating a metric where threshold is exceeded."""
        threshold = MockThreshold(80.0, "gt")
        alerting_service.register_alert_rule("cpu_usage", threshold)

        metric = MockMetric("cpu_usage", 85.0)
        result = alerting_service.evaluate_metric(metric)

        assert result.is_success
        assert result.data is not None
        assert result.data["title"] == "Metric cpu_usage threshold exceeded"
        assert result.data["severity"] == "medium"
        assert result.data["metric"] == metric
        assert result.data["threshold"] == threshold

    def test_evaluate_metric_exception_handling(self, alerting_service: Any) -> None:
        """Test exception handling in evaluate_metric."""
        # Create a mock threshold that raises an exception
        threshold = Mock()
        threshold.compare.side_effect = ValueError("Test error")

        alerting_service.register_alert_rule("cpu_usage", threshold)
        metric = MockMetric("cpu_usage", 85.0)

        result = alerting_service.evaluate_metric(metric)

        assert not result.is_success
        assert "Failed to evaluate metric: Test error" in result.error


class TestMetricsAnalysisService:
    """Test MetricsAnalysisService class comprehensively."""

    @pytest.fixture
    def metrics_analysis_service(self) -> Any:
        """Create MetricsAnalysisService instance."""
        return MetricsAnalysisService()

    def test_init(self, metrics_analysis_service: Any) -> None:
        """Test MetricsAnalysisService initialization."""
        assert metrics_analysis_service._metric_history == {}

    def test_analyze_trend_first_metric(self, metrics_analysis_service: Any) -> None:
        """Test analyzing trend for the first metric."""
        metric = MockMetric("cpu_usage", 75.0)
        result = metrics_analysis_service.analyze_trend(metric)

        assert result.is_success
        assert result.data["trend"] == "unknown"
        assert result.data["change"] == 0.0
        assert result.data["points"] == 1

        # Verify metric was stored
        assert "cpu_usage" in metrics_analysis_service._metric_history
        assert len(metrics_analysis_service._metric_history["cpu_usage"]) == 1

    def test_analyze_trend_insufficient_data(
        self,
        metrics_analysis_service: Any,
    ) -> None:
        """Test analyzing trend when there's insufficient data."""
        # Add only one metric - should trigger the < 2 check after slicing
        metrics_list = []
        for _i in range(11):  # Add 11 metrics to test the [-10:] slicing
            metric = MockMetric("cpu_usage", 50.0)
            metrics_list.append(metric)
            metrics_analysis_service.analyze_trend(metric)

        # Now create a scenario where we get < 2 recent values after processing
        # We can't easily trigger this since we always add at least 1 metric
        # But we can test an edge case with a single metric in a fresh service
        fresh_service = MetricsAnalysisService()
        metric = MockMetric("cpu_usage", 75.0)
        result = fresh_service.analyze_trend(metric)

        assert result.is_success
        assert result.data is not None
        assert result.data["trend"] == "unknown"
        assert result.data is not None
        assert result.data["change"] == 0.0
        assert result.data is not None
        assert result.data["points"] == 1

    def test_analyze_trend_second_metric(self, metrics_analysis_service: Any) -> None:
        """Test analyzing trend for the second metric."""
        metric1 = MockMetric("cpu_usage", 75.0)
        metric2 = MockMetric("cpu_usage", 85.0)

        metrics_analysis_service.analyze_trend(metric1)
        result = metrics_analysis_service.analyze_trend(metric2)

        assert result.is_success
        # With 2 points, it calculates trend: first_half=[75.0], second_half=[85.0]
        # change = ((85-75)/75)*100 = 13.33%, which is > 5% so trend = "increasing"
        assert result.data["trend"] == "increasing"
        assert result.data["points"] == 2

    def test_analyze_trend_increasing(self, metrics_analysis_service: Any) -> None:
        """Test analyzing trend for increasing metrics."""
        # Add 10 metrics with increasing values
        for i in range(10):
            metric = MockMetric("cpu_usage", 50.0 + i * 5.0)
            metrics_analysis_service.analyze_trend(metric)

        # Add one more to get the trend analysis
        metric = MockMetric("cpu_usage", 100.0)
        result = metrics_analysis_service.analyze_trend(metric)

        assert result.is_success
        assert result.data["trend"] == "increasing"
        assert result.data["change"] > 5  # Should be a significant increase

    def test_analyze_trend_decreasing(self, metrics_analysis_service: Any) -> None:
        """Test analyzing trend for decreasing metrics."""
        # Add 10 metrics with decreasing values
        for i in range(10):
            metric = MockMetric("cpu_usage", 100.0 - i * 5.0)
            metrics_analysis_service.analyze_trend(metric)

        # Add one more to get the trend analysis
        metric = MockMetric("cpu_usage", 45.0)
        result = metrics_analysis_service.analyze_trend(metric)

        assert result.is_success
        assert result.data["trend"] == "decreasing"
        assert result.data["change"] < -5  # Should be a significant decrease

    def test_analyze_trend_stable(self, metrics_analysis_service: Any) -> None:
        """Test analyzing trend for stable metrics."""
        # Add 10 metrics with similar values (small variation)
        for i in range(10):
            metric = MockMetric("cpu_usage", 75.0 + (i % 3) * 0.5)  # Small variation
            metrics_analysis_service.analyze_trend(metric)

        # Add one more to get the trend analysis
        metric = MockMetric("cpu_usage", 75.5)
        result = metrics_analysis_service.analyze_trend(metric)

        assert result.is_success
        assert result.data["trend"] == "stable"
        assert abs(result.data["change"]) < 5  # Should be small change

    def test_analyze_trend_history_limit(self, metrics_analysis_service: Any) -> None:
        """Test that metric history is limited to 100 entries."""
        # Add 150 metrics
        for i in range(150):
            metric = MockMetric("cpu_usage", 50.0 + i)
            metrics_analysis_service.analyze_trend(metric)

        # Should only have 100 metrics stored
        assert len(metrics_analysis_service._metric_history["cpu_usage"]) == 100

    def test_analyze_trend_zero_division_protection(
        self,
        metrics_analysis_service: Any,
    ) -> None:
        """Test protection against zero division."""
        # Add metrics where the first half average will be 0
        # Need exactly 10 metrics so that first_half=[0,0,0,0,0] and
        # second_half=[0,0,0,0,0]
        for _i in range(10):
            metric = MockMetric("cpu_usage", 0.0)
            metrics_analysis_service.analyze_trend(metric)

        # Now add one more metric - this should trigger the zero division protection
        # because all the recent_values[-10:] will be [0,0,0,0,0,0,0,0,0,0]
        # first_half = [0,0,0,0,0] (avg = 0)
        # second_half = [0,0,0,0,0] (avg = 0)
        # Since avg_first is 0, the code should return change = 0
        metric = MockMetric("cpu_usage", 0.0)
        result = metrics_analysis_service.analyze_trend(metric)

        assert result.is_success
        assert result.data["change"] == 0  # Should handle zero division

    def test_analyze_trend_exception_handling(
        self,
        metrics_analysis_service: Any,
    ) -> None:
        """Test exception handling in analyze_trend."""
        # First add some valid metrics to build up history
        for i in range(2):
            valid_metric = MockMetric("test_metric", 50.0 + i)
            metrics_analysis_service.analyze_trend(valid_metric)

        # Now create a mock metric that will cause an exception in the trend calculation
        invalid_metric = Mock()
        invalid_metric.name = "test_metric"
        invalid_metric.value = (
            "invalid"  # This should cause an error when converting to float
        )

        result = metrics_analysis_service.analyze_trend(invalid_metric)

        assert not result.is_success
        assert "Failed to analyze trend" in result.error


class TestHealthAnalysisService:
    """Test HealthAnalysisService class comprehensively."""

    @pytest.fixture
    def health_analysis_service(self) -> Any:
        """Create HealthAnalysisService instance."""
        return HealthAnalysisService()

    def test_init(self, health_analysis_service: Any) -> None:
        """Test HealthAnalysisService initialization."""
        assert health_analysis_service._component_health == {}

    def test_update_component_health_new_component(
        self,
        health_analysis_service: Any,
    ) -> None:
        """Test updating health for a new component."""
        health_check = MockHealthCheck("database", "healthy")
        result = health_analysis_service.update_component_health(health_check)

        assert result.is_success
        assert result.data is True  # Status changed (new component)

        # Verify component was stored
        assert "database" in health_analysis_service._component_health

    def test_update_component_health_same_status(
        self,
        health_analysis_service: Any,
    ) -> None:
        """Test updating health with the same status."""
        health_check1 = MockHealthCheck("database", "healthy")
        health_check2 = MockHealthCheck("database", "healthy")

        health_analysis_service.update_component_health(health_check1)
        result = health_analysis_service.update_component_health(health_check2)

        assert result.is_success
        assert result.data is False  # Status did not change

    def test_update_component_health_status_changed(
        self,
        health_analysis_service: Any,
    ) -> None:
        """Test updating health with changed status."""
        health_check1 = MockHealthCheck("database", "healthy")
        health_check2 = MockHealthCheck("database", "unhealthy")

        health_analysis_service.update_component_health(health_check1)
        result = health_analysis_service.update_component_health(health_check2)

        assert result.is_success
        assert result.data is True  # Status changed

    def test_update_component_health_exception_handling(
        self,
        health_analysis_service: Any,
    ) -> None:
        """Test exception handling in update_component_health."""
        # Create a mock health check that will cause an exception
        health_check = Mock()
        health_check.component.__str__ = Mock(side_effect=ValueError("Test error"))

        result = health_analysis_service.update_component_health(health_check)

        assert not result.is_success
        assert "Failed to update component health: Test error" in result.error

    def test_get_system_health_no_components(
        self,
        health_analysis_service: Any,
    ) -> None:
        """Test getting system health with no components."""
        result = health_analysis_service.get_system_health()

        assert result.is_success
        assert result.data["overall_status"] == "unknown"
        assert result.data["healthy_components"] == 0
        assert result.data["unhealthy_components"] == 0
        assert result.data["total_components"] == 0
        assert result.data["health_score"] == 0.0

    def test_get_system_health_all_healthy(self, health_analysis_service: Any) -> None:
        """Test getting system health with all healthy components."""
        # Add some healthy components
        health_checks = [
            MockHealthCheck("database", "healthy"),
            MockHealthCheck("cache", "healthy"),
            MockHealthCheck("api", "healthy"),
        ]

        for hc in health_checks:
            health_analysis_service.update_component_health(hc)

        result = health_analysis_service.get_system_health()

        assert result.is_success
        assert result.data["overall_status"] == "healthy"
        assert result.data["healthy_components"] == 3
        assert result.data["unhealthy_components"] == 0
        assert result.data["total_components"] == 3
        assert result.data["health_score"] == 1.0

    def test_get_system_health_mixed_status(self, health_analysis_service: Any) -> None:
        """Test getting system health with mixed component statuses."""
        # Add mixed health components
        health_checks = [
            MockHealthCheck("database", "healthy"),
            MockHealthCheck("cache", "healthy"),
            MockHealthCheck("api", "unhealthy"),
            MockHealthCheck("queue", "failed"),
        ]

        for hc in health_checks:
            health_analysis_service.update_component_health(hc)

        result = health_analysis_service.get_system_health()

        assert result.is_success
        assert result.data["overall_status"] == "degraded"  # < 80% healthy
        assert result.data["healthy_components"] == 2
        assert result.data["unhealthy_components"] == 2
        assert result.data["total_components"] == 4
        assert result.data["health_score"] == 0.5

    def test_get_system_health_mostly_healthy(
        self,
        health_analysis_service: Any,
    ) -> None:
        """Test getting system health with mostly healthy components (>80%)."""
        # Add mostly healthy components - need >80% for "healthy" status
        health_checks = [
            MockHealthCheck("database", "healthy"),
            MockHealthCheck("cache", "healthy"),
            MockHealthCheck("api", "healthy"),
            MockHealthCheck("queue", "healthy"),
            # Need 4 healthy out of 4 = 100% to be > 80%
        ]

        for hc in health_checks:
            health_analysis_service.update_component_health(hc)

        result = health_analysis_service.get_system_health()

        assert result.is_success
        assert result.data["overall_status"] == "healthy"  # 100% > 80%
        assert result.data["healthy_components"] == 4
        assert result.data["unhealthy_components"] == 0
        assert result.data["total_components"] == 4
        assert result.data["health_score"] == 1.0

    def test_get_system_health_exactly_80_percent(
        self,
        health_analysis_service: Any,
    ) -> None:
        """Test getting system health with exactly 80% healthy components (should be degraded)."""
        # Add exactly 80% healthy components - should be "degraded" since
        # threshold is > 80%
        health_checks = [
            MockHealthCheck("database", "healthy"),
            MockHealthCheck("cache", "healthy"),
            MockHealthCheck("api", "healthy"),
            MockHealthCheck("queue", "healthy"),
            MockHealthCheck("search", "unhealthy"),  # 4 healthy out of 5 = 80%
        ]

        for hc in health_checks:
            health_analysis_service.update_component_health(hc)

        result = health_analysis_service.get_system_health()

        assert result.is_success
        assert (
            result.data["overall_status"] == "degraded"
        )  # 80% == threshold, needs > 80%
        assert result.data["healthy_components"] == 4
        assert result.data["unhealthy_components"] == 1
        assert result.data["total_components"] == 5
        assert result.data["health_score"] == 0.8

    def test_get_system_health_exception_handling(
        self,
        health_analysis_service: Any,
    ) -> None:
        """Test exception handling in get_system_health."""
        # Add a mock health check that will cause an exception during analysis
        mock_hc = Mock()
        mock_hc.status = Mock()
        mock_hc.status.__str__ = Mock(side_effect=ValueError("Test error"))

        health_analysis_service._component_health["test"] = mock_hc

        result = health_analysis_service.get_system_health()

        assert not result.is_success
        assert "Failed to get system health: Test error" in result.error


class TestLogAnalysisService:
    """Test LogAnalysisService class comprehensively."""

    @pytest.fixture
    def log_analysis_service(self) -> Any:
        """Create LogAnalysisService instance."""
        return LogAnalysisService()

    def test_init(self, log_analysis_service: Any) -> None:
        """Test LogAnalysisService initialization."""
        assert log_analysis_service._error_patterns == {}

    def test_analyze_log_entry_info_level(self, log_analysis_service: Any) -> None:
        """Test analyzing an info level log entry."""
        log_entry = MockLogEntry("INFO", "User logged in successfully")
        result = log_analysis_service.analyze_log_entry(log_entry)

        assert result.is_success
        assert result.data["is_error"] is False
        assert result.data["severity"] == "INFO"
        assert result.data["has_exception"] is False
        assert result.data["patterns"] == []

    def test_analyze_log_entry_error_level(self, log_analysis_service: Any) -> None:
        """Test analyzing an error level log entry."""
        log_entry = MockLogEntry("ERROR", "Database connection failed", is_error=True)
        result = log_analysis_service.analyze_log_entry(log_entry)

        assert result.is_success
        assert result.data["is_error"] is True
        assert result.data["severity"] == "ERROR"
        assert result.data["has_exception"] is False

    def test_analyze_log_entry_with_exception(self, log_analysis_service: Any) -> None:
        """Test analyzing a log entry with exception."""
        log_entry = MockLogEntry("ERROR", "Database connection failed", is_error=True)
        log_entry.exception = "ConnectionError: Unable to connect"

        result = log_analysis_service.analyze_log_entry(log_entry)

        assert result.is_success
        assert result.data is not None
        assert result.data["has_exception"] is True

    def test_analyze_log_entry_with_pattern_extraction(
        self,
        log_analysis_service: Any,
    ) -> None:
        """Test analyzing log entry with pattern extraction."""
        log_entry = MockLogEntry(
            "ERROR",
            "Failed to process order 12345",
            is_error=True,
        )
        result = log_analysis_service.analyze_log_entry(log_entry)

        assert result.is_success
        assert len(result.data["patterns"]) > 0

        # Should extract pattern with number replaced
        pattern = result.data["patterns"][0]
        assert "Failed to process order {number}" in pattern

    def test_analyze_log_entry_exception_handling(
        self,
        log_analysis_service: Any,
    ) -> None:
        """Test exception handling in analyze_log_entry."""
        # Use None to trigger an exception when accessing attributes
        result = log_analysis_service.analyze_log_entry(None)

        assert not result.is_success
        assert "Failed to analyze log entry" in result.error

    def test_extract_error_pattern_numbers(self, log_analysis_service: Any) -> None:
        """Test pattern extraction with numbers."""
        pattern = log_analysis_service._extract_error_pattern(
            "Error processing order 12345",
        )
        assert pattern == "Error processing order {number}"

    def test_extract_error_pattern_uuids(self, log_analysis_service: Any) -> None:
        """Test pattern extraction with UUIDs."""
        pattern = log_analysis_service._extract_error_pattern(
            "Failed to find user 550e8400-e29b-41d4-a716-446655440000",
        )
        # Numbers are replaced first, so UUID gets mangled
        assert "{number}" in pattern

    def test_extract_error_pattern_file_paths(self, log_analysis_service: Any) -> None:
        """Test pattern extraction with file paths."""
        pattern = log_analysis_service._extract_error_pattern(
            "Cannot read file /var/log/app.log",
        )
        assert pattern == "Cannot read file {path}"

    def test_extract_error_pattern_no_change(self, log_analysis_service: Any) -> None:
        """Test pattern extraction when no pattern is found."""
        pattern = log_analysis_service._extract_error_pattern("Simple error message")
        assert pattern is None

    def test_get_error_patterns_empty(self, log_analysis_service: Any) -> None:
        """Test getting error patterns when none exist."""
        result = log_analysis_service.get_error_patterns()

        assert result.is_success
        assert result.data == {}

    def test_get_error_patterns_with_data(self, log_analysis_service: Any) -> None:
        """Test getting error patterns with sorted data."""
        # Manually add some patterns
        log_analysis_service._error_patterns = {
            "Pattern A": 5,
            "Pattern B": 10,
            "Pattern C": 3,
        }

        result = log_analysis_service.get_error_patterns()

        assert result.is_success
        patterns = list(result.data.keys())
        assert patterns[0] == "Pattern B"  # Most frequent first
        assert patterns[1] == "Pattern A"
        assert patterns[2] == "Pattern C"  # Least frequent last

    def test_get_error_patterns_exception_handling(
        self,
        log_analysis_service: Any,
    ) -> None:
        """Test exception handling in get_error_patterns."""
        # Break the _error_patterns dict to cause an exception
        log_analysis_service._error_patterns = Mock()
        log_analysis_service._error_patterns.items.side_effect = ValueError(
            "Test error",
        )

        result = log_analysis_service.get_error_patterns()

        assert not result.is_success
        assert "Failed to get error patterns: Test error" in result.error

    def test_pattern_counting(self, log_analysis_service: Any) -> None:
        """Test that error patterns are counted correctly."""
        # Create multiple log entries with the same pattern
        log_entries = [
            MockLogEntry("ERROR", "Failed to process order 123", is_error=True),
            MockLogEntry("ERROR", "Failed to process order 456", is_error=True),
            MockLogEntry("ERROR", "Failed to process order 789", is_error=True),
        ]

        for log_entry in log_entries:
            log_analysis_service.analyze_log_entry(log_entry)

        result = log_analysis_service.get_error_patterns()
        assert result.is_success

        # Should have one pattern with count of 3
        patterns = result.data
        assert len(patterns) == 1
        pattern_count = next(iter(patterns.values()))
        assert pattern_count == 3


class TestTraceAnalysisService:
    """Test TraceAnalysisService class comprehensively."""

    @pytest.fixture
    def trace_analysis_service(self) -> Any:
        """Create TraceAnalysisService instance."""
        return TraceAnalysisService()

    def test_init(self, trace_analysis_service: Any) -> None:
        """Test TraceAnalysisService initialization."""
        assert trace_analysis_service._trace_history == {}

    def test_analyze_trace_success(self, trace_analysis_service: Any) -> None:
        """Test analyzing a successful trace."""
        trace = MockTrace("process_payment", "completed", 150.0)
        result = trace_analysis_service.analyze_trace(trace)

        assert result.is_success
        assert result.data["operation"] == "process_payment"
        assert result.data["status"] == "completed"
        assert result.data["duration_ms"] == 150.0
        assert result.data["is_error"] is False
        assert result.data["has_logs"] is False

        # Verify trace was stored
        assert "process_payment" in trace_analysis_service._trace_history
        assert len(trace_analysis_service._trace_history["process_payment"]) == 1

    def test_analyze_trace_failed(self, trace_analysis_service: Any) -> None:
        """Test analyzing a failed trace."""
        trace = MockTrace("process_payment", "failed", 50.0)
        result = trace_analysis_service.analyze_trace(trace)

        assert result.is_success
        assert result.data["is_error"] is True

    def test_analyze_trace_with_logs(self, trace_analysis_service: Any) -> None:
        """Test analyzing a trace with logs."""
        trace = MockTrace("process_payment", "completed", 150.0)
        trace.logs = ["Log entry 1", "Log entry 2"]

        result = trace_analysis_service.analyze_trace(trace)

        assert result.is_success
        assert result.data["has_logs"] is True

    def test_analyze_trace_history_limit(self, trace_analysis_service: Any) -> None:
        """Test that trace history is limited to 1000 entries per operation."""
        # Add 1200 traces
        for _i in range(1200):
            trace = MockTrace("test_operation", "completed", 100.0)
            trace_analysis_service.analyze_trace(trace)

        # Should only have 1000 traces stored
        assert len(trace_analysis_service._trace_history["test_operation"]) == 1000

    def test_analyze_trace_exception_handling(
        self,
        trace_analysis_service: Any,
    ) -> None:
        """Test exception handling in analyze_trace."""
        # Use None to trigger an exception when accessing attributes
        result = trace_analysis_service.analyze_trace(None)

        assert not result.is_success
        assert "Failed to analyze trace" in result.error

    def test_get_operation_stats_no_traces(self, trace_analysis_service: Any) -> None:
        """Test getting operation stats with no traces."""
        result = trace_analysis_service.get_operation_stats("unknown_operation")

        assert result.is_success
        assert result.data["operation"] == "unknown_operation"
        assert result.data["total_traces"] == 0
        assert result.data["success_rate"] == 0.0
        assert result.data["error_rate"] == 0.0
        assert result.data["avg_duration_ms"] == 0.0

    def test_get_operation_stats_all_successful(
        self,
        trace_analysis_service: Any,
    ) -> None:
        """Test getting operation stats with all successful traces."""
        # Add successful traces
        for i in range(10):
            trace = MockTrace("process_payment", "completed", 100.0 + i * 10)
            trace_analysis_service.analyze_trace(trace)

        result = trace_analysis_service.get_operation_stats("process_payment")

        assert result.is_success
        assert result.data["operation"] == "process_payment"
        assert result.data["total_traces"] == 10
        assert result.data["successful_traces"] == 10
        assert result.data["failed_traces"] == 0
        assert result.data["success_rate"] == 1.0
        assert result.data["error_rate"] == 0.0
        assert result.data["avg_duration_ms"] == 145.0  # Average of 100 to 190

    def test_get_operation_stats_mixed_results(
        self,
        trace_analysis_service: Any,
    ) -> None:
        """Test getting operation stats with mixed successful and failed traces."""
        # Add 7 successful and 3 failed traces
        for _i in range(7):
            trace = MockTrace("process_payment", "completed", 100.0)
            trace_analysis_service.analyze_trace(trace)

        for _i in range(3):
            trace = MockTrace("process_payment", "failed", 50.0)
            trace_analysis_service.analyze_trace(trace)

        result = trace_analysis_service.get_operation_stats("process_payment")

        assert result.is_success
        assert result.data["total_traces"] == 10
        assert result.data["successful_traces"] == 7
        assert result.data["failed_traces"] == 3
        assert result.data["success_rate"] == 0.7
        assert result.data["error_rate"] == 0.3
        assert result.data["avg_duration_ms"] == 85.0  # (7*100 + 3*50) / 10

    def test_get_operation_stats_exception_handling(
        self,
        trace_analysis_service: Any,
    ) -> None:
        """Test exception handling in get_operation_stats."""
        # Break the _trace_history dict to cause an exception during processing
        trace_analysis_service._trace_history = Mock()
        trace_analysis_service._trace_history.get.side_effect = ValueError("Test error")

        result = trace_analysis_service.get_operation_stats("test_operation")

        assert not result.is_success
        assert "Failed to get operation stats" in result.error

    def test_get_operation_stats_zero_duration_handling(
        self,
        trace_analysis_service: Any,
    ) -> None:
        """Test handling of traces with zero or missing duration."""
        # Add traces with no duration_ms attribute
        for _i in range(3):
            trace = MockTrace("test_operation", "completed")
            # Remove duration_ms to test default handling
            delattr(trace, "duration_ms")
            trace_analysis_service.analyze_trace(trace)

        result = trace_analysis_service.get_operation_stats("test_operation")

        assert result.is_success
        assert result.data["avg_duration_ms"] == 0.0
