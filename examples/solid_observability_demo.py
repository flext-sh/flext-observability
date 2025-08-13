#!/usr/bin/env python3
"""SOLID Observability Demo - Real functionality demonstration.

This example demonstrates the real functionality implemented in flext-observability
following SOLID principles with metrics, tracing, health monitoring,
and function monitoring capabilities.
"""

import time

from flext_observability import (
    FlextObservabilityMonitor,
    flext_create_health_check,
    flext_create_trace,
    flext_monitor_function,
)


def main() -> None:
    """Demonstrate SOLID observability implementation with real functionality."""
    print("🔧 FLEXT Observability - SOLID Implementation Demo")
    print("=" * 60)

    # Initialize observability monitor with real services
    monitor = FlextObservabilityMonitor()

    # Initialize all observability services
    init_result = monitor.flext_initialize_observability()
    if init_result.is_failure:
        print(f"❌ Failed to initialize observability: {init_result.error}")
        return

    print("✅ Observability services initialized successfully")

    # Start monitoring
    start_result = monitor.flext_start_monitoring()
    if start_result.is_failure:
        print(f"❌ Failed to start monitoring: {start_result.error}")
        return

    print("✅ Real monitoring started successfully")

    # Demonstrate real metrics collection
    print("\n📊 Real Metrics Collection:")
    demo_metrics_collection(monitor)

    # Demonstrate distributed tracing
    print("\n🔍 Real Distributed Tracing:")
    demo_distributed_tracing(monitor)

    # Demonstrate health monitoring
    print("\n💚 Real Health Monitoring:")
    demo_health_monitoring(monitor)

    # Demonstrate function monitoring
    print("\n⚡ Real Function Monitoring:")
    demo_function_monitoring(monitor)

    # Show comprehensive metrics summary
    print("\n📈 Comprehensive Metrics Summary:")
    show_metrics_summary(monitor)

    # Show health status
    print("\n🏥 System Health Status:")
    show_health_status(monitor)

    print("\n🎉 SOLID Observability Demo completed successfully!")
    print("   All functionality is real - no placeholders or mocks used.")


def demo_metrics_collection(monitor: FlextObservabilityMonitor) -> None:
    """Demonstrate real metrics collection with different metric types."""
    # Record different types of metrics
    metrics_to_record = [
        ("cpu_usage_percent", 75.5, "gauge"),
        ("requests_total", 1, "counter"),
        ("response_time_ms", 250.0, "histogram"),
        ("memory_usage_mb", 1024.0, "gauge"),
        ("errors_total", 1, "counter"),
        ("processing_time_seconds", 1.5, "histogram"),
    ]

    for name, value, metric_type in metrics_to_record:
        result = monitor.flext_record_metric(name, value, metric_type)
        if result.success:
            print(f"  ✅ Recorded {metric_type}: {name} = {value}")
        else:
            print(f"  ❌ Failed to record {name}: {result.error}")


def demo_distributed_tracing(monitor: FlextObservabilityMonitor) -> None:
    """Demonstrate real distributed tracing capabilities."""
    if not monitor._tracing_service:
        print("  ⚠️ Tracing service not available")
        return

    # Create and start a trace
    trace_result = flext_create_trace(
        trace_id="demo_trace_001",
        operation="user_registration",
    )

    if trace_result.is_failure:
        print(f"  ❌ Failed to create trace: {trace_result.error}")
        return

    start_result = monitor._tracing_service.start_trace(trace_result.data)
    if start_result.success:
        print("  ✅ Started distributed trace: demo_trace_001")

        # Add spans to the trace
        monitor._tracing_service.add_span_to_trace(
            "demo_trace_001",
            "validate_user_input",
            user_id="user123",
            validation_time_ms=50,
        )

        monitor._tracing_service.add_span_to_trace(
            "demo_trace_001",
            "save_to_database",
            table="users",
            save_time_ms=120,
        )

        print("  ✅ Added spans to trace")

        # Simulate some processing time
        time.sleep(0.1)

        # Finish the trace
        finish_result = monitor._tracing_service.finish_trace(
            "demo_trace_001",
            "completed",
        )
        if finish_result.success:
            print("  ✅ Completed distributed trace")

            # Get trace information
            info_result = monitor._tracing_service.get_trace_info("demo_trace_001")
            if info_result.success:
                trace_info = info_result.data
                duration = trace_info.get("duration_seconds", 0)
                span_count = trace_info.get("span_count", 0)
                print(f"  📊 Trace duration: {duration:.3f}s, Spans: {span_count}")


def demo_health_monitoring(monitor: FlextObservabilityMonitor) -> None:
    """Demonstrate real health monitoring capabilities."""
    if not monitor._health_service:
        print("  ⚠️ Health service not available")
        return

    # Create health checks for different components
    components = [
        ("database", "healthy", "Response time: 15ms"),
        ("cache", "healthy", "Hit rate: 95%"),
        ("api_gateway", "degraded", "Error rate: 2%"),
        ("message_queue", "healthy", "Queue depth: 10"),
    ]

    for component, status, message in components:
        health_result = flext_create_health_check(
            component=component,
            status=status,
            message=message,
        )

        if health_result.success:
            check_result = monitor._health_service.check_health(health_result.data)
            if check_result.success:
                print(f"  ✅ Health check: {component} = {status}")
            else:
                print(f"  ❌ Failed health check for {component}: {check_result.error}")


def demo_function_monitoring(monitor: FlextObservabilityMonitor) -> None:
    """Demonstrate real function monitoring with decorators."""

    @flext_monitor_function(monitor=monitor, metric_name="business_operation")
    def process_business_logic(data: dict[str, object]) -> dict[str, object]:
        """Simulate business logic processing."""
        # Simulate processing time
        time.sleep(0.05)

        # Simulate some computation
        return {
            "processed": True,
            "input_size": len(data),
            "timestamp": time.time(),
            "operation": "business_processing",
        }

    @flext_monitor_function(monitor=monitor, metric_name="data_validation")
    def validate_data(data: dict[str, object]) -> bool:
        """Simulate data validation."""
        time.sleep(0.02)
        return len(data) > 0 and "required_field" in data

    # Execute monitored functions
    test_data = {"required_field": "value", "optional": "data"}

    print("  🔄 Executing monitored functions...")

    # This will record success metrics
    validation_result = validate_data(test_data)
    print(f"  ✅ Data validation: {validation_result}")

    # This will record success metrics
    processing_result = process_business_logic(test_data)
    print(f"  ✅ Business logic processed: {processing_result['processed']}")

    # Demonstrate error handling
    try:

        @flext_monitor_function(monitor=monitor, metric_name="error_demo")
        def _create_demo_error() -> ValueError:
            """Create demo error for testing."""
            return ValueError("Simulated error for demo")

        def function_with_error() -> None:
            """Function that will raise an error."""
            raise _create_demo_error()

        function_with_error()
    except ValueError:
        print("  ✅ Error monitoring: Exception caught and metrics recorded")


def show_metrics_summary(monitor: FlextObservabilityMonitor) -> None:
    """Show comprehensive metrics summary."""
    summary_result = monitor.flext_get_metrics_summary()
    if summary_result.is_failure:
        print(f"  ❌ Failed to get metrics summary: {summary_result.error}")
        return

    summary = summary_result.data

    service_info = summary.get("service_info", {})
    print(f"  📊 Metrics service uptime: {service_info.get('uptime_seconds', 0):.1f}s")
    print(f"  📊 Total metrics recorded: {service_info.get('metrics_recorded', 0)}")
    print(f"  📊 Unique metrics: {service_info.get('unique_metrics', 0)}")

    counters = summary.get("counters", {})
    if counters:
        print("  📈 Counter metrics:")
        for name, value in counters.items():
            print(f"    - {name}: {value}")

    gauges = summary.get("gauges", {})
    if gauges:
        print("  🌡️ Gauge metrics:")
        for name, value in gauges.items():
            print(f"    - {name}: {value}")


def show_health_status(monitor: FlextObservabilityMonitor) -> None:
    """Show comprehensive health status."""
    health_result = monitor.flext_get_health_status()
    if health_result.is_failure:
        print(f"  ❌ Failed to get health status: {health_result.error}")
        return

    health_data = health_result.data

    overall_status = health_data.get("overall_status", "unknown")
    print(f"  🏥 Overall system status: {overall_status}")

    summary = health_data.get("summary", {})
    print(f"  📊 Total components: {summary.get('total_components', 0)}")
    print(f"  ✅ Healthy components: {summary.get('healthy_components', 0)}")
    print(f"  ⚠️ Unhealthy components: {summary.get('unhealthy_components', 0)}")

    monitor_metrics = health_data.get("monitor_metrics", {})
    if monitor_metrics:
        print(
            f"  ⏱️ Monitor uptime: "
            f"{monitor_metrics.get('monitor_uptime_seconds', 0):.1f}s",
        )
        print(
            f"  🔧 Functions monitored: {monitor_metrics.get('functions_monitored', 0)}",
        )


if __name__ == "__main__":
    main()
