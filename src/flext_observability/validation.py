"""FLEXT Observability Validation & Exceptions - Consolidated using flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Consolidated validation and exceptions using flext-core patterns.
"""

from __future__ import annotations

import re

from flext_core import FlextResult

from flext_observability.constants import ObservabilityConstants

# Constants for validation
MAX_LOG_MESSAGE_LENGTH = 10000
MAX_ALERT_TITLE_LENGTH = 200

# ============================================================================
# VALIDATION - Simplified and consolidated
# ============================================================================


class ObservabilityValidators:
    """Consolidated validators for observability data."""

    @staticmethod
    def is_valid_string(value: object) -> bool:
        """Check if value is a valid non-empty string."""
        return isinstance(value, str) and len(value.strip()) > 0

    @staticmethod
    def is_valid_dict(value: object) -> bool:
        """Check if value is a valid dictionary."""
        return isinstance(value, dict)

    @staticmethod
    def is_valid_boolean(value: object) -> bool:
        """Check if value is a valid boolean."""
        return isinstance(value, bool)

    @staticmethod
    def is_valid_numeric(value: object) -> bool:
        """Check if value is numeric."""
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    @staticmethod
    def is_valid_metric_name(value: object) -> bool:
        """Validate metric name."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_.-]*$", str(value)))

    @staticmethod
    def is_valid_metric_value(value: object) -> bool:
        """Validate metric value."""
        return ObservabilityValidators.is_valid_numeric(value)

    @staticmethod
    def is_valid_log_level(value: object) -> bool:
        """Validate log level."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return str(value).lower() in ObservabilityConstants.LOG_LEVELS

    @staticmethod
    def is_valid_log_message(value: object) -> bool:
        """Validate log message."""
        return (
            ObservabilityValidators.is_valid_string(value)
            and len(str(value)) <= MAX_LOG_MESSAGE_LENGTH
        )

    @staticmethod
    def is_valid_trace_id(value: object) -> bool:
        """Validate trace ID."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return bool(re.match(r"^[a-fA-F0-9-]{16,64}$", str(value)))

    @staticmethod
    def is_valid_operation_name(value: object) -> bool:
        """Validate operation name."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_.-]*$", str(value)))

    @staticmethod
    def is_valid_alert_title(value: object) -> bool:
        """Validate alert title."""
        return (
            ObservabilityValidators.is_valid_string(value)
            and len(str(value)) <= MAX_ALERT_TITLE_LENGTH
        )

    @staticmethod
    def is_valid_alert_severity(value: object) -> bool:
        """Validate alert severity."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return str(value).lower() in ObservabilityConstants.ALERT_SEVERITIES

    @staticmethod
    def is_valid_component_name(value: object) -> bool:
        """Validate component name."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_.-]*$", str(value)))

    @staticmethod
    def is_valid_health_status(value: object) -> bool:
        """Validate health status."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return str(value).lower() in ObservabilityConstants.HEALTH_STATUSES


# ============================================================================
# EXCEPTIONS - Consolidated with validation
# ============================================================================


def create_observability_result_error(
    error_type: str,
    message: str,
    **context: object,
) -> FlextResult[object]:
    """Create standardized observability error result."""
    # Note: Context is logged but not passed to FlextResult.fail
    # as it only accepts error message string
    error_msg = f"[{error_type.upper()}] {message}"
    if context:
        context_str = " | ".join(f"{k}={v}" for k, v in context.items())
        error_msg += f" | Context: {context_str}"
    return FlextResult.fail(error_msg)
