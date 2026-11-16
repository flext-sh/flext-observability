"""Base constants for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import ClassVar

from flext_cli import c


class FlextObservabilityConstantsBase:
    """Base constants for flext-observability."""

    class Observability:
        """Observability domain constants owned by ``_constants``."""

        DEFAULT_SERVICE_NAME: ClassVar[str] = "flext-service"
        DEFAULT_LOG_LEVEL: ClassVar[str] = "INFO"
        DEFAULT_METRIC_UNIT: ClassVar[str] = c.ParserBooleanToken.ONE


__all__: list[str] = ["FlextObservabilityConstantsBase"]
