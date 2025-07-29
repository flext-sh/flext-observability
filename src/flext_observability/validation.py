"""FLEXT Observability Validation & Exceptions - Consolidated using flext-core.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Consolidated validation and exceptions using flext-core patterns.
"""

from __future__ import annotations

import re
from typing import Any

from flext_core import FlextResult

from flext_observability.constants import ObservabilityConstants

# ============================================================================
# VALIDATION - Simplified and consolidated
# ============================================================================


class ObservabilityValidators:
    """Consolidated validators for observability data."""

    @staticmethod
    def is_valid_string(value: Any) -> bool:
        """Check if value is a valid non-empty string."""
        return isinstance(value, str) and len(value.strip()) > 0

    @staticmethod
    def is_valid_dict(value: Any) -> bool:
        """Check if value is a valid dictionary."""
        return isinstance(value, dict)

    @staticmethod
    def is_valid_boolean(value: Any) -> bool:
        """Check if value is a valid boolean."""
        return isinstance(value, bool)

    @staticmethod
    def is_valid_numeric(value: Any) -> bool:
        """Check if value is numeric."""
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    @staticmethod
    def is_valid_metric_name(value: Any) -> bool:
        """Validate metric name."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_.-]*$", value))

    @staticmethod
    def is_valid_metric_value(value: Any) -> bool:
        """Validate metric value."""
        return ObservabilityValidators.is_valid_numeric(value)

    @staticmethod
    def is_valid_log_level(value: Any) -> bool:
        """Validate log level."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return value.lower() in ObservabilityConstants.LOG_LEVELS

    @staticmethod
    def is_valid_log_message(value: Any) -> bool:
        """Validate log message."""
        return ObservabilityValidators.is_valid_string(value) and len(value) <= 10000

    @staticmethod
    def is_valid_trace_id(value: Any) -> bool:
        """Validate trace ID."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return bool(re.match(r"^[a-fA-F0-9-]{16,64}$", value))

    @staticmethod
    def is_valid_operation_name(value: Any) -> bool:
        """Validate operation name."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_.-]*$", value))

    @staticmethod
    def is_valid_alert_title(value: Any) -> bool:
        """Validate alert title."""
        return ObservabilityValidators.is_valid_string(value) and len(value) <= 200

    @staticmethod
    def is_valid_alert_severity(value: Any) -> bool:
        """Validate alert severity."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return value.lower() in ObservabilityConstants.ALERT_SEVERITIES

    @staticmethod
    def is_valid_component_name(value: Any) -> bool:
        """Validate component name."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_.-]*$", value))

    @staticmethod
    def is_valid_health_status(value: Any) -> bool:
        """Validate health status."""
        if not ObservabilityValidators.is_valid_string(value):
            return False
        return value.lower() in ObservabilityConstants.HEALTH_STATUSES


# ============================================================================
# EXCEPTIONS - Consolidated with validation
# ============================================================================

def create_observability_result_error(
    error_type: str,
    message: str,
    **context: Any,
) -> FlextResult[Any]:
    """Create standardized observability error result."""
    return FlextResult.error(f"[{error_type.upper()}] {message}", context=context)
