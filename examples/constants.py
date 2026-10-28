"""Public examples constants facade for flext-observability.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from collections.abc import MutableSequence

from flext_core import FlextConstants


class ExamplesFlextObservabilityConstants(FlextConstants):
    """Public examples constants facade — inherits canonical c."""

    class ExamplesFlextObservability:
        """Canonical namespace for example constants."""


c = ExamplesFlextObservabilityConstants

__all__: MutableSequence[str] = ["ExamplesFlextObservabilityConstants", "c"]
