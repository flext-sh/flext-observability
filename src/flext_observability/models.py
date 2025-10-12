"""FLEXT Observability Models.

Core domain models following flext-core patterns with proper separation of concerns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextCore

# Import focused domain models
from flext_observability.alerting import FlextObservabilityAlerting
from flext_observability.health import FlextObservabilityHealth
from flext_observability.logging import FlextObservabilityLogging
from flext_observability.metrics import FlextObservabilityMetrics
from flext_observability.tracing import FlextObservabilityTracing


class FlextObservabilityModels(FlextCore.Models):
    """Observability domain models extending FlextCore.Models.

    Provides access to focused observability domain models through namespace classes.
    Each domain maintains its own module with proper separation of concerns.
    """

    # Core domain namespace classes
    Metrics = FlextObservabilityMetrics
    Tracing = FlextObservabilityTracing
    Alerting = FlextObservabilityAlerting
    Health = FlextObservabilityHealth
    Logging = FlextObservabilityLogging


__all__ = [
    "FlextObservabilityModels",
]
