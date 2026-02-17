"""Custom metrics registry for domain-specific business metrics.

Provides type-safe metric registration and management for FLEXT projects to
track domain-specific indicators without code duplication.

FLEXT Pattern:
- Single FlextObservabilityCustomMetrics class
- Type-safe metric templates
- Integration with OpenTelemetry meters
- Thread-safe global registry

Key Features:
- Business metric templates (counters, gauges, histograms)
- Type-safe metric creation with validation
- Automatic metric registration
- Per-project metric namespacing
"""

from __future__ import annotations

from dataclasses import dataclass, field

from flext_core import FlextLogger, FlextResult, FlextTypes as t

from flext_observability.constants import c

# Alias for backward compatibility - MetricType is now centralized in constants.py
MetricType = c.Observability.MetricType


@dataclass
class CustomMetricDefinition:
    """Definition for a custom metric."""

    name: str
    metric_type: MetricType
    description: str
    unit: str = "1"
    labels: dict[str, str] = field(default_factory=dict)


class FlextObservabilityCustomMetrics:
    """Custom metrics registry for domain-specific metrics.

    Enables FLEXT projects to register and track business-specific metrics
    without duplication.

    Usage:
        ```python
        from flext_observability import FlextObservabilityCustomMetrics

        # Define custom metrics
        metrics = FlextObservabilityCustomMetrics.get_registry()

        # Register business metric
        metrics.register_metric(
            name="user_logins",
            metric_type="counter",
            description="Number of user logins",
            unit="1",
        )

        # Use metric
        counter = metrics.get_metric("user_logins")
        counter.increment()

        # List all registered metrics
        all_metrics = metrics.get_all_metrics()
        ```

    Nested Classes:
        Registry: Metric registry management
    """

    _logger = FlextLogger.get_logger(__name__)
    _registry_instance: FlextObservabilityCustomMetrics.Registry | None = None

    class Registry:
        """Metric registry for managing custom metrics."""

        def __init__(self) -> None:
            """Initialize metric registry."""
            self._metrics: dict[str, CustomMetricDefinition] = {}
            self._metric_instances: dict[str, t.GeneralValueType] = {}
            self._namespaces: dict[str, str] = {}  # Namespace prefixes

        def register_metric(
            self,
            name: str,
            metric_type: str | MetricType,
            description: str,
            unit: str = "1",
            namespace: str = "default",
        ) -> FlextResult[bool]:
            """Register a custom metric.

            Args:
                name: Metric name (e.g., "user_logins")
                metric_type: Type of metric (counter, gauge, histogram)
                description: Metric description for documentation
                unit: Metric unit (default "1")
                namespace: Namespace for metric organization

            Returns:
                FlextResult[bool] - Ok if registration successful

            Behavior:
                - Validates metric name and type
                - Creates namespaced metric identifier
                - Stores definition in registry
                - Enables retrieval by name or namespace

            """
            try:
                # Validate inputs
                if not name or not name.strip():
                    return FlextResult[bool].fail("Metric name cannot be empty")

                if not description or not description.strip():
                    return FlextResult[bool].fail("Metric description cannot be empty")

                # Convert metric_type to enum
                if isinstance(metric_type, str):
                    try:
                        metric_type_enum = MetricType(metric_type.lower())
                    except ValueError:
                        return FlextResult[bool].fail(
                            f"Invalid metric type: {metric_type}. "
                            f"Must be one of {['counter', 'gauge', 'histogram']}",
                        )
                else:
                    metric_type_enum = metric_type

                # Create namespaced name
                namespaced_name = (
                    f"{namespace}:{name}" if namespace != "default" else name
                )

                # Check for duplicates
                if namespaced_name in self._metrics:
                    return FlextResult[bool].fail(
                        f"Metric '{namespaced_name}' already registered",
                    )

                # Create metric definition
                definition = CustomMetricDefinition(
                    name=name,
                    metric_type=metric_type_enum,
                    description=description,
                    unit=unit,
                )

                # Register metric
                self._metrics[namespaced_name] = definition
                self._namespaces[namespace] = namespace

                FlextObservabilityCustomMetrics._logger.debug(
                    f"Metric registered: {namespaced_name} ({metric_type_enum.value})",
                )
                return FlextResult[bool].ok(value=True)

            except Exception as e:
                return FlextResult[bool].fail(f"Metric registration failed: {e}")

        def get_metric(
            self,
            name: str,
            namespace: str = "default",
        ) -> CustomMetricDefinition | None:
            """Get metric definition by name.

            Args:
                name: Metric name
                namespace: Namespace (default "default")

            Returns:
                CustomMetricDefinition or None if not found

            """
            namespaced_name = f"{namespace}:{name}" if namespace != "default" else name
            return self._metrics.get(namespaced_name)

        def get_all_metrics(
            self,
            namespace: str | None = None,
        ) -> dict[str, CustomMetricDefinition]:
            """Get all registered metrics.

            Args:
                namespace: Optional namespace filter

            Returns:
                dict - All metrics (or filtered by namespace)

            """
            if namespace:
                return {
                    k: v
                    for k, v in self._metrics.items()
                    if k.startswith(f"{namespace}:")
                }
            return self._metrics.copy()

        def get_metrics_by_type(
            self,
            metric_type: MetricType,
        ) -> dict[str, CustomMetricDefinition]:
            """Get all metrics of a specific type.

            Args:
                metric_type: Metric type to filter

            Returns:
                dict - Metrics matching the type

            """
            return {
                k: v for k, v in self._metrics.items() if v.metric_type == metric_type
            }

        def list_metrics(self) -> list[str]:
            """List all registered metric names.

            Returns:
                list - Metric names (namespaced)

            """
            return sorted(self._metrics.keys())

        def get_metric_info(
            self,
            name: str,
            namespace: str = "default",
        ) -> dict[str, t.GeneralValueType] | None:
            """Get detailed metric information.

            Args:
                name: Metric name
                namespace: Namespace (default "default")

            Returns:
                dict - Metric information or None

            """
            metric = self.get_metric(name, namespace)
            if not metric:
                return None

            return {
                "name": metric.name,
                "type": metric.metric_type.value,
                "description": metric.description,
                "unit": metric.unit,
                "labels": metric.labels,
            }

        def unregister_metric(
            self,
            name: str,
            namespace: str = "default",
        ) -> FlextResult[bool]:
            """Unregister a metric.

            Args:
                name: Metric name
                namespace: Namespace (default "default")

            Returns:
                FlextResult[bool] - Ok if unregistered

            """
            try:
                namespaced_name = (
                    f"{namespace}:{name}" if namespace != "default" else name
                )

                if namespaced_name not in self._metrics:
                    return FlextResult[bool].fail(
                        f"Metric '{namespaced_name}' not found",
                    )

                del self._metrics[namespaced_name]

                FlextObservabilityCustomMetrics._logger.debug(
                    f"Metric unregistered: {namespaced_name}",
                )
                return FlextResult[bool].ok(value=True)

            except Exception as e:
                return FlextResult[bool].fail(f"Metric unregistration failed: {e}")

        def clear_metrics(self, namespace: str | None = None) -> FlextResult[bool]:
            """Clear metrics from registry.

            Args:
                namespace: Optional namespace to clear (clears all if None)

            Returns:
                FlextResult[bool] - Ok if successful

            """
            try:
                if namespace:
                    keys_to_remove = [
                        k for k in self._metrics if k.startswith(f"{namespace}:")
                    ]
                    for key in keys_to_remove:
                        del self._metrics[key]
                else:
                    self._metrics.clear()

                FlextObservabilityCustomMetrics._logger.debug(
                    f"Metrics cleared: {namespace or 'all'}",
                )
                return FlextResult[bool].ok(value=True)

            except Exception as e:
                return FlextResult[bool].fail(f"Failed to clear metrics: {e}")

    @staticmethod
    def get_registry() -> FlextObservabilityCustomMetrics.Registry:
        """Get global metric registry instance (singleton).

        Returns:
            Registry - Global metric registry

        """
        if FlextObservabilityCustomMetrics._registry_instance is None:
            FlextObservabilityCustomMetrics._registry_instance = (
                FlextObservabilityCustomMetrics.Registry()
            )

        return FlextObservabilityCustomMetrics._registry_instance

    @staticmethod
    def register_metric(
        name: str,
        metric_type: str | MetricType,
        description: str,
        unit: str = "1",
        namespace: str = "default",
    ) -> FlextResult[bool]:
        """Convenience function: register a metric.

        Args:
            name: Metric name
            metric_type: Metric type (counter, gauge, histogram)
            description: Metric description
            unit: Metric unit (default "1")
            namespace: Namespace (default "default")

        Returns:
            FlextResult[bool] - Ok if successful

        """
        registry = FlextObservabilityCustomMetrics.get_registry()
        return registry.register_metric(
            name=name,
            metric_type=metric_type,
            description=description,
            unit=unit,
            namespace=namespace,
        )

    @staticmethod
    def get_metric(
        name: str,
        namespace: str = "default",
    ) -> CustomMetricDefinition | None:
        """Convenience function: get metric definition.

        Args:
            name: Metric name
            namespace: Namespace (default "default")

        Returns:
            CustomMetricDefinition or None

        """
        registry = FlextObservabilityCustomMetrics.get_registry()
        return registry.get_metric(name, namespace)

    @staticmethod
    def list_all_metrics() -> list[str]:
        """Convenience function: list all metrics.

        Returns:
            list - All registered metric names

        """
        registry = FlextObservabilityCustomMetrics.get_registry()
        return registry.list_metrics()


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    "CustomMetricDefinition",
    "FlextObservabilityCustomMetrics",
    "MetricType",
]
