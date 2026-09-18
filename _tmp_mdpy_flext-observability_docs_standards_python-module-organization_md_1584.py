# from flext-observability_docs/standards/python-module-organization.md:1584
from __future__ import annotations

# ✅ Extend observability configuration patterns
from flext_core import FlextSettings


class ObservabilitySettings(FlextSettings):
    """Observability configuration extending core patterns."""

    metrics_enabled: bool = True
    tracing_enabled: bool = True
    log_level: str = "INFO"
    correlation_id_header: str = "X-Correlation-ID"

    class Config:
        env_prefix = "OBSERVABILITY_"


class UserServiceSettings(FlextSettings):
    """User service configuration with observability."""

    service_name: str = "user-service"
    database_url: str = "postgresql://localhost/users"
    observability: ObservabilitySettings = field(default_factory=ObservabilitySettings)

    class Config:
        env_prefix = "USER_SERVICE_"
        env_nested_delimiter = "__"


# Usage in service initialization
class UserService:
    def __init__(self, settings: UserServiceSettings) -> None:
        self.settings = settings

        # Initialize observability based on configuration
        if settings.observability.metrics_enabled:
            self.metrics_service = FlextMetricsService(container)

        if settings.observability.tracing_enabled:
            self.tracing_service = FlextTracingService(container)
