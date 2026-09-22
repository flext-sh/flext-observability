"""Base constants for flext-observability.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final


class FlextObservabilityConstantsBase:
    """Base constants for flext-observability."""

    class Observability:
        """Observability domain constants owned by ``_constants``."""

        DEFAULT_SERVICE_NAME: Final[str] = "flext-service"
        DEFAULT_LOG_LEVEL: Final[str] = "INFO"
        DEFAULT_METRIC_UNIT: Final[str] = "1"
