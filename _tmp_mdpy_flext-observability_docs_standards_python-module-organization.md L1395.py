# from flext-observability/docs/standards/python-module-organization.md:1395
from __future__ import annotations


def create_business_observability_dashboard(
    service_name: str, metrics_config: m.Dict, trace_config: m.Dict
) -> p.Result[m.Dict]:
    """Create comprehensive business observability dashboard.

    This function implements the complete observability setup for a business
    service including metrics collection, distributed tracing, and health
    monitoring. It follows FLEXT observability patterns for consistent
    monitoring across the ecosystem.

    Args:
        service_name: Name of the service to monitor (e.g., "user-api", "payment-service")
        metrics_config: Configuration for metrics collection including names,
            types, and collection intervals. Example:
            {
                "response_time": {"type": "histogram", "unit": "seconds"},
                "request_count": {"type": "counter", "unit": "count"}
            }
        trace_config: Configuration for distributed tracing including sampling
            rates and context propagation. Example:
            {
                "sampling_rate": 0.1,
                "propagate_context": True,
                "trace_external_calls": True
            }

    Returns:
        r[m.Dict]: Success contains dashboard configuration
        with metric definitions, trace setup, and health check configuration.
        Failure contains detailed error message explaining setup failure.

    Example:
        >>> metrics = {"api_requests": {"type": "counter", "unit": "count"}}
        >>> traces = {"sampling_rate": 0.1}
        >>> result = create_business_observability_dashboard(
        ...     "user-api", metrics, traces
        ... )
        >>> if result.success:
        ...     dashboard = result.value
        ...     print(f"Created dashboard with {len(dashboard['metrics'])} metrics")
        ... else:
        ...     print(f"Dashboard creation failed: {result.error}")

    Integration:
        - Uses FlextMetricsService for metrics collection coordination
        - Integrates with FlextTracingService for distributed tracing
        - Coordinates with FlextHealthService for health monitoring
        - Built on flext-core r patterns for error handling

    """
    try:
        # Create service-specific observability components
        dashboard_config = {
            "service_name": service_name,
            "metrics": [],
            "traces": [],
            "health_checks": [],
        }

        # Setup metrics based on configuration
        for metric_name, settings in metrics_config.items():
            metric_result = flext_create_metric(
                name=f"{service_name}_{metric_name}",
                value=0,  # Initial value
                unit=settings.get("unit", "count"),
                metric_type=settings.get("type", "gauge"),
            )

            if metric_result.failure:
                return r[bool].fail(
                    f"Failed to create metric {metric_name}: {metric_result.error}"
                )

            dashboard_config["metrics"].append(metric_result.value)

        # Setup tracing based on configuration
        trace_result = flext_create_trace(
            operation_name=f"{service_name}_operations",
            service_name=service_name,
            context=trace_config,
        )

        if trace_result.failure:
            return r[bool].fail(f"Failed to create trace setup: {trace_result.error}")

        dashboard_config["traces"].append(trace_result.value)

        return r[bool].ok(dashboard_config)

    except Exception as e:
        return r[bool].fail(f"Unexpected error creating observability dashboard: {e!s}")
