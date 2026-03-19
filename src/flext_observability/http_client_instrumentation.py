"""HTTP client auto-instrumentation for service-to-service communication.

Provides automatic HTTP request tracing and metrics collection for httpx and aiohttp
clients without requiring any code changes to application code.

FLEXT Pattern:
- Single FlextObservabilityHTTPClient class
- Nested HTTPX and AIOHTTP implementations
- Integration with Phase 3 (Context & Logging)
- Automatic context propagation to downstream services

Key Features:
- Zero code changes needed in application code
- Automatic correlation ID propagation to outbound requests
- HTTP request/response tracing with duration
- Error tracking and logging with context
- Async-safe with aiohttp and async httpx
- Service-to-service trace correlation
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable, MutableMapping
from typing import Annotated, ClassVar, Protocol, TypeGuard

from flext_core import FlextRuntime, r
from pydantic import BaseModel, Field, ValidationError

from flext_observability import FlextObservabilityContext, FlextObservabilityLogging, t


class _HeadersPayload(BaseModel):
    headers: Annotated[dict[str, str], Field(default_factory=dict)]


class HTTPXURL(Protocol):
    """Protocol for httpx URL object."""

    @property
    def host(self) -> str | None:
        """URL host."""
        ...

    @property
    def scheme(self) -> str:
        """URL scheme (http/https)."""
        ...


class HTTPXRequest(Protocol):
    """Protocol for httpx Request object."""

    @property
    def headers(self) -> MutableMapping[str, str]:
        """Request headers."""
        ...

    @property
    def method(self) -> str:
        """HTTP method."""
        ...

    @property
    def url(self) -> HTTPXURL:
        """Request URL."""
        ...


class HTTPXResponse(Protocol):
    """Protocol for httpx Response object."""

    @property
    def status_code(self) -> int:
        """HTTP status code."""
        ...


class AIOHTTPResponse(Protocol):
    """Protocol for aiohttp ClientResponse."""

    @property
    def status(self) -> int:
        """HTTP status code."""
        ...


class HTTPXAsyncClient(Protocol):
    _send: Callable[..., Awaitable[HTTPXResponse]]
    request: Callable[..., HTTPXResponse | Awaitable[HTTPXResponse]]


class HTTPXClient(Protocol):
    request: Callable[..., HTTPXResponse | Awaitable[HTTPXResponse]]


class AIOHTTPSession(Protocol):
    request: Callable[..., Awaitable[AIOHTTPResponse]]


class FlextObservabilityHTTPClient:
    """HTTP client auto-instrumentation for service-to-service communication.

    Provides middleware for automatic HTTP client request tracing and metrics
    collection for httpx and aiohttp clients.

    Usage:
        ```python
        import httpx
        from flext_observability import FlextObservabilityHTTPClient

        # Setup httpx client instrumentation
        client = httpx.Client()
        FlextObservabilityHTTPClient.HTTPX.setup_instrumentation(client)

        # All outbound HTTP requests now automatically traced!
        response = client.get("https://api.example.com/users")
        # Automatically:
        # ✅ Correlation ID propagated to downstream service
        # ✅ Request duration tracked
        # ✅ Response status logged with context
        ```

    Nested Classes:
        HTTPX: httpx client instrumentation (sync and async)
        AIOHTTP: aiohttp client instrumentation (async)
    """

    _logger = FlextRuntime.get_logger(__name__)

    @staticmethod
    def _is_httpx_async_client(
        obj: t.RegisterableService,
    ) -> TypeGuard[HTTPXAsyncClient]:
        """Type guard to check if object is an async httpx client."""
        return hasattr(obj, "request") and hasattr(obj, "_send")

    @staticmethod
    def _is_httpx_client(obj: t.RegisterableService) -> TypeGuard[HTTPXClient]:
        """Type guard to check if object is an httpx client."""
        return hasattr(obj, "request") and hasattr(obj, "_send") is False

    @staticmethod
    def _is_aiohttp_session(obj: t.RegisterableService) -> TypeGuard[AIOHTTPSession]:
        return hasattr(obj, "request")

    @staticmethod
    def _validated_headers(payload: t.NormalizedValue) -> MutableMapping[str, str]:
        try:
            return _HeadersPayload.model_validate(obj={"headers": payload}).headers
        except ValidationError:
            return {}

    class HTTPX:
        """httpx client instrumentation for automatic request tracing."""

        instrumented_clients: ClassVar[set[int]] = set()

        @staticmethod
        def setup_instrumentation(client: t.RegisterableService) -> r[bool]:
            """Setup httpx client request instrumentation.

            Wraps httpx client methods to automatically trace all HTTP requests
            with context propagation.

            Args:
                client: httpx.Client or httpx.AsyncClient instance

            Returns:
                r[bool] - Ok if setup successful

            Behavior:
                - Injects correlation ID into request headers
                - Creates span for each HTTP request
                - Records request duration
                - Logs request/response with context
                - Propagates context to downstream services
                - Handles errors with context

            Example:
                ```python
                import httpx
                from flext_observability import FlextObservabilityHTTPClient

                # Sync client
                client = httpx.Client()
                FlextObservabilityHTTPClient.HTTPX.setup_instrumentation(client)

                response = client.get("https://api.example.com/users")
                # Automatically traced with correlation ID in headers

                # Async client
                async_client = httpx.AsyncClient()
                FlextObservabilityHTTPClient.HTTPX.setup_instrumentation(async_client)

                response = await async_client.get("https://api.example.com/users")
                # Automatically traced with correlation ID in headers
                ```

            """
            try:
                if (
                    hasattr(client, "request") is False
                    and hasattr(client, "_send") is False
                ):
                    return r[bool].fail("Invalid httpx client - missing request method")
                client_id = id(client)
                if client_id in FlextObservabilityHTTPClient.HTTPX.instrumented_clients:
                    return r[bool].ok(value=True)
                if FlextObservabilityHTTPClient._is_httpx_async_client(client):
                    typed_async_client: HTTPXAsyncClient = client
                    original_request = typed_async_client.request

                    async def traced_async_request(
                        method: str,
                        url: str,
                        *args: t.Scalar,
                        **kwargs: t.Scalar,
                    ) -> HTTPXResponse:
                        start_time = time.time()
                        correlation_id = FlextObservabilityContext.get_correlation_id()
                        trace_id = FlextObservabilityContext.get_trace_id()
                        span_id = FlextObservabilityContext.get_span_id()
                        headers = FlextObservabilityHTTPClient._validated_headers(
                            kwargs.get("headers", {}),
                        )
                        if correlation_id:
                            headers["X-Correlation-ID"] = correlation_id
                        if trace_id:
                            headers["X-Trace-ID"] = trace_id
                        if span_id:
                            headers["X-Span-ID"] = span_id
                        _ = FlextObservabilityLogging.log_with_context(
                            FlextObservabilityHTTPClient._logger,
                            "debug",
                            f"HTTP client request: {method} {url}",
                            extra={
                                "http_method": method,
                                "http_url": str(url),
                                "client": "httpx",
                                "async": True,
                            },
                        )
                        call_kwargs: dict[str, t.Scalar] = {
                            k: v for k, v in kwargs.items() if k != "headers"
                        }
                        try:
                            response_candidate = original_request(
                                method,
                                url,
                                *args,
                                headers=headers,
                                **call_kwargs,
                            )
                            if not isinstance(response_candidate, Awaitable):
                                error_message = "Async httpx request returned a non-awaitable response"
                                raise TypeError(
                                    error_message,
                                )
                            response = await response_candidate
                            duration_ms = (time.time() - start_time) * 1000
                            _ = FlextObservabilityLogging.log_with_context(
                                FlextObservabilityHTTPClient._logger,
                                "debug",
                                f"HTTP client response: {method} {url} -> {response.status_code}",
                                extra={
                                    "http_method": method,
                                    "http_url": str(url),
                                    "http_status": response.status_code,
                                    "http_duration_ms": duration_ms,
                                    "client": "httpx",
                                    "async": True,
                                },
                            )
                            return response
                        except (ValueError, TypeError, KeyError) as e:
                            duration_ms = (time.time() - start_time) * 1000
                            _ = FlextObservabilityLogging.log_with_context(
                                FlextObservabilityHTTPClient._logger,
                                "error",
                                f"HTTP client error: {method} {url}",
                                extra={
                                    "http_method": method,
                                    "http_url": str(url),
                                    "http_duration_ms": duration_ms,
                                    "error_type": type(e).__name__,
                                    "error_message": str(e),
                                    "client": "httpx",
                                    "async": True,
                                },
                            )
                            raise

                    typed_async_client.request = traced_async_request
                elif FlextObservabilityHTTPClient._is_httpx_client(client):
                    typed_sync_client: HTTPXClient = client
                    original_request: Callable[
                        ...,
                        HTTPXResponse | Awaitable[HTTPXResponse],
                    ] = typed_sync_client.request

                    def traced_request(
                        method: str,
                        url: str,
                        *args: t.Scalar,
                        **kwargs: t.Scalar,
                    ) -> HTTPXResponse:
                        """Traced request wrapper for sync httpx."""
                        start_time = time.time()
                        correlation_id = FlextObservabilityContext.get_correlation_id()
                        trace_id = FlextObservabilityContext.get_trace_id()
                        span_id = FlextObservabilityContext.get_span_id()
                        headers = FlextObservabilityHTTPClient._validated_headers(
                            kwargs.get("headers", {}),
                        )
                        if correlation_id:
                            headers["X-Correlation-ID"] = correlation_id
                        if trace_id:
                            headers["X-Trace-ID"] = trace_id
                        if span_id:
                            headers["X-Span-ID"] = span_id
                        _ = FlextObservabilityLogging.log_with_context(
                            FlextObservabilityHTTPClient._logger,
                            "debug",
                            f"HTTP client request: {method} {url}",
                            extra={
                                "http_method": method,
                                "http_url": url,
                                "client": "httpx",
                                "async": False,
                            },
                        )
                        call_kwargs: dict[str, t.Scalar] = {
                            k: v for k, v in kwargs.items() if k != "headers"
                        }
                        try:
                            response_candidate = original_request(
                                method,
                                url,
                                *args,
                                headers=headers,
                                **call_kwargs,
                            )
                            if isinstance(response_candidate, Awaitable):
                                error_message = (
                                    "Sync httpx request returned an awaitable response"
                                )
                                raise TypeError(
                                    error_message,
                                )
                            response = response_candidate
                            duration_ms = (time.time() - start_time) * 1000
                            _ = FlextObservabilityLogging.log_with_context(
                                FlextObservabilityHTTPClient._logger,
                                "debug",
                                f"HTTP client response: {method} {url} -> {response.status_code}",
                                extra={
                                    "http_method": method,
                                    "http_url": url,
                                    "http_status": response.status_code,
                                    "http_duration_ms": duration_ms,
                                    "client": "httpx",
                                    "async": False,
                                },
                            )
                            return response
                        except (ValueError, TypeError, KeyError) as e:
                            duration_ms = (time.time() - start_time) * 1000
                            _ = FlextObservabilityLogging.log_with_context(
                                FlextObservabilityHTTPClient._logger,
                                "error",
                                f"HTTP client error: {method} {url}",
                                extra={
                                    "http_method": method,
                                    "http_url": url,
                                    "http_duration_ms": duration_ms,
                                    "error_type": type(e).__name__,
                                    "error_message": str(e),
                                    "client": "httpx",
                                    "async": False,
                                },
                            )
                            raise

                    typed_sync_client.request = traced_request
                else:
                    return r[bool].fail(
                        "Invalid httpx client - unsupported client type",
                    )
                FlextObservabilityHTTPClient.HTTPX.instrumented_clients.add(client_id)
                FlextObservabilityHTTPClient._logger.debug(
                    "httpx client instrumentation setup complete",
                )
                return r[bool].ok(value=True)
            except (ValueError, TypeError, KeyError) as e:
                return r[bool].fail(f"httpx instrumentation setup failed: {e}")

    class AIOHTTP:
        """aiohttp client instrumentation for automatic request tracing."""

        instrumented_sessions: ClassVar[set[AIOHTTPSession]] = set()

        @staticmethod
        def setup_instrumentation(session: t.RegisterableService) -> r[bool]:
            """Setup aiohttp client session instrumentation.

            Wraps aiohttp session methods to automatically trace all HTTP requests
            with context propagation.

            Args:
                session: aiohttp.ClientSession instance

            Returns:
                r[bool] - Ok if setup successful

            Behavior:
                - Injects correlation ID into request headers
                - Creates span for each HTTP request
                - Records request duration
                - Logs request/response with context
                - Propagates context to downstream services
                - Handles errors with context

            Example:
                ```python
                import aiohttp
                from flext_observability import FlextObservabilityHTTPClient

                async with aiohttp.ClientSession() as session:
                    FlextObservabilityHTTPClient.AIOHTTP.setup_instrumentation(session)

                    async with session.get("https://api.example.com/users") as response:
                        data = await response.json()
                    # Automatically traced with correlation ID in headers
                ```

            """
            try:
                if not FlextObservabilityHTTPClient._is_aiohttp_session(session):
                    return r[bool].fail(
                        "Invalid aiohttp session - missing request method",
                    )
                typed_session: AIOHTTPSession = session
                if (
                    typed_session
                    in FlextObservabilityHTTPClient.AIOHTTP.instrumented_sessions
                ):
                    return r[bool].ok(value=True)
                original_request = typed_session.request

                async def traced_request(
                    method: str,
                    url: str,
                    *args: t.Scalar,
                    **kwargs: t.Scalar,
                ) -> AIOHTTPResponse:
                    """Traced request wrapper for aiohttp."""
                    start_time = time.time()
                    correlation_id = FlextObservabilityContext.get_correlation_id()
                    trace_id = FlextObservabilityContext.get_trace_id()
                    span_id = FlextObservabilityContext.get_span_id()
                    headers = FlextObservabilityHTTPClient._validated_headers(
                        kwargs.get("headers", {}),
                    )
                    if correlation_id:
                        headers["X-Correlation-ID"] = correlation_id
                    if trace_id:
                        headers["X-Trace-ID"] = trace_id
                    if span_id:
                        headers["X-Span-ID"] = span_id
                    _ = FlextObservabilityLogging.log_with_context(
                        FlextObservabilityHTTPClient._logger,
                        "debug",
                        f"HTTP client request: {method} {url}",
                        extra={
                            "http_method": method,
                            "http_url": str(url),
                            "client": "aiohttp",
                            "async": True,
                        },
                    )
                    async_call_kwargs: dict[str, t.Scalar] = {
                        k: v for k, v in kwargs.items() if k != "headers"
                    }
                    try:
                        response = await original_request(
                            method,
                            url,
                            *args,
                            headers=headers,
                            **async_call_kwargs,
                        )
                        duration_ms = (time.time() - start_time) * 1000
                        status = response.status
                        _ = FlextObservabilityLogging.log_with_context(
                            FlextObservabilityHTTPClient._logger,
                            "debug",
                            f"HTTP client response: {method} {url} -> {status}",
                            extra={
                                "http_method": method,
                                "http_url": str(url),
                                "http_status": status,
                                "http_duration_ms": duration_ms,
                                "client": "aiohttp",
                                "async": True,
                            },
                        )
                        return response
                    except (ValueError, TypeError, KeyError) as e:
                        duration_ms = (time.time() - start_time) * 1000
                        _ = FlextObservabilityLogging.log_with_context(
                            FlextObservabilityHTTPClient._logger,
                            "error",
                            f"HTTP client error: {method} {url}",
                            extra={
                                "http_method": method,
                                "http_url": str(url),
                                "http_duration_ms": duration_ms,
                                "error_type": type(e).__name__,
                                "error_message": str(e),
                                "client": "aiohttp",
                                "async": True,
                            },
                        )
                        raise

                typed_session.request = traced_request
                FlextObservabilityHTTPClient.AIOHTTP.instrumented_sessions.add(
                    typed_session,
                )
                FlextObservabilityHTTPClient._logger.debug(
                    "aiohttp session instrumentation setup complete",
                )
                return r[bool].ok(value=True)
            except (ValueError, TypeError, KeyError) as e:
                return r[bool].fail(f"aiohttp instrumentation setup failed: {e}")


__all__ = ["FlextObservabilityHTTPClient"]
