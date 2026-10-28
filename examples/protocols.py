"""Public examples protocols facade for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableSequence

from flext_core import FlextProtocols


class ExamplesFlextObservabilityProtocols(FlextProtocols):
    """Public examples protocols facade — inherits canonical p."""

    class ExamplesFlextObservability:
        """Canonical namespace for example protocols."""


p = ExamplesFlextObservabilityProtocols

__all__: MutableSequence[str] = ["ExamplesFlextObservabilityProtocols", "p"]
