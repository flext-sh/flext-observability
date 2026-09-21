"""Observability domain protocols owned by the private protocols family."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Protocol, runtime_checkable

from flext_cli import m, p

from flext_core import t


class FlextObservabilityProtocolsDomains:
    """Observability domain-specific protocols.

    Provides the observability service contract plus HTTP framework
    instrumentation protocols.
    """

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
                self, error_type: type[Exception]
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
