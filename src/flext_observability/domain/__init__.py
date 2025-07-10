"""Domain layer for observability - pure business logic."""

from flext_core.domain.types import AlertSeverity
from flext_core.domain.types import LogLevel
from flext_core.domain.types import MetricType
from flext_core.domain.types import TraceStatus
from flext_observability.domain.entities import Alert
from flext_observability.domain.entities import HealthCheck
from flext_observability.domain.entities import LogEntry
from flext_observability.domain.entities import Metric
from flext_observability.domain.entities import Trace
from flext_observability.domain.events import AlertTriggered
from flext_observability.domain.events import HealthCheckCompleted
from flext_observability.domain.events import MetricCollected
from flext_observability.domain.events import TraceCompleted
from flext_observability.domain.events import TraceStarted
from flext_observability.domain.services import AlertingService
from flext_observability.domain.services import HealthAnalysisService
from flext_observability.domain.services import MetricsAnalysisService
from flext_observability.domain.specifications import AlertThresholdSpec
from flext_observability.domain.specifications import HealthStatusSpec
from flext_observability.domain.specifications import MetricValidationSpec
from flext_observability.domain.value_objects import ComponentName
from flext_observability.domain.value_objects import Duration
from flext_observability.domain.value_objects import HealthStatus
from flext_observability.domain.value_objects import MetricValue
from flext_observability.domain.value_objects import ThresholdValue
from flext_observability.domain.value_objects import TraceId

__all__ = [
    # Entities
    "Alert",
    # Value Objects
    "AlertSeverity",
    # Specifications
    "AlertThresholdSpec",
    # Events
    "AlertTriggered",
    # Services
    "AlertingService",
    "ComponentName",
    "Duration",
    "HealthAnalysisService",
    "HealthCheck",
    "HealthCheckCompleted",
    "HealthStatus",
    "HealthStatusSpec",
    "LogEntry",
    "LogLevel",
    "Metric",
    "MetricCollected",
    "MetricType",
    "MetricValidationSpec",
    "MetricValue",
    "MetricsAnalysisService",
    "ThresholdValue",
    "Trace",
    "TraceCompleted",
    "TraceId",
    "TraceStarted",
    "TraceStatus",
]
