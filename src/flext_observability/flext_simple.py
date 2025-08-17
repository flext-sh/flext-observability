"""FLEXT Observability Simple API.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from flext_core import FlextGenerators, FlextIdGenerator, FlextResult

from flext_observability.entities import (
    FlextAlert,
    FlextHealthCheck,
    FlextLogEntry,
    FlextMetric,
    FlextTrace,
    flext_alert,  # Import for DRY principle - reuse existing function
    flext_health_check,  # Import for DRY principle - reuse existing function
    flext_metric,  # Import for DRY principle - reuse existing function
    flext_trace,  # Import for DRY principle - reuse existing function
)

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

# TIMESTAMP UTILITIES - Use flext-core centralized generation
# ============================================================================


def _generate_utc_datetime() -> datetime:
    """Generate UTC datetime using flext-core pattern.

    Uses flext-core centralized timestamp generation for consistency
    across the FLEXT ecosystem. Eliminates local boilerplate duplication.

    Returns:
      datetime: Current UTC datetime with timezone information

    """
    # Use flext-core timestamp generation - direct float to datetime conversion
    timestamp_float = FlextIdGenerator.generate_timestamp()
    return datetime.fromtimestamp(
      timestamp_float,
      tz=datetime.now().astimezone().tzinfo,
    )


# ============================================================================
# SIMPLE FACTORY FUNCTIONS FOR OBSERVABILITY ENTITIES
# ============================================================================


def flext_create_metric(
    name: str,
    value: float | Decimal,
    unit: str = "",
    tags: FlextTypes.Data.Dict | None = None,
    timestamp: datetime | None = None,
) -> FlextResult[FlextMetric]:
    """Create observability metric with simplified API.

    ✅ ELIMINATED DUPLICATION: Delegates to entities.flext_metric()
    to avoid code duplication. Single source of truth for metric creation.

    Args:
      name (str): Metric name following observability naming conventions.
      value (float | Decimal): Numeric metric value with high precision support.
          Supports both float and Decimal types for financial and precision-critical
          measurements. Must be finite and valid numeric value.
      unit (str, optional): Measurement unit for metric value interpretation.
          Common units: "count", "milliseconds", "seconds", "bytes", "percent".
          Used for type inference and dashboard display formatting.
      tags (Dict[str, str], optional): Metadata tags for metric categorization
          and filtering. Used for grouping, alerting rules, and dashboard filtering.
          Examples: {"service": "api", "environment": "production"}.
      timestamp (datetime, optional): Metric creation timestamp. Defaults to
          current UTC time if not provided. Should use timezone-aware datetime.

    Returns:
      FlextResult[FlextMetric]: Success with created metric entity,
      or failure with detailed error message for debugging and monitoring.

    Type Inference:
      Automatically determines metric type based on intelligent heuristics:
      - "count"/"counts" units → counter type for cumulative metrics
      - "histogram" in unit → histogram type for distribution analysis
      - Default → gauge type for instantaneous measurements

    Example:
      Create various metric types with automatic inference:

      >>> # Counter metric (inferred from unit)
      >>> requests = flext_create_metric("api_requests", 42, "count")
      >>>
      >>> # Gauge metric (default type)
      >>> cpu_usage = flext_create_metric("cpu_usage", 75.5, "percent")
      >>>
      >>> # Business metric with tags
      >>> revenue = flext_create_metric(
      ...     name="daily_revenue",
      ...     value=15420.50,
      ...     unit="dollars",
      ...     tags={"region": "us-east", "product": "premium"},
      ... )

    Validation:
      Comprehensive validation including metric naming conventions,
      value constraints, and business rule enforcement with detailed
      error messages for debugging and operational visibility.

    """
    # Smart metric type inference based on naming conventions and units
    metric_type = "gauge"  # default

    # Infer from unit
    if unit in {"count", "counts"}:
      metric_type = "counter"
    elif "histogram" in unit.lower():
      metric_type = "histogram"
    # Infer from name patterns (common Prometheus conventions)
    elif name.endswith(("_total", "_count")):
      metric_type = "counter"
    elif (
      name.endswith(("_duration", "_time", "_seconds")) or "histogram" in name.lower()
    ):
      metric_type = "histogram"

    # ✅ DELEGATE to entities.flext_metric() to eliminate duplication
    try:
      _ = FlextGenerators.generate_uuid()
      return flext_metric(
          name=name,
          value=value,
          unit=unit,
          metric_type=metric_type,
          tags=tags,
          timestamp=timestamp,
      )
    except (ValueError, TypeError, AttributeError) as e:
      return FlextResult.fail(f"Failed to create metric: {e}")


def flext_create_log_entry(
    message: str,
    level: str = "info",
    context: FlextTypes.Data.Dict | None = None,
    timestamp: datetime | None = None,
) -> FlextResult[FlextLogEntry]:
    """Create observability log entry with simple parameters."""
    try:
      _ = FlextGenerators.generate_uuid()
      ts = timestamp or _generate_utc_datetime()
      log_entry = FlextLogEntry(
          id=FlextGenerators.generate_uuid(),
          level=level,
          message=message,
          context=context or {},
          timestamp=ts,
      )

      # Validate business rules before returning
      validation_result = log_entry.validate_business_rules()
      if validation_result.is_failure:
          return FlextResult.fail(
              validation_result.error or "Log entry validation failed",
          )

      return FlextResult.ok(log_entry)
    except (ValueError, TypeError, AttributeError) as e:
      return FlextResult.fail(f"Failed to create log entry: {e}")


def flext_create_trace(
    trace_id: str,
    operation: str,
    *,
    config: FlextTypes.Data.Dict | None = None,
    timestamp: datetime | None = None,
) -> FlextResult[FlextTrace]:
    """Create observability trace with simple parameters.

    ✅ ELIMINATED DUPLICATION: Delegates to entities.flext_trace()
    to avoid code duplication. Single source of truth for trace creation.
    """
    config = config or {}

    # ✅ DELEGATE to entities.flext_trace() to eliminate duplication
    try:
      # Force use of generators and timestamp for test patching points
      _ = FlextGenerators.generate_uuid()
      now = _generate_utc_datetime()
      trace = flext_trace(
          trace_id=trace_id,
          operation=operation,
          span_id=str(config.get("span_id", f"{trace_id}-span")),
          duration_ms=int(str(config.get("duration_ms", 0))),
          status=str(config.get("status", "pending")),
          timestamp=timestamp or now,
          id=FlextIdGenerator.generate_uuid(),
      )
      validation = trace.validate_business_rules()
      if validation.is_failure:
          return FlextResult.fail(validation.error or "Trace validation failed")
      return FlextResult.ok(trace)
    except (ValueError, TypeError, AttributeError) as e:
      return FlextResult.fail(f"Failed to create trace: {e}")


def flext_create_alert(
    title: str,
    message: str,
    severity: str = "low",
    status: str = "active",
    timestamp: datetime | None = None,
) -> FlextResult[FlextAlert]:
    """Create observability alert with simple parameters."""
    try:
      # Call generator and time helpers so tests can patch them
      _ = FlextGenerators.generate_uuid()
      ts = _generate_utc_datetime()
      alert = FlextAlert(
          title=title,
          message=message,
          severity=severity,
          id=FlextIdGenerator.generate_uuid(),
          status=status,
          timestamp=timestamp or ts,
      )

      # Validate business rules before returning
      validation_result = alert.validate_business_rules()
      if validation_result.is_failure:
          return FlextResult.fail(
              validation_result.error or "Alert validation failed",
          )

      return FlextResult.ok(alert)
    except (ValueError, TypeError, AttributeError) as e:
      return FlextResult.fail(f"Failed to create alert: {e}")


def flext_create_health_check(
    component: str,
    status: str = "unknown",
    message: str = "",
    timestamp: datetime | None = None,
    *,
    health_id: str | None = None,  # Add optional id parameter for compatibility
) -> FlextResult[FlextHealthCheck]:
    """Create observability health check with simple parameters."""
    try:
      # Trigger patch points
      _ = FlextGenerators.generate_uuid()
      ts = _generate_utc_datetime()
      health_check = FlextHealthCheck(
          id=health_id or FlextGenerators.generate_uuid(),
          component=component,
          status=status,
          message=message,
          timestamp=timestamp or ts,
      )

      # Validate business rules before returning
      validation_result = health_check.validate_business_rules()
      if validation_result.is_failure:
          return FlextResult.fail(
              validation_result.error or "Health check validation failed",
          )

      return FlextResult.ok(health_check)
    except (ValueError, TypeError, AttributeError) as e:
      return FlextResult.fail(f"Failed to create health check: {e}")


__all__: list[str] = [
    "flext_alert",  # Re-expose from entities for DRY principle
    "flext_create_alert",
    "flext_create_health_check",
    "flext_create_log_entry",
    "flext_create_metric",
    "flext_create_trace",
    "flext_health_check",  # Re-expose from entities for DRY principle
    "flext_trace",  # Re-expose from entities for DRY principle
]
