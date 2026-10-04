"""Public examples utilities facade for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextUtilities

if TYPE_CHECKING:
    from examples.typings import t


class ExamplesFlextObservabilityUtilities(FlextUtilities):
    """Public examples utilities facade — inherits canonical u."""

    class ExamplesFlextObservability:
        """Canonical namespace for example utilities."""


u = ExamplesFlextObservabilityUtilities

__all__: t.MutableSequenceOf[str] = ["ExamplesFlextObservabilityUtilities", "u"]
