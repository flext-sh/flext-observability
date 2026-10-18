"""Real logging consumers and snapshot-restored runtime fixtures.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import io

import pytest

from flext_observability import FlextObservability
from tests import c, m, p, t, u


class TestsObservabilityLoggingFixtures:
    """Provide actual streams and retain the caller's logging composition."""

    class Capture:
        """An application receiver that writes the typed event as JSON."""

        def __init__(self) -> None:
            self.records: list[p.LoggingRecord] = []
            self.stream = io.StringIO()
            self.failure: BaseException | None = None

        def __call__(self, event: p.LoggingRecord) -> None:
            """Deliver to the selected stream, retaining native write failure."""
            serialized = m.LoggingRecord.model_validate(
                event,
                from_attributes=True,
            ).model_dump_json()
            try:
                self.stream.write(serialized + "\n")
            except ValueError as error:
                self.failure = error
                raise
            self.records.append(event)

    @pytest.fixture
    def logging_streams(self) -> t.IteratorOf[t.LoggingStreams]:
        """Keep real output streams alive until the composition is restored."""
        with io.StringIO() as structured, io.StringIO() as console:
            yield structured, console

    @pytest.fixture
    def logging_runtime(
        self,
        logging_streams: t.LoggingStreams,
    ) -> t.IteratorOf[p.StructlogOptions]:
        """Restore the captured provider/options/context, never fixed defaults."""
        original_settings = u.logging_settings()
        original_options = u.logging_options()
        original_context = (
            FlextObservability.correlation_id(),
            FlextObservability.trace_id(),
            FlextObservability.span_id(),
        )
        structured, console = logging_streams
        options = m.StructlogOptions(
            handlers=(
                u.create_logging_handler(stream=structured),
                u.create_logging_handler(stream=console, console_renderer=True),
            ),
            async_logging=False,
            cache_logger_on_first_use=True,
        )
        selected = u.resolve_logging_settings(
            runtime_settings=original_settings,
            log_level=c.LogLevel.DEBUG,
            debug=False,
            trace=True,
        )
        try:
            u.configure_structlog(settings=options, runtime_settings=selected)
            yield options
        finally:
            u.configure_structlog(
                settings=original_options,
                runtime_settings=original_settings,
            )
            FlextObservability.update_correlation_id(original_context[0])
            FlextObservability.update_trace_id(original_context[1])
            FlextObservability.update_span_id(original_context[2])
            for handler in options.handlers:
                handler.close()
