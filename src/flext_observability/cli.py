"""CLI facade for flext-observability — thin transport adapter.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flext_observability import t


class FlextObservabilityCli:
    """Flext-observability CLI facade — thin transport adapter over flext-cli."""


def main(args: t.StrSequence | None = None) -> int:
    """Console-script entry point — commands are not implemented yet.

    Returns:
        The resulting ``int``.
    """
    _ = args
    return 0


__all__: t.VariadicTuple[str] = ("FlextObservabilityCli", "main")
