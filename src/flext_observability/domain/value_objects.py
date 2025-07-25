"""Domain value objects for observability.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Domain value objects for observability functionality.
"""

from __future__ import annotations

from flext_core import FlextValueObject


class ComponentName(FlextValueObject):
    """Component name value object."""

    def __init__(self, value: str) -> None:
        """Initialize component name."""
        super().__init__()
        self.value = value

    def is_valid(self) -> bool:
        """Validate component name."""
        return bool(self.value and len(self.value.strip()) > 0)
