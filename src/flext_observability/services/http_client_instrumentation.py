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

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from typing import ClassVar, TypeIs

from flext_observability import c, m, p, r, t, u
from flext_observability.services.context import FlextObservabilityContext
from flext_observability.services.logging_integration import FlextObservabilityLogging


def _bind_traced_request(
    client: p.Observability.HttpClient.HTTPXAsyncClient
    | p.Observability.HttpClient.HTTPXClient,
    traced: Callable[
        ...,
        p.Observability.HttpClient.HTTPXResponse
        | Awaitable[p.Observability.HttpClient.HTTPXResponse],
    ],
) -> None:
    """Rebind one httpx client's ``request`` attribute to its traced wrapper."""
    client.request = traced


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

    logger = u.fetch_logger(__name__)

    @staticmethod
    def _matches_httpx_async_client(
        obj: t.RegisterableService
        | p.Observability.HttpClient.HTTPXAsyncClient
        | p.Observability.HttpClient.HTTPXClient,
    ) -> TypeIs[p.Observability.HttpClient.HTTPXAsyncClient]:
        """Type guard to check if t.JsonValue is an async httpx client.

        Returns:
            The resulting ``TypeIs[p.Observability.HttpClient.HTTPXAsyncClient]``.
        """
        # Runtime check goes through the owning protocol surface, which
        # declares both ``request`` and ``_send``; no private-name probing.
        return isinstance(obj, p.Observability.HttpClient.HTTPXAsyncClient)

    @staticmethod
    def _matches_httpx_client(
        obj: t.RegisterableService
        | p.Observability.HttpClient.HTTPXAsyncClient
        | p.Observability.HttpClient.HTTPXClient,
    ) -> TypeIs[p.Observability.HttpClient.HTTPXClient]:
        """Type guard to check if t.JsonValue is an httpx client.

        Returns:
            The resulting ``TypeIs[p.Observability.HttpClient.HTTPXClient]``.
        """
        # Sync httpx clients structurally satisfy the async protocol too, so
        # exclude the async surface explicitly; checks stay on the declared
        # protocol, never on private-name probing.
        return not isinstance(
            obj,
            p.Observability.HttpClient.HTTPXAsyncClient,
        ) and isinstance(obj, p.Observability.HttpClient.HTTPXClient)

    @staticmethod
    def _matches_aiohttp_session(
        obj: t.RegisterableService | p.Observability.HttpClient.AIOHTTPSession,
    ) -> TypeIs[p.Observability.HttpClient.AIOHTTPSession]:
        missing = object()
        return getattr(obj, "request", missing) is not missing

    @staticmethod
    def _validated_headers(
        payload: t.Scalar | t.JsonValue | None,
    ) -> t.MutableStrMapping:
        if payload is None:
            return {}
        return dict(
            m.Observability.HeadersPayload.model_validate(
                obj={"headers": payload},
            ).headers,
        )

    class HTTPX:
        """httpx client instrumentation for automatic request tracing."""

        instrumented_clients: ClassVar[set[int]] = set()

        @staticmethod
        def context_headers(kwargs: t.ConfigurationMapping) -> t.ConfigurationMapping:
            """Build request headers with the current correlation/trace ids.

            Returns:
                The resulting ``t.ConfigurationMapping``.

            """
            headers = FlextObservabilityHTTPClient._validated_headers(
                kwargs.get("headers"),
            )
            correlation_id = FlextObservabilityContext.correlation_id()
            trace_id = FlextObservabilityContext.trace_id()
            span_id = FlextObservabilityContext.span_id()
            if correlation_id:
                headers["X-Correlation-ID"] = correlation_id
            if trace_id:
                headers["X-Trace-ID"] = trace_id
            if span_id:
                headers["X-Span-ID"] = span_id
            return headers

        @staticmethod
        def http_log_extra(
            method: str,
            url: str,
            *,
            is_async: bool,
            **extra: t.Scalar,
        ) -> t.ConfigurationMapping:
            """Build the shared httpx log payload for one request event.

            Returns:
                The resulting ``t.ConfigurationMapping``.

            """
            return {
                "http_method": method,
                "http_url": url,
                "client": "httpx",
                "async": is_async,
                **extra,
            }

        @classmethod
        def log_http_request(
            cls,
            method: str,
            url: str,
            *,
            is_async: bool,
        ) -> None:
            """Log the outgoing httpx request at debug severity."""
            _ = FlextObservabilityLogging.log_with_context(
                FlextObservabilityHTTPClient.logger,
                c.Observability.ErrorSeverity.DEBUG.value,
                f"HTTP client request: {method} {url}",
                extra=cls.http_log_extra(method, url, is_async=is_async),
            )

        @classmethod
        def log_http_error(
            cls,
            method: str,
            url: str,
            *,
            is_async: bool,
            duration_ms: float,
            error: BaseException,
        ) -> None:
            """Log a failed httpx request at error severity."""
            _ = FlextObservabilityLogging.log_with_context(
                FlextObservabilityHTTPClient.logger,
                c.Observability.ErrorSeverity.ERROR.value,
                f"HTTP client error: {method} {url}",
                extra=cls.http_log_extra(
                    method,
                    url,
                    is_async=is_async,
                    http_duration_ms=duration_ms,
                    error_type=type(error).__name__,
                    error_message=str(error),
                ),
            )

        @classmethod
        def log_http_response(
            cls,
            method: str,
            url: str,
            *,
            is_async: bool,
            duration_ms: float,
            status_code: int,
        ) -> None:
            """Log a completed httpx response at debug severity."""
            _ = FlextObservabilityLogging.log_with_context(
                FlextObservabilityHTTPClient.logger,
                c.Observability.ErrorSeverity.DEBUG.value,
                f"HTTP client response: {method} {url} -> {status_code}",
                extra=cls.http_log_extra(
                    method,
                    url,
                    is_async=is_async,
                    http_duration_ms=duration_ms,
                    http_status=status_code,
                ),
            )

        @staticmethod
        def instrument_httpx_async(
            typed_async_client: p.Observability.HttpClient.HTTPXAsyncClient,
        ) -> None:
            """Wrap the async client request method with tracing."""
            original_request = typed_async_client.request

            async def traced_async_request(
                method: str,
                url: str,
                *args: t.Scalar,
                **kwargs: t.Scalar,
            ) -> p.Observability.HttpClient.HTTPXResponse:
                """Trace one async httpx request with context propagation.

                Returns:
                    The resulting ``p.Observability.HttpClient.HTTPXResponse``.

                Raises:
                    TypeError: If the async request returned a non-awaitable.
                    EXC_MAPPING_TYPE: If a ``c.EXC_MAPPING_TYPE`` is caught.
                """
                helpers = FlextObservabilityHTTPClient.HTTPX
                start_time = time.time()
                headers = helpers.context_headers(kwargs)
                helpers.log_http_request(method, url, is_async=True)
                call_kwargs: t.ConfigurationMapping = {
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
                        msg = "Async httpx request returned a non-awaitable response"
                        raise TypeError(msg)
                    response = await response_candidate
                except c.EXC_MAPPING_TYPE as e:
                    helpers.log_http_error(
                        method,
                        url,
                        is_async=True,
                        duration_ms=(time.time() - start_time) * 1000,
                        error=e,
                    )
                    raise
                helpers.log_http_response(
                    method,
                    url,
                    is_async=True,
                    duration_ms=(time.time() - start_time) * 1000,
                    status_code=response.status_code,
                )
                return response

            _bind_traced_request(typed_async_client, traced_async_request)

        @staticmethod
        def instrument_httpx_sync(
            typed_sync_client: p.Observability.HttpClient.HTTPXClient,
        ) -> None:
            """Wrap the sync client request method with tracing."""
            original_sync_request: Callable[
                ...,
                p.Observability.HttpClient.HTTPXResponse
                | Awaitable[p.Observability.HttpClient.HTTPXResponse],
            ] = typed_sync_client.request

            def traced_request(
                method: str,
                url: str,
                *args: t.Scalar,
                **kwargs: t.Scalar,
            ) -> p.Observability.HttpClient.HTTPXResponse:
                """Traced request wrapper for sync httpx.

                Returns:
                    The resulting ``p.Observability.HttpClient.HTTPXResponse``.

                Raises:
                    TypeError: If Sync httpx request returned an awaitable response.
                    EXC_MAPPING_TYPE: If a ``c.EXC_MAPPING_TYPE`` is caught.
                """
                helpers = FlextObservabilityHTTPClient.HTTPX
                start_time = time.time()
                headers = helpers.context_headers(kwargs)
                helpers.log_http_request(method, url, is_async=False)
                call_kwargs: t.ConfigurationMapping = {
                    k: v for k, v in kwargs.items() if k != "headers"
                }
                try:
                    response_candidate = original_sync_request(
                        method,
                        url,
                        *args,
                        headers=headers,
                        **call_kwargs,
                    )
                    if isinstance(response_candidate, Awaitable):
                        msg = "Sync httpx request returned an awaitable response"
                        raise TypeError(msg)
                    response = response_candidate
                except c.EXC_MAPPING_TYPE as e:
                    helpers.log_http_error(
                        method,
                        url,
                        is_async=False,
                        duration_ms=(time.time() - start_time) * 1000,
                        error=e,
                    )
                    raise
                helpers.log_http_response(
                    method,
                    url,
                    is_async=False,
                    duration_ms=(time.time() - start_time) * 1000,
                    status_code=response.status_code,
                )
                return response

            _bind_traced_request(typed_sync_client, traced_request)

        @staticmethod
        def _apply_httpx_instrumentation(
            client: t.RegisterableService
            | p.Observability.HttpClient.HTTPXAsyncClient
            | p.Observability.HttpClient.HTTPXClient,
        ) -> p.Result[bool]:
            """Apply httpx instrumentation to a validated client.

            Why the wider parameter type: with only `t.RegisterableService` (a
            DI-service union structurally disjoint from the httpx client
            protocols), mypy proves the TypeIs guards below can never succeed
            and marks everything past them unreachable — correct for the
            narrower static type, but wrong for the real httpx client objects
            this is called with.

            Args:
                client: httpx.Client or httpx.AsyncClient instance

            Returns:
                r[bool] - Ok if setup successful

            """
            client_id = id(client)
            if client_id in FlextObservabilityHTTPClient.HTTPX.instrumented_clients:
                return r[bool].ok(value=True)
            if FlextObservabilityHTTPClient._matches_httpx_async_client(client):
                typed_async_client: p.Observability.HttpClient.HTTPXAsyncClient = client
                FlextObservabilityHTTPClient.HTTPX.instrument_httpx_async(
                    typed_async_client,
                )
            elif FlextObservabilityHTTPClient._matches_httpx_client(client):
                typed_sync_client: p.Observability.HttpClient.HTTPXClient = client
                FlextObservabilityHTTPClient.HTTPX.instrument_httpx_sync(
                    typed_sync_client,
                )
            else:
                return r[bool].fail("Invalid httpx client - unsupported client type")
            FlextObservabilityHTTPClient.HTTPX.instrumented_clients.add(client_id)
            FlextObservabilityHTTPClient.logger.debug(
                "httpx client instrumentation setup complete",
            )
            return r[bool].ok(value=True)

        @classmethod
        def setup_instrumentation(cls, client: t.RegisterableService) -> p.Result[bool]:
            """Set up httpx client request instrumentation.

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
                return cls._apply_httpx_instrumentation(client)
            except c.EXC_MAPPING_TYPE as e:
                return r[bool].fail_op("httpx instrumentation setup", e)

    class AIOHTTP:
        """aiohttp client instrumentation for automatic request tracing."""

        instrumented_sessions: ClassVar[
            set[p.Observability.HttpClient.AIOHTTPSession]
        ] = set()

        @classmethod
        def setup_instrumentation(
            cls,
            session: t.RegisterableService,
        ) -> p.Result[bool]:
            """Set up aiohttp client session instrumentation.

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
                return cls._apply_aiohttp_instrumentation(session)
            except c.EXC_MAPPING_TYPE as e:
                return r[bool].fail_op("aiohttp instrumentation setup", e)

        @staticmethod
        def _apply_aiohttp_instrumentation(
            session: t.RegisterableService | p.Observability.HttpClient.AIOHTTPSession,
        ) -> p.Result[bool]:
            """Apply aiohttp instrumentation to a validated session.

            Why the wider parameter type: see
            ``HTTPX._apply_httpx_instrumentation`` for the full rationale.

            Args:
                session: aiohttp.ClientSession instance

            Returns:
                r[bool] - Ok if setup successful

            """
            if not FlextObservabilityHTTPClient._matches_aiohttp_session(session):
                return r[bool].fail("Invalid aiohttp session - missing request method")
            typed_session: p.Observability.HttpClient.AIOHTTPSession = session
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
            ) -> p.Observability.HttpClient.AIOHTTPResponse:
                """Traced request wrapper for aiohttp.

                Returns:
                    The resulting ``p.Observability.HttpClient.AIOHTTPResponse``.

                Raises:
                    EXC_MAPPING_TYPE: If a ``c.EXC_MAPPING_TYPE`` is caught.
                """
                start_time = time.time()
                correlation_id = FlextObservabilityContext.correlation_id()
                trace_id = FlextObservabilityContext.trace_id()
                span_id = FlextObservabilityContext.span_id()
                headers = FlextObservabilityHTTPClient._validated_headers(
                    kwargs.get("headers"),
                )
                if correlation_id:
                    headers["X-Correlation-ID"] = correlation_id
                if trace_id:
                    headers["X-Trace-ID"] = trace_id
                if span_id:
                    headers["X-Span-ID"] = span_id
                _ = FlextObservabilityLogging.log_with_context(
                    FlextObservabilityHTTPClient.logger,
                    c.Observability.ErrorSeverity.DEBUG.value,
                    f"HTTP client request: {method} {url}",
                    extra={
                        "http_method": method,
                        "http_url": url,
                        "client": "aiohttp",
                        "async": True,
                    },
                )
                async_call_kwargs: t.ConfigurationMapping = {
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
                except c.EXC_MAPPING_TYPE as e:
                    duration_ms = (time.time() - start_time) * 1000
                    _ = FlextObservabilityLogging.log_with_context(
                        FlextObservabilityHTTPClient.logger,
                        c.Observability.ErrorSeverity.ERROR.value,
                        f"HTTP client error: {method} {url}",
                        extra={
                            "http_method": method,
                            "http_url": url,
                            "http_duration_ms": duration_ms,
                            "error_type": type(e).__name__,
                            "error_message": str(e),
                            "client": "aiohttp",
                            "async": True,
                        },
                    )
                    raise
                duration_ms = (time.time() - start_time) * 1000
                status = response.status
                _ = FlextObservabilityLogging.log_with_context(
                    FlextObservabilityHTTPClient.logger,
                    c.Observability.ErrorSeverity.DEBUG.value,
                    f"HTTP client response: {method} {url} -> {status}",
                    extra={
                        "http_method": method,
                        "http_url": url,
                        "http_status": status,
                        "http_duration_ms": duration_ms,
                        "client": "aiohttp",
                        "async": True,
                    },
                )
                return response

            typed_session.request = traced_request
            FlextObservabilityHTTPClient.AIOHTTP.instrumented_sessions.add(
                typed_session,
            )
            FlextObservabilityHTTPClient.logger.debug(
                "aiohttp session instrumentation setup complete",
            )
            return r[bool].ok(value=True)


__all__: list[str] = ["FlextObservabilityHTTPClient"]
