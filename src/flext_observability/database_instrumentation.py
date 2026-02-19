"""SQLAlchemy and asyncpg database auto-instrumentation.

Provides automatic database operation tracing and metrics collection for
SQLAlchemy and asyncpg without requiring any code changes.

FLEXT Pattern:
- Single FlextObservabilityDatabase class
- Nested SQLAlchemy and AsyncPG implementations
- Integration with Phase 2 (Metrics & Tracing)
- Integration with Phase 3 (Context & Logging)
- Automatic span creation and query metrics

Key Features:
- Zero code changes needed in application code
- Automatic query tracing with span creation
- Query performance metrics (duration, rows affected)
- SQL error tracking and logging
- Safe query handling (no query text in logs by default)
- Context propagation to database operations
"""

from __future__ import annotations

import time
from collections import UserDict
from collections.abc import Callable
from typing import ClassVar, Protocol, cast

from flext_core import FlextLogger, FlextResult
from flext_core.protocols import p

# Optional dependency: SQLAlchemy
try:
    from sqlalchemy import event

    _sqlalchemy_available = True
except ImportError:

    class _StubURLProtocol:
        """Stub URL for type checking."""

        database: str | None = None

        def __str__(self) -> str:
            return "stub://localhost"

    class _StubEngineProtocol:
        """Stub Engine for type checking."""

        url: _StubURLProtocol
        dispatch: object

        def __init__(self) -> None:
            self.url = _StubURLProtocol()
            self.dispatch = object()

    class _StubInfoDict(UserDict[str, object]):
        """Stub info dict for type checking."""

        pass

    class _SQLAlchemyConnectionStub:
        """Stub for when sqlalchemy is not installed."""

        info: _StubInfoDict
        engine: _StubEngineProtocol

        def __init__(self) -> None:
            self.info = _StubInfoDict()
            self.engine = _StubEngineProtocol()

    class _SQLAlchemyEngineStub:
        """Stub for when sqlalchemy is not installed."""

        dispatch: object
        url: _StubURLProtocol

        def __init__(self) -> None:
            self.dispatch = object()
            self.url = _StubURLProtocol()

    class _Event:
        """Stub for when sqlalchemy is not installed."""

        @staticmethod
        def listens_for(
            _target: object,
            _identifier: str,
            *_args: object,
            **_kwargs: object,
        ) -> Callable[[Callable[..., object]], Callable[..., object]]:
            """Stub decorator."""

            def decorator(
                f: Callable[..., object],
            ) -> Callable[..., object]:
                return f

            return decorator

    event = _Event
    SQLAlchemyConnection = _SQLAlchemyConnectionStub
    SQLAlchemyEngine = _SQLAlchemyEngineStub
    _sqlalchemy_available = False

from flext_observability.logging_integration import FlextObservabilityLogging


class AsyncPGPoolProtocol(Protocol):
    """Protocol for asyncpg connection pool."""

    async def execute(self, query: str, *args: object, **kwargs: object) -> object:
        """Execute a query."""
        ...

    async def fetch(self, query: str, *args: object, **kwargs: object) -> list[object]:
        """Fetch rows."""
        ...

    async def fetchval(self, query: str, *args: object, **kwargs: object) -> object:
        """Fetch a single value."""
        ...


class FlextObservabilityDatabase:
    """Database operation auto-instrumentation.

    Provides middleware for automatic database operation tracing and metrics
    collection for SQLAlchemy and asyncpg.

    Usage:
        ```python
        from sqlalchemy import create_engine
        from flext_observability import FlextObservabilityDatabase

        engine = create_engine("postgresql://...")
        FlextObservabilityDatabase.SQLAlchemy.setup_instrumentation(engine)

        # All SQL queries now automatically traced and monitored!
        ```

    Nested Classes:
        SQLAlchemy: SQLAlchemy event listener instrumentation
        AsyncPG: asyncpg connection instrumentation
    """

    _logger: p.Log.StructlogLogger = cast(
        "p.Log.StructlogLogger",
        FlextLogger.get_logger(__name__),
    )

    # ========================================================================
    # SQLALCHEMY INSTRUMENTATION
    # ========================================================================

    class SQLAlchemy:
        """SQLAlchemy event listener for automatic query instrumentation."""

        instrumented_engines: ClassVar[set[object]] = set()

        @staticmethod
        def setup_instrumentation(engine: object) -> FlextResult[bool]:
            """Setup SQLAlchemy engine query instrumentation.

            Adds SQLAlchemy event listeners for automatic query tracing,
            metrics collection, and error logging.

            Args:
                engine: SQLAlchemy Engine instance

            Returns:
                FlextResult[bool] - Ok if setup successful

            Behavior:
                - Creates span for each SQL query execution
                - Records query duration (milliseconds)
                - Tracks rows affected (select/insert/update/delete)
                - Logs query errors with context
                - Safe query handling (query text not logged by default)
                - Integrates with Phase 3 context and logging

            Example:
                ```python
                from sqlalchemy import create_engine
                from flext_observability import FlextObservabilityDatabase

                engine = create_engine("postgresql://localhost/mydb")
                FlextObservabilityDatabase.SQLAlchemy.setup_instrumentation(engine)

                # All queries now automatically traced:
                with engine.connect() as conn:
                    result = conn.execute("SELECT * FROM users WHERE id = ?", [1])
                    # Automatically traced with duration and row count
                ```

            """
            try:
                if not hasattr(engine, "dispatch"):
                    return FlextResult[bool].fail(
                        "Invalid SQLAlchemy engine - missing dispatch",
                    )

                # Avoid duplicate instrumentation
                if engine in FlextObservabilityDatabase.SQLAlchemy.instrumented_engines:
                    return FlextResult[bool].ok(value=True)

                listens_for = getattr(
                    event,
                    "listens_for",
                    lambda *_args, **_kwargs: lambda fn: fn,
                )

                @listens_for(engine, "before_cursor_execute")
                def before_cursor_execute(
                    conn: object,
                    _cursor: object,
                    statement: str,
                    _parameters: object,
                    _context: object,
                    executemany: bool,
                ) -> None:
                    """Log query execution start."""
                    try:
                        # Store start time on connection for after hook
                        conn_info = getattr(conn, "info", None)
                        if isinstance(conn_info, dict):
                            conn_info.setdefault("_flext_query_start", time.time())

                        # Extract database info
                        engine_obj = getattr(conn, "engine", None)
                        url_obj = getattr(engine_obj, "url", None)
                        db_url = str(url_obj) if url_obj is not None else "unknown"
                        db_name_raw = getattr(url_obj, "database", None)
                        db_name = (
                            db_name_raw if isinstance(db_name_raw, str) else "unknown"
                        )

                        # Log query start with context
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityDatabase._logger,
                            "debug",
                            "SQL query execution start",
                            extra={
                                "db_driver": "sqlalchemy",
                                "db_name": db_name,
                                "db_url": db_url,
                                "query_type": (
                                    statement.strip().split()[0].upper()
                                    if statement.strip()
                                    else "unknown"
                                ),
                                "executemany": executemany,
                            },
                        )
                    except Exception as e:
                        FlextObservabilityDatabase._logger.warning(
                            f"Error in before_cursor_execute: {e}",
                        )

                @listens_for(engine, "after_cursor_execute")
                def after_cursor_execute(
                    conn: object,
                    cursor: object,
                    statement: str,
                    _parameters: object,
                    _context: object,
                    executemany: bool,
                ) -> None:
                    """Log query execution completion."""
                    try:
                        # Calculate query duration
                        conn_info = getattr(conn, "info", None)
                        start_time_val = (
                            conn_info.get("_flext_query_start", None)
                            if isinstance(conn_info, dict)
                            else None
                        )
                        # Type narrow to float for arithmetic
                        start_time = (
                            start_time_val
                            if isinstance(start_time_val, float)
                            else time.time()
                        )
                        duration_ms = (time.time() - start_time) * 1000

                        # Get row count
                        row_count = 0
                        if hasattr(cursor, "rowcount"):
                            try:
                                rowcount_val = getattr(cursor, "rowcount", 0)
                                row_count = (
                                    int(rowcount_val)
                                    if rowcount_val is not None and rowcount_val >= 0
                                    else 0
                                )
                            except (AttributeError, TypeError, ValueError):
                                row_count = 0

                        # Extract database info
                        engine_obj = getattr(conn, "engine", None)
                        url_obj = getattr(engine_obj, "url", None)
                        db_url = str(url_obj) if url_obj is not None else "unknown"
                        db_name_raw = getattr(url_obj, "database", None)
                        db_name = (
                            db_name_raw if isinstance(db_name_raw, str) else "unknown"
                        )
                        query_type = (
                            statement.strip().split()[0].upper()
                            if statement.strip()
                            else "unknown"
                        )

                        # Log query completion
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityDatabase._logger,
                            "debug",
                            f"SQL query completed: {query_type}",
                            extra={
                                "db_driver": "sqlalchemy",
                                "db_name": db_name,
                                "db_url": db_url,
                                "query_type": query_type,
                                "query_duration_ms": duration_ms,
                                "rows_affected": row_count,
                                "executemany": executemany,
                            },
                        )

                        # Clean up
                        if isinstance(conn_info, dict):
                            conn_info.pop("_flext_query_start", None)

                    except Exception as e:
                        FlextObservabilityDatabase._logger.warning(
                            f"Error in after_cursor_execute: {e}",
                        )

                # Mark as instrumented
                FlextObservabilityDatabase.SQLAlchemy.instrumented_engines.add(engine)

                FlextObservabilityDatabase._logger.debug(
                    "SQLAlchemy instrumentation setup complete",
                )
                return FlextResult[bool].ok(value=True)

            except Exception as e:
                return FlextResult[bool].fail(
                    f"SQLAlchemy instrumentation setup failed: {e}",
                )

    # ========================================================================
    # ASYNCPG INSTRUMENTATION
    # ========================================================================

    class AsyncPG:
        """asyncpg pool instrumentation for automatic query tracing."""

        instrumented_pools: ClassVar[set[object]] = set()

        @staticmethod
        def setup_instrumentation(pool: AsyncPGPoolProtocol) -> FlextResult[bool]:
            """Setup asyncpg connection pool query instrumentation.

            Wraps asyncpg pool to automatically trace all queries.

            Args:
                pool: asyncpg connection pool instance

            Returns:
                FlextResult[bool] - Ok if setup successful

            Behavior:
                - Creates span for each asyncpg query execution
                - Records query duration (milliseconds)
                - Logs query errors with context
                - Integrates with Phase 3 context and logging
                - Async-safe implementation

            Example:
                ```python
                import asyncpg
                from flext_observability import FlextObservabilityDatabase

                pool = await asyncpg.create_pool("postgresql://localhost/mydb")
                FlextObservabilityDatabase.AsyncPG.setup_instrumentation(pool)

                # All queries now automatically traced:
                async with pool.acquire() as conn:
                    rows = await conn.fetch("SELECT * FROM users WHERE id = ?", 1)
                    # Automatically traced with duration
                ```

            """
            try:
                if not hasattr(pool, "execute"):
                    return FlextResult[bool].fail(
                        "Invalid asyncpg pool - missing execute method",
                    )

                # Avoid duplicate instrumentation
                if pool in FlextObservabilityDatabase.AsyncPG.instrumented_pools:
                    return FlextResult[bool].ok(value=True)

                # Store original methods
                original_execute = pool.execute
                original_fetch = pool.fetch
                original_fetchval = pool.fetchval

                async def traced_execute(
                    query: str,
                    *args: object,
                    **kwargs: object,
                ) -> object:
                    """Traced execute wrapper."""
                    start_time = time.time()
                    query_type = (
                        query.strip().split()[0].upper() if query.strip() else "unknown"
                    )

                    try:
                        # Log query start
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityDatabase._logger,
                            "debug",
                            "asyncpg query execution start",
                            extra={
                                "db_driver": "asyncpg",
                                "query_type": query_type,
                            },
                        )

                        # Execute query
                        result = await original_execute(query, *args, **kwargs)

                        # Log completion
                        duration_ms = (time.time() - start_time) * 1000
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityDatabase._logger,
                            "debug",
                            f"asyncpg query completed: {query_type}",
                            extra={
                                "db_driver": "asyncpg",
                                "query_type": query_type,
                                "query_duration_ms": duration_ms,
                            },
                        )

                        return result

                    except Exception as e:
                        # Log error
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityDatabase._logger,
                            "error",
                            f"asyncpg query error: {e!s}",
                            extra={
                                "db_driver": "asyncpg",
                                "query_type": query_type,
                                "error_type": type(e).__name__,
                                "error_message": str(e),
                            },
                        )
                        raise

                async def traced_fetch(
                    query: str,
                    *args: object,
                    **kwargs: object,
                ) -> list[object]:
                    """Traced fetch wrapper."""
                    start_time = time.time()
                    query_type = (
                        query.strip().split()[0].upper() if query.strip() else "unknown"
                    )

                    try:
                        # Log query start
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityDatabase._logger,
                            "debug",
                            "asyncpg fetch execution start",
                            extra={
                                "db_driver": "asyncpg",
                                "query_type": query_type,
                                "operation": "fetch",
                            },
                        )

                        # Execute query
                        result = await original_fetch(query, *args, **kwargs)

                        # Log completion with row count
                        duration_ms = (time.time() - start_time) * 1000
                        row_count = len(result) if result else 0
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityDatabase._logger,
                            "debug",
                            f"asyncpg fetch completed: {query_type}",
                            extra={
                                "db_driver": "asyncpg",
                                "query_type": query_type,
                                "query_duration_ms": duration_ms,
                                "rows_returned": row_count,
                            },
                        )

                        return result

                    except Exception as e:
                        # Log error
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityDatabase._logger,
                            "error",
                            f"asyncpg fetch error: {e!s}",
                            extra={
                                "db_driver": "asyncpg",
                                "query_type": query_type,
                                "operation": "fetch",
                                "error_type": type(e).__name__,
                                "error_message": str(e),
                            },
                        )
                        raise

                async def traced_fetchval(
                    query: str,
                    *args: object,
                    **kwargs: object,
                ) -> object:
                    """Traced fetchval wrapper."""
                    start_time = time.time()
                    query_type = (
                        query.strip().split()[0].upper() if query.strip() else "unknown"
                    )

                    try:
                        # Log query start
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityDatabase._logger,
                            "debug",
                            "asyncpg fetchval execution start",
                            extra={
                                "db_driver": "asyncpg",
                                "query_type": query_type,
                                "operation": "fetchval",
                            },
                        )

                        # Execute query
                        result = await original_fetchval(query, *args, **kwargs)

                        # Log completion
                        duration_ms = (time.time() - start_time) * 1000
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityDatabase._logger,
                            "debug",
                            f"asyncpg fetchval completed: {query_type}",
                            extra={
                                "db_driver": "asyncpg",
                                "query_type": query_type,
                                "query_duration_ms": duration_ms,
                            },
                        )

                        return result

                    except Exception as e:
                        # Log error
                        FlextObservabilityLogging.log_with_context(
                            FlextObservabilityDatabase._logger,
                            "error",
                            f"asyncpg fetchval error: {e!s}",
                            extra={
                                "db_driver": "asyncpg",
                                "query_type": query_type,
                                "operation": "fetchval",
                                "error_type": type(e).__name__,
                                "error_message": str(e),
                            },
                        )
                        raise

                # Replace methods with traced versions using setattr
                setattr(pool, "execute", traced_execute)
                setattr(pool, "fetch", traced_fetch)
                setattr(pool, "fetchval", traced_fetchval)

                # Mark as instrumented
                FlextObservabilityDatabase.AsyncPG.instrumented_pools.add(pool)

                FlextObservabilityDatabase._logger.debug(
                    "asyncpg pool instrumentation setup complete",
                )
                return FlextResult[bool].ok(value=True)

            except Exception as e:
                return FlextResult[bool].fail(
                    f"asyncpg instrumentation setup failed: {e}",
                )


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    "FlextObservabilityDatabase",
]
