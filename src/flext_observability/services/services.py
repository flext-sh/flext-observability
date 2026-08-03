"""Generic FLEXT Observability Services.

Minimal, generic services following SOLID principles with complete delegation to FLEXT core.
Single unified class for all observability operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextContainer
from flext_observability import c, m, p, r, t, u


class FlextObservabilityServices:
    """Generic observability services delegating to FLEXT core patterns.

    Single unified class providing generic observability operations through
    complete delegation to FlextContainer, `u.fetch_logger(...)` / `p.Logger`, and r patterns.
    No domain-specific logic - pure generic foundation.
    """

    _container_type: ClassVar[p.ContainerType] = FlextContainer

    def __init__(self) -> None:
        """Initialize with FLEXT core components."""
        super().__init__()
        self._container = self._container_type.shared()
        self.logger = u.fetch_logger(__name__)

    @property
    def container(self) -> p.Container:
        """Access FLEXT container."""
        return self._container

    @property
    def health_service(self) -> m.Dict | None:
        """Generic health service - not implemented in base service."""
        return None

    def create_alert(self, **kwargs: t.Scalar) -> p.Result[m.Dict]:
        """Create a generic alert - not implemented in base service."""
        requested_keys: t.JsonValueList = list(kwargs)
        self.logger.debug(
            "create_alert not implemented in generic service",
            requested_keys=requested_keys,
        )
        return r[m.Dict].fail("Alert creation not implemented in generic service")

    def metrics_summary(self) -> p.Result[m.Dict]:
        """Summarize generic metrics - not implemented in base service."""
        return r[m.Dict].fail("Metrics summary not implemented in generic service")

    def status(self) -> p.Result[m.Dict]:
        """Resolve generic service status through FLEXT patterns."""
        try:
            status = {
                "service": "flext_observability",
                "status": "operational",
                "timestamp": "now",
                "version": "generic",
            }
            status_result = m.Dict({
                "service": status["service"],
                "status": status["status"],
                "timestamp": status["timestamp"],
                "version": status["version"],
            })
            return r[m.Dict].ok(status_result)
        except c.EXC_MAPPING_TYPE as e:
            return r[m.Dict].fail_op("Status check", e)

    def process_entry(self, entry_data: m.Dict) -> p.Result[m.Dict]:
        """Process generic observability entry through FLEXT patterns."""
        try:
            if not entry_data:
                return r[m.Dict].fail("Entry data required")
            processed = entry_data.model_copy(deep=True)
            processed["processed_at"] = "now"
            processed["processor"] = "flext_observability"
            return r[m.Dict].ok(processed)
        except c.EXC_MAPPING_TYPE as e:
            return r[m.Dict].fail_op("Entry processing", e)


__all__: list[str] = ["FlextObservabilityServices"]
