"""Observability constants extending flext-core patterns.

Includes metric types, alert levels, trace statuses, and configuration defaults.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import c

from ._constants.base import FlextObservabilityConstantsBase
from ._constants.domains import FlextObservabilityConstantsDomains


class FlextObservabilityConstants(c, FlextObservabilityConstantsBase):
    """Observability-specific constants extending flext-core patterns.

    Usage:
    ```python
    from flext_observability import FlextObservabilityConstants

    service_name = FlextObservabilityConstants.Observability.DEFAULT_SERVICE_NAME
    metric_type = FlextObservabilityConstants.Observability.MetricType.COUNTER
    ```
    """

    class Observability(
        FlextObservabilityConstantsBase, FlextObservabilityConstantsDomains
    ):
        """Observability domain constants namespace."""


c = FlextObservabilityConstants
__all__: list[str] = ["FlextObservabilityConstants", "c"]
