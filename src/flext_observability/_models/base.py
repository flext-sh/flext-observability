"""Base models for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_observability.config_models import FlextObservabilityConfigModels


class FlextObservabilityModelsBase(FlextObservabilityConfigModels):
    """Base models for flext-observability."""


__all__: list[str] = ["FlextObservabilityModelsBase"]
