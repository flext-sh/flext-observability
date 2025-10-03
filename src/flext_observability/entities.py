"""FLEXT Observability Entities Module.

This module provides unified observability entity definitions following the
FLEXT ecosystem patterns. All entities are organized under a single namespace
class to reduce file-level complexity while maintaining clean architecture.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import math
import time
import uuid
from datetime import UTC, datetime
from decimal import Decimal
from typing import cast

from pydantic import ConfigDict, Field, field_validator

from flext_core import (
    FlextLogger,
    FlextMixins,
    FlextModels,
    FlextResult,
)
from flext_observability.typings import FlextObservabilityTypes


class FlextObservabilityEntities:
    """Unified namespace for all FLEXT observability entities.

    Single class containing all observability domain entities following
    unified class pattern. Reduces file-level complexity while maintaining
    clean separation of concerns and domain-driven design principles.
    """

    class UtilitiesGenerators:
            """Utility generators for entity creation and IDs.

            Compatibility shim for tests expecting FlextUtilities.Generators.
            Maps to flext-core functions with observability-specific extensions.
            """

            @staticmethod
            def generate_timestamp() -> float:
                """Generate a timestamp."""
                return time.time()

            @staticmethod
            def generate_uuid() -> str:
                """Generate a UUID string."""
                return str(uuid.uuid4())

            @staticmethod
            def generate_entity_id() -> str:
                """Generate an entity ID."""
                return str(uuid.uuid4())

            @staticmethod
            def generate_correlation_id() -> str:
                """Generate a correlation ID."""
                return str(uuid.uuid4())

            @staticmethod
            def generate_iso_timestamp() -> str:
                """Generate an ISO timestamp string."""
                return datetime.now(tz=UTC).isoformat()

            # ============================================================================
            # TIMESTAMP UTILITIES - Use flext-core centralized generation
            # ============================================================================

            @staticmethod
            def _generate_utc_datetime() -> datetime:
                """Generate UTC datetime using flext-core pattern.

                Uses flext-core centralized timestamp generation for consistency
                across the FLEXT ecosystem. Eliminates local boilerplate duplication.

                Returns:
                  datetime: Current UTC datetime with timezone information
                """
                return datetime.now(tz=UTC)


        # ============================================================================
        # CORE ENTITIES - Simplified using flext-core patterns
        # ============================================================================

    class FlextMetric(FlextModels.Entity):
        """Observability metric entity for collecting and validating measurement data.

    Core domain entity representing a single metric measurement with comprehensive
    validation, type safety, and business rule enforcement. Supports both float
    and Decimal values for financial precision, includes metadata tags for
    categorization, and implements domain-driven validation patterns.

    Attributes:
      name: Metric identifier following naming conventions (e.g., "api_response_time")
      value: Numeric measurement value supporting float and Decimal types
      unit: Unit of measurement (e.g., "seconds", "bytes", "count", "percent")
      tags: Key-value metadata for metric categorization and filtering
      timestamp: UTC timestamp of metric creation (auto-generated)
      metric_type: Metric classification ("gauge", "counter", "histogram")

    Domain Rules:
      - Name must be non-empty string following naming conventions
      - Value must be numeric (float, int, or Decimal) and convertible
      - Metric type must be valid classification
      - Timestamp automatically set to UTC creation time

    Example:
      Create and validate a performance metric:

      >>> metric = FlextMetric(
      ...     name="api_response_time",
      ...     value=150.5,
      ...     unit="milliseconds",
      ...     tags={"service": user - api, "endpoint": "/users"},
      ...     metric_type="histogram",
      ... )
      >>> validation = metric.validate_business_rules()
      >>> assert validation.success

      Create financial metric with decimal precision:

      >>> from decimal import Decimal
      >>> financial_metric = FlextMetric(
      ...     name="transaction_amount",
      ...     value=Decimal("1234.56"),
      ...     unit="USD",
      ...     tags={"account_type": "premium"},
      ... )

    Integration:
      - Created via FlextObservabilityMasterFactory.create_metric()
      - Processed by FlextMetricsService for collection and storage
      - Exported via Prometheus-compatible formatters
      - Used across FLEXT ecosystem for consistent metrics collection

        """

        model_config = ConfigDict(
            frozen=False,  # Allow dynamic attributes
        )

        name: str = Field(..., description="Metric name")
        value: float | Decimal = Field(..., description="Metric value")
        unit: str = Field(default="", description="Metric unit")
        tags: FlextObservabilityTypes.Core.TagsDict = Field(
            default_factory=dict, description="Metric tags"
        )
        timestamp: datetime = Field(default_factory=FlextObservabilityEntities._generate_utc_datetime)
        metric_type: str = Field(default="gauge", description="Metric type")

        @field_validator("name")
        @classmethod
        def validate_metric_name(cls, v: str) -> str:
            """Validate metric name is non-empty and follows naming conventions."""
            if not (v and str(v).strip()):
                msg = "Metric name cannot be empty"
                raise ValueError(msg)
            return v

        @field_validator("value")
        @classmethod
        def validate_metric_value(cls, v: float | Decimal) -> float | Decimal:
            """Validate metric value is numeric and not NaN/infinite."""
            # Try to convert to float to validate it's numeric
            try:
                float_val = float(v)
            except (ValueError, TypeError) as e:
                msg = "Metric value must be numeric"
                raise ValueError(msg) from e

            # Check for NaN and infinite values after successful float conversion
            if math.isnan(float_val) or math.isinf(float_val):
                cls._raise_invalid_metric_value()

            return v

        @classmethod
        def _raise_invalid_metric_value(cls: object) -> None:
            """Helper to raise metric value error."""
            msg = "Metric value cannot be NaN or infinite"
            raise ValueError(msg)

        @field_validator("metric_type")
        @classmethod
        def validate_metric_type(cls, v: str) -> str:
            """Validate metric type is a valid classification."""
            valid_types = {"gauge", "counter", "histogram", "summary"}
            if v not in valid_types:
                msg = f"Invalid metric type: {v}. Must be one of {valid_types}"
                raise ValueError(msg)
            return v

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate metric business rules and domain constraints.

            Implements comprehensive business rule validation including name verification,
            value type checking, and domain rule enforcement. Follows railway-oriented
            programming patterns with FlextResult error handling following foundation patterns.

            """
            # Use direct validation for standardized validation
            if not (self.name and str(self.name).strip()):
                return FlextResult[None].fail("Invalid metric name")

            if not isinstance(self.value, (int, float)):
                try:
                    float(self.value)  # Test if it can be converted to float
                except (ValueError, TypeError):
                    return FlextResult[None].fail("Invalid metric value")
            return FlextResult[None].ok(None)


    class FlextLogEntry(FlextModels.Entity):
            """Structured Logging Entity for FLEXT Ecosystem.

        Enterprise-grade structured logging entity implementing comprehensive logging
        semantics with severity classification, rich contextual information, and
        correlation ID support. Designed for centralized log aggregation, searchability,
        and business intelligence across the FLEXT data integration platform.

            """

            message: str = Field(..., description="Log message")
            level: str = Field(default="info", description="Log level")
            context: FlextObservabilityTypes.Core.MetadataDict = Field(
                default_factory=dict,
                description="Log context",
            )
            timestamp: datetime = Field(default_factory=FlextObservabilityEntities._generate_utc_datetime)

            @field_validator("message")
            @classmethod
            def validate_log_message(cls, v: str) -> str:
                """Validate log message is non-empty and meaningful."""
                if not (v and str(v).strip()):
                    msg = "Log message cannot be empty"
                    raise ValueError(msg)
                return v

            @field_validator("level")
            @classmethod
            def validate_log_level(cls, v: str) -> str:
                """Validate log level is a valid severity classification."""
                valid_levels = {"debug", "info", "warning", "error", "critical"}
                if v not in valid_levels:
                    msg = f"Invalid log level: {v}. Must be one of {valid_levels}"
                    raise ValueError(msg)
                return v

            def validate_business_rules(self) -> FlextResult[None]:
                """Validate structured logging business rules and domain constraints.

                Enforces business rules specific to structured logging within the FLEXT
                ecosystem, ensuring log data integrity and compatibility with log aggregation
                infrastructure. Validates message content, severity levels, and domain
                constraints for reliable log processing and searchability.

                """
                # Use direct validation for standardized validation
                if not (self.message and str(self.message).strip()):
                    return FlextResult[None].fail("Invalid log message")
                if self.level not in {"debug", "info", "warning", "error", "critical"}:
                    return FlextResult[None].fail("Invalid log level")
                return FlextResult[None].ok(None)


    class FlextTrace(FlextModels.Entity):
        """Distributed Tracing Span Entity for FLEXT Ecosystem.

    Enterprise-grade distributed tracing entity implementing OpenTelemetry-compatible
    span semantics with comprehensive context propagation, timing precision, and
    cross-service correlation. Enables end-to-end request tracking across the FLEXT
    data integration platform, supporting complex workflows involving Singer taps,
    DBT transformations, and Meltano orchestration.

    This entity represents a single span within a distributed trace, capturing
    operation timing, business context, and hierarchical relationships for
    comprehensive observability across microservices and data processing pipelines.

    """

    trace_id: str = Field(..., description="Trace ID")
    operation: str = Field(..., description="Operation name")
    span_id: str = Field(..., description="Span ID")
    span_attributes: FlextObservabilityTypes.Core.SpanAttributesDict = Field(
        default_factory=dict,
        description="Span attributes",
    )
    duration_ms: int = Field(default=0, description="Duration in milliseconds")
    status: str = Field(default="pending", description="Trace status")
    timestamp: datetime = Field(default_factory=FlextObservabilityEntities._generate_utc_datetime)

    @field_validator("trace_id")
    @classmethod
    def validate_trace_id(cls, v: str) -> str:
        """Validate trace ID is non-empty for global correlation."""
        if not (v and str(v).strip()):
            msg = "Trace ID cannot be empty"
            raise ValueError(msg)
        return v

    @field_validator("operation")
    @classmethod
    def validate_operation_name(cls, v: str) -> str:
        """Validate operation name is meaningful and searchable."""
        if not (v and str(v).strip()):
            msg = "Operation name cannot be empty"
            raise ValueError(msg)
        return v

    @field_validator("span_id")
    @classmethod
    def validate_span_id(cls, v: str) -> str:
        """Validate span ID is non-empty for unique identification."""
        if not (v and str(v).strip()):
            msg = "Span ID cannot be empty"
            raise ValueError(msg)
        return v

    @field_validator("duration_ms")
    @classmethod
    def validate_duration(cls, v: int) -> int:
        """Validate duration is non-negative for timing consistency."""
        if v < 0:
            msg = "Duration must be non-negative"
            raise ValueError(msg)
        return v

    @field_validator("status")
    @classmethod
    def validate_trace_status(cls, v: str) -> str:
        """Validate status is a valid lifecycle state."""
        valid_statuses = {"pending", "completed", "error", "timeout"}
        if v not in valid_statuses:
            msg = f"Invalid trace status: {v}. Must be one of {valid_statuses}"
            raise ValueError(msg)
        return v

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate distributed tracing business rules and domain constraints.

        Enforces business rules specific to distributed tracing within the FLEXT
        ecosystem, ensuring trace data integrity and compatibility with tracing
        infrastructure. Validates required identifiers, data consistency, and
        domain constraints for reliable trace collection and analysis.

        """
        # Use direct validation for standardized validation
        if not (self.trace_id and str(self.trace_id).strip()):
            return FlextResult[None].fail("Invalid trace ID")
        if not (self.operation and str(self.operation).strip()):
            return FlextResult[None].fail("Invalid operation name")
        return FlextResult[None].ok(None)


    class FlextAlert(FlextModels.Entity):
        """Alert Management Entity for FLEXT Ecosystem Monitoring.

        Enterprise-grade alert entity implementing comprehensive alerting semantics
        with severity classification, lifecycle management, and rich contextual
        information. Designed for integration with monitoring systems, notification
        channels, and incident management workflows within the FLEXT data platform.

        """

        title: str = Field(..., description="Alert title")
        message: str = Field(..., description="Alert message")
        severity: str = Field(default="low", description="Alert severity")
        status: str = Field(default="active", description="Alert status")
        tags: FlextObservabilityTypes.Core.TagsDict = Field(
            default_factory=dict, description="Alert tags"
        )
        timestamp: datetime = Field(default_factory=FlextObservabilityEntities._generate_utc_datetime)

        @field_validator("title")
        @classmethod
        def validate_alert_title(cls, v: str) -> str:
            """Validate alert title is non-empty and descriptive."""
            if not (v and str(v).strip()):
                msg = "Alert title cannot be empty"
                raise ValueError(msg)
            return v

        @field_validator("message")
        @classmethod
        def validate_alert_message(cls, v: str) -> str:
            """Validate alert message provides sufficient detail."""
            if not (v and str(v).strip()):
                msg = "Alert message cannot be empty"
                raise ValueError(msg)
            return v

        @field_validator("severity")
        @classmethod
        def validate_alert_severity(cls, v: str) -> str:
            """Validate alert severity is a valid classification level."""
            valid_severities = {"low", "medium", "high", "critical", "emergency"}
            if v not in valid_severities:
                msg = f"Invalid alert severity: {v}. Must be one of {valid_severities}"
                raise ValueError(msg)
            return v

        @field_validator("status")
        @classmethod
        def validate_alert_status(cls, v: str) -> str:
            """Validate alert status is a valid lifecycle state."""
            valid_statuses = {"active", "acknowledged", "resolved", "suppressed"}
            if v not in valid_statuses:
                msg = f"Invalid alert status: {v}. Must be one of {valid_statuses}"
                raise ValueError(msg)
            return v

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate alert management business rules and domain constraints.

            Enforces business rules specific to alert management within the FLEXT
            ecosystem, ensuring alert data integrity and compatibility with monitoring
            infrastructure. Validates required fields, severity levels, and domain
            constraints for reliable alert processing and incident response.

            Business Rules Validated:
                - Title must be non-empty and descriptive for identification
                - Message must provide sufficient detail for investigation
                - Severity must be valid classification level for routing
                - Status must be valid lifecycle state for workflow management
                - Tags should follow string-only conventions for filtering

            Returns:
                FlextResult[None]: Success if all business rules pass,
                failure with descriptive error message explaining violation.

            Example:
                >>> alert = FlextAlert(title="", message="test")  # Invalid empty title
                >>> result: FlextResult[object] = alert.validate_business_rules()
                >>> result.is_failure
                True
                >>> "title" in result.error
                True

            """
            # Use direct validation for standardized validation
            if not (self.title and str(self.title).strip()):
                return FlextResult[None].fail("Invalid alert title")
            if not (self.message and str(self.message).strip()):
                return FlextResult[None].fail("Invalid alert message")
            if self.severity not in {"low", "medium", "high", "critical", "emergency"}:
                return FlextResult[None].fail("Invalid alert severity")
            return FlextResult[None].ok(None)


    class FlextHealthCheck(FlextModels.Entity):
        """Health Monitoring Entity for FLEXT Ecosystem Components.

    Enterprise-grade health check entity implementing comprehensive service health
    semantics with status classification, diagnostic metrics, and dependency validation.
    Designed for continuous monitoring of FLEXT ecosystem components including
    services, databases, external integrations, and data processing pipelines.

    This entity represents the health state of individual components within the
    distributed FLEXT architecture, enabling proactive monitoring, automated
    health checks, and incident prevention through early detection of degradation
    patterns and dependency failures across the data integration platform.

    Attributes:
      component (str): Unique identifier for the monitored component or service.
          Should clearly identify the system being monitored (e.g.,
          "postgresql-database",
          "flext-tap-oracle", "meltano-orchestrator"). Used for health dashboard
          organization and dependency mapping.
      status (str): Current health classification: healthy (operating normally),
          "unhealthy" (service failure), "degraded" (reduced performance),
          "unknown" (cannot determine status). Used for alerting and routing.
      message (str): Detailed health status description providing diagnostic context,
          error details, performance indicators, and recommended actions.
          Empty string indicates no additional information beyond status.
      metrics (dict["str", "object"]): Quantitative health indicators including response
          times, error rates, resource utilization, and custom business metrics.
          Supports nested objects for comprehensive health telemetry.
      timestamp (datetime): UTC timestamp when health check was performed with
          microsecond precision. Used for health trend analysis and SLA monitoring.

    Domain Rules:
      - Component name must be non-empty and uniquely identifiable
      - Status must be valid health classification level
      - Message should provide meaningful diagnostic information
      - Metrics should remain serializable for dashboard integration
      - Timestamp reflects actual health check execution time

    Integration:
      Designed for integration with health monitoring systems, service discovery,
      load balancers, and automated recovery mechanisms. Supports health check
      aggregation and dependency health correlation.

    Example:
      Database health check with detailed metrics:

      >>> from flext_observability.entities import FlextHealthCheck
      >>> db_health = FlextHealthCheck(
      ...     component="postgresql-primary",
      ...     status="healthy",
      ...     message="Database responding normally. All connections active.",
      ...     metrics={
      ...         "response_time_ms": 15.2,
      ...         "active_connections": 45,
      ...         "max_connections": 100,
      ...         "cpu_usage_percent": 12.5,
      ...         "memory_usage_mb": 2048,
      ...     },
      ... )
      >>> db_health.status
      'healthy'

      Service degradation health check:

      >>> api_health = FlextHealthCheck(
      ...     component="flext-api-service",
      ...     status="degraded",
      ...     message="API response time elevated. Average 2.1s vs 500ms target.",
      ...     metrics={
      ...         "avg_response_time_ms": 2100,
      ...         "error_rate_percent": 2.3,
      ...         "requests_per_second": 450,
      ...     },
      ... )

    Architecture:
      Part of the Domain Layer in Clean Architecture, encapsulating health
      monitoring business rules. Integrates with Application Services for
      health collection and Infrastructure Layer for monitoring system export.

    FLEXT Integration:
      - Built on flext-core FlextModels foundation with validation patterns
      - Processed by FlextHealthService for aggregation and correlation
      - Integrates with FlextMetricsService for health metrics collection
      - Compatible with FlextResult error handling throughout the platform

    """

        component: str = Field(..., description="Component name")
        status: str = Field(default="unknown", description="Health status")
        message: str = Field(default="", description="Health message")
        metrics: FlextObservabilityTypes.Core.HealthMetricsDict = Field(
            default_factory=dict,
            description="Health metrics",
        )
        timestamp: datetime = Field(default_factory=FlextObservabilityEntities._generate_utc_datetime)
        
        @field_validator("component")
        @classmethod
        def validate_component_name(cls, v: str) -> str:
            """Validate component name is non-empty and identifiable."""
            if not (v and str(v).strip()):
                msg = "Component name cannot be empty"
                raise ValueError(msg)
            return v
        
        @field_validator("status")
        @classmethod
        def validate_health_status(cls, v: str) -> str:
            """Validate status is a valid health classification level."""
            valid_statuses = {"healthy", "unhealthy", "degraded", "unknown"}
            if v not in valid_statuses:
                msg = f"Invalid health status: {v}. Must be one of {valid_statuses}"
                raise ValueError(msg)
            return v
        
        def validate_business_rules(self) -> FlextResult[None]:
            """Validate health monitoring business rules and domain constraints.
        
            Enforces business rules specific to health monitoring within the FLEXT
            ecosystem, ensuring health check data integrity and compatibility with
            monitoring infrastructure. Validates component identification, status
            classification, and domain constraints for reliable health assessment.
        
            Business Rules Validated:
                - Component name must be non-empty and identifiable
                - Status must be valid health classification level
                - Message should provide meaningful diagnostic context
                - Metrics should remain serializable for integration
                - Health data should support dependency correlation
        
            Returns:
                FlextResult[None]: Success if all business rules pass,
                failure with descriptive error message explaining violation.
        
            Example:
                >>> health = FlextHealthCheck(component="", status="healthy")
                >>> result: FlextResult[object] = health.validate_business_rules()
                >>> result.is_failure
                True
                >>> "component" in result.error
                True
        
            """
            # Use direct validation for standardized validation
            if not (self.component and str(self.component).strip()):
                return FlextResult[None].fail("Invalid component name")
            if self.status not in {"healthy", "unhealthy", "degraded", "unknown"}:
                return FlextResult[None].fail("Invalid health status")
            return FlextResult[None].ok(None)
        
        
        # ============================================================================
    # FACTORY FUNCTIONS - Create entities with proper validation
    # ============================================================================

    @staticmethod
    def flext_alert(
    title: str,
    message: str,
    severity: str = "low",
    status: str = "active",
    **kwargs: object,
    ) -> FlextAlert:
        """Create a FlextAlert entity with proper validation."""
        tags = cast("FlextObservabilityTypes.Core.TagsDict", kwargs.get("tags", {}))
        timestamp = cast("datetime", kwargs.get("timestamp", FlextObservabilityEntities._generate_utc_datetime()))

        # Create with explicit kwargs for better type safety
        if "id" in kwargs and "version" in kwargs:
            return FlextObservabilityEntities.FlextAlert(
                id=cast("str", kwargs["id"]),
                version=cast("int", kwargs["version"]),
                title=title,
                message=message,
                severity=severity,
                status=status,
                tags=tags,
                timestamp=timestamp,
            )
        if "id" in kwargs:
            return FlextObservabilityEntities.FlextAlert(
                id=cast("str", kwargs["id"]),
                title=title,
                message=message,
                severity=severity,
                status=status,
                tags=tags,
                timestamp=timestamp,
            )
        return FlextObservabilityEntities.FlextAlert(
            id=FlextObservabilityEntities.UtilitiesGenerators.generate_entity_id(),
            title=title,
            message=message,
            severity=severity,
            status=status,
            tags=tags,
            timestamp=timestamp,
        )


    def flext_trace(
    trace_id: str,
    operation: str,
    span_id: str,
    status: str = "pending",
    **kwargs: object,
    ) -> FlextTrace:
        """Create a FlextTrace entity with proper validation."""
        span_attributes = cast("FlextObservabilityTypes.Core.SpanAttributesDict", kwargs.get("span_attributes", {}))
        duration_ms = cast("int", kwargs.get("duration_ms", 0))
        timestamp = cast("datetime", kwargs.get("timestamp", FlextObservabilityEntities._generate_utc_datetime()))

        # Create with explicit kwargs for better type safety
        if "id" in kwargs:
            return FlextTrace(
                id=cast("str", kwargs["id"]),
                trace_id=trace_id,
                operation=operation,
                span_id=span_id,
                span_attributes=span_attributes,
                duration_ms=duration_ms,
                status=status,
                timestamp=timestamp,
            )
        return FlextTrace(
            id=FlextUtilitiesGenerators.generate_entity_id(),
            trace_id=trace_id,
            operation=operation,
            span_id=span_id,
            span_attributes=span_attributes,
            duration_ms=duration_ms,
            status=status,
            timestamp=timestamp,
        )


        def flext_metric(
        name: str,
        value: float | Decimal,
        unit: str = "",
        metric_type: str = "gauge",
        **kwargs: object,
    ) -> FlextResult[FlextMetric]:
        """Create a FlextMetric entity with proper validation and type safety."""
        try:
            tags = cast("FlextObservabilityTypes.Core.TagsDict", kwargs.get("tags", {}))
            timestamp = cast("datetime", kwargs.get("timestamp", FlextObservabilityEntities._generate_utc_datetime()))

            # Create with explicit kwargs for better type safety
            if "id" in kwargs and "version" in kwargs:
                metric = FlextMetric(
                    id=cast("str", kwargs["id"]),
                    version=cast("int", kwargs["version"]),
                    name=name,
                    value=value,
                    unit=unit,
                    tags=tags,
                    timestamp=timestamp,
                )
            elif "id" in kwargs:
                metric = FlextMetric(
                    id=cast("str", kwargs["id"]),
                    name=name,
                    value=value,
                    unit=unit,
                    tags=tags,
                    timestamp=timestamp,
                )
            else:
                metric = FlextMetric(
                    id=FlextUtilitiesGenerators.generate_entity_id(),
                    name=name,
                    value=value,
                    unit=unit,
                    tags=tags,
                    timestamp=timestamp,
                )

            # Set metric_type directly on the field
            metric.metric_type = metric_type

            # Validate business rules
            validation_result = metric.validate_business_rules()
            if validation_result.is_failure:
                return FlextResult[FlextMetric].fail(
                    validation_result.error or "Metric validation failed",
                )

            return FlextResult[FlextMetric].ok(metric)

        except (ValueError, TypeError, AttributeError) as e:
            return FlextResult[FlextMetric].fail(f"Failed to create metric: {e}")
        except Exception as e:  # Ensure forced errors are captured for tests
            return FlextResult[FlextMetric].fail(f"Failed to create metric: {e}")


        def flext_health_check(
        component: str,
        status: str = "unknown",
        message: str = "",
        **kwargs: object,
    ) -> FlextHealthCheck:
        """Create a FlextHealthCheck entity with proper validation."""
        metrics: FlextObservabilityTypes.Core.HealthMetricsDict = cast(
            "FlextObservabilityTypes.Core.HealthMetricsDict", kwargs.get("metrics", {})
        )
        timestamp = cast("datetime", kwargs.get("timestamp", FlextObservabilityEntities._generate_utc_datetime()))

        # Create with explicit kwargs for better type safety
        if "id" in kwargs:
            return FlextHealthCheck(
                id=cast("str", kwargs["id"]),
                component=component,
                status=status,
                message=message,
                metrics=metrics,
                timestamp=timestamp,
            )
        return FlextHealthCheck(
            id=FlextUtilitiesGenerators.generate_entity_id(),
            component=component,
            status=status,
            message=message,
            metrics=metrics,
            timestamp=timestamp,
        )


    # ============================================================================
    # PYDANTIC MODEL REBUILDING - Fix "not fully defined" errors
    # ============================================================================

    _logger = FlextLogger(__name__)
    try:
        # Explicitly rebuild models to ensure forward refs (Decimal) are resolved
        FlextMetric.model_rebuild(_types_namespace={"Decimal": "Decimal"})
        FlextTrace.model_rebuild(_types_namespace={"Decimal": "Decimal"})
        FlextAlert.model_rebuild(_types_namespace={"Decimal": "Decimal"})
        FlextLogEntry.model_rebuild(_types_namespace={"Decimal": "Decimal"})
        FlextHealthCheck.model_rebuild(_types_namespace={"Decimal": "Decimal"})
    except Exception as exc:  # pragma: no cover - Pydantic internal failure unlikely
        _logger.warning(  # pragma: no cover
            "Pydantic model_rebuild failed for flext-observability entities",
            error=str(exc),
        )

    __all__ = [
        "FlextAlert",
        "FlextHealthCheck",
        "FlextLogEntry",
        "FlextMetric",
        "FlextMixins",
        "FlextTrace",
        "FlextUtilitiesGenerators",
        "_generate_utc_datetime",
    ]
