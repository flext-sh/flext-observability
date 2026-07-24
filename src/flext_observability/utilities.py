"""FLEXT Observability Utilities - Centralized domain utilities.

Unified utilities facade inheriting core FLEXT utilities.
Provides namespace classes for performance and sampling operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import u
from flext_observability import p, r


class FlextObservabilityUtilities(u):
    """Centralized utilities for FLEXT Observability.

    Inherits CLI FLEXT utilities, providing additional namespace classes
    for observability domain operations.
    """

    class Observability:
        """Observability-specific project utilities."""

        class Performance:
            """Performance tracking helpers."""

            @staticmethod
            def calculate_duration(start_ns: int, end_ns: int) -> p.Result[float]:
                """Calculate duration in seconds from nanosecond timestamps."""
                if end_ns < start_ns:
                    return r[float].fail("end_ns must be >= start_ns")
                return r[float].ok((end_ns - start_ns) / 1000000000)

        class Sampling:
            """Sampling strategy helpers."""

            @staticmethod
            def should_sample(rate: float, request_id: int) -> bool:
                """Determine if a request should be sampled based on rate."""
                if rate <= 0.0:
                    return False
                if rate >= 1.0:
                    return True
                return request_id % 100 < int(rate * 100)


u = FlextObservabilityUtilities

__all__: list[str] = ["FlextObservabilityUtilities", "u"]
