"""Observability domain protocols owned by the private protocols family.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping, MutableMapping
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_observability.typings import t

if TYPE_CHECKING:
    from collections.abc import Sequence
    from datetime import datetime
    from typing import Self

    from flext_cli import p

    from flext_observability._constants import FlextObservabilityConstantsDomains


class FlextObservabilityProtocolsDomains:
    """Observability domain-specific protocols.

    Provides the observability service contract plus HTTP framework
    instrumentation protocols.
    """

    @runtime_checkable
    class LoggingContext(Protocol):
        """Read the selected operation's existing correlation and span context."""

        def correlation_id(self) -> str: ...

        def trace_id(self) -> str: ...

        def span_id(self) -> str: ...

    @runtime_checkable
    class ErrorEvent(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def error_type(self) -> t.NonEmptyStr:
            """Error classification type."""
            ...

        @property
        def message(self) -> t.NonEmptyStr:
            """Error message."""
            ...

        @property
        def severity(self) -> FlextObservabilityConstantsDomains.ErrorSeverity:
            """Error severity level."""
            ...

        @property
        def fingerprint(self) -> str:
            """SHA256 deduplication fingerprint."""
            ...

        @property
        def correlation_id(self) -> str:
            """Correlation identifier."""
            ...

        def calculate_fingerprint(self) -> Self:
            """Calculate SHA256 fingerprint from error type and message."""
            ...

    @runtime_checkable
    class ErrorRecorder(Protocol):
        """Record an actual domain error without coupling to its service class."""

        def record_error(
            self,
            error: FlextObservabilityProtocolsDomains.ErrorEvent,
        ) -> p.Result[FlextObservabilityProtocolsDomains.ErrorEvent]: ...

    @runtime_checkable
    class ErrorHandler(ErrorRecorder, Protocol):
        """Actual error aggregation operations exposed by the service facade."""

        def clear_error_counts(
            self, older_than_sec: float | None = None
        ) -> p.Result[bool]: ...

        def resolve_error_count(self, fingerprint: str) -> int: ...

        def resolve_escalated_severity(
            self,
            error: FlextObservabilityProtocolsDomains.ErrorEvent,
        ) -> t.Observability.ErrorSeverity: ...

        def record_alert_sent(
            self, error: FlextObservabilityProtocolsDomains.ErrorEvent
        ) -> None: ...

        def update_alert_cooldown(self, seconds: float) -> p.Result[bool]: ...

        def update_escalation_threshold(self, threshold: int) -> p.Result[bool]: ...

        def should_alert_for_error(
            self, error: FlextObservabilityProtocolsDomains.ErrorEvent
        ) -> bool: ...

    @runtime_checkable
    class ObservabilityService(Protocol):
        """Protocol for observability services providing alerts and metrics."""

        def create_alert(self, **kwargs: t.Scalar) -> p.Result[p.Dict]:
            """Create an alert with given parameters."""
            ...

        def metrics_summary(self) -> p.Result[p.Dict]:
            """Get summary of collected metrics."""
            ...

    class Http:
        """Protocols for Flask and FastAPI HTTP instrumentation."""

        @runtime_checkable
        class FlaskHook(Protocol):
            """Protocol for Flask request hooks."""

            def __call__[T](self, callback: Callable[..., T]) -> Callable[..., T]:
                """Call the hook with a callback."""
                ...

        @runtime_checkable
        class FlaskErrorHandler(Protocol):
            """Protocol for Flask error handler decorator."""

            def __call__(
                self,
                error_type: type[Exception],
            ) -> FlextObservabilityProtocolsDomains.Http.FlaskHook:
                """Return a hook for the given error type."""
                ...

        @runtime_checkable
        class FlaskApp(Protocol):
            """Protocol for Flask application."""

            before_request: FlextObservabilityProtocolsDomains.Http.FlaskHook
            after_request: FlextObservabilityProtocolsDomains.Http.FlaskHook
            errorhandler: FlextObservabilityProtocolsDomains.Http.FlaskErrorHandler

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

            headers: p.Dict
            method: str
            url: FlextObservabilityProtocolsDomains.Http.RequestURL
            client: FlextObservabilityProtocolsDomains.Http.RequestClient | None

        @runtime_checkable
        class Response(Protocol):
            """Protocol for HTTP response objects used by middleware."""

            status_code: int
            headers: p.Dict

    class HttpClient:
        """Protocols for httpx and aiohttp HTTP client instrumentation."""

        @runtime_checkable
        class HTTPXResponse(Protocol):
            """Protocol for httpx Response t.JsonValue."""

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
                Awaitable[FlextObservabilityProtocolsDomains.HttpClient.HTTPXResponse],
            ]
            request: Callable[
                ...,
                FlextObservabilityProtocolsDomains.HttpClient.HTTPXResponse
                | Awaitable[
                    FlextObservabilityProtocolsDomains.HttpClient.HTTPXResponse
                ],
            ]

        @runtime_checkable
        class HTTPXClient(Protocol):
            """Protocol for sync httpx client."""

            request: Callable[
                ...,
                FlextObservabilityProtocolsDomains.HttpClient.HTTPXResponse
                | Awaitable[
                    FlextObservabilityProtocolsDomains.HttpClient.HTTPXResponse
                ],
            ]

        @runtime_checkable
        class AIOHTTPSession(Protocol):
            """Protocol for aiohttp ClientSession."""

            request: Callable[
                ...,
                Awaitable[
                    FlextObservabilityProtocolsDomains.HttpClient.AIOHTTPResponse
                ],
            ]

    @runtime_checkable
    class MetricEntry(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        metric_id: str
        name: t.NonEmptyStr
        value: t.Numeric
        unit: t.NonEmptyStr
        source: str

    @runtime_checkable
    class _EntityWithId(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        id: str

    @runtime_checkable
    class Metric(_EntityWithId, Protocol):
        """Structural data contract projected from the owning model."""

        name: t.NonEmptyStr
        value: t.PositiveFloat
        unit: t.NonEmptyStr
        metric_type: t.NonEmptyStr
        labels: Mapping[str, t.Scalar]

    @runtime_checkable
    class Trace(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        trace_id: str
        name: t.NonEmptyStr
        attributes: Mapping[str, t.Scalar]

    @runtime_checkable
    class Alert(_EntityWithId, Protocol):
        """Structural data contract projected from the owning model."""

        title: t.NonEmptyStr
        message: t.NonEmptyStr
        severity: t.NonEmptyStr
        source: t.NonEmptyStr
        labels: Mapping[str, t.Scalar]

    @runtime_checkable
    class HealthCheck(_EntityWithId, Protocol):
        """Structural data contract projected from the owning model."""

        component: t.NonEmptyStr
        status: t.NonEmptyStr
        details: Mapping[str, t.Scalar]

    @runtime_checkable
    class LogEntry(_EntityWithId, Protocol):
        """Structural data contract projected from the owning model."""

        message: t.NonEmptyStr
        level: t.NonEmptyStr
        component: t.NonEmptyStr
        timestamp: datetime
        context: Mapping[str, t.Scalar]

    @runtime_checkable
    class StartTimePayload(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def value(self) -> float:
            """Request start time in seconds since epoch."""
            ...

    @runtime_checkable
    class HeadersPayload(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def headers(self) -> Mapping[str, str]:
            """HTTP header key-value pairs."""
            ...

    @runtime_checkable
    class ContextSnapshot(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def correlation_id(self) -> str:
            """Correlation identifier."""
            ...

        @property
        def trace_id(self) -> str:
            """Trace identifier."""
            ...

        @property
        def span_id(self) -> str:
            """Span identifier."""
            ...

        @property
        def baggage(self) -> Mapping[str, str]:
            """Propagated baggage key-value pairs."""
            ...

        @property
        def metadata(self) -> t.ConfigurationMapping:
            """Additional context metadata."""
            ...

    @runtime_checkable
    class BaggageKeyModel(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def key(self) -> t.NonEmptyStr:
            """Baggage key name."""
            ...

    @runtime_checkable
    class MetricTypeInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def metric_type(self) -> FlextObservabilityConstantsDomains.MetricType:
            """Type of metric to create."""
            ...

    @runtime_checkable
    class CustomMetricDefinition(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def name(self) -> t.NonEmptyStr:
            """Custom metric name."""
            ...

        @property
        def metric_type(self) -> FlextObservabilityConstantsDomains.MetricType:
            """Type of metric."""
            ...

        @property
        def description(self) -> t.NonEmptyStr:
            """Human-readable metric description."""
            ...

        @property
        def unit(self) -> str:
            """Measurement unit."""
            ...

        @property
        def labels(self) -> Mapping[str, str]:
            """Metric labels for categorization."""
            ...

    @runtime_checkable
    class CooldownInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def seconds(self) -> t.PositiveFloat:
            """Cooldown duration in seconds."""
            ...

    @runtime_checkable
    class ThresholdInput(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def threshold(self) -> t.PositiveInt:
            """Error count threshold."""
            ...

    @runtime_checkable
    class ErrorHandlingState(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        error_counts: t.MutableIntMapping
        last_alert_time: MutableMapping[str, float]
        alert_cooldown_sec: float
        escalation_threshold: int
        deduplication_window_sec: int

    @runtime_checkable
    class LogContext(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def correlation_id(self) -> str | None:
            """Correlation identifier."""
            ...

        @property
        def trace_id(self) -> str | None:
            """Trace identifier."""
            ...

        @property
        def span_id(self) -> str | None:
            """Span identifier."""
            ...

        @property
        def baggage(self) -> str | None:
            """Serialized baggage string."""
            ...

        @property
        def extra(self) -> p.Dict:
            """Additional context data."""
            ...

    @runtime_checkable
    class PerformanceMetrics(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def operation(self) -> t.NonEmptyStr:
            """Operation name being measured."""
            ...

        @property
        def start_time(self) -> float:
            """Operation start time in seconds since epoch."""
            ...

        @property
        def end_time(self) -> float:
            """Operation end time in seconds since epoch."""
            ...

        @property
        def duration_ms(self) -> float:
            """Operation duration in milliseconds."""
            ...

        @property
        def memory_used_mb(self) -> float:
            """Memory used in megabytes."""
            ...

        @property
        def cpu_percent(self) -> float:
            """CPU usage percentage."""
            ...

        @property
        def success(self) -> bool:
            """Whether the operation succeeded."""
            ...

        @property
        def error_message(self) -> str:
            """Error message if operation failed."""
            ...

        def calculate_duration(self) -> Self:
            """Structural member projected from the owning model.

            Calculate operation duration in milliseconds from start and end times.
            """
            ...


__all__: list[str] = ["FlextObservabilityProtocolsDomains"]
