"""Public examples protocols facade for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextProtocols

if TYPE_CHECKING:
    from examples import t


class ExamplesFlextObservabilityProtocols(FlextProtocols):
    """Public examples protocols facade — inherits canonical p."""

    class ExamplesFlextObservability:
        """Canonical namespace for example protocols."""


p = ExamplesFlextObservabilityProtocols

__all__: t.MutableSequenceOf[str] = ["ExamplesFlextObservabilityProtocols", "p"]
