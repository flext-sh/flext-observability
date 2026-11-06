"""CLI facade for flext-observability — thin transport adapter.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence


class FlextObservabilityCli:
    """Flext-observability CLI facade — thin transport adapter over flext-cli."""


def main(args: Sequence[str] | None = None) -> int:
    """Console-script entry point — commands are not implemented yet.

    Returns:
        The resulting ``int``.

    """
    _ = args
    return 0


__all__: tuple[str, ...] = ("FlextObservabilityCli", "main")
