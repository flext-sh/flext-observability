"""Base protocol facade for flext-observability.

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


class FlextObservabilityProtocolsBase:
    """FLEXT Observability transport protocol namespace."""


__all__: list[str] = ["FlextObservabilityProtocolsBase"]
