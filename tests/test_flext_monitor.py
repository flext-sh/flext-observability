"""Comprehensive tests for FlextObservabilityMonitor.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import pytest

from flext_core import FlextContainer, FlextResult, FlextTypes
from flext_observability import (
    FlextObservabilityMonitor,
    flext_monitor_function,
)

# Constants
EXPECTED_BULK_SIZE = 2
EXPECTED_DATA_COUNT = 3


def assert_failure_with_error[T](result: FlextResult[T]) -> str:
    """Assert result is failure and return non-None error."""
    assert result.is_failure
    assert result.error is not None
    return result.error


class TestFlextObservabilityMonitor:
    """Complete tests for observability monitor."""

    def test_init_with_container(self) -> None:
        """Test monitor initialization with container."""
        container = FlextContainer()
        monitor = FlextObservabilityMonitor(container)
        assert monitor.container is container
        assert not monitor._initialized
        assert not monitor._running

    def test_init_without_container(self) -> None:
        """Test monitor initialization without container."""
        monitor = FlextObservabilityMonitor()
        assert monitor.container is not None
        assert isinstance(monitor.container, FlextContainer)
        assert not monitor._initialized
        assert not monitor._running

    def test_initialize_observability_success(self) -> None:
        """Test successful observability initialization."""
        monitor = FlextObservabilityMonitor()

        result = monitor.flext_initialize_observability()

        assert result.is_success
        assert monitor._initialized
        assert monitor._metrics_service is not None
        assert monitor._logging_service is not None
        assert monitor._tracing_service is not None
        assert monitor._alert_service is not None
        assert monitor._health_service is not None

    def test_initialize_observability_already_initialized(self) -> None:
        """Test initialization when already initialized."""
        monitor = FlextObservabilityMonitor()
        monitor._initialized = True

        result = monitor.flext_initialize_observability()

        assert result.is_success

    def test_initialize_observability_with_real_container(self) -> None:
        """Test initialization with real container."""
        container = FlextContainer()
        monitor = FlextObservabilityMonitor(container)
        result = monitor.flext_initialize_observability()

        # Should succeed with real container
        assert result.is_success

    def test_initialize_observability_multiple_times(self) -> None:
        """Test multiple initialization calls."""
        monitor = FlextObservabilityMonitor()

        # First initialization should succeed
        result1 = monitor.flext_initialize_observability()
        assert result1.is_success

        # Second initialization should also succeed (idempotent)
        result2 = monitor.flext_initialize_observability()
        assert result2.is_success

    def test_start_monitoring_success(self) -> None:
        """Test successful monitoring start."""
        monitor = FlextObservabilityMonitor()
        monitor._initialized = True

        result = monitor.flext_start_monitoring()

        assert result.is_success
        assert monitor._running

    def test_start_monitoring_not_initialized(self) -> None:
        """Test monitoring start when not initialized."""
        monitor = FlextObservabilityMonitor()

        result = monitor.flext_start_monitoring()

        assert result.is_failure
        error = assert_failure_with_error(result)
        if "Monitor not initialized" not in error:
            raise AssertionError(f"Expected {'Monitor not initialized'} in {error}")

    def test_start_monitoring_already_running(self) -> None:
        """Test monitoring start when already running."""
        monitor = FlextObservabilityMonitor()
        monitor._initialized = True
        monitor._running = True

        result = monitor.flext_start_monitoring()

        assert result.is_success

    def test_start_monitoring_without_initialization(self) -> None:
        """Test monitoring start without proper initialization."""
        monitor = FlextObservabilityMonitor()
        # Don't set _initialized = True to test this error case

        result = monitor.flext_start_monitoring()

        assert result.is_failure
        error = assert_failure_with_error(result)
        # Should fail because monitor is not initialized
        assert "not initialized" in error or "Failed to start" in error

    def test_stop_monitoring_success(self) -> None:
        """Test successful monitoring stop."""
        monitor = FlextObservabilityMonitor()
        monitor._running = True

        result = monitor.flext_stop_monitoring()

        assert result.is_success
        assert not monitor._running

    def test_stop_monitoring_not_running(self) -> None:
        """Test monitoring stop when not running."""
        monitor = FlextObservabilityMonitor()

        result = monitor.flext_stop_monitoring()

        assert result.is_success

    def test_stop_monitoring_without_running(self) -> None:
        """Test monitoring stop when not running."""
        monitor = FlextObservabilityMonitor()
        # Don't set _running = True to test this case

        result = monitor.flext_stop_monitoring()

        # Should succeed even if not running (idempotent operation)
        assert result.is_success

    def test_get_health_status_success(self) -> None:
        """Test successful health status retrieval."""
        monitor = FlextObservabilityMonitor()

        # Initialize to create health service
        monitor.flext_initialize_observability()

        result = monitor.flext_get_health_status()

        assert result.is_success
        assert isinstance(result.data, dict)

    def test_get_health_status_no_service(self) -> None:
        """Test health status with no health service."""
        monitor = FlextObservabilityMonitor()

        result = monitor.flext_get_health_status()

        assert result.is_failure
        error = assert_failure_with_error(result)
        if "Health service not available" not in error:
            raise AssertionError(
                f"Expected {'Health service not available'} in {error}",
            )

    def test_get_health_status_with_real_initialization(self) -> None:
        """Test health status with proper initialization."""
        monitor = FlextObservabilityMonitor()

        # Initialize properly first
        init_result = monitor.flext_initialize_observability()
        assert init_result.is_success

        # Health status should now work
        result = monitor.flext_get_health_status()

        # Should succeed with proper initialization
        assert result.is_success
        assert isinstance(result.data, dict)

    def test_is_monitoring_active_true(self) -> None:
        """Test monitoring active check when active."""
        monitor = FlextObservabilityMonitor()
        monitor._initialized = True
        monitor._running = True

        assert monitor.flext_is_monitoring_active()

    def test_is_monitoring_active_false_not_initialized(self) -> None:
        """Test monitoring active check when not initialized."""
        monitor = FlextObservabilityMonitor()
        monitor._running = True

        assert not monitor.flext_is_monitoring_active()

    def test_is_monitoring_active_false_not_running(self) -> None:
        """Test monitoring active check when not running."""
        monitor = FlextObservabilityMonitor()
        monitor._initialized = True

        assert not monitor.flext_is_monitoring_active()

    def test_full_workflow_success(self) -> None:
        """Test complete initialization and monitoring workflow."""
        monitor = FlextObservabilityMonitor()

        # Initialize
        init_result = monitor.flext_initialize_observability()
        assert init_result.is_success

        # Start monitoring
        start_result = monitor.flext_start_monitoring()
        assert start_result.is_success

        # Check status
        assert monitor.flext_is_monitoring_active()

        # Get health
        health_result = monitor.flext_get_health_status()
        assert health_result.is_success

        # Stop monitoring
        stop_result = monitor.flext_stop_monitoring()
        assert stop_result.is_success

        assert not monitor.flext_is_monitoring_active()


class TestFlextMonitorFunction:
    """Tests for function monitoring decorator."""

    def test_monitor_function_no_monitor(self) -> None:
        """Test function monitoring without monitor."""

        @flext_monitor_function()
        def test_func(x: int, y: int) -> int:
            return x + y

        result = test_func(1, 2)
        if result != EXPECTED_DATA_COUNT:
            raise AssertionError(f"Expected {3}, got {result}")

    def test_monitor_function_with_inactive_monitor(self) -> None:
        """Test function monitoring with inactive monitor."""
        monitor = FlextObservabilityMonitor()

        @flext_monitor_function(monitor)
        def test_func(x: int, y: int) -> int:
            return x + y

        result = test_func(1, 2)
        if result != EXPECTED_DATA_COUNT:
            raise AssertionError(f"Expected {3}, got {result}")

    def test_monitor_function_with_active_monitor(self) -> None:
        """Test function monitoring with active monitor."""
        monitor = FlextObservabilityMonitor()
        monitor.flext_initialize_observability()
        monitor.flext_start_monitoring()

        @flext_monitor_function(monitor)
        def test_func(x: int, y: int) -> int:
            return x + y

        result = test_func(1, 2)
        if result != EXPECTED_DATA_COUNT:
            raise AssertionError(f"Expected {3}, got {result}")

    def test_monitor_function_with_kwargs(self) -> None:
        """Test function monitoring with keyword arguments."""
        monitor = FlextObservabilityMonitor()
        monitor.flext_initialize_observability()
        monitor.flext_start_monitoring()

        @flext_monitor_function(monitor)
        def test_func(x: int, y: int = 10) -> int:
            return x + y

        result = test_func(5, y=15)
        if result != 20:
            raise AssertionError(f"Expected {20}, got {result}")

    def test_monitor_function_exception_handling(self) -> None:
        """Test function monitoring with exception."""
        monitor = FlextObservabilityMonitor()
        monitor.flext_initialize_observability()
        monitor.flext_start_monitoring()

        @flext_monitor_function(monitor)
        def test_func() -> None:
            msg = "Test error"
            raise ValueError(msg)

        with pytest.raises(ValueError, match="Test error"):
            test_func()

    def test_monitor_function_with_none_monitor(self) -> None:
        """Test function monitoring with None monitor."""

        @flext_monitor_function(None)
        def test_func(x: int) -> int:
            return x * 2

        result = test_func(5)
        if result != 10:
            raise AssertionError(f"Expected {10}, got {result}")

    def test_monitor_function_return_types(self) -> None:
        """Test function monitoring preserves return types."""
        monitor = FlextObservabilityMonitor()

        @flext_monitor_function(monitor)
        def return_string() -> str:
            return "test"

        @flext_monitor_function(monitor)
        def return_dict() -> FlextTypes.StringDict:
            return {"key": "value"}

        @flext_monitor_function(monitor)
        def return_none() -> None:
            return None

        if return_string() != "test":
            raise AssertionError(f"Expected {'test'}, got {return_string()}")
        assert return_dict() == {"key": "value"}
        assert return_none() is None
