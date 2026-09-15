"""Public examples constants facade for flext-observability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import c as _c

if TYPE_CHECKING:
    from examples.typings import t


class ExamplesFlextObservabilityConstants(_c):
    """Public examples constants facade — inherits canonical c."""

    class ExamplesFlextObservability:
        """Canonical namespace for example constants."""


c = ExamplesFlextObservabilityConstants

__all__: t.MutableSequenceOf[str] = ["ExamplesFlextObservabilityConstants", "c"]
