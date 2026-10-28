"""Public examples utilities facade for flext-observability.

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

from flext_core import FlextUtilities


class ExamplesFlextObservabilityUtilities(FlextUtilities):
    """Public examples utilities facade — inherits canonical u."""

    class ExamplesFlextObservability:
        """Canonical namespace for example utilities."""


u = ExamplesFlextObservabilityUtilities

__all__: MutableSequence[str] = ["ExamplesFlextObservabilityUtilities", "u"]
