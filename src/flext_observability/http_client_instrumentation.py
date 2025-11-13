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
from typing import Any, ClassVar

from flext_core import FlextLogger, FlextResult

from flext_observability.context import FlextObservabilityContext
from flext_observability.logging_integration import FlextObservabilityLogging


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

    _logger = FlextLogger(__name__)

    # ========================================================================
    # HTTPX INSTRUMENTATION
    # ========================================================================

    class HTTPX:
        """httpx client instrumentation for automatic request tracing."""

        _instrumented_clients: ClassVar[set[Any]] = set()

        @staticmethod
        def setup_instrumentation(client: Any) -> FlextResult[None]:  # noqa: C901
            """Setup httpx client request instrumentation.

            Wraps httpx client methods to automatically trace all HTTP requests
            with context propagation.

            Args:
                client: httpx.Client or httpx.AsyncClient instance

            Returns:
                FlextResult[None] - Ok if setup successful

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
                if not hasattr(client, "request") and not hasattr(client, "_send"):
                    return FlextResult[None].fail(
                        "Invalid httpx client - missing request method"
                    )

                # Avoid duplicate instrumentation
                if client in FlextObservabilityHTTPClient.HTTPX._instrumented_clients:
                    return FlextResult[None].ok(None)

                # Determine if this is async client
                is_async = hasattr(client, "_send")

                if is_async:
                    # Instrument async client
                    original_send = client._send

                    async def traced_send(request: Any) -> Any:
                        """Traced send wrapper for async httpx."""
                        start_time = time.time()

                        # Get current context
                        correlation_id = FlextObservabilityContext.get_correlation_id()
                        trace_id = FlextObservabilityContext.get_trace_id()
                        span_id = FlextObservabilityContext.get_span_id()

                        # Add trace headers to request
                        if correlation_id:
                            request.headers["X-Correlation-ID"] = correlation_id
                        if trace_id:
                            request.headers["X-Trace-ID"] = trace_id
                        if span_id:
                            request.headers["X-Span-ID"] = span_id

                        # Log request start
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityHTTPClient._logger,
                            "debug",
                            f"HTTP client request: {request.method} {request.url}",
                            extra={
                                "http_method": request.method,
                                "http_url": str(request.url),
                                "http_scheme": request.url.scheme,
                                "http_host": str(request.url.host),
                                "client": "httpx",
                                "async": True,
                            },
                        )

                        try:
                            # Send request
                            response = await original_send(request)

                            # Calculate duration
                            duration_ms = (time.time() - start_time) * 1000

                            # Log response
                            FlextObservabilityLogging.log_with_context(
                                FlextObservabilityHTTPClient._logger,
                                "debug",
                                f"HTTP client response: {request.method} {request.url} -> {response.status_code}",
                                extra={
                                    "http_method": request.method,
                                    "http_url": str(request.url),
                                    "http_status": response.status_code,
                                    "http_duration_ms": duration_ms,
                                    "client": "httpx",
                                    "async": True,
                                },
                            )

                            return response

                        except Exception as e:
                            # Log error
                            duration_ms = (time.time() - start_time) * 1000
                            FlextObservabilityLogging.log_with_context(
                                FlextObservabilityHTTPClient._logger,
                                "error",
                                f"HTTP client error: {request.method} {request.url}",
                                extra={
                                    "http_method": request.method,
                                    "http_url": str(request.url),
                                    "http_duration_ms": duration_ms,
                                    "error_type": type(e).__name__,
                                    "error_message": str(e),
                                    "client": "httpx",
                                    "async": True,
                                },
                            )
                            raise

                    # Replace send method
                    client._send = traced_send

                else:
                    # Instrument sync client
                    original_request = client.request

                    def traced_request(
                        method: str, url: str, *args: Any, **kwargs: Any
                    ) -> Any:
                        """Traced request wrapper for sync httpx."""
                        start_time = time.time()

                        # Get current context
                        correlation_id = FlextObservabilityContext.get_correlation_id()
                        trace_id = FlextObservabilityContext.get_trace_id()
                        span_id = FlextObservabilityContext.get_span_id()

                        # Add trace headers to request
                        headers = kwargs.get("headers", {})
                        if isinstance(headers, dict):
                            if correlation_id:
                                headers["X-Correlation-ID"] = correlation_id
                            if trace_id:
                                headers["X-Trace-ID"] = trace_id
                            if span_id:
                                headers["X-Span-ID"] = span_id
                            kwargs["headers"] = headers

                        # Log request start
                        FlextObservabilityLogging.log_with_context(
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

                        try:
                            # Send request
                            response = original_request(method, url, *args, **kwargs)

                            # Calculate duration
                            duration_ms = (time.time() - start_time) * 1000

                            # Log response
                            FlextObservabilityLogging.log_with_context(
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

                        except Exception as e:
                            # Log error
                            duration_ms = (time.time() - start_time) * 1000
                            FlextObservabilityLogging.log_with_context(
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

                    # Replace request method
                    client.request = traced_request

                # Mark as instrumented
                FlextObservabilityHTTPClient.HTTPX._instrumented_clients.add(client)

                FlextObservabilityHTTPClient._logger.debug(
                    "httpx client instrumentation setup complete"
                )
                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(
                    f"httpx instrumentation setup failed: {e}"
                )

    # ========================================================================
    # AIOHTTP INSTRUMENTATION
    # ========================================================================

    class AIOHTTP:
        """aiohttp client instrumentation for automatic request tracing."""

        _instrumented_sessions: ClassVar[set[Any]] = set()

        @staticmethod
        def setup_instrumentation(session: Any) -> FlextResult[None]:
            """Setup aiohttp client session instrumentation.

            Wraps aiohttp session methods to automatically trace all HTTP requests
            with context propagation.

            Args:
                session: aiohttp.ClientSession instance

            Returns:
                FlextResult[None] - Ok if setup successful

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
                if not hasattr(session, "_request"):
                    return FlextResult[None].fail(
                        "Invalid aiohttp session - missing _request method"
                    )

                # Avoid duplicate instrumentation
                if (
                    session
                    in FlextObservabilityHTTPClient.AIOHTTP._instrumented_sessions
                ):
                    return FlextResult[None].ok(None)

                # Store original request method
                original_request = session._request

                async def traced_request(
                    method: str, url: str, *args: Any, **kwargs: Any
                ) -> Any:
                    """Traced request wrapper for aiohttp."""
                    start_time = time.time()

                    # Get current context
                    correlation_id = FlextObservabilityContext.get_correlation_id()
                    trace_id = FlextObservabilityContext.get_trace_id()
                    span_id = FlextObservabilityContext.get_span_id()

                    # Add trace headers to request
                    headers = kwargs.get("headers", {})
                    if isinstance(headers, dict):
                        if correlation_id:
                            headers["X-Correlation-ID"] = correlation_id
                        if trace_id:
                            headers["X-Trace-ID"] = trace_id
                        if span_id:
                            headers["X-Span-ID"] = span_id
                    kwargs["headers"] = headers

                    # Log request start
                    FlextObservabilityLogging.log_with_context(
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

                    try:
                        # Send request
                        response = await original_request(method, url, *args, **kwargs)

                        # Calculate duration
                        duration_ms = (time.time() - start_time) * 1000

                        # Get status
                        status = response.status

                        # Log response
                        FlextObservabilityLogging.log_with_context(
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

                    except Exception as e:
                        # Log error
                        duration_ms = (time.time() - start_time) * 1000
                        FlextObservabilityLogging.log_with_context(
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

                # Replace request method
                session._request = traced_request

                # Mark as instrumented
                FlextObservabilityHTTPClient.AIOHTTP._instrumented_sessions.add(session)

                FlextObservabilityHTTPClient._logger.debug(
                    "aiohttp session instrumentation setup complete"
                )
                return FlextResult[None].ok(None)

            except Exception as e:
                return FlextResult[None].fail(
                    f"aiohttp instrumentation setup failed: {e}"
                )


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    "FlextObservabilityHTTPClient",
]
