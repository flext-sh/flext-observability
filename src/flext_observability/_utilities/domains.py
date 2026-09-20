"""Observability-specific project utilities owned by the private utilities family."""

from __future__ import annotations

from flext_core import p, r


class FlextObservabilityUtilitiesDomains:
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


__all__: list[str] = ["FlextObservabilityUtilitiesDomains"]
