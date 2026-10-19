"""Observability context enrichment at the native Core processor boundary.

Applications compose this provider with their existing Core options once per
operation. Logger creation, policy, sanitization, capture and delivery remain
owned by Core; enrichment never creates correlation or span identifiers.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_observability import p
from flext_observability.services.context import FlextObservabilityContext


class FlextObservabilityLogging:
    """Small native providers composed by the outer application."""

    class ContextStage:
        """Read the existing task-local context for every emitted event."""

        def __call__(
            self,
            logger: p.OutputLogger,
            method_name: str,
            event_dict: p.LoggingEvent,
        ) -> p.LoggingEvent:
            """Enrich before Core sanitizes and captures the event.

            Returns:
                The event updated with current task-local identifiers.

            """
            _ = logger, method_name
            for key, value in (
                ("correlation_id", FlextObservabilityContext.correlation_id()),
                ("trace_id", FlextObservabilityContext.trace_id()),
                ("span_id", FlextObservabilityContext.span_id()),
            ):
                if value:
                    event_dict[key] = value
                else:
                    event_dict.pop(key, None)
            return event_dict


__all__: list[str] = ["FlextObservabilityLogging"]
