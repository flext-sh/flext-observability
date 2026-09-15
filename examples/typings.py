"""Public examples typings facade for flext-observability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import t as _t

if TYPE_CHECKING:
    from examples.typings import t


class ExamplesFlextObservabilityTypes(_t):
    """Public examples typings facade — inherits canonical t."""

    class ExamplesFlextObservability:
        """Canonical namespace for example type aliases."""


t = ExamplesFlextObservabilityTypes

__all__: t.MutableSequenceOf[str] = ["ExamplesFlextObservabilityTypes", "t"]
