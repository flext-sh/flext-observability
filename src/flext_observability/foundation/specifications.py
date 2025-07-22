"""Observability Specifications - Business Rules and Constraints.

Specifications encapsulate business rules and constraints
for observability components using the Specification pattern.
"""

from __future__ import annotations

import abc
from typing import Any

from flext_core import SpecificationPattern


class ObservabilitySpecification[T](SpecificationPattern[T], abc.ABC):
    """Base specification for observability domain rules.

    Encapsulates business rules and constraints that apply
    to observability data and operations.
    """

    @abc.abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        """Check if the candidate satisfies this specification."""


# Domain-specific specifications

class MetricValiditySpecification(ObservabilitySpecification[dict[str, Any]]):
    """Specification for valid metric data.

    Ensures metrics have required fields and valid values.
    """

    def is_satisfied_by(self, metric: dict[str, Any]) -> bool:
        """Check if metric data is valid."""
        required_fields = {"name", "value", "timestamp"}

        # Check required fields
        if not required_fields.issubset(metric.keys()):
            return False

        # Check name is non-empty string
        if not isinstance(metric["name"], str) or not metric["name"].strip():
            return False

        # Check value is numeric
        if not isinstance(metric["value"], (int, float)):
            return False

        # Check timestamp is valid
        return isinstance(metric["timestamp"], (int, float))


class TraceValiditySpecification(ObservabilitySpecification[dict[str, Any]]):
    """Specification for valid trace data.

    Ensures traces have required fields and proper structure.
    """

    def is_satisfied_by(self, trace: dict[str, Any]) -> bool:
        """Check if trace data is valid."""
        required_fields = {"trace_id", "span_id", "operation_name", "start_time"}

        # Check required fields
        if not required_fields.issubset(trace.keys()):
            return False

        # Check IDs are non-empty strings
        for id_field in ["trace_id", "span_id"]:
            if not isinstance(trace[id_field], str) or not trace[id_field].strip():
                return False

        # Check operation name
        if not isinstance(trace["operation_name"], str) or not trace["operation_name"].strip():
            return False

        # Check start time
        if not isinstance(trace["start_time"], (int, float)):
            return False

        # If end_time exists, it should be after start_time
        if "end_time" in trace:
            if not isinstance(trace["end_time"], (int, float)):
                return False
            if trace["end_time"] < trace["start_time"]:
                return False

        return True


class LogValiditySpecification(ObservabilitySpecification[dict[str, Any]]):
    """Specification for valid log entry data.

    Ensures log entries have required fields and proper structure.
    """

    def is_satisfied_by(self, log: dict[str, Any]) -> bool:
        """Check if log entry is valid."""
        required_fields = {"level", "message", "timestamp"}

        # Check required fields
        if not required_fields.issubset(log.keys()):
            return False

        # Check level is valid
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if log["level"] not in valid_levels:
            return False

        # Check message is non-empty string
        if not isinstance(log["message"], str) or not log["message"].strip():
            return False

        # Check timestamp
        return isinstance(log["timestamp"], (int, float))


class AlertRuleValiditySpecification(ObservabilitySpecification[dict[str, Any]]):
    """Specification for valid alert rule configuration.

    Ensures alert rules have proper configuration and constraints.
    """

    def is_satisfied_by(self, rule: dict[str, Any]) -> bool:
        """Check if alert rule is valid."""
        required_fields = {"rule_id", "condition", "threshold", "notification_channels"}

        # Check required fields
        if not required_fields.issubset(rule.keys()):
            return False

        # Check rule_id is non-empty string
        if not isinstance(rule["rule_id"], str) or not rule["rule_id"].strip():
            return False

        # Check condition is non-empty string
        if not isinstance(rule["condition"], str) or not rule["condition"].strip():
            return False

        # Check threshold is numeric
        if not isinstance(rule["threshold"], (int, float)):
            return False

        # Check notification_channels is non-empty list
        return not (not isinstance(rule["notification_channels"], list) or not rule["notification_channels"])


class HealthCheckValiditySpecification(ObservabilitySpecification[dict[str, Any]]):
    """Specification for valid health check configuration.

    Ensures health checks have proper configuration.
    """

    def is_satisfied_by(self, check: dict[str, Any]) -> bool:
        """Check if health check is valid."""
        required_fields = {"component_name", "check_function"}

        # Check required fields
        if not required_fields.issubset(check.keys()):
            return False

        # Check component_name is non-empty string
        if not isinstance(check["component_name"], str) or not check["component_name"].strip():
            return False

        # Check check_function is callable
        return callable(check["check_function"])
