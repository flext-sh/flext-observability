"""New Semantic Architecture for FLEXT Observability.

🎯 SEMANTIC ORGANIZATION:
- foundation/: Core observability abstractions and protocols
- domain/: Pure observability business logic (metrics, traces, logs)
- application/: Observability use cases and workflows
- infrastructure/: Concrete implementations (Prometheus, Jaeger, etc.)
- configuration/: Settings and validation for observability
- integration/: Adapters for different observability backends

🔄 MIGRATION PATH:
Old imports from root module will work with deprecation warnings.
New code should use semantic imports:
- from flext_observability.foundation import ObservabilityProtocol
- from flext_observability.domain.metrics import Metric
- from flext_observability.application.services import MetricsCollectionService

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# This module establishes the new semantic structure
# Actual implementations will be in respective semantic modules

__all__ = [
    "Alert",
    "AlertManagerProtocol",
    "AlertingService",
    "DistributedTracingService",
    "HealthCheck",
    "HealthMonitoringService",
    "LogAggregationService",
    "LogAggregatorProtocol",
    "LogEntry",
    # Domain layer
    "Metric",
    "MetricCollectorProtocol",
    # Application layer
    "MetricsCollectionService",
    # Foundation layer
    "ObservabilityProtocol",
    "Trace",
    "TraceExporterProtocol",
]
