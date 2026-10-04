"""Public examples typings facade for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextTypes


class ExamplesFlextObservabilityTypes(FlextTypes):
    """Public examples typings facade — inherits canonical t."""

    class ExamplesFlextObservability:
        """Canonical namespace for example type aliases."""


t = ExamplesFlextObservabilityTypes

__all__: t.MutableSequenceOf[str] = ["ExamplesFlextObservabilityTypes", "t"]
