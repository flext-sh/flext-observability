"""Public examples utilities facade for flext-observability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import u as _u

if TYPE_CHECKING:
    from examples.typings import t


class ExamplesFlextObservabilityUtilities(_u):
    """Public examples utilities facade — inherits canonical u."""

    class ExamplesFlextObservability:
        """Canonical namespace for example utilities."""


u = ExamplesFlextObservabilityUtilities

__all__: t.MutableSequenceOf[str] = ["ExamplesFlextObservabilityUtilities", "u"]
