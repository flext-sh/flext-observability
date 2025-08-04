"""Comprehensive tests for FlextObservabilityMasterFactory."""

from datetime import UTC, datetime
from unittest.mock import Mock, patch

from flext_core import FlextContainer, FlextResult

from flext_observability.factory import (
    FlextObservabilityMasterFactory,
    alert,
    get_global_factory,
    health_check,
    log,
    metric,
    reset_global_factory,
    trace,
)


class TestFlextObservabilityMasterFactory:
    """Complete tests for master factory."""

    def test_init_with_container(self) -> None:
        """Test factory initialization with container."""
        container = FlextContainer()
        factory = FlextObservabilityMasterFactory(container)
        assert factory.container is container

    def test_init_without_container(self) -> None:
        """Test factory initialization without container."""
        factory = FlextObservabilityMasterFactory()
        assert factory.container is not None
        assert isinstance(factory.container, FlextContainer)

    def test_setup_services_success(self) -> None:
        """Test successful service setup."""
        factory = FlextObservabilityMasterFactory()
        # Services should be registered automatically

        # Check if services are registered
        metrics_result = factory.container.get("metrics_service")
        logging_result = factory.container.get("logging_service")
        tracing_result = factory.container.get("tracing_service")
        alert_result = factory.container.get("alert_service")
        health_result = factory.container.get("health_service")

        assert metrics_result.success
        assert logging_result.success
        assert tracing_result.success
        assert alert_result.success
        assert health_result.success

    def test_setup_services_with_failures(self) -> None:
        """Test service setup with registration failures."""
        mock_container = Mock(spec=FlextContainer)
        mock_container.register.return_value = FlextResult.fail("Registration failed")

        with patch("flext_observability.factory.get_logger") as mock_logger:
            FlextObservabilityMasterFactory(mock_container)
            mock_logger.return_value.warning.assert_called()

    def test_metric_creation_success(self) -> None:
        """Test successful metric creation."""
        factory = FlextObservabilityMasterFactory()

        result = factory.metric(
            "test_metric",
            42.5,
            unit="ms",
            tags={"service": "test"},
            timestamp=datetime.now(UTC),
        )

        assert result.success
        assert result.data is not None

    def test_metric_creation_with_service(self) -> None:
        """Test metric creation with working service."""
        mock_service = Mock()
        mock_service.record_metric.return_value = FlextResult.ok("recorded")

        mock_container = Mock(spec=FlextContainer)
        mock_container.get.return_value = FlextResult.ok(mock_service)

        factory = FlextObservabilityMasterFactory(mock_container)
        result = factory.metric("test", 1.0)

        assert result.success

    def test_metric_creation_service_failure(self) -> None:
        """Test metric creation with service failure."""
        mock_service = Mock()
        mock_service.record_metric.return_value = FlextResult.fail("Service error")

        mock_container = Mock(spec=FlextContainer)
        mock_container.get.return_value = FlextResult.ok(mock_service)

        factory = FlextObservabilityMasterFactory(mock_container)
        result = factory.metric("test", 1.0)

        assert result.is_failure

    def test_metric_creation_exception(self) -> None:
        """Test metric creation with exception."""
        factory = FlextObservabilityMasterFactory()

        # Pass invalid value type to trigger exception
        result = factory.metric("test", "invalid_value")

        assert result.is_failure
        assert result.error is not None
        if "Failed to create metric" not in result.error:
            msg: str = f"Expected {'Failed to create metric'} in {result.error}"
            raise AssertionError(msg)

    def test_log_creation_success(self) -> None:
        """Test successful log creation."""
        factory = FlextObservabilityMasterFactory()

        result = factory.log(
            "test message",
            level="info",
            context={"user": "test"},
            timestamp=datetime.now(UTC),
        )

        assert result.success
        assert result.data is not None

    def test_log_creation_with_service(self) -> None:
        """Test log creation with working service."""
        mock_service = Mock()
        mock_service.log_entry.return_value = FlextResult.ok("logged")

        mock_container = Mock(spec=FlextContainer)
        mock_container.get.return_value = FlextResult.ok(mock_service)

        factory = FlextObservabilityMasterFactory(mock_container)
        result = factory.log("test message")

        assert result.success

    def test_log_creation_exception(self) -> None:
        """Test log creation with exception."""
        # Mock to raise exception during entity creation
        with patch(
            "flext_observability.factory.FlextLogEntry",
            side_effect=ValueError("Test error"),
        ):
            factory = FlextObservabilityMasterFactory()
            result = factory.log("test")

            assert result.is_failure
            assert result.error is not None
            if "Failed to create log" not in result.error:
                msg: str = f"Expected {'Failed to create log'} in {result.error}"
                raise AssertionError(msg)

    def test_alert_creation_success(self) -> None:
        """Test successful alert creation."""
        factory = FlextObservabilityMasterFactory()

        result = factory.alert(
            "Test Alert",
            "Alert message",
            severity="high",
            status="active",
            tags={"team": "ops"},
            timestamp=datetime.now(UTC),
        )

        assert result.success
        assert result.data is not None

    def test_alert_creation_with_service(self) -> None:
        """Test alert creation with working service."""
        mock_service = Mock()
        mock_service.create_alert.return_value = FlextResult.ok("created")

        mock_container = Mock(spec=FlextContainer)
        mock_container.get.return_value = FlextResult.ok(mock_service)

        factory = FlextObservabilityMasterFactory(mock_container)
        result = factory.alert("title", "message")

        assert result.success

    def test_alert_creation_exception(self) -> None:
        """Test alert creation with exception."""
        with patch(
            "flext_observability.factory.FlextAlert",
            side_effect=ValueError("Test error"),
        ):
            factory = FlextObservabilityMasterFactory()
            result = factory.alert("title", "message")

            assert result.is_failure
            assert result.error is not None
            if "Failed to create alert" not in result.error:
                msg: str = f"Expected {'Failed to create alert'} in {result.error}"
                raise AssertionError(msg)

    def test_trace_creation_success(self) -> None:
        """Test successful trace creation."""
        factory = FlextObservabilityMasterFactory()

        result = factory.trace(
            "trace-123",
            "test_operation",
            span_id="span-456",
            span_attributes={"method": "GET"},
            duration_ms=100,
            status="completed",
            timestamp=datetime.now(UTC),
        )

        assert result.success
        assert result.data is not None

    def test_trace_creation_with_service(self) -> None:
        """Test trace creation with working service."""
        mock_service = Mock()
        mock_service.start_trace.return_value = FlextResult.ok("started")

        mock_container = Mock(spec=FlextContainer)
        mock_container.get.return_value = FlextResult.ok(mock_service)

        factory = FlextObservabilityMasterFactory(mock_container)
        result = factory.trace("trace-id", "operation")

        assert result.success

    def test_trace_creation_exception(self) -> None:
        """Test trace creation with exception."""
        with patch(
            "flext_observability.factory.FlextTrace",
            side_effect=ValueError("Test error"),
        ):
            factory = FlextObservabilityMasterFactory()
            result = factory.trace("trace-id", "operation")

            assert result.is_failure
            assert result.error is not None
            if "Failed to create trace" not in result.error:
                msg: str = f"Expected {'Failed to create trace'} in {result.error}"
                raise AssertionError(msg)

    def test_health_check_creation_success(self) -> None:
        """Test successful health check creation."""
        factory = FlextObservabilityMasterFactory()

        result = factory.health_check(
            "database",
            status="healthy",
            message="Connection OK",
            metrics={"response_time": 50},
            timestamp=datetime.now(UTC),
        )

        assert result.success
        assert result.data is not None

    def test_health_check_creation_with_service(self) -> None:
        """Test health check creation with working service."""
        mock_service = Mock()
        mock_service.check_health.return_value = FlextResult.ok("checked")

        mock_container = Mock(spec=FlextContainer)
        mock_container.get.return_value = FlextResult.ok(mock_service)

        factory = FlextObservabilityMasterFactory(mock_container)
        result = factory.health_check("component")

        assert result.success

    def test_health_check_creation_exception(self) -> None:
        """Test health check creation with exception."""
        with patch(
            "flext_observability.factory.flext_create_health_check",
            side_effect=ValueError("Test error"),
        ):
            factory = FlextObservabilityMasterFactory()
            result = factory.health_check("component")

            assert result.is_failure
            assert result.error is not None
            if "Failed to create health check" not in result.error:
                msg: str = (
                    f"Expected {'Failed to create health check'} in {result.error}"
                )
                raise AssertionError(msg)

    def test_health_status_success(self) -> None:
        """Test successful health status retrieval."""
        mock_service = Mock()
        mock_service.get_overall_health.return_value = FlextResult.ok(
            {"status": "healthy"}
        )

        mock_container = Mock(spec=FlextContainer)
        mock_container.get.return_value = FlextResult.ok(mock_service)

        factory = FlextObservabilityMasterFactory(mock_container)
        result = factory.health_status()

        assert result.success
        assert result.data is not None
        if result.data["status"] != "healthy":
            msg: str = f"Expected {'healthy'}, got {result.data['status']}"
            raise AssertionError(msg)

    def test_health_status_no_service(self) -> None:
        """Test health status with no service available."""
        mock_container = Mock(spec=FlextContainer)
        mock_container.get.return_value = FlextResult.fail("Service not found")

        factory = FlextObservabilityMasterFactory(mock_container)
        result = factory.health_status()

        assert result.success
        assert result.data is not None
        if result.data["status"] != "healthy":
            msg: str = f"Expected {'healthy'}, got {result.data['status']}"
            raise AssertionError(msg)
        assert result.data["mode"] == "fallback"

    def test_health_status_exception(self) -> None:
        """Test health status with exception."""
        mock_container = Mock(spec=FlextContainer)
        mock_container.get.side_effect = ValueError("Container error")

        factory = FlextObservabilityMasterFactory(mock_container)
        result = factory.health_status()

        assert result.is_failure
        assert result.error is not None
        if "Health status check failed" not in result.error:
            msg: str = f"Expected {'Health status check failed'} in {result.error}"
            raise AssertionError(msg)


class TestGlobalFactory:
    """Tests for global factory functions."""

    def setup_method(self) -> None:
        """Reset global factory before each test."""
        reset_global_factory()

    def test_get_global_factory_creates_instance(self) -> None:
        """Test global factory creation."""
        # Reset factory first to ensure clean test
        reset_global_factory()
        factory = get_global_factory()
        if type(factory).__name__ != "FlextObservabilityMasterFactory":
            msg: str = f"Expected {'FlextObservabilityMasterFactory'}, got {type(factory).__name__}"
            raise AssertionError(msg)
        assert hasattr(factory, "container")

    def test_get_global_factory_returns_same_instance(self) -> None:
        """Test global factory singleton behavior."""
        factory1 = get_global_factory()
        factory2 = get_global_factory()
        assert factory1 is factory2

    def test_get_global_factory_with_container(self) -> None:
        """Test global factory with custom container."""
        container = FlextContainer()
        factory = get_global_factory(container)
        assert factory.container is container

    def test_reset_global_factory(self) -> None:
        """Test global factory reset."""
        factory1 = get_global_factory()
        reset_global_factory()
        factory2 = get_global_factory()
        assert factory1 is not factory2

    def test_global_metric_function(self) -> None:
        """Test global metric convenience function."""
        result = metric("test_metric", 42.0)
        assert result.success

    def test_global_log_function(self) -> None:
        """Test global log convenience function."""
        result = log("test message", level="info")
        assert result.success

    def test_global_alert_function(self) -> None:
        """Test global alert convenience function."""
        result = alert("Test Alert", "Alert message", severity="low")
        assert result.success

    def test_global_trace_function(self) -> None:
        """Test global trace convenience function."""
        result = trace("trace-123", "test_operation")
        assert result.success

    def test_global_health_check_function(self) -> None:
        """Test global health check convenience function."""
        result = health_check("database", status="healthy")
        assert result.success
