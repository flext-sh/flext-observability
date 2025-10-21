"""FLEXT Observability Utilities - Zero Tolerance CONSOLIDATION.

IMPORTANT: FlextObservabilityUtilities was DUPLICATED between utilities.py and services.py.
This was a Zero Tolerance violation of the user's explicit requirements.

RESOLUTION: FlextObservabilityUtilities is now ONLY in services.py and imported from there.
This file is kept minimal to maintain import compatibility but all functionality
is consolidated in services.py to eliminate duplication.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Zero Tolerance CONSOLIDATION: Import from services.py to eliminate duplication
from flext_observability.services import FlextObservabilityUtilities

# Export consolidated utilities class
__all__ = ["FlextObservabilityUtilities"]
