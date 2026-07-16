"""Observability protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Awaitable,
    Callable,
)
from typing import Protocol, runtime_checkable

from flext_cli import p
from flext_observability import p, t


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
    service: p.Observability.ObservabilityService
    request: p.Observability.Http.Request
    """

    class Observability:
        """Observability domain-specific protocols.

        Provides the observability service contract plus HTTP framework
        instrumentation protocols.
        """

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

                headers: p.Dict
                method: str
                url: FlextObservabilityProtocols.Observability.Http.RequestURL
                client: (
                    FlextObservabilityProtocols.Observability.Http.RequestClient | None
                )

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
__all__: list[str] = ["FlextObservabilityProtocols", "p"]
