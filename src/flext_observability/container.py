"""DI Container Configuration - Clean Architecture setup using flext-core.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

Following SOLID principles with dependency inversion using flext-core DI container.
"""

from __future__ import annotations

from flext_core import get_container

from flext_observability.application.services import (
    AlertService,
    HealthService,
    LoggingService,
    MetricsService,
    TracingService,
)
from flext_observability.domain.services import (
    AlertDomainService,
    HealthDomainService,
    MetricsDomainService,
)
from flext_observability.infrastructure.repositories import (
    InMemoryLoggingRepository,
    InMemoryMetricsRepository,
)


def configure_observability_container() -> None:
    """Configure DI container with observability components."""
    container = get_container()

    # Domain Services
    container.register("metrics_domain_service", MetricsDomainService())
    container.register("alert_domain_service", AlertDomainService())
    container.register("health_domain_service", HealthDomainService())

    # Repositories (using in-memory for simplicity)
    container.register("metrics_repository", InMemoryMetricsRepository())
    container.register("logging_repository", InMemoryLoggingRepository())

    # Application Services
    container.register("metrics_service", MetricsService())
    container.register("logging_service", LoggingService())
    container.register("tracing_service", TracingService())
    container.register("alert_service", AlertService())
    container.register("health_service", HealthService())


def get_observability_service(service_name: str) -> object:
    """Get observability service from DI container."""
    container = get_container()
    return container.get(service_name)
