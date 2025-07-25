"""Domain types for observability.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Domain types and enums for observability functionality.
"""

from __future__ import annotations

from enum import Enum


class MetricType(Enum):
    """Metric types for observability."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"
