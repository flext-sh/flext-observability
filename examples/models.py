"""Public examples models facade for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextModels

if TYPE_CHECKING:
    from examples import t


class ExamplesFlextObservabilityModels(FlextModels):
    """Public examples model facade — inherits canonical m."""

    class ExamplesFlextObservability:
        """Canonical namespace for all example domain models."""


m = ExamplesFlextObservabilityModels

__all__: t.MutableSequenceOf[str] = ["ExamplesFlextObservabilityModels", "m"]
