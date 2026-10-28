"""Observability domain protocols owned by the private protocols family.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import p

if TYPE_CHECKING:
    from flext_observability import m, t


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
    class ErrorEvent(Protocol):
        """Read-only domain error data at the recording boundary."""

        @property
        def error_type(self) -> str: ...

        @property
        def message(self) -> str: ...

        @property
        def severity(self) -> t.Observability.ErrorSeverity: ...

        @property
        def fingerprint(self) -> str: ...

        @property
        def correlation_id(self) -> str: ...

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

        def create_alert(self, **kwargs: t.Scalar) -> p.Result[m.Dict]:
            """Create an alert with given parameters."""
            ...

        def metrics_summary(self) -> p.Result[m.Dict]:
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

            headers: m.Dict
            method: str
            url: FlextObservabilityProtocolsDomains.Http.RequestURL
            client: FlextObservabilityProtocolsDomains.Http.RequestClient | None

        @runtime_checkable
        class Response(Protocol):
            """Protocol for HTTP response objects used by middleware."""

            status_code: int
            headers: m.Dict

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


__all__: list[str] = ["FlextObservabilityProtocolsDomains"]
