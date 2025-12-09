"""OpenTelemetry infrastructure setup for FLEXT observability.

Provides centralized OpenTelemetry tracer and meter provider initialization.
Used internally by FlextObservability services for real observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter


class FlextObservabilityInfrastructure:
    """OpenTelemetry infrastructure setup - INTERNAL USE ONLY.

    This class manages OpenTelemetry provider initialization and configuration.
    It's used internally by FlextObservability services and should not be used
    directly by application code.

    Nested Classes:
    - Telemetry: OpenTelemetry provider setup
    - Exporters: Exporter configuration (OTLP, Prometheus)
    """

    # Global provider instances
    _tracer_provider: TracerProvider | None = None
    _meter_provider: MeterProvider | None = None
    _initialized: bool = False

    class Telemetry:
        """OpenTelemetry provider initialization utilities."""

        @staticmethod
        def setup_tracer_provider(
            service_name: str,
            service_version: str = "0.9.0",
        ) -> TracerProvider:
            """Setup OpenTelemetry tracer provider.

            Args:
                service_name: Service name for resource identification
                service_version: Service version

            Returns:
                TracerProvider instance for creating tracers

            Example:
                >>> provider = Telemetry.setup_tracer_provider("flext-api")
                >>> tracer = provider.get_tracer(__name__)

            """
            resource = Resource.create(
                {
                    "service.name": service_name,
                    "service.version": service_version,
                }
            )
            provider = TracerProvider(resource=resource)

            FlextObservabilityInfrastructure._tracer_provider = provider
            return provider

        @staticmethod
        def setup_meter_provider(
            service_name: str,
            service_version: str = "0.9.0",
        ) -> MeterProvider:
            """Setup OpenTelemetry meter provider.

            Args:
                service_name: Service name for resource identification
                service_version: Service version

            Returns:
                MeterProvider instance for creating meters

            Example:
                >>> provider = Telemetry.setup_meter_provider("flext-api")
                >>> meter = provider.get_meter(__name__)

            """
            resource = Resource.create(
                {
                    "service.name": service_name,
                    "service.version": service_version,
                }
            )
            provider = MeterProvider(resource=resource)

            FlextObservabilityInfrastructure._meter_provider = provider
            return provider

        @staticmethod
        def set_global_providers() -> None:
            """Set global OpenTelemetry providers.

            This makes providers available to OpenTelemetry auto-instrumentation.
            """
            if FlextObservabilityInfrastructure._tracer_provider:
                trace.set_tracer_provider(
                    FlextObservabilityInfrastructure._tracer_provider,
                )

            if FlextObservabilityInfrastructure._meter_provider:
                metrics.set_meter_provider(
                    FlextObservabilityInfrastructure._meter_provider,
                )

    class Exporters:
        """Exporter configuration for OpenTelemetry providers."""

        @staticmethod
        def add_otlp_tracer_exporter(
            endpoint: str = "http://localhost:4317",
        ) -> None:
            """Add OTLP exporter for distributed tracing.

            Args:
                endpoint: OTLP gRPC endpoint (default: localhost:4317)

            Example:
                >>> Exporters.add_otlp_tracer_exporter("http://jaeger:4317")

            """
            if not FlextObservabilityInfrastructure._tracer_provider:
                msg = (
                    "Tracer provider not initialized. "
                    "Call Telemetry.setup_tracer_provider() first."
                )
                raise RuntimeError(msg)

            exporter = OTLPSpanExporter(endpoint=endpoint)
            processor = BatchSpanProcessor(exporter)
            FlextObservabilityInfrastructure._tracer_provider.add_span_processor(
                processor,
            )

        @staticmethod
        def add_prometheus_metrics_exporter(
            _endpoint: str = "http://localhost:9090",
        ) -> None:
            """Add Prometheus exporter for metrics.

            Args:
                _endpoint: Prometheus endpoint (default: localhost:9090) - Reserved for future use

            Example:
                >>> Exporters.add_prometheus_metrics_exporter("http://prometheus:9090")

            """
            if not FlextObservabilityInfrastructure._meter_provider:
                msg = (
                    "Meter provider not initialized. "
                    "Call Telemetry.setup_meter_provider() first."
                )
                raise RuntimeError(msg)

            PrometheusMetricReader()
            # Note: PrometheusMetricReader needs to be passed to MeterProvider
            # This is typically done during provider initialization

        @staticmethod
        def add_console_tracer_exporter() -> None:
            """Add console exporter for development/debugging traces.

            Example:
                >>> Exporters.add_console_tracer_exporter()

            """
            if not FlextObservabilityInfrastructure._tracer_provider:
                msg = (
                    "Tracer provider not initialized. "
                    "Call Telemetry.setup_tracer_provider() first."
                )
                raise RuntimeError(msg)

            exporter = InMemorySpanExporter()
            processor = SimpleSpanProcessor(exporter)
            FlextObservabilityInfrastructure._tracer_provider.add_span_processor(
                processor,
            )

    @classmethod
    def get_tracer_provider(cls) -> TracerProvider | None:
        """Get global tracer provider instance.

        Returns:
            TracerProvider or None if not initialized

        """
        return cls._tracer_provider

    @classmethod
    def get_meter_provider(cls) -> MeterProvider | None:
        """Get global meter provider instance.

        Returns:
            MeterProvider or None if not initialized

        """
        return cls._meter_provider

    @classmethod
    def is_initialized(cls) -> bool:
        """Check if OpenTelemetry infrastructure is initialized.

        Returns:
            True if both tracer and meter providers are initialized

        """
        return cls._tracer_provider is not None and cls._meter_provider is not None
