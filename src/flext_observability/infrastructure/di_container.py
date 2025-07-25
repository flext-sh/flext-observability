"""🚨 ARCHITECTURAL COMPLIANCE: ELIMINATED DUPLICATE DI Container.

REFATORADO COMPLETO:
- REMOVIDA TODAS as duplicações de FlextContainer/DIContainer
- USA APENAS FlextContainer oficial do flext-core
- Mantém apenas utilitários flext_observability-específicos
- SEM fallback, backward compatibility ou código duplicado

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any

# 🚨 ARCHITECTURAL COMPLIANCE: Use ONLY official flext-core FlextContainer
from flext_core import FlextContainer, FlextLoggerFactory, FlextLoggerName

# Use correct FlextLoggerFactory pattern
_factory = FlextLoggerFactory()
logger = _factory.create_logger(FlextLoggerName(__name__))


# ==================== FLEXT_OBSERVABILITY-SPECIFIC DI UTILITIES ====================

_flext_observability_container_instance: FlextContainer | None = None


def get_flext_observability_container() -> FlextContainer:
    """Get FLEXT_OBSERVABILITY-specific DI container instance.

    Returns:
        FlextContainer: Official container from flext-core.

    """
    global _flext_observability_container_instance
    if _flext_observability_container_instance is None:
        _flext_observability_container_instance = FlextContainer()
    return _flext_observability_container_instance


def configure_flext_observability_dependencies() -> None:
    """Configure FLEXT_OBSERVABILITY dependencies using official FlextContainer."""
    get_flext_observability_container()

    try:
        # Register module-specific dependencies
        # Register observability services
        container.register("health_service", HealthService())
        container.register("metrics_service", MetricsService())
        container.register("logging_service", LoggingService())

        logger.info("FLEXT_OBSERVABILITY dependencies configured successfully")

    except ImportError:
        logger.exception("Failed to configure FLEXT_OBSERVABILITY dependencies")


def get_flext_observability_service(service_name: str) -> Any:
    """Get flext_observability service from container.

    Args:
        service_name: Name of service to retrieve.

    Returns:
        Service instance or None if not found.

    """
    container = get_flext_observability_container()
    result = container.get(service_name)

    if result.success:
        return result.data

    logger.warning(
        f"FLEXT_OBSERVABILITY service '{service_name}' not found: {result.error}",
    )
    return None


# ==================== MISSING FUNCTIONS RESTORED ====================


def get_base_config() -> Any:
    """Get base configuration from container.

    Returns:
        Base configuration instance.

    """
    return get_flext_observability_service("base_config")


def get_domain_entity() -> Any:
    """Get domain entity from container.

    Returns:
        Domain entity instance.

    """
    return get_flext_observability_service("domain_entity")


def get_domain_value_object() -> Any:
    """Get domain value object from container.

    Returns:
        Domain value object instance.

    """
    return get_flext_observability_service("domain_value_object")


def get_infrastructure_adapter() -> Any:
    """Get infrastructure adapter from container.

    Returns:
        Infrastructure adapter instance.

    """
    return get_flext_observability_service("infrastructure_adapter")


def get_service_result() -> Any:
    """Get service result from container.

    Returns:
        Service result instance.

    """
    return get_flext_observability_service("service_result")


# Initialize flext_observability dependencies on module import
configure_flext_observability_dependencies()
