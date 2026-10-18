"""Real Core emission, native destinations and injected Observability capture.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import asyncio

import pytest

from flext_observability import FlextObservability, c, m, p, u
from tests import t, tm
from tests.fixtures.logging import TestsObservabilityLoggingFixtures


@pytest.mark.usefixtures("test_runtime")
class TestsObservabilityLogging(TestsObservabilityLoggingFixtures):
    """Exercise the public composition with actual handlers and consumers."""

    def test_two_destinations_capture_once_and_remove_idempotently(
        self,
        logging_runtime: p.StructlogOptions,
        logging_streams: t.LoggingStreams,
    ) -> None:
        """Existing cached loggers observe live context and tuple replacement."""
        stage = FlextObservability.ContextStage()
        capture = self.Capture()
        unrelated = self.Capture()
        errors = u.Observability.ErrorObserver(FlextObservability.Handler())

        def application_stage(
            logger: p.OutputLogger,
            method_name: str,
            event: t.LoggingEvent,
        ) -> t.LoggingEvent:
            _ = logger, method_name
            event["application_event"] = event["event"]
            return event

        base = m.StructlogOptions.model_validate(
            logging_runtime,
            from_attributes=True,
        ).model_copy(
            update={
                "observers": (unrelated,),
                "processing_stages": (application_stage,),
            },
        )
        logger = u.fetch_logger("observability.cached")
        tm.ok(logger.info("warm cached logger"))
        selected = FlextObservability.compose_logging(
            base, context_stage=stage, capture=capture, errors=errors
        )
        selected = FlextObservability.compose_logging(
            selected, context_stage=stage, capture=capture, errors=errors
        )
        u.configure_structlog(settings=selected)
        for correlation in ("first-operation", "second-operation"):
            FlextObservability.update_correlation_id(correlation)
            FlextObservability.update_trace_id(f"trace-{correlation}")
            FlextObservability.update_span_id(f"span-{correlation}")
            tm.ok(logger.warning(correlation))
        tm.that(len(capture.records), eq=2)
        tm.that(
            [record.context["correlation_id"] for record in capture.records],
            eq=["first-operation", "second-operation"],
        )
        structured, console = logging_streams
        for record in capture.records:
            tm.that(structured.getvalue(), has=record.message)
            tm.that(console.getvalue(), has=record.message)
            tm.that(record.context["trace_id"], eq=f"trace-{record.message}")
            tm.that(record.context["span_id"], eq=f"span-{record.message}")
            tm.that(record.context["application_event"], eq=record.message)
        disabled = FlextObservability.compose_logging(
            selected, context_stage=stage, capture=capture, errors=errors, enabled=False
        )
        disabled = FlextObservability.compose_logging(
            disabled, context_stage=stage, capture=capture, errors=errors, enabled=False
        )
        u.configure_structlog(settings=disabled)
        tm.ok(logger.warning("after removal"))
        tm.that(len(capture.records), eq=2)
        tm.that(len(unrelated.records), eq=3)
        tm.that(unrelated.records[-1].message, eq="after removal")
        tm.that(
            unrelated.records[-1].context["application_event"],
            eq="after removal",
        )
        tm.that(disabled.processing_stages[0] is application_stage, eq=True)
        tm.that(disabled.handlers is base.handlers, eq=True)
        tm.that(disabled.cache_logger_on_first_use, eq=base.cache_logger_on_first_use)
        tm.that(disabled.async_logging, eq=base.async_logging)

    def test_enrichment_does_not_create_missing_context(
        self, logging_runtime: p.StructlogOptions
    ) -> None:
        """A missing operation context stays absent rather than becoming IDs."""
        capture = self.Capture()
        options = FlextObservability.compose_logging(
            logging_runtime,
            context_stage=FlextObservability.ContextStage(),
            capture=capture,
            errors=u.Observability.ErrorObserver(FlextObservability.Handler()),
        )
        u.configure_structlog(settings=options)
        FlextObservability.clear_correlation_id()
        FlextObservability.clear_trace_id()
        FlextObservability.clear_span_id()
        tm.ok(u.log("without correlation"))
        for key in ("correlation_id", "trace_id", "span_id"):
            tm.that(key in capture.records[-1].context, eq=False)
        tm.that(FlextObservability.correlation_id(), eq="")
        tm.that(FlextObservability.trace_id(), eq="")
        tm.that(FlextObservability.span_id(), eq="")

    def test_async_tasks_capture_their_own_live_context(
        self, logging_runtime: p.StructlogOptions
    ) -> None:
        """Task interleaving never borrows another task's correlation/span."""
        capture = self.Capture()
        options = FlextObservability.compose_logging(
            logging_runtime,
            context_stage=FlextObservability.ContextStage(),
            capture=capture,
            errors=u.Observability.ErrorObserver(FlextObservability.Handler()),
        )
        u.configure_structlog(settings=options)
        parent_context = FlextObservability.correlation_id()
        logger = u.fetch_logger("observability.async")

        async def exercise() -> None:
            first_ready = asyncio.Event()
            second_ready = asyncio.Event()

            async def emit(
                name: str, ready: t.LoggingBarrier, other: t.LoggingBarrier
            ) -> None:
                FlextObservability.update_correlation_id(name)
                FlextObservability.update_trace_id(f"trace-{name}")
                FlextObservability.update_span_id(f"span-{name}")
                ready.set()
                await other.wait()
                tm.ok(logger.warning(name, payload={"nested": [name, {"ok": True}]}))

            await asyncio.gather(
                emit("first", first_ready, second_ready),
                emit("second", second_ready, first_ready),
            )

        asyncio.run(exercise())
        tm.that(len(capture.records), eq=2)
        for record in capture.records:
            tm.that(record.context["correlation_id"], eq=record.message)
            tm.that(record.context["trace_id"], eq=f"trace-{record.message}")
            tm.that(record.context["span_id"], eq=f"span-{record.message}")
            tm.that(
                record.context["payload"],
                eq={"nested": [record.message, {"ok": True}]},
            )
        tm.that(FlextObservability.correlation_id(), eq=parent_context)

    def test_original_exception_is_local_and_capture_is_sanitized(
        self, logging_runtime: p.StructlogOptions
    ) -> None:
        """Typed capture retains the causal reference but serialization excludes it."""
        capture = self.Capture()
        handler = FlextObservability.Handler()
        errors = u.Observability.ErrorObserver(handler)
        secret = "private-capture-value"
        base = m.StructlogOptions.model_validate(
            logging_runtime,
            from_attributes=True,
        ).model_copy(update={"redacted_values": (secret,)})
        options = FlextObservability.compose_logging(
            base,
            context_stage=FlextObservability.ContextStage(),
            capture=capture,
            errors=errors,
        )
        u.configure_structlog(settings=options)
        FlextObservability.update_correlation_id("captured-operation")
        original = OSError(f"storage rejected {secret}")
        tm.ok(
            u.failure("storage failure", exception=original, payload={"values": [1, 2]})
        )
        record = capture.records[-1]
        tm.that(record.exception is original, eq=True)
        tm.that(record.context["correlation_id"], eq="captured-operation")
        tm.that(record.context["payload"], eq={"values": [1, 2]})
        tm.that(capture.stream.getvalue(), lacks=secret)
        serialized = m.LoggingRecord.model_validate(
            record, from_attributes=True
        ).model_dump()
        tm.that("exception" in serialized, eq=False)
        error = m.Observability.ErrorEvent(
            error_type=type(original).__name__,
            message=u.str_adapter().validate_python(
                record.context["exception_message"]
            ),
            severity=c.Observability.ErrorSeverity(record.level),
            correlation_id="captured-operation",
        ).calculate_fingerprint()
        tm.that(handler.resolve_error_count(error.fingerprint), eq=1)
        before = handler.resolve_error_count(error.fingerprint)
        tm.ok(u.log("plain ERROR is not an exception", level=c.LogLevel.ERROR))
        tm.that(handler.resolve_error_count(error.fingerprint), eq=before)

    @pytest.mark.parametrize("correlation", ["", "captured-operation"])
    def test_error_handler_preserves_explicit_snapshot_after_context_changes(
        self,
        logging_runtime: p.StructlogOptions,
        correlation: str,
    ) -> None:
        """Absent captured context is explicit and never replaced at consumption."""
        _ = logging_runtime
        handler = FlextObservability.Handler()
        FlextObservability.update_correlation_id("later-operation")
        event = m.Observability.ErrorEvent(
            error_type="OSError",
            message="captured error",
            correlation_id=correlation,
        )
        recorded = tm.ok(handler.record_error(event))
        tm.that(recorded.correlation_id, eq=event.correlation_id)

    @pytest.mark.parametrize("business_failure", [False, True])
    def test_capture_write_failure_is_not_swallowed(
        self, logging_runtime: p.StructlogOptions, *, business_failure: bool
    ) -> None:
        """Native capture failure stays visible without replacing a causal error."""
        capture = self.Capture()
        options = FlextObservability.compose_logging(
            logging_runtime,
            context_stage=FlextObservability.ContextStage(),
            capture=capture,
            errors=u.Observability.ErrorObserver(FlextObservability.Handler()),
        )
        u.configure_structlog(settings=options)
        capture.stream.close()
        original = OSError("business operation failed")
        if business_failure:
            with pytest.raises(OSError) as business_caught:
                u.failure("failed operation", exception=original)
            tm.that(business_caught.value is original, eq=True)
            tm.that(original.__context__ is capture.failure, eq=True)
        else:
            with pytest.raises(ValueError) as capture_caught:
                u.warning("selected capture is closed")
            tm.that(capture_caught.value is capture.failure, eq=True)
        tm.that(capture.failure, none=False)
        tm.that(capture.records, eq=[])

    def test_http_logging_preserves_original_exception_and_core_result(
        self, logging_runtime: p.StructlogOptions
    ) -> None:
        """The actual HTTP logging consumer uses the same installed providers."""
        capture = self.Capture()
        options = FlextObservability.compose_logging(
            logging_runtime,
            context_stage=FlextObservability.ContextStage(),
            capture=capture,
            errors=u.Observability.ErrorObserver(FlextObservability.Handler()),
        )
        u.configure_structlog(settings=options)
        original = OSError("HTTP transport failed")
        result = FlextObservability.HTTPX.log_http_error(
            "GET",
            "https://service.invalid/resource",
            is_async=False,
            duration_ms=3.5,
            error=original,
        )
        tm.ok(result)
        tm.that(capture.records[-1].exception is original, eq=True)
        tm.that(capture.records[-1].context["http_method"], eq="GET")
