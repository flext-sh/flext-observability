"""Public examples models facade for flext-observability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextModels

if TYPE_CHECKING:
    from examples.typings import t


class ExamplesFlextObservabilityModels(FlextModels):
    """Public examples model facade — inherits canonical m."""

    class ExamplesFlextObservability:
        """Canonical namespace for all example domain models."""


m = ExamplesFlextObservabilityModels

__all__: t.MutableSequenceOf[str] = ["ExamplesFlextObservabilityModels", "m"]
