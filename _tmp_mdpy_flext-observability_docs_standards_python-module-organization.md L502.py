# from flext-observability/docs/standards/python-module-organization.md:502
from __future__ import annotations

# Simple API functions use flext_create_ prefix
def flext_create_metric(name: str, value: float, unit: str = "") -> p.Result[FlextMetric]
def flext_create_trace(operation_name: str, service_name: str) -> p.Result[FlextTrace]
def flext_create_alert(name: str, severity: str, message: str) -> p.Result[FlextAlert]
def flext_create_health_check(name: str, status: str) -> p.Result[FlextHealthCheck]
def flext_create_log_entry(level: str, message: str) -> p.Result[FlextLogEntry]

# Monitoring functions use flext_monitor_ prefix
def flext_monitor_function(operation_name: str) -> Callable
def correlation_id() -> str
def update_correlation_id(correlation_id: str) -> None

# Factory access functions
def global_factory() -> FlextObservabilityMasterFactory
def clear_global_factory() -> None
