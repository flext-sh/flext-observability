"""Comprehensive tests for application services - achieving high coverage."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest
from flext_core import FlextContainer, FlextResult

# Use corrected imports from flext-observability root
from flext_observability import (
    FlextAlert,
    FlextAlertService,
    FlextHealthCheck,
    FlextHealthService,
    FlextLogEntry,
    FlextLoggingService,
    FlextMetric,
    FlextMetricsService,
    FlextTrace,
    FlextTracingService,
)


class TestMetricsDomainService:
    """Test FlextMetricsService class comprehensively."""

    @pytest.fixture
    def container(self) -> FlextContainer:
        """Create FlextContainer for FlextMetricsService."""
        return FlextContainer()

    @pytest.fixture
    def metrics_service(self, container: FlextContainer) -> FlextMetricsService:
        """Create FlextMetricsService instance with container."""
        return FlextMetricsService(container=container)

    @pytest.fixture
    def sample_metric(self) -> Mock:
        """Create a sample metric for testing."""
        metric = Mock()
        metric.name = "test_metric"
        metric.value = Decimal("42.0")
        metric.unit = "count"
        metric.timestamp = datetime.now(UTC)
        metric.tags = {"env": "test"}
        return metric

    def test_record_metric_success(
        self,
        metrics_service: FlextMetricsService,
        container: FlextContainer,
        sample_metric: FlextMetric,
    ) -> None:
        """Test successful metric recording."""
        # Setup mock repository
        mock_repository = Mock()
        mock_repository.save.return_value = FlextResult.ok(sample_metric)

        # Mock the container.get() to return FlextResult.ok(mock_repository)
        container.register("metrics_repository", mock_repository)

        # Execute
        result = metrics_service.record_metric(sample_metric)

        # Verify
        assert result.is_success
        # Verify repository save was called
        mock_repository.save.assert_called_once_with(sample_metric)

    def test_record_metric_no_repository(
        self,
        metrics_service: FlextMetricsService,
        sample_metric: FlextMetric,
    ) -> None:
        """Test metric recording with no repository configured."""
        # Execute without repository
        result = metrics_service.record_metric(sample_metric)

        # Verify
        assert not result.is_success
        assert "Metrics repository not configured" in result.error

    def test_get_metric_success(
        self,
        metrics_service: FlextMetricsService,
        container: FlextContainer,
        sample_metric: FlextMetric,
    ) -> None:
        """Test successful metric retrieval."""
        # Setup mock repository
        mock_repository = Mock()
        mock_repository.get_by_id.return_value = FlextResult.ok(sample_metric)
        container.register("metrics_repository", mock_repository)

        # Execute
        result = metrics_service.get_metric("test_id")

        # Verify
        assert result.is_success
        # Verify repository get was called
        mock_repository.get_by_id.assert_called_once_with("test_id")

    def test_get_metric_no_repository(
        self,
        metrics_service: FlextMetricsService,
    ) -> None:
        """Test metric retrieval with no repository configured."""
        # Execute without repository
        result = metrics_service.get_metric("test_id")

        # Verify
        assert not result.is_success
        assert "Metrics repository not configured" in result.error


class TestLoggingDomainService:
    """Test FlextLoggingService class comprehensively."""

    @pytest.fixture
    def container(self) -> FlextContainer:
        """Create FlextContainer for FlextLoggingService."""
        return FlextContainer()

    @pytest.fixture
    def logging_service(self, container: FlextContainer) -> FlextLoggingService:
        """Create FlextLoggingService instance with container."""
        return FlextLoggingService(container=container)

    @pytest.fixture
    def sample_log_entry(self) -> Mock:
        """Create a sample log entry for testing."""
        log_entry = Mock()
        log_entry.level = "info"
        log_entry.message = "Test log message"
        log_entry.timestamp = datetime.now(UTC)
        log_entry.context = {"custom_field": "custom_value"}
        return log_entry

    def test_log_entry_success(
        self,
        logging_service: FlextLoggingService,
        container: FlextContainer,
        sample_log_entry: FlextLogEntry,
    ) -> None:
        """Test successful log entry creation."""
        # Setup mock repository
        mock_repository = Mock()
        mock_repository.save.return_value = FlextResult.ok(sample_log_entry)
        container.register("logging_repository", mock_repository)

        # Execute
        result = logging_service.log_entry(sample_log_entry)

        # Verify
        assert result.is_success

    def test_log_entry_no_repository(
        self,
        logging_service: FlextLoggingService,
        sample_log_entry: FlextLogEntry,
    ) -> None:
        """Test log entry with no repository configured."""
        # Execute without repository
        result = logging_service.log_entry(sample_log_entry)

        # Verify
        assert not result.is_success
        assert "Logging repository not configured" in result.error

    def test_get_logs_success(
        self,
        logging_service: FlextLoggingService,
        container: FlextContainer,
        sample_log_entry: FlextLogEntry,
    ) -> None:
        """Test successful logs retrieval."""
        # Setup mock repository
        mock_repository = Mock()
        mock_logs_list = [sample_log_entry]
        mock_repository.find_by_level.return_value = FlextResult.ok(mock_logs_list)
        container.register("logging_repository", mock_repository)

        # Execute
        result = logging_service.get_logs("info")

        # Verify
        assert result.is_success
        assert len(result.data) == 1
        assert result.data[0] == sample_log_entry

    def test_get_logs_no_repository(
        self,
        logging_service: FlextLoggingService,
    ) -> None:
        """Test logs retrieval with no repository configured."""
        # Execute without repository
        result = logging_service.get_logs("info")

        # Verify
        assert not result.is_success
        assert "Logging repository not configured" in result.error


class TestAlertDomainService:
    """Test FlextAlertService class comprehensively."""

    @pytest.fixture
    def container(self) -> FlextContainer:
        """Create FlextContainer for FlextAlertService."""
        return FlextContainer()

    @pytest.fixture
    def alert_service(self, container: FlextContainer) -> FlextAlertService:
        """Create FlextAlertService instance with container."""
        return FlextAlertService(container=container)

    @pytest.fixture
    def sample_alert(self) -> Mock:
        """Create a sample alert for testing."""
        alert = Mock()
        alert.title = "Test Alert"
        alert.message = "Test alert message"
        alert.severity = "medium"
        alert.status = "active"
        alert.timestamp = datetime.now(UTC)
        return alert

    def test_create_alert_success(
        self,
        alert_service: FlextAlertService,
        container: FlextContainer,
        sample_alert: FlextAlert,
    ) -> None:
        """Test successful alert creation."""
        # Setup mock repository
        mock_repository = Mock()
        mock_repository.save.return_value = FlextResult.ok(sample_alert)
        container.register("alert_repository", mock_repository)

        # Execute
        result = alert_service.create_alert(sample_alert)

        # Verify
        assert result.is_success

    def test_create_alert_no_repository(
        self,
        alert_service: FlextAlertService,
        sample_alert: FlextAlert,
    ) -> None:
        """Test alert creation with no repository configured."""
        # Execute without repository
        result = alert_service.create_alert(sample_alert)

        # Verify
        assert not result.is_success
        assert "Alert repository not configured" in result.error


class TestHealthDomainService:
    """Test FlextHealthService class comprehensively."""

    @pytest.fixture
    def container(self) -> FlextContainer:
        """Create FlextContainer for FlextHealthService."""
        return FlextContainer()

    @pytest.fixture
    def health_service(self, container: FlextContainer) -> FlextHealthService:
        """Create FlextHealthService instance with container."""
        return FlextHealthService(container=container)

    @pytest.fixture
    def sample_health_check(self) -> Mock:
        """Create a sample health check for testing."""
        health_check = Mock()
        health_check.component = "database"
        health_check.status = "healthy"
        health_check.message = "Database is operational"
        health_check.timestamp = datetime.now(UTC)
        return health_check

    def test_check_health_success(
        self,
        health_service: FlextHealthService,
        container: FlextContainer,
        sample_health_check: FlextHealthCheck,
    ) -> None:
        """Test successful health check."""
        # Setup mock repository
        mock_repository = Mock()
        mock_repository.get_by_component.return_value = FlextResult.ok(sample_health_check)
        container.register("health_repository", mock_repository)

        # Execute
        result = health_service.check_health("database")

        # Verify
        assert result.is_success

    def test_check_health_no_repository(
        self,
        health_service: FlextHealthService,
    ) -> None:
        """Test health check with no repository configured."""
        # Execute without repository
        result = health_service.check_health("database")

        # Verify
        assert not result.is_success
        assert "Health repository not configured" in result.error

    def test_get_overall_health_success(
        self,
        health_service: FlextHealthService,
        container: FlextContainer,
        sample_health_check: FlextHealthCheck,
    ) -> None:
        """Test successful overall health retrieval."""
        # Setup mock repository and domain service
        mock_repository = Mock()
        mock_repository.get_all.return_value = FlextResult.ok([sample_health_check])
        container.register("health_repository", mock_repository)

        mock_domain_service = Mock()
        mock_domain_service.calculate_overall_health.return_value = FlextResult.ok("healthy")
        container.register("health_domain_service", mock_domain_service)

        # Execute
        result = health_service.get_overall_health()

        # Verify
        assert result.is_success
        assert result.data == "healthy"

    def test_get_overall_health_no_repository(
        self,
        health_service: FlextHealthService,
    ) -> None:
        """Test overall health with no repository configured."""
        # Execute without repository
        result = health_service.get_overall_health()

        # Verify
        assert not result.is_success
        assert "Health repository not configured" in result.error


class TestTracingDomainService:
    """Test FlextTracingService class comprehensively."""

    @pytest.fixture
    def container(self) -> FlextContainer:
        """Create FlextContainer for FlextTracingService."""
        return FlextContainer()

    @pytest.fixture
    def tracing_service(self, container: FlextContainer) -> FlextTracingService:
        """Create FlextTracingService instance with container."""
        return FlextTracingService(container=container)

    @pytest.fixture
    def sample_trace(self) -> Mock:
        """Create a sample trace for testing."""
        trace = Mock()
        trace.trace_id = "123456789abcdef0123456789abcdef0"
        trace.span_id = "123456789abcdef0"
        trace.operation = "test_operation"
        trace.duration_ms = 150
        trace.status = "pending"
        trace.timestamp = datetime.now(UTC)
        return trace

    def test_start_trace_success(
        self,
        tracing_service: FlextTracingService,
        container: FlextContainer,
        sample_trace: FlextTrace,
    ) -> None:
        """Test successful trace start."""
        # Setup mock repository
        mock_repository = Mock()
        mock_repository.save.return_value = FlextResult.ok(sample_trace)
        container.register("tracing_repository", mock_repository)

        # Execute
        result = tracing_service.start_trace(sample_trace)

        # Verify
        assert result.is_success
        assert result.data.status == "started"

    def test_start_trace_no_repository(
        self,
        tracing_service: FlextTracingService,
        sample_trace: FlextTrace,
    ) -> None:
        """Test trace start with no repository configured."""
        # Execute without repository
        result = tracing_service.start_trace(sample_trace)

        # Verify
        assert not result.is_success
        assert "Tracing repository not configured" in result.error

    def test_complete_trace_success(
        self,
        tracing_service: FlextTracingService,
        container: FlextContainer,
        sample_trace: FlextTrace,
    ) -> None:
        """Test successful trace completion."""
        # Setup mock repository
        mock_repository = Mock()
        mock_repository.get_by_id.return_value = FlextResult.ok(sample_trace)
        mock_repository.save.return_value = FlextResult.ok(sample_trace)
        container.register("tracing_repository", mock_repository)

        # Execute
        result = tracing_service.complete_trace("test_id", 200)

        # Verify
        assert result.is_success
        assert result.data.status == "completed"
        assert result.data.duration_ms == 200

    def test_complete_trace_no_repository(
        self,
        tracing_service: FlextTracingService,
    ) -> None:
        """Test trace completion with no repository configured."""
        # Execute without repository
        result = tracing_service.complete_trace("test_id", 200)

        # Verify
        assert not result.is_success
        assert "Tracing repository not configured" in result.error
