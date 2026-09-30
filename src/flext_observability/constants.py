"""Observability constants extending flext-core patterns.

Includes metric types, alert levels, trace statuses, and configuration defaults.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import FlextCliConstants

from ._constants import (
    FlextObservabilityConstantsBase,
    FlextObservabilityConstantsDomains,
)


class FlextObservabilityConstants(FlextCliConstants, FlextObservabilityConstantsBase):
    """Observability-specific constants extending flext-core patterns.

    Usage:
    ```python
    from flext_observability import FlextObservabilityConstants

    service_name = FlextObservabilityConstants.Observability.DEFAULT_SERVICE_NAME
    metric_type = FlextObservabilityConstants.Observability.MetricType.COUNTER
    ```
    """

    class Observability(
        FlextObservabilityConstantsBase.Observability,
        FlextObservabilityConstantsDomains,
    ):
        """Observability domain constants namespace.

        Every scalar, enum and derived label is owned by
        ``flext_observability._constants`` (base and domains) and re-exported
        through this facade subclass.
        """


c = FlextObservabilityConstants
__all__: list[str] = ["FlextObservabilityConstants", "c"]
