"""Test entity validation error paths for complete coverage.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import pytest
from pydantic import ValidationError

from flext_observability import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
)


class TestEntityValidationErrors:
    """Test entity validation error paths to improve coverage."""

    def test_metric_invalid_name_validation(self) -> None:
        """Test FlextMetric with invalid name (empty string)."""
        with pytest.raises(ValidationError, match="Metric name cannot be empty"):
            FlextMetric(
                name="",  # Empty name should fail Pydantic validation
                value=42.0,
                unit="count",
            )

    def test_metric_invalid_value_validation(self) -> None:
        """Test FlextMetric with invalid value type."""
        metric = FlextMetric(
            name="test_metric",
            value=42.0,
            unit="count",
        )
        # Test business rule validation for negative values (currently allowed)
        setattr(metric, "value", -10.0)
        result = metric.validate_business_rules()
        # Current implementation allows negative values
        assert result.success

    def test_log_entry_invalid_message_validation(self) -> None:
        """Test FlextLogEntry with invalid message (empty string)."""
        with pytest.raises(ValidationError, match="Log message cannot be empty"):
            FlextLogEntry(
                message="",  # Empty message should fail Pydantic validation
                level="info",
            )

    def test_log_entry_invalid_level_validation(self) -> None:
        """Test FlextLogEntry with invalid level."""
        log_entry = FlextLogEntry(
            message="Test message",
            level="info",  # Valid level for construction
        )
        # Test business rule validation for invalid level after creation (bypass Pydantic validation)
        setattr(log_entry, "level", "INVALID_LEVEL")
        result = log_entry.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Invalid log level" in result.error

    def test_trace_invalid_trace_id_validation(self) -> None:
        """Test FlextTrace trace_id validation (empty string)."""
        with pytest.raises(ValidationError, match="Trace ID cannot be empty"):
            FlextTrace(
                operation="test_operation",
                trace_id="",  # Empty trace_id should fail validation
                span_id="span_123",
            )

    def test_trace_invalid_operation_validation(self) -> None:
        """Test FlextTrace with invalid operation (empty string)."""
        with pytest.raises(ValidationError, match="Operation name cannot be empty"):
            FlextTrace(
                operation="",  # Empty operation should fail Pydantic validation
                trace_id="trace_123",
                span_id="span_123",
            )

    def test_alert_invalid_title_validation(self) -> None:
        """Test FlextAlert with invalid message (empty string)."""
        with pytest.raises(ValidationError, match="Alert message cannot be empty"):
            FlextAlert(
                title="Test Alert",
                message="",  # Empty message should fail Pydantic validation
                severity="medium",
            )

    def test_alert_invalid_message_validation(self) -> None:
        """Test FlextAlert business rule validation."""
        alert = FlextAlert(
            title="Test Alert",
            message="Valid message",
            severity="low",
        )
        # Test business rule validation for empty message after creation (bypass Pydantic validation)
        setattr(alert, "message", "")
        result = alert.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Invalid alert message" in result.error

    def test_alert_invalid_severity_validation(self) -> None:
        """Test FlextAlert with invalid level."""
        alert = FlextAlert(
            title="Test Alert",
            message="Test message",
            severity="low",  # Valid severity for construction
        )
        # Test business rule validation for invalid severity after creation (bypass Pydantic validation)
        setattr(alert, "severity", "invalid_severity")
        result = alert.validate_business_rules()
        assert result.is_failure
        assert result.error is not None
        assert "Invalid alert severity" in result.error

    def test_health_check_invalid_component_validation(self) -> None:
        """Test FlextHealthCheck with invalid service_name (empty string)."""
        with pytest.raises(ValidationError, match="Component name cannot be empty"):
            FlextHealthCheck(
                component="",  # Empty component should fail Pydantic validation
                status="healthy",
            )

    def test_health_check_invalid_status_validation(self) -> None:
        """Test FlextHealthCheck with invalid status."""
        with pytest.raises(ValidationError) as exc_info:
            FlextHealthCheck(
                component="test_component",
                status="invalid_status",  # Invalid status for business rules
            )
        assert "Invalid health status: invalid_status" in str(exc_info.value)
