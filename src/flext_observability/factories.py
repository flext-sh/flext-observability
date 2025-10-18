"""Generic FLEXT Observability Factories.

Minimal, generic factories following SOLID principles with complete delegation to FLEXT core.
Single unified class for all observability entity creation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Any

from flext_core import FlextResult

from flext_observability.models import FlextObservabilityModels


class FlextObservabilityFactories:
    """Generic observability factories delegating to FLEXT core patterns.

    Single class providing generic entity creation through complete delegation
    to FlextResult and generic model patterns. No domain-specific logic.
    """

    @classmethod
    def create_entry(
        cls,
        name: str,
        entry_type: str,
        data: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> FlextResult[FlextObservabilityModels.GenericObservabilityEntry]:
        """Create generic observability entry through FLEXT patterns."""
        try:
            if not name or not isinstance(name, str):
                return FlextResult[
                    FlextObservabilityModels.GenericObservabilityEntry
                ].fail("Entry name must be a non-empty string")

            if not entry_type or not isinstance(entry_type, str):
                return FlextResult[
                    FlextObservabilityModels.GenericObservabilityEntry
                ].fail("Entry type must be a non-empty string")

            entry = FlextObservabilityModels.GenericObservabilityEntry(
                name=name.strip(),
                type=entry_type.strip(),
                data=data or {},
                metadata=metadata or {},
            )

            return FlextResult[FlextObservabilityModels.GenericObservabilityEntry].ok(
                entry
            )
        except Exception as e:
            return FlextResult[FlextObservabilityModels.GenericObservabilityEntry].fail(
                f"Entry creation failed: {e}"
            )


__all__ = ["FlextObservabilityFactories"]
