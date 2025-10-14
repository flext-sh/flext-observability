"""Unit tests for flext_observability.exceptions module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_observability import (
    FlextAlertCreationError,
    FlextAlertEscalationError,
    FlextAlertingError,
    FlextHealthCheckError,
    FlextHealthMonitorError,
    FlextMetricsCollectionError,
    FlextMetricsError,
    FlextMetricsRecordingError,
    FlextMonitoringError,
    FlextMonitoringSetupError,
    FlextObservabilityConfigError,
    FlextObservabilityError,
    FlextObservabilityExceptions,
    FlextTraceCompleteError,
    FlextTraceStartError,
    FlextTracingError,
)


class TestFlextObservabilityExceptions:
    """Test the FlextObservabilityExceptions class."""

    def test_inherits_from_flext_exceptions(self) -> None:
        """Test that FlextObservabilityExceptions inherits from FlextCore.Exceptions."""
        from flext_core import FlextCore

        assert issubclass(FlextObservabilityExceptions, FlextCore.Exceptions)


class TestFlextObservabilityError:
    """Test the base FlextObservabilityError exception."""

    def test_inherits_from_exception(self) -> None:
        """Test that FlextObservabilityError inherits from Exception."""
        assert issubclass(FlextObservabilityError, Exception)

    def test_error_creation(self) -> None:
        """Test error creation with message."""
        error = FlextObservabilityError("Test error message")
        assert str(error) == "Test error message"

    def test_error_with_code(self) -> None:
        """Test error creation with error code."""
        error = FlextObservabilityError("Test error", error_code="TEST_001")
        assert str(error) == "Test error"
        assert hasattr(error, "error_code")


class TestFlextMetricsError:
    """Test metrics-related exceptions."""

    def test_inherits_from_observability_error(self) -> None:
        """Test that FlextMetricsError inherits from FlextObservabilityError."""
        assert issubclass(FlextMetricsError, FlextObservabilityError)

    def test_collection_error_inheritance(self) -> None:
        """Test that FlextMetricsCollectionError inherits from FlextMetricsError."""
        assert issubclass(FlextMetricsCollectionError, FlextMetricsError)

    def test_recording_error_inheritance(self) -> None:
        """Test that FlextMetricsRecordingError inherits from FlextMetricsError."""
        assert issubclass(FlextMetricsRecordingError, FlextMetricsError)


class TestFlextTracingError:
    """Test tracing-related exceptions."""

    def test_inherits_from_observability_error(self) -> None:
        """Test that FlextTracingError inherits from FlextObservabilityError."""
        assert issubclass(FlextTracingError, FlextObservabilityError)

    def test_trace_start_error_inheritance(self) -> None:
        """Test that FlextTraceStartError inherits from FlextTracingError."""
        assert issubclass(FlextTraceStartError, FlextTracingError)

    def test_trace_complete_error_inheritance(self) -> None:
        """Test that FlextTraceCompleteError inherits from FlextTracingError."""
        assert issubclass(FlextTraceCompleteError, FlextTracingError)


class TestFlextAlertingError:
    """Test alerting-related exceptions."""

    def test_inherits_from_observability_error(self) -> None:
        """Test that FlextAlertingError inherits from FlextObservabilityError."""
        assert issubclass(FlextAlertingError, FlextObservabilityError)

    def test_alert_creation_error_inheritance(self) -> None:
        """Test that FlextAlertCreationError inherits from FlextAlertingError."""
        assert issubclass(FlextAlertCreationError, FlextAlertingError)

    def test_alert_escalation_error_inheritance(self) -> None:
        """Test that FlextAlertEscalationError inherits from FlextAlertingError."""
        assert issubclass(FlextAlertEscalationError, FlextAlertingError)


class TestFlextHealthCheckError:
    """Test health check-related exceptions."""

    def test_inherits_from_observability_error(self) -> None:
        """Test that FlextHealthCheckError inherits from FlextObservabilityError."""
        assert issubclass(FlextHealthCheckError, FlextObservabilityError)

    def test_health_monitor_error_inheritance(self) -> None:
        """Test that FlextHealthMonitorError inherits from FlextHealthCheckError."""
        assert issubclass(FlextHealthMonitorError, FlextHealthCheckError)


class TestFlextMonitoringError:
    """Test monitoring-related exceptions."""

    def test_inherits_from_observability_error(self) -> None:
        """Test that FlextMonitoringError inherits from FlextObservabilityError."""
        assert issubclass(FlextMonitoringError, FlextObservabilityError)

    def test_monitoring_setup_error_inheritance(self) -> None:
        """Test that FlextMonitoringSetupError inherits from FlextMonitoringError."""
        assert issubclass(FlextMonitoringSetupError, FlextMonitoringError)


class TestFlextObservabilityConfigError:
    """Test configuration-related exceptions."""

    def test_inherits_from_observability_error(self) -> None:
        """Test that FlextObservabilityConfigError inherits from FlextObservabilityError."""
        assert issubclass(FlextObservabilityConfigError, FlextObservabilityError)


class TestErrorCodes:
    """Test error codes functionality."""

    def test_error_codes_class_exists(self) -> None:
        """Test that FlextObservabilityErrorCodes class exists."""
        assert hasattr(FlextObservabilityExceptions, "FlextObservabilityErrorCodes")

    def test_error_codes_constants(self) -> None:
        """Test that error code constants are defined."""
        error_codes = FlextObservabilityExceptions.FlextObservabilityErrorCodes

        # Test some key error codes exist
        assert hasattr(error_codes, "METRICS_COLLECTION_FAILED")
        assert hasattr(error_codes, "TRACING_START_FAILED")
        assert hasattr(error_codes, "ALERT_CREATION_FAILED")
        assert hasattr(error_codes, "CONFIG_VALIDATION_FAILED")
