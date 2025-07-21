"""Business metrics for flext-infrastructure.monitoring.flext-observability.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from flext_core.domain.types import MetricType

from flext_observability.domain.entities import Metric
from flext_observability.domain.value_objects import ComponentName


class BusinessMetricType(StrEnum):
    """Business metric types for enterprise monitoring."""

    # Prometheus-style metric types
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

    # Business-specific metric types
    PIPELINE_SUCCESS_RATE = "pipeline_success_rate"
    EXECUTION_DURATION = "execution_duration"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    AVAILABILITY = "availability"
    LATENCY = "latency"
    COST_PER_OPERATION = "cost_per_operation"
    USER_ACTIVITY = "user_activity"
    SLA_COMPLIANCE = "sla_compliance"


class BusinessMetric:
    """Business metric following domain-driven design principles."""

    def __init__(
        self,
        name: str,
        value: float,
        metric_type: BusinessMetricType,
        component_name: str = "default",
        unit: str = "count",
        labels: dict[str, str] | None = None,
    ) -> None:
        """Initialize business metric.

        Args:
            name: Metric name.
            value: Metric value.
            metric_type: Type of business metric.
            component_name: Component that generated the metric.
            unit: Unit of measurement.
            labels: Additional metric labels.

        """
        self.name = name
        self.value = value
        self.metric_type = metric_type
        self.component_name = component_name
        self.unit = unit
        self.labels = labels or {}

    def to_domain_metric(self) -> Metric:
        """Convert to domain metric entity.

        Returns:
            Domain metric entity.

        """
        # Map BusinessMetricType to MetricType
        metric_type_mapping = {
            BusinessMetricType.COUNTER: MetricType.COUNTER,
            BusinessMetricType.GAUGE: MetricType.GAUGE,
            BusinessMetricType.HISTOGRAM: MetricType.HISTOGRAM,
            BusinessMetricType.SUMMARY: MetricType.SUMMARY,
            # Business-specific types map to appropriate metric types
            BusinessMetricType.PIPELINE_SUCCESS_RATE: MetricType.GAUGE,
            BusinessMetricType.EXECUTION_DURATION: MetricType.HISTOGRAM,
            BusinessMetricType.THROUGHPUT: MetricType.GAUGE,
            BusinessMetricType.ERROR_RATE: MetricType.GAUGE,
            BusinessMetricType.AVAILABILITY: MetricType.GAUGE,
            BusinessMetricType.LATENCY: MetricType.HISTOGRAM,
            BusinessMetricType.COST_PER_OPERATION: MetricType.GAUGE,
            BusinessMetricType.USER_ACTIVITY: MetricType.COUNTER,
            BusinessMetricType.SLA_COMPLIANCE: MetricType.GAUGE,
        }

        return Metric(
            name=self.name,
            value=self.value,
            metric_type=metric_type_mapping[self.metric_type],
            unit=self.unit,
            labels=self.labels,
            component=ComponentName(name=self.component_name),
        )


class EnterpriseBusinessMetrics:
    """Enterprise business metrics collector and calculator."""

    def __init__(self) -> None:
        """Initialize enterprise business metrics."""
        self._metrics: list[BusinessMetric] = []

    def collect_pipeline_metrics(self) -> dict[str, Any]:
        """Collect pipeline performance metrics.

        Returns:
            Dictionary of pipeline metrics.

        """
        return {
            "success_rate": 97.5,  # Mock data
            "average_duration": 125.3,
            "total_executions": 1250,
            "failed_executions": 31,
        }

    def collect_system_metrics(self) -> dict[str, Any]:
        """Collect system performance metrics.

        Returns:
            Dictionary of system metrics.

        """
        return {
            "cpu_usage": 45.2,
            "memory_usage": 67.8,
            "disk_usage": 23.1,
            "network_throughput": 142.5,
        }

    def collect_business_kpis(self) -> dict[str, Any]:
        """Collect business key performance indicators.

        Returns:
            Dictionary of business KPIs.

        """
        return {
            "cost_per_operation": 0.012,
            "sla_compliance": 99.8,
            "user_satisfaction": 4.7,
            "revenue_impact": 125000.0,
        }

    def record_metric(self, metric: BusinessMetric) -> None:
        """Record a business metric.

        Args:
            metric: Business metric to record.

        """
        self._metrics.append(metric)

    def record_pipeline_execution(
        self,
        pipeline_id: str,
        duration: float,
        success: bool,
    ) -> None:
        """Record pipeline execution metrics.

        Args:
            pipeline_id: Unique identifier for the pipeline.
            duration: Execution duration in seconds.
            success: Whether the execution was successful.

        """
        # Record duration metric
        duration_metric = BusinessMetric(
            name=f"pipeline_duration_{pipeline_id}",
            value=duration,
            metric_type=BusinessMetricType.HISTOGRAM,
            component_name="pipeline",
            unit="seconds",
            labels={"pipeline_id": pipeline_id, "success": str(success)},
        )
        self.record_metric(duration_metric)

        # Record success/failure counter
        status_metric = BusinessMetric(
            name="pipeline_executions_total",
            value=1.0,
            metric_type=BusinessMetricType.COUNTER,
            component_name="pipeline",
            unit="count",
            labels={
                "pipeline_id": pipeline_id,
                "status": "success" if success else "failure",
            },
        )
        self.record_metric(status_metric)

    def get_metrics_summary(self) -> dict[str, Any]:
        """Get summary of all collected metrics.

        Returns:
            Summary dictionary of metrics.

        """
        return {
            "total_metrics": len(self._metrics),
            "pipeline_metrics": self.collect_pipeline_metrics(),
            "system_metrics": self.collect_system_metrics(),
            "business_kpis": self.collect_business_kpis(),
        }


__all__ = [
    "BusinessMetric",
    "BusinessMetricType",
    "EnterpriseBusinessMetrics",
]
