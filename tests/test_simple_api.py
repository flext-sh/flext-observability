"""Comprehensive tests for simple_api.py to achieve high coverage."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, Mock, patch

import pytest


class TestFlextObservability:
    """Test FlextObservability class."""

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    def test_init_with_defaults(self, mock_container: Any, mock_settings: Any) -> None:
        """Test FlextObservability initialization with defaults."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()

        assert obs._initialized is False
        assert obs._running is False
        mock_settings.assert_called_once()
        mock_container.assert_called_once()

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    def test_init_with_custom_settings(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test FlextObservability initialization with custom settings."""
        custom_settings = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability(settings=custom_settings)

        assert obs.settings == custom_settings
        mock_settings.assert_not_called()
        mock_container.assert_called_once()

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_initialize_success(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test successful initialization."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        # Mock services
        mock_metrics_service = AsyncMock()
        mock_logging_service = AsyncMock()
        mock_tracing_service = AsyncMock()
        mock_alert_service = AsyncMock()
        mock_health_service = AsyncMock()

        obs = FlextObservability()
        obs.container.resolve.side_effect = [  # Mock container resolve method
            mock_metrics_service,
            mock_logging_service,
            mock_tracing_service,
            mock_alert_service,
            mock_health_service,
        ]

        await obs.initialize()

        assert obs._initialized is True
        assert obs.metrics_service == mock_metrics_service
        assert obs.logging_service == mock_logging_service
        assert obs.tracing_service == mock_tracing_service
        assert obs.alert_service == mock_alert_service
        assert obs.health_service == mock_health_service

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_initialize_already_initialized(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test initialization when already initialized."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs._initialized = True

        await obs.initialize()

        # Should not call container.get since already initialized
        obs.container.get.assert_not_called()  # Assert container method not called

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_initialize_failure(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test initialization failure handling."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs.container.resolve.side_effect = Exception(
            "Service initialization failed",
        )  # Mock container exception

        with pytest.raises(Exception, match="Service initialization failed"):
            await obs.initialize()

        assert obs._initialized is False

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_start_success(self, mock_container: Any, mock_settings: Any) -> None:
        """Test successful start."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs._initialized = True
        obs.metrics_service = AsyncMock()
        obs.logging_service = AsyncMock()
        obs.tracing_service = AsyncMock()
        obs.health_service = AsyncMock()

        await obs.start()

        assert obs._running is True
        obs.metrics_service.start.assert_called_once()
        obs.logging_service.start.assert_called_once()
        obs.tracing_service.start.assert_called_once()
        obs.health_service.start.assert_called_once()

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_start_not_initialized(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test start when not initialized."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs._initialized = False

        with pytest.raises(DomainError, match="Observability services not initialized"):
            await obs.start()

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_start_already_running(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test start when already running."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs._initialized = True
        obs._running = True
        obs.metrics_service = AsyncMock()

        await obs.start()

        # Should not call start on services if already running
        obs.metrics_service.start.assert_not_called()

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_stop_success(self, mock_container: Any, mock_settings: Any) -> None:
        """Test successful stop."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs._running = True
        obs.metrics_service = AsyncMock()
        obs.logging_service = AsyncMock()
        obs.tracing_service = AsyncMock()
        obs.health_service = AsyncMock()

        await obs.stop()

        assert obs._running is False
        obs.metrics_service.stop.assert_called_once()
        obs.logging_service.stop.assert_called_once()
        obs.tracing_service.stop.assert_called_once()
        obs.health_service.stop.assert_called_once()

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_stop_not_running(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test stop when not running."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs._running = False
        obs.metrics_service = AsyncMock()

        await obs.stop()

        # Should not call stop on services if not running
        obs.metrics_service.stop.assert_not_called()

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_collect_metrics_success(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test successful metrics collection."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        expected_metrics = [
            {"name": "cpu_usage", "value": 75.5},
            {"name": "memory_usage", "value": 1024},
        ]

        obs = FlextObservability()
        obs.metrics_service = AsyncMock()
        obs.metrics_service.collect_all_metrics.return_value = expected_metrics

        result = await obs.collect_metrics()

        assert result == expected_metrics
        obs.metrics_service.collect_all_metrics.assert_called_once()

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_collect_metrics_with_filters(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test metrics collection with filters."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs.metrics_service = AsyncMock()

        await obs.collect_metrics(metric_types=["system"], labels={"env": "prod"})

        obs.metrics_service.collect_metrics.assert_called_once_with(
            metric_types=["system"],
            labels={"env": "prod"},
        )

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_log_event_success(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test successful event logging."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs.logging_service = AsyncMock()

        await obs.log_event(
            event_type="user_login",
            level="INFO",
            message="User logged in successfully",
            user_id="user123",
        )

        obs.logging_service.log_event.assert_called_once_with(
            event_type="user_login",
            level="INFO",
            message="User logged in successfully",
            user_id="user123",
        )

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_trace_operation_success(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test successful operation tracing."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs.tracing_service = AsyncMock()

        async def test_operation() -> str:
            return "operation_result"

        result = await obs.trace_operation(
            operation_name="test_operation",
            operation_func=test_operation,
            operation_id="op123",
        )

        assert result == "operation_result"
        obs.tracing_service.trace_operation.assert_called_once()

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_create_alert_success(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test successful alert creation."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs.alert_service = AsyncMock()

        await obs.create_alert(
            alert_type="threshold",
            metric_name="cpu_usage",
            threshold=80.0,
            severity="high",
        )

        obs.alert_service.create_alert.assert_called_once_with(
            alert_type="threshold",
            metric_name="cpu_usage",
            threshold=80.0,
            severity="high",
        )

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_get_health_status_success(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test successful health status retrieval."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        expected_health = {
            "status": "healthy",
            "components": {"database": "healthy", "redis": "healthy"},
        }

        obs = FlextObservability()
        obs.health_service = AsyncMock()
        obs.health_service.get_health_status.return_value = expected_health

        result = await obs.get_health_status()

        assert result == expected_health
        obs.health_service.get_health_status.assert_called_once()

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_context_manager_success(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test FlextObservability as context manager."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs.initialize = AsyncMock()  # Mock initialization method
        obs.start = AsyncMock()  # Mock start method
        obs.stop = AsyncMock()  # Mock stop method

        async with obs:
            assert obs._initialized

        obs.initialize.assert_called_once()
        obs.start.assert_called_once()
        obs.stop.assert_called_once()

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_context_manager_exception_handling(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test FlextObservability context manager with exception."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs.initialize = AsyncMock()  # Mock initialization method
        obs.start = AsyncMock()  # Mock start method
        obs.stop = AsyncMock()  # Mock stop method

        msg = "Test exception"
        with pytest.raises(ValueError, match="Test exception"):
            async with obs:
                raise ValueError(msg)

        # Should still call stop even if exception occurred
        obs.stop.assert_called_once()


class TestModuleFunctions:
    """Test module-level convenience functions."""

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_setup_observability(self, mock_flext_obs: Any) -> None:
        """Test setup_observability function."""
        mock_instance = AsyncMock()
        mock_flext_obs.return_value = mock_instance

        settings = Mock()
        result = await setup_observability(settings=settings)

        assert result == mock_instance
        mock_flext_obs.assert_called_once_with(settings=settings)
        mock_instance.initialize.assert_called_once()

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_start_observability(self, mock_flext_obs: Any) -> None:
        """Test start_observability function."""
        mock_instance = AsyncMock()
        mock_flext_obs.return_value = mock_instance

        await start_observability(mock_instance)

        mock_instance.start.assert_called_once()

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_stop_observability(self, mock_flext_obs: Any) -> None:
        """Test stop_observability function."""
        mock_instance = AsyncMock()
        mock_flext_obs.return_value = mock_instance

        await stop_observability(mock_instance)

        mock_instance.stop.assert_called_once()

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_get_health_status_function(self, mock_flext_obs: Any) -> None:
        """Test get_health_status function."""
        mock_instance = AsyncMock()
        mock_instance.get_health_status.return_value = {"status": "healthy"}
        mock_flext_obs.return_value = mock_instance

        result = await get_health_status(mock_instance)

        assert result == {"status": "healthy"}
        mock_instance.get_health_status.assert_called_once()

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_collect_metrics_function(self, mock_flext_obs: Any) -> None:
        """Test collect_metrics function."""
        mock_instance = AsyncMock()
        expected_metrics = [{"name": "test", "value": 100}]
        mock_instance.collect_metrics.return_value = expected_metrics
        mock_flext_obs.return_value = mock_instance

        result = await collect_metrics(
            mock_instance,
            metric_types=["system"],
            labels={"env": "test"},
        )

        assert result == expected_metrics
        mock_instance.collect_metrics.assert_called_once_with(
            metric_types=["system"],
            labels={"env": "test"},
        )

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_log_event_function(self, mock_flext_obs: Any) -> None:
        """Test log_event function."""
        mock_instance = AsyncMock()
        mock_flext_obs.return_value = mock_instance

        await log_event(
            mock_instance,
            event_type="test_event",
            level="INFO",
            message="Test message",
            custom_field="custom_value",
        )

        mock_instance.log_event.assert_called_once_with(
            event_type="test_event",
            level="INFO",
            message="Test message",
            custom_field="custom_value",
        )

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_trace_operation_function(self, mock_flext_obs: Any) -> None:
        """Test trace_operation function."""
        mock_instance = AsyncMock()
        mock_instance.trace_operation.return_value = "traced_result"
        mock_flext_obs.return_value = mock_instance

        async def test_func() -> str:
            return "test_result"

        result = await trace_operation(
            mock_instance,
            operation_name="test_op",
            operation_func=test_func,
            trace_id="trace123",
        )

        assert result == "traced_result"
        mock_instance.trace_operation.assert_called_once_with(
            operation_name="test_op",
            operation_func=test_func,
            trace_id="trace123",
        )

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_create_alert_function(self, mock_flext_obs: Any) -> None:
        """Test create_alert function."""
        mock_instance = AsyncMock()
        mock_flext_obs.return_value = mock_instance

        await create_alert(
            mock_instance,
            alert_type="anomaly",
            metric_name="response_time",
            threshold=500.0,
            severity="medium",
        )

        mock_instance.create_alert.assert_called_once_with(
            alert_type="anomaly",
            metric_name="response_time",
            threshold=500.0,
            severity="medium",
        )

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_quick_setup(self, mock_flext_obs: Any) -> None:
        """Test quick_setup function."""
        mock_instance = AsyncMock()
        mock_flext_obs.return_value = mock_instance

        result = await quick_setup(
            enable_metrics=True,
            enable_tracing=False,
            enable_logging=True,
            log_level="DEBUG",
        )

        assert result == mock_instance
        mock_flext_obs.assert_called_once()
        mock_instance.initialize.assert_called_once()
        mock_instance.start.assert_called_once()

    @patch("flext_observability.simple_api.FlextObservability")
    def test_monitor_function_decorator(self, mock_flext_obs: Any) -> None:
        """Test monitor_function decorator."""
        mock_instance = AsyncMock()
        mock_flext_obs.return_value = mock_instance

        @monitor_function(  # Monitor decorator test
            observability=mock_instance,
            _metric_name="test_function",
            trace_name="test_trace",
        )
        async def test_func(x: int, y: int) -> int:
            return x + y

        # Test that the decorator was applied
        assert hasattr(test_func, "__wrapped__")
        assert callable(test_func)

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_monitor_function_decorator_execution(
        self,
        mock_flext_obs: Any,
    ) -> None:
        """Test monitor_function decorator execution."""
        mock_instance = AsyncMock()
        mock_instance.trace_operation.return_value = 42
        mock_flext_obs.return_value = mock_instance

        @monitor_function(  # Monitor decorator test
            observability=mock_instance,
            _metric_name="test_function",
            trace_name="test_trace",
        )
        async def test_func(x: int, y: int) -> int:
            return x + y

        result = await test_func(5, 7)

        # The decorator should have called trace_operation
        assert mock_instance.trace_operation.called
        # The result should come from the mock
        assert result == 42


class TestEdgeCases:
    """Test edge cases and error conditions."""

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_multiple_initialization_calls(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test multiple initialization calls."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs.container.resolve.side_effect = [  # Mock container resolve method
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
        ]

        # First initialization
        await obs.initialize()
        assert obs._initialized is True

        # Second initialization should not re-initialize
        container_call_count = obs.container.resolve.call_count  # Mock call count
        await obs.initialize()
        assert (
            obs.container.resolve.call_count == container_call_count
        )  # Assert mock call count

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_service_start_failure(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test handling of service start failure."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs._initialized = True
        obs.metrics_service = AsyncMock()
        obs.metrics_service.start.side_effect = Exception("Start failed")
        obs.logging_service = AsyncMock()
        obs.tracing_service = AsyncMock()
        obs.health_service = AsyncMock()

        with pytest.raises(Exception, match="Start failed"):
            await obs.start()

        # Should not be marked as running if start failed
        assert obs._running is False

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_function_decoration_with_none_observability(
        self,
        mock_flext_obs: Any,
    ) -> None:
        """Test monitor_function decorator with None observability."""

        @monitor_function(
            observability=None,
            _metric_name="test_function",
        )  # Monitor with params
        async def test_func() -> str:
            return "result"

        # Should still work even with None observability
        result = await test_func()
        assert result == "result"

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_collect_metrics_service_error(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test collect_metrics when service raises error."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs.metrics_service = AsyncMock()
        obs.metrics_service.collect_all_metrics.side_effect = Exception(
            "Collection failed",
        )

        with pytest.raises(Exception, match="Collection failed"):
            await obs.collect_metrics()

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_quick_setup_with_minimal_options(self, mock_flext_obs: Any) -> None:
        """Test quick_setup with minimal options."""
        mock_instance = AsyncMock()
        mock_flext_obs.return_value = mock_instance

        result = await quick_setup()

        assert result == mock_instance
        mock_instance.initialize.assert_called_once()
        mock_instance.start.assert_called_once()

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_quick_setup_initialization_failure(
        self,
        mock_flext_obs: Any,
    ) -> None:
        """Test quick_setup when initialization fails."""
        mock_instance = AsyncMock()
        mock_instance.initialize.side_effect = Exception("Init failed")
        mock_flext_obs.return_value = mock_instance

        with pytest.raises(Exception, match="Init failed"):
            await quick_setup()

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_context_manager_initialization_failure(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test context manager when initialization fails."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        obs = FlextObservability()
        obs.initialize = AsyncMock(
            side_effect=Exception("Init failed"),
        )  # Mock init failure
        obs.stop = AsyncMock()  # Mock stop method

        with pytest.raises(Exception, match="Init failed"):
            async with obs:
                pass

        # Stop should still be called even if initialization failed
        obs.stop.assert_called_once()


class TestIntegration:
    """Integration tests combining multiple features."""

    @patch("flext_observability.simple_api.get_settings")
    @patch("flext_observability.simple_api.get_container")
    async def test_full_lifecycle(
        self,
        mock_container: Any,
        mock_settings: Any,
    ) -> None:
        """Test full observability lifecycle."""
        mock_settings.return_value = Mock()
        mock_container.return_value = Mock()

        # Setup mocks with proper async methods
        metrics_service = AsyncMock()
        metrics_service.start = AsyncMock()
        metrics_service.stop = AsyncMock()
        metrics_service.collect_all_metrics = AsyncMock(return_value=[])

        logging_service = AsyncMock()
        logging_service.start = AsyncMock()
        logging_service.stop = AsyncMock()
        logging_service.log_event = AsyncMock()

        tracing_service = AsyncMock()
        tracing_service.start = AsyncMock()
        tracing_service.stop = AsyncMock()

        alert_service = AsyncMock()
        alert_service.create_alert = AsyncMock()

        health_service = AsyncMock()
        health_service.start = AsyncMock()
        health_service.stop = AsyncMock()
        health_service.get_health_status = AsyncMock(return_value={"status": "healthy"})

        obs = FlextObservability()
        obs.container.resolve.side_effect = [  # Mock container resolve method
            metrics_service,
            logging_service,
            tracing_service,
            alert_service,
            health_service,
        ]

        # Full lifecycle test
        await obs.initialize()
        assert obs._initialized is True

        await obs.start()
        assert obs._running is True

        # Use services
        await obs.collect_metrics()
        await obs.get_health_status()

        await obs.log_event("test", "INFO", "Test message")
        await obs.create_alert("threshold", "cpu", 80.0)

        await obs.stop()
        assert obs._running is False

    @patch("flext_observability.simple_api.FlextObservability")
    async def test_module_functions_integration(self, mock_flext_obs: Any) -> None:
        """Test integration of module functions."""
        mock_instance = AsyncMock()
        mock_instance.get_health_status.return_value = {"status": "healthy"}
        mock_instance.collect_metrics.return_value = [{"name": "cpu", "value": 50}]
        mock_flext_obs.return_value = mock_instance

        # Setup
        observability = await setup_observability()
        await start_observability(observability)

        # Use
        health = await get_health_status(observability)
        metrics = await collect_metrics(observability)
        await log_event(observability, "test", "INFO", "Test")

        # Teardown
        await stop_observability(observability)

        # Verify all calls were made
        assert health == {"status": "healthy"}
        assert metrics == [{"name": "cpu", "value": 50}]
        mock_instance.initialize.assert_called_once()
        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
