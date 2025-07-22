"""Foundation Layer - Observability Core Abstractions.

This module provides the fundamental abstractions and protocols
for observability capabilities built on flext_core foundation.

🏷️ FOUNDATION PRINCIPLE:
This layer contains ONLY pure abstractions, interfaces, and base patterns
for observability. NO concrete implementations.

Builds upon flext_core.foundation patterns:
- AbstractEntity, AbstractValueObject, AbstractService
- ResultPattern, SpecificationPattern
- Protocols for extensibility
"""

from __future__ import annotations

from flext_observability.foundation.abstractions import ObservabilityAbstraction
from flext_observability.foundation.protocols import (
    AlertManagerProtocol,
    LogAggregatorProtocol,
    MetricCollectorProtocol,
    ObservabilityProtocol,
    TraceExporterProtocol,
)
from flext_observability.foundation.specifications import ObservabilitySpecification

__all__ = [
    "AlertManagerProtocol",
    "LogAggregatorProtocol",
    "MetricCollectorProtocol",
    # Core abstractions
    "ObservabilityAbstraction",
    # Protocols for extensibility
    "ObservabilityProtocol",
    # Specifications
    "ObservabilitySpecification",
    "TraceExporterProtocol",
]
