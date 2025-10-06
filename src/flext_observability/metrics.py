"""FLEXT Observability Metrics Domain Models.

Provides focused metrics models following the namespace class pattern.
Contains metric entities, configurations, and factory methods for metrics operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import math
from datetime import UTC, datetime
from decimal import Decimal
from typing import Self

from flext_core import FlextModels, FlextResult, FlextTypes
from pydantic import (
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)


class FlextObservabilityMetrics(FlextModels):
    """Focused metrics models for observability operations extending FlextModels.

    Provides comprehensive metric entities, configurations, and operations
    for metrics collection, validation, and management within the FLEXT ecosystem.
    """

    # Core Metrics Models
    class MetricEntry(FlextModels.Value):
        """Comprehensive metric entry model."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="forbid",
            frozen=False,
        )

        metric_id: str = Field(description="Unique metric identifier")
        name: str = Field(description="Metric name")
        value: float = Field(description="Metric value")
        unit: str = Field(default="count", description="Metric unit")
        timestamp: datetime = Field(
            default_factory=datetime.now, description="Metric timestamp"
        )
        labels: FlextTypes.StringDict = Field(
            default_factory=dict, description="Metric labels"
        )
        source: str = Field(description="Metric source service")

        @computed_field
        @property
        def metric_key(self) -> str:
            """Computed field for unique metric key."""
            return f"{self.source}.{self.name}"

        @computed_field
        @property
        def formatted_value(self) -> str:
            """Computed field for formatted metric value with unit."""
            return f"{self.value} {self.unit}"

        @field_validator("name")
        @classmethod
        def validate_name(cls, v: str) -> str:
            """Validate metric name is not empty."""
            if not v or not v.strip():
                msg = "Metric name cannot be empty"
                raise ValueError(msg)
            return v.strip()

        @field_serializer("labels", when_used="json")
        def serialize_labels_with_metadata(
            self, value: FlextTypes.StringDict, _info: object
        ) -> FlextTypes.Dict:
            """Serialize labels with metadata for monitoring."""
            return {
                "labels": value,
                "label_count": len(value),
                "metric_context": self.source,
            }

    class MetricConfig(FlextModels.Configuration):
        """Metric configuration model."""

        model_config = ConfigDict(
            validate_assignment=True,
            extra="forbid",
            frozen=False,
        )

        collection_interval: float = Field(
            default=60.0,  # 1 minute default
            description="Collection interval in seconds",
        )
        retention_days: int = Field(
            default=30,
            description="Metric retention in days",
        )
        aggregation_method: str = Field(default="sum", description="Aggregation method")
        enable_alerting: bool = Field(
            default=True, description="Enable alerting for metrics"
        )

        @computed_field
        @property
        def config_summary(self) -> FlextTypes.Dict:
            """Computed field for metric configuration summary."""
            return {
                "collection_interval_minutes": self.collection_interval / 60,
                "retention_weeks": self.retention_days / 7,
                "alerting_enabled": self.enable_alerting,
                "aggregation": self.aggregation_method,
            }

        @model_validator(mode="after")
        def validate_metric_config(self) -> Self:
            """Validate metric configuration parameters."""
            if self.collection_interval <= 0:
                msg = "Collection interval must be positive"
                raise ValueError(msg)
            if self.retention_days <= 0:
                msg = "Retention days must be positive"
                raise ValueError(msg)
            return self

    class FlextMetric(FlextModels.Entity):
        """Observability metric entity for collecting and validating measurement data.

        Core domain entity representing a single metric measurement with comprehensive
        validation, type safety, and business rule enforcement. Supports both float
        and Decimal values for financial precision, includes metadata tags for
        categorization, and implements domain-driven validation patterns.
        """

        model_config = ConfigDict(
            frozen=False,  # Allow dynamic attributes
        )

        name: str = Field(..., description="Metric name")
        value: float | Decimal = Field(..., description="Metric value")
        unit: str = Field(default="", description="Metric unit")
        tags: FlextTypes.Dict = Field(default_factory=dict, description="Metric tags")
        timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
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
                msg = "Metric value cannot be NaN or infinite"
                raise ValueError(msg)

            return v

        @field_validator("metric_type")
        @classmethod
        def validate_metric_type(cls, v: str) -> str:
            """Validate metric type is one of the supported types."""
            valid_types = {"counter", "gauge", "histogram", "summary"}
            if v not in valid_types:
                msg = f"Metric type must be one of {valid_types}"
                raise ValueError(msg)
            return v

        @field_validator("unit")
        @classmethod
        def validate_unit(cls, v: str) -> str:
            """Validate unit is a reasonable string."""
            if not isinstance(v, str):
                msg = "Unit must be a string"
                raise TypeError(msg)
            return v

        def validate_business_rules(self) -> FlextResult[bool]:
            """Validate business rules for metric entity."""
            try:
                # Additional business rule validations can be added here
                if not self.name:
                    return FlextResult[bool].fail("Metric name is required")

                if self.value is None:
                    return FlextResult[bool].fail("Metric value is required")

                # Validate tags structure
                if not isinstance(self.tags, dict):
                    return FlextResult[bool].fail("Tags must be a dictionary")

                return FlextResult[bool].ok(True)
            except Exception as e:
                return FlextResult[bool].fail(f"Business rule validation failed: {e}")

    # Factory methods for direct entity creation
    @staticmethod
    def flext_metric(
        name: str,
        value: float | Decimal,
        unit: str = "",
        metric_type: str = "gauge",
        **kwargs: object,
    ) -> FlextResult[FlextObservabilityMetrics.FlextMetric]:
        """Create a FlextMetric entity directly."""
        try:
            # Filter kwargs to only include valid FlextMetric parameters
            valid_kwargs: dict[str, object] = {}
            if "tags" in kwargs and isinstance(kwargs["tags"], dict):
                valid_kwargs["tags"] = kwargs["tags"]
            if "timestamp" in kwargs and isinstance(kwargs["timestamp"], datetime):
                valid_kwargs["timestamp"] = kwargs["timestamp"]

            return FlextResult[FlextObservabilityMetrics.FlextMetric].ok(
                FlextObservabilityMetrics.FlextMetric(
                    name=name, value=value, unit=unit, metric_type=metric_type
                )
            )
        except Exception as e:
            return FlextResult[FlextObservabilityMetrics.FlextMetric].fail(
                f"Failed to create metric: {e}"
            )


# Export the focused metrics namespace class
__all__ = [
    "FlextObservabilityMetrics",
]
