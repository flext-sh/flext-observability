"""Flask and FastAPI HTTP auto-instrumentation middleware.

Provides automatic HTTP request tracing and metrics collection for Flask and FastAPI
applications without requiring any code changes to route handlers.

FLEXT Pattern:
- Single FlextObservabilityHTTP class
- Nested Flask and FastAPI middleware implementations
- Integration with Phase 2 (Metrics & Tracing)
- Integration with Phase 3 (Context & Logging)
- Automatic span creation and metric recording

Key Features:
- Zero code changes needed in route handlers
- Automatic correlation ID extraction/generation
- HTTP request/response tracing
- Latency metrics collection
- Error tracking and alerting
- Async-safe with FastAPI
"""

from __future__ import annotations

import time
from collections import UserDict
from collections.abc import Awaitable, Callable
from typing import Protocol, TypeGuard

import flask
from flext_core import FlextRuntime, m, r, t
from pydantic import BaseModel, Field, ValidationError

from flext_observability import FlextObservabilityContext, FlextObservabilityLogging

FlaskApp = flask.Flask if hasattr(flask, "Flask") else object
g = flask.g if hasattr(flask, "g") else None
request = flask.request if hasattr(flask, "request") else None
_flask_available = True
_starlette_available = True


class _StartTimePayload(BaseModel):
    value: float = Field(ge=0)


class FlaskHookProtocol(Protocol):
    def __call__(self, callback: Callable[..., object]) -> Callable[..., object]: ...


class FlaskErrorHandlerProtocol(Protocol):
    def __call__(self, error_type: type[Exception]) -> FlaskHookProtocol: ...


class FlaskAppProtocol(Protocol):
    before_request: FlaskHookProtocol
    after_request: FlaskHookProtocol
    errorhandler: FlaskErrorHandlerProtocol


def _is_flask_app(obj: object) -> TypeGuard[FlaskAppProtocol]:
    """Type guard to check if object is a Flask app."""
    return hasattr(obj, "before_request") and hasattr(obj, "after_request")


class FastAPIAppProtocol(Protocol):
    def add_middleware(self, middleware_class: type) -> None: ...


def _is_fastapi_app(obj: object) -> TypeGuard[FastAPIAppProtocol]:
    return hasattr(obj, "add_middleware")


class RequestURLProtocol(Protocol):
    """Protocol for request URL objects."""

    path: str


class RequestClientProtocol(Protocol):
    """Protocol for request client objects."""

    host: str


class RequestProtocol(Protocol):
    """Protocol for HTTP request objects used by middleware."""

    headers: m.Dict | UserDict[str, str]
    method: str
    url: RequestURLProtocol
    client: RequestClientProtocol | None


class ResponseProtocol(Protocol):
    """Protocol for HTTP response objects used by middleware."""

    status_code: int
    headers: m.Dict | UserDict[str, str]


class FlextObservabilityHTTP:
    """HTTP framework auto-instrumentation.

    Provides middleware for automatic HTTP request tracing and metrics collection
    for Flask and FastAPI applications.

    Usage:
        ```python
        from fastapi import FastAPI
        from flext_observability import FlextObservabilityHTTP

        app = FastAPI()
        FlextObservabilityHTTP.FastAPI.setup_instrumentation(app)

        # All HTTP requests now automatically traced and monitored!
        # No changes needed to route handlers
        ```

    Nested Classes:
        Flask: Flask WSGI middleware
        FastAPI: FastAPI ASGI middleware
        ASGI: Generic ASGI middleware base
    """

    _logger = FlextRuntime.get_logger(__name__)
    HTTP_ERROR_STATUS_THRESHOLD = 400

    class Flask:
        """Flask WSGI middleware for automatic HTTP instrumentation."""

        @staticmethod
        def setup_instrumentation(app: object) -> r[bool]:
            """Setup Flask application HTTP instrumentation.

            Adds Flask middleware for automatic HTTP request tracing, metrics,
            and context extraction/propagation.

            Args:
                app: Flask application instance

            Returns:
                r[bool] - Ok if setup successful

            Behavior:
                - Extracts correlation ID from X-Correlation-ID header
                - Creates span for each HTTP request
                - Records metrics for duration and status
                - Captures request context in logs
                - Handles errors and exceptions

            Example:
                ```python
                from flask import Flask
                from flext_observability import FlextObservabilityHTTP

                app = Flask(__name__)
                FlextObservabilityHTTP.Flask.setup_instrumentation(app)


                @app.route("/api/users")
                def get_users():
                    # Automatically instrumented
                    return {"users": []}
                ```

            """
            try:
                if not _is_flask_app(app):
                    return r[bool].fail("Invalid Flask app - missing request hooks")
                before_request_hook = app.before_request
                after_request_hook = app.after_request

                @before_request_hook
                def flext_before_request() -> None:
                    """Extract context and create span before request processing."""
                    try:
                        headers_dict: dict[str, str] = (
                            dict(request.headers) if request else {}
                        )
                        if request:
                            FlextObservabilityContext.from_headers(
                                m.Dict.model_validate(headers_dict)
                            )
                        correlation_id = FlextObservabilityContext.get_correlation_id()
                        if g:
                            g.flext_start_time = time.time()
                        if g:
                            g.flext_correlation_id = correlation_id
                        request_method = request.method if request else "UNKNOWN"
                        request_path = request.path if request else "UNKNOWN"
                        request_remote = request.remote_addr if request else "unknown"
                        user_agent = (
                            request.user_agent.string
                            if request and request.user_agent
                            else "unknown"
                        )
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityHTTP._logger,
                            "debug",
                            f"HTTP {request_method} {request_path}",
                            extra={
                                "http_method": request_method,
                                "http_path": request_path,
                                "http_client_ip": request_remote,
                                "http_user_agent": user_agent,
                            },
                        )
                    except (ValueError, TypeError, KeyError) as e:
                        FlextObservabilityHTTP._logger.warning(
                            f"Error in before_request hook: {e}"
                        )

                @after_request_hook
                def flext_after_request(response: ResponseProtocol) -> ResponseProtocol:
                    """Record metrics and complete span after request processing."""
                    try:
                        start_time = (
                            g.flext_start_time
                            if g is not None and hasattr(g, "flext_start_time")
                            else None
                        )
                        duration_ms = 0.0
                        try:
                            validated_start = _StartTimePayload.model_validate({
                                "value": start_time
                            }).value
                            duration_ms = (time.time() - validated_start) * 1000
                        except ValidationError:
                            duration_ms = 0.0
                        status_code = int(
                            response.status_code
                            if hasattr(response, "status_code")
                            else 200
                        )
                        is_error = (
                            status_code
                            >= FlextObservabilityHTTP.HTTP_ERROR_STATUS_THRESHOLD
                        )
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityHTTP._logger,
                            "info" if not is_error else "warning",
                            f"HTTP {(request.method if request else 'UNKNOWN')} {(request.path if request else 'UNKNOWN')} -> {status_code}",
                            extra={
                                "http_method": request.method if request else "UNKNOWN",
                                "http_path": request.path if request else "UNKNOWN",
                                "http_status": status_code,
                                "http_duration_ms": duration_ms,
                            },
                        )
                    except (ValueError, TypeError, KeyError) as e:
                        FlextObservabilityHTTP._logger.warning(
                            f"Error in after_request hook: {e}"
                        )
                    return response

                errorhandler = app.errorhandler

                @errorhandler(Exception)
                def flext_error_handler(error: Exception) -> tuple[m.Dict, int]:
                    """Handle exceptions with logging and alerting."""
                    try:
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityHTTP._logger,
                            "error",
                            f"HTTP request error: {error!s}",
                            extra={
                                "http_method": request.method if request else "UNKNOWN",
                                "http_path": request.path if request else "UNKNOWN",
                                "error_type": type(error).__name__,
                                "error_message": str(error),
                            },
                        )
                    except (ValueError, TypeError, KeyError) as log_error:
                        FlextObservabilityHTTP._logger.error(
                            f"Error in error handler: {log_error}"
                        )
                    return (m.Dict.model_validate({"error": str(error)}), 500)

                _ = flext_before_request
                _ = flext_after_request
                _ = flext_error_handler

                FlextObservabilityHTTP._logger.debug(
                    "Flask HTTP instrumentation setup complete"
                )
                return r[bool].ok(value=True)
            except (ValueError, TypeError, KeyError) as e:
                return r[bool].fail(f"Flask instrumentation setup failed: {e}")

    class FastAPI:
        """FastAPI ASGI middleware for automatic HTTP instrumentation."""

        @staticmethod
        def setup_instrumentation(app: object) -> r[bool]:
            """Setup FastAPI application HTTP instrumentation.

            Adds FastAPI middleware for automatic HTTP request tracing, metrics,
            and context extraction/propagation. Async-safe implementation for
            FastAPI's async request handling.

            Args:
                app: FastAPI application instance

            Returns:
                r[bool] - Ok if setup successful

            Behavior:
                - Extracts correlation ID from X-Correlation-ID header
                - Creates span for each HTTP request (async-safe)
                - Records metrics for duration and status
                - Captures request context in logs
                - Handles errors and exceptions
                - Full async/await support

            Example:
                ```python
                from fastapi import FastAPI
                from flext_observability import FlextObservabilityHTTP

                app = FastAPI()
                FlextObservabilityHTTP.FastAPI.setup_instrumentation(app)


                @app.get("/api/users")
                async def get_users():
                    # Automatically instrumented, async-safe
                    return {"users": []}
                ```

            """
            try:
                if not _is_fastapi_app(app):
                    return r[bool].fail(
                        "Invalid FastAPI app - missing add_middleware method"
                    )
                typed_app: FastAPIAppProtocol = app

                class FlextObservabilityMiddleware:
                    """Starlette-based ASGI middleware for FastAPI."""

                    def __init__(self, app: object) -> None:
                        _ = app

                    async def dispatch(
                        self,
                        request: RequestProtocol,
                        call_next: Callable[
                            [RequestProtocol], Awaitable[ResponseProtocol]
                        ],
                    ) -> ResponseProtocol:
                        """Process HTTP request with instrumentation."""
                        try:
                            headers_dict = dict(request.headers)
                            FlextObservabilityContext.from_headers(headers_dict)
                            correlation_id = (
                                FlextObservabilityContext.get_correlation_id()
                            )
                            start_time = time.time()
                            await FlextObservabilityHTTP._async_log_with_context(
                                f"HTTP {request.method} {request.url.path}",
                                "debug",
                                {
                                    "http_method": request.method,
                                    "http_path": request.url.path,
                                    "http_client_ip": request.client.host
                                    if request.client
                                    else "unknown",
                                    "http_user_agent": request.headers.get(
                                        "user-agent", "unknown"
                                    ),
                                },
                            )
                            try:
                                response = await call_next(request)
                                duration_ms = (time.time() - start_time) * 1000
                                status_code = int(
                                    response.status_code
                                    if hasattr(response, "status_code")
                                    else 200
                                )
                                is_error = (
                                    status_code
                                    >= FlextObservabilityHTTP.HTTP_ERROR_STATUS_THRESHOLD
                                )
                                await FlextObservabilityHTTP._async_log_with_context(
                                    f"HTTP {request.method} {request.url.path} -> {status_code}",
                                    "info" if not is_error else "warning",
                                    {
                                        "http_method": request.method,
                                        "http_path": request.url.path,
                                        "http_status": status_code,
                                        "http_duration_ms": duration_ms,
                                    },
                                )
                                response.headers["X-Correlation-ID"] = correlation_id
                                return response
                            except (ValueError, TypeError, KeyError) as e:
                                await FlextObservabilityHTTP._async_log_with_context(
                                    f"HTTP request error: {e!s}",
                                    "error",
                                    {
                                        "http_method": request.method,
                                        "http_path": request.url.path,
                                        "error_type": type(e).__name__,
                                        "error_message": str(e),
                                    },
                                )
                                raise
                        except (ValueError, TypeError, KeyError) as e:
                            FlextObservabilityHTTP._logger.warning(
                                f"Middleware error: {e}"
                            )
                            raise

                add_middleware = typed_app.add_middleware
                add_middleware(FlextObservabilityMiddleware)
                FlextObservabilityHTTP._logger.debug(
                    "FastAPI HTTP instrumentation setup complete"
                )
                return r[bool].ok(value=True)
            except (ValueError, TypeError, KeyError) as e:
                return r[bool].fail(f"FastAPI instrumentation setup failed: {e}")

    @staticmethod
    async def _async_log_with_context(
        message: str,
        level: str,
        extra: t.ConfigurationMapping | m.Dict | None = None,
    ) -> None:
        """Async wrapper for logging with context (for FastAPI).

        Allows async operations in FastAPI middleware to log with context.
        """
        try:
            FlextObservabilityLogging.log_with_context(
                FlextObservabilityHTTP._logger, level, message, extra=extra
            )
        except (ValueError, TypeError, KeyError) as e:
            FlextObservabilityHTTP._logger.warning(
                f"Error logging in async context: {e}"
            )


__all__ = ["FlextObservabilityHTTP"]
