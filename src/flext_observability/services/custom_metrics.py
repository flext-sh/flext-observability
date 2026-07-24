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

from typing import TYPE_CHECKING

from flext_observability import c, e, m, p, r, t, u

if TYPE_CHECKING:
    from collections.abc import MutableMapping


class FlextObservabilityCustomMetrics:
    """Custom metrics registry for domain-specific metrics.

    Enables FLEXT projects to register and track business-specific metrics
    without duplication.

    Usage:
        ```python
        from flext_observability import FlextObservabilityCustomMetrics

        # Define custom metrics
        metrics = FlextObservabilityCustomMetrics.active_registry()

        # Register business metric
        metrics.register_metric(
            name="user_logins",
            metric_type="counter",
            description="Number of user logins",
            unit="1",
        )

        # Use metric
        counter = metrics.resolve_metric("user_logins")
        counter.increment()

        # List all registered metrics
        all_metrics = metrics.resolve_metrics()
        ```

    Nested Classes:
        Registry: Metric registry management
    """

    logger = u.fetch_logger(__name__)
    _registry_instance: FlextObservabilityCustomMetrics.Registry | None = None

    class Registry:
        """Metric registry for managing custom metrics."""

        def __init__(self) -> None:
            """Initialize metric registry."""
            self._metrics: MutableMapping[
                str, m.Observability.CustomMetricDefinition
            ] = {}
            self._metric_instances: t.MutableScalarMapping = dict[str, t.Scalar]()
            self._namespaces: t.MutableStrMapping = dict[str, str]()

        def clear_metrics(self, namespace: str | None = None) -> p.Result[bool]:
            """Clear metrics from registry.

            Args:
                namespace: Optional namespace to clear (clears all if None)

            Returns:
                r[bool] - Ok if successful

            """
            try:
                return self._clear_metrics(namespace)
            except c.EXC_MAPPING_TYPE as exc:
                return e.fail_operation("clear metrics", exc, result_type=r[bool])

        def _clear_metrics(self, namespace: str | None) -> p.Result[bool]:
            """Clear metrics for one namespace or the complete registry."""
            if namespace:
                keys_to_remove = [
                    key for key in self._metrics if key.startswith(f"{namespace}:")
                ]
                for key in keys_to_remove:
                    del self._metrics[key]
            else:
                self._metrics.clear()
            FlextObservabilityCustomMetrics.logger.debug(
                f"Metrics cleared: {namespace or 'all'}"
            )
            return r[bool].ok(value=True)

        def resolve_metrics(self, namespace: str | None = None) -> p.Dict:
            """Resolve all registered metrics.

            Args:
                namespace: Optional namespace filter

            Returns:
                dict - All metrics (or filtered by namespace)

            """
            if namespace:
                filtered = {
                    metric_name: metric
                    for metric_name, metric in self._metrics.items()
                    if metric_name.startswith(f"{namespace}:")
                }
                return m.Dict.model_validate(filtered)
            return m.Dict.model_validate(self._metrics)

        def resolve_metric(
            self, name: str, namespace: str = "default"
        ) -> p.Observability.CustomMetricDefinition | None:
            """Resolve a metric definition by name.

            Args:
                name: Metric name
                namespace: Namespace (default "default")

            Returns:
                CustomMetricDefinition or None if not found

            """
            namespaced_name = f"{namespace}:{name}" if namespace != "default" else name
            value = self._metrics.get(namespaced_name)
            if isinstance(value, m.Observability.CustomMetricDefinition):
                return value
            return None

        def resolve_metric_info(
            self, name: str, namespace: str = "default"
        ) -> p.Dict | None:
            """Resolve detailed metric information.

            Args:
                name: Metric name
                namespace: Namespace (default "default")

            Returns:
                dict - Metric information or None

            """
            metric = self.resolve_metric(name, namespace)
            if not metric:
                return None
            return m.Dict({
                "name": metric.name,
                "type": metric.metric_type.value,
                "description": metric.description,
                "unit": metric.unit,
                "labels": metric.labels,
            })

        def resolve_metrics_by_type(
            self, metric_type: c.Observability.MetricType
        ) -> p.Dict:
            """Resolve all metrics of a specific type.

            Args:
                metric_type: Metric type to filter

            Returns:
                dict - Metrics matching the type

            """
            return m.Dict({
                metric_name: metric
                for metric_name, metric in self._metrics.items()
                if metric.metric_type == metric_type
            })

        def list_metrics(self) -> t.StrSequence:
            """List all registered metric names.

            Returns:
                list - Metric names (namespaced)

            """
            return sorted(self._metrics.keys())

        def register_metric(
            self,
            name: str,
            metric_type: str | c.Observability.MetricType,
            description: str,
            unit: str = "1",
            namespace: str = "default",
        ) -> p.Result[bool]:
            """Register a custom metric.

            Args:
                name: Metric name (e.g., "user_logins")
                metric_type: Type of metric (counter, gauge, histogram)
                description: Metric description for documentation
                unit: Metric unit (default "1")
                namespace: Namespace for metric organization

            Returns:
                r[bool] - Ok if registration successful

            Behavior:
                - Validates metric name and type
                - Creates namespaced metric identifier
                - Stores definition in registry
                - Enables retrieval by name or namespace

            """
            try:
                return self._register_metric_definition(
                    name=name,
                    metric_type=metric_type,
                    description=description,
                    unit=unit,
                    namespace=namespace,
                )
            except c.EXC_MAPPING_TYPE as exc:
                return e.fail_operation("Metric registration", exc, result_type=r[bool])

        def _register_metric_definition(
            self,
            *,
            name: str,
            metric_type: str | c.Observability.MetricType,
            description: str,
            unit: str,
            namespace: str,
        ) -> p.Result[bool]:
            """Validate and store one metric definition."""
            validation_result = self._validate_metric_definition_input(
                name, description, metric_type
            )
            if validation_result.failure:
                return r[bool].fail(
                    validation_result.error or "Invalid metric definition",
                    exception=validation_result.exception,
                )
            metric_type_enum = validation_result.value
            namespaced_name = f"{namespace}:{name}" if namespace != "default" else name
            if namespaced_name in self._metrics:
                return e.fail_conflict(
                    "Metric",
                    namespaced_name,
                    reason="already registered",
                    result_type=r[bool],
                )
            self._metrics[namespaced_name] = m.Observability.CustomMetricDefinition(
                name=name,
                metric_type=metric_type_enum,
                description=description,
                unit=unit,
                labels={},
            )
            self._namespaces[namespace] = namespace
            FlextObservabilityCustomMetrics.logger.debug(
                f"Metric registered: {namespaced_name} ({metric_type_enum.value})"
            )
            return r[bool].ok(value=True)

        @staticmethod
        def _validate_metric_definition_input(
            name: str, description: str, metric_type: str | c.Observability.MetricType
        ) -> p.Result[c.Observability.MetricType]:
            """Validate metric definition fields and resolve its enum type."""
            if not name or not name.strip():
                return e.fail_validation(
                    "Metric name cannot be empty",
                    result_type=r[c.Observability.MetricType],
                )
            if not description or not description.strip():
                return e.fail_validation(
                    "Metric description cannot be empty",
                    result_type=r[c.Observability.MetricType],
                )
            metric_input = metric_type.lower()
            try:
                metric_type_enum = m.Observability.MetricTypeInput.model_validate(
                    obj={"metric_type": metric_input}
                ).metric_type
            except c.ValidationError as exc_validate:
                return e.fail_validation(
                    f"Invalid metric type: {metric_type}. Must be one of ['counter', 'gauge', 'histogram']",
                    error=exc_validate,
                    result_type=r[c.Observability.MetricType],
                )
            return r[c.Observability.MetricType].ok(metric_type_enum)

        def unregister_metric(
            self, name: str, namespace: str = "default"
        ) -> p.Result[bool]:
            """Unregister a metric.

            Args:
                name: Metric name
                namespace: Namespace (default "default")

            Returns:
                r[bool] - Ok if unregistered

            """
            try:
                namespaced_name = (
                    f"{namespace}:{name}" if namespace != "default" else name
                )
                if namespaced_name not in self._metrics:
                    return e.fail_not_found(
                        "Metric", namespaced_name, result_type=r[bool]
                    )
                del self._metrics[namespaced_name]
                FlextObservabilityCustomMetrics.logger.debug(
                    f"Metric unregistered: {namespaced_name}"
                )
                return r[bool].ok(value=True)
            except c.EXC_MAPPING_TYPE as exc:
                return e.fail_operation(
                    "Metric unregistration", exc, result_type=r[bool]
                )

    @staticmethod
    def resolve_metric(
        name: str, namespace: str = "default"
    ) -> p.Observability.CustomMetricDefinition | None:
        """Resolve a metric definition.

        Args:
            name: Metric name
            namespace: Namespace (default "default")

        Returns:
            CustomMetricDefinition or None

        """
        registry = FlextObservabilityCustomMetrics.active_registry()
        return registry.resolve_metric(name, namespace)

    @staticmethod
    def active_registry() -> FlextObservabilityCustomMetrics.Registry:
        """Return the global metric registry instance.

        Returns:
            Registry - Global metric registry

        """
        if FlextObservabilityCustomMetrics._registry_instance is None:
            FlextObservabilityCustomMetrics._registry_instance = (
                FlextObservabilityCustomMetrics.Registry()
            )
        return FlextObservabilityCustomMetrics._registry_instance

    @staticmethod
    def list_all_metrics() -> t.StrSequence:
        """List all metrics.

        Returns:
            list - All registered metric names

        """
        registry = FlextObservabilityCustomMetrics.active_registry()
        return registry.list_metrics()

    @staticmethod
    def register_metric(
        name: str,
        metric_type: str | c.Observability.MetricType,
        description: str,
        unit: str = "1",
        namespace: str = "default",
    ) -> p.Result[bool]:
        """Register a metric.

        Args:
            name: Metric name
            metric_type: Metric type (counter, gauge, histogram)
            description: Metric description
            unit: Metric unit (default "1")
            namespace: Namespace (default "default")

        Returns:
            r[bool] - Ok if successful

        """
        registry = FlextObservabilityCustomMetrics.active_registry()
        return registry.register_metric(
            name=name,
            metric_type=metric_type,
            description=description,
            unit=unit,
            namespace=namespace,
        )


__all__: list[str] = ["FlextObservabilityCustomMetrics"]
