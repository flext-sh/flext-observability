"""Public examples protocols facade for flext-observability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextProtocols

if TYPE_CHECKING:
    from examples.typings import t


class ExamplesFlextObservabilityProtocols(FlextProtocols):
    """Public examples protocols facade — inherits canonical p."""

    class ExamplesFlextObservability:
        """Canonical namespace for example protocols."""


p = ExamplesFlextObservabilityProtocols

__all__: t.MutableSequenceOf[str] = ["ExamplesFlextObservabilityProtocols", "p"]
