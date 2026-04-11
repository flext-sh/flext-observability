"""Observability protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from typing import Protocol, runtime_checkable

from flext_core import p, r
from flext_observability import t


class FlextObservabilityProtocols(p):
    """Unified observability protocols following FLEXT domain extension pattern.

    Extends p to inherit all foundation protocols (Result, Service, etc.)
    and adds observability-specific protocols in the Observability namespace.

    Architecture:
    - EXTENDS: p (inherits Foundation, Domain, Application, etc.)
    - ADDS: Observability-specific protocols in Observability namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_core import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # Observability-specific protocols
    metrics: p.Observability.Metrics
    tracing: p.Observability.Tracing
    """

    class Observability:
        """Observability domain-specific protocols.

        Provides protocols for metrics collection, distributed tracing,
        alerting, health checks, logging, and dashboard visualization.
        """

        @runtime_checkable
        class _Span(Protocol):
            """Protocol for OpenTelemetry Span interface."""

            def update_attribute(self, key: str, *, value: t.Scalar) -> None:
                """Set span attribute."""
                ...

            def update_status(self, status: int) -> None:
                """Set span status."""
                ...

        @runtime_checkable
        class Metrics(p.Service[bool], Protocol):
            """Protocol for metrics collection and management operations."""

            def create_counter(
                self,
                name: str,
                description: str,
                *,
                unit: str = "count",
            ) -> p.Result[bool]:
                """Create a counter metric."""
                ...

            def create_gauge(
                self,
                name: str,
                description: str,
                *,
                unit: str = "value",
            ) -> p.Result[bool]:
                """Create a gauge metric."""
                ...

            def create_histogram(
                self,
                name: str,
                description: str,
                *,
                unit: str = "seconds",
                buckets: t.ScalarList | None = None,
            ) -> p.Result[bool]:
                """Create a histogram metric."""
                ...

            def fetch_metrics(
                self,
                name_pattern: t.Scalar | None = None,
                *,
                start_time: t.Scalar | None = None,
                end_time: t.Scalar | None = None,
            ) -> p.Result[t.ScalarList]:
                """Get collected metrics."""
                ...

            def record_metric(
                self,
                name: str,
                value: float,
                *,
                unit: str = "count",
                tags: t.ConfigurationMapping | None = None,
            ) -> p.Result[bool]:
                """Record a metric value."""
                ...

        @runtime_checkable
        class Tracing(p.Service[bool], Protocol):
            """Protocol for distributed tracing operations."""

            def add_span_tag(
                self,
                span: FlextObservabilityProtocols.Observability._Span,
                key: str,
                value: t.Scalar,
            ) -> p.Result[bool]:
                """Add tag to trace span."""
                ...

            def finish_span(
                self,
                span: FlextObservabilityProtocols.Observability._Span,
                *,
                status: str = "ok",
                error: t.Scalar | None = None,
            ) -> p.Result[bool]:
                """Finish a trace span."""
                ...

            def fetch_trace(self, trace_id: str) -> p.Result[t.RuntimeData]:
                """Get trace by ID."""
                ...

            def search_traces(
                self,
                *,
                service_name: t.Scalar | None = None,
                operation_name: t.Scalar | None = None,
                start_time: t.Scalar | None = None,
                end_time: t.Scalar | None = None,
            ) -> p.Result[t.ScalarList]:
                """Search traces by criteria."""
                ...

            def start_span(
                self,
                operation_name: str,
                *,
                service_name: t.Scalar | None = None,
                parent_span_id: t.Scalar | None = None,
            ) -> p.Result[t.RuntimeData]:
                """Start a new trace span."""
                ...

        @runtime_checkable
        class Alerting(p.Service[bool], Protocol):
            """Protocol for alerting and notification operations."""

            def create_alert(
                self,
                message: str,
                level: str,
                *,
                service: t.Scalar | None = None,
                tags: t.ConfigurationMapping | None = None,
            ) -> p.Result[str]:
                """Create an alert."""
                ...

            def create_alert_rule(
                self,
                name: str,
                condition: str,
                *,
                threshold: t.Scalar | None = None,
                duration: t.Scalar | None = None,
            ) -> p.Result[str]:
                """Create an alert rule."""
                ...

            def fetch_alerts(
                self,
                *,
                level: t.Scalar | None = None,
                service: t.Scalar | None = None,
                resolved: t.Scalar | None = None,
            ) -> p.Result[t.ScalarList]:
                """Get alerts by criteria."""
                ...

            def resolve_alert(self, alert_id: str) -> p.Result[bool]:
                """Resolve an alert."""
                ...

        @runtime_checkable
        class HealthCheck(p.Service[bool], Protocol):
            """Protocol for health check operations."""

            def check_health(
                self,
                service_name: str,
            ) -> p.Result[t.RuntimeData]:
                """Perform health check for a service."""
                ...

            def services_status(
                self,
            ) -> p.Result[t.RuntimeData]:
                """Get health status for all services."""
                ...

            def service_status(
                self,
                service_name: str,
            ) -> p.Result[t.RuntimeData]:
                """Get service health status."""
                ...

            def register_health_check(
                self,
                service_name: str,
                check_function: Callable[[], bool],
                *,
                interval: int = 60,
            ) -> p.Result[bool]:
                """Register a health check."""
                ...

        @runtime_checkable
        class Logging(p.Service[bool], Protocol):
            """Protocol for logging operations."""

            def configure_logging(
                self,
                settings: t.ConfigurationMapping,
            ) -> p.Result[bool]:
                """Configure logging system."""
                ...

            def create_logger(
                self,
                name: str,
                *,
                level: str = "info",
                format_string: t.Scalar | None = None,
            ) -> p.Result[p.Logger]:
                """Create a logger instance."""
                ...

            def fetch_logs(
                self,
                *,
                level: t.Scalar | None = None,
                service: t.Scalar | None = None,
                correlation_id: t.Scalar | None = None,
                start_time: t.Scalar | None = None,
                end_time: t.Scalar | None = None,
            ) -> p.Result[t.ScalarList]:
                """Get logs by criteria."""
                ...

            def log_message(
                self,
                message: str,
                level: str,
                *,
                service: t.Scalar | None = None,
                correlation_id: t.Scalar | None = None,
                extra: t.ConfigurationMapping | None = None,
            ) -> p.Result[bool]:
                """Log a message."""
                ...

        @runtime_checkable
        class ObservabilityService(Protocol):
            """Protocol for observability services providing alerts and metrics."""

            def create_alert(self, **kwargs: t.Scalar) -> r[t.Dict]:
                """Create an alert with given parameters."""
                ...

            def metrics_summary(self) -> r[t.Dict]:
                """Get summary of collected metrics."""
                ...

        @runtime_checkable
        class Dashboard(p.Service[bool], Protocol):
            """Protocol for dashboard and visualization operations."""

            def add_widget(
                self,
                dashboard_id: str,
                widget_config: t.ConfigurationMapping,
            ) -> p.Result[str]:
                """Add widget to dashboard."""
                ...

            def create_dashboard(
                self,
                name: str,
                description: str,
                *,
                widgets: Sequence[t.ConfigurationMapping] | None = None,
            ) -> p.Result[str]:
                """Create a dashboard."""
                ...

            def fetch_dashboard(
                self,
                dashboard_id: str,
            ) -> p.Result[t.RuntimeData]:
                """Get dashboard by ID."""
                ...

            def fetch_dashboard_data(
                self,
                dashboard_id: str,
                *,
                start_time: t.Scalar | None = None,
                end_time: t.Scalar | None = None,
            ) -> p.Result[t.RuntimeData]:
                """Get dashboard data."""
                ...

        class Http:
            """Protocols for Flask and FastAPI HTTP instrumentation."""

            @runtime_checkable
            class FlaskHook(Protocol):
                """Protocol for Flask request hooks."""

                def __call__[T](
                    self,
                    callback: Callable[..., T],
                ) -> Callable[..., T]:
                    """Call the hook with a callback."""
                    ...

            @runtime_checkable
            class FlaskErrorHandler(Protocol):
                """Protocol for Flask error handler decorator."""

                def __call__(
                    self,
                    error_type: type[Exception],
                ) -> FlextObservabilityProtocols.Observability.Http.FlaskHook:
                    """Return a hook for the given error type."""
                    ...

            @runtime_checkable
            class FlaskApp(Protocol):
                """Protocol for Flask application."""

                before_request: FlextObservabilityProtocols.Observability.Http.FlaskHook
                after_request: FlextObservabilityProtocols.Observability.Http.FlaskHook
                errorhandler: (
                    FlextObservabilityProtocols.Observability.Http.FlaskErrorHandler
                )

            @runtime_checkable
            class FastAPIApp(Protocol):
                """Protocol for FastAPI application."""

                def add_middleware(self, middleware_class: type) -> None:
                    """Add middleware to the FastAPI app."""
                    ...

            @runtime_checkable
            class RequestURL(Protocol):
                """Protocol for request URL objects."""

                path: str

            @runtime_checkable
            class RequestClient(Protocol):
                """Protocol for request client objects."""

                host: str

            @runtime_checkable
            class Request(Protocol):
                """Protocol for HTTP request objects used by middleware."""

                headers: t.Dict
                method: str
                url: FlextObservabilityProtocols.Observability.Http.RequestURL
                client: (
                    FlextObservabilityProtocols.Observability.Http.RequestClient | None
                )

            @runtime_checkable
            class Response(Protocol):
                """Protocol for HTTP response objects used by middleware."""

                status_code: int
                headers: t.Dict

        class HttpClient:
            """Protocols for httpx and aiohttp HTTP client instrumentation."""

            @runtime_checkable
            class HTTPXURL(Protocol):
                """Protocol for httpx URL t.NormalizedValue."""

                @property
                def host(self) -> str | None:
                    """URL host."""
                    ...

                @property
                def scheme(self) -> str:
                    """URL scheme (http/https)."""
                    ...

            @runtime_checkable
            class HTTPXRequest(Protocol):
                """Protocol for httpx Request t.NormalizedValue."""

                @property
                def headers(self) -> t.MutableStrMapping:
                    """Request headers."""
                    ...

                @property
                def method(self) -> str:
                    """HTTP method."""
                    ...

                @property
                def url(
                    self,
                ) -> FlextObservabilityProtocols.Observability.HttpClient.HTTPXURL:
                    """Request URL."""
                    ...

            @runtime_checkable
            class HTTPXResponse(Protocol):
                """Protocol for httpx Response t.NormalizedValue."""

                @property
                def status_code(self) -> int:
                    """HTTP status code."""
                    ...

            @runtime_checkable
            class AIOHTTPResponse(Protocol):
                """Protocol for aiohttp ClientResponse."""

                @property
                def status(self) -> int:
                    """HTTP status code."""
                    ...

            @runtime_checkable
            class HTTPXAsyncClient(Protocol):
                """Protocol for async httpx client."""

                _send: Callable[
                    ...,
                    Awaitable[
                        FlextObservabilityProtocols.Observability.HttpClient.HTTPXResponse
                    ],
                ]
                request: Callable[
                    ...,
                    FlextObservabilityProtocols.Observability.HttpClient.HTTPXResponse
                    | Awaitable[
                        FlextObservabilityProtocols.Observability.HttpClient.HTTPXResponse
                    ],
                ]

            @runtime_checkable
            class HTTPXClient(Protocol):
                """Protocol for sync httpx client."""

                request: Callable[
                    ...,
                    FlextObservabilityProtocols.Observability.HttpClient.HTTPXResponse
                    | Awaitable[
                        FlextObservabilityProtocols.Observability.HttpClient.HTTPXResponse
                    ],
                ]

            @runtime_checkable
            class AIOHTTPSession(Protocol):
                """Protocol for aiohttp ClientSession."""

                request: Callable[
                    ...,
                    Awaitable[
                        FlextObservabilityProtocols.Observability.HttpClient.AIOHTTPResponse
                    ],
                ]


p = FlextObservabilityProtocols
__all__ = ["FlextObservabilityProtocols", "p"]
