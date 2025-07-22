"""Deprecation Management for FLEXT Observability.

Manages deprecation warnings and migration paths for
the semantic reorganization of flext_observability.

🚨 SEMANTIC REORGANIZATION IN PROGRESS:
All current imports are being moved to semantic structure.
This module provides compatibility and migration guidance.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


class FlextObservabilityDeprecationWarning(DeprecationWarning):
    """Custom deprecation warning for FLEXT Observability.

    Used to distinguish FLEXT-specific deprecation warnings
    from general Python deprecation warnings.
    """


def warn_deprecated_import(old_path: str, new_path: str, simple_import: str = "", version: str = "1.0.0") -> None:
    """Issue deprecation warning for imports with simple alternatives.

    Args:
        old_path: The deprecated import path
        new_path: The new semantic import path
        simple_import: Simple root-level import alternative
        version: Version when support will be removed

    """
    message_parts = [
        f"❌ DEPRECATED: '{old_path}' is deprecated.",
    ]

    if simple_import:
        message_parts.append(f"✅ SIMPLE: from flext_observability import {simple_import}")

    message_parts.extend([
        f"🏗️ SEMANTIC: from {new_path} (for Clean Architecture)",
        f"⏰ Removed in v{version}",
    ])

    warnings.warn("\n".join(message_parts), FlextObservabilityDeprecationWarning, stacklevel=3)


def warn_deprecated_class(old_class: str, new_class: str, version: str = "1.0.0") -> None:
    """Issue deprecation warning for class usage.

    Args:
        old_class: The deprecated class name
        new_class: The new recommended class
        version: Version when support will be removed

    """
    warnings.warn(
        f"\n\n🚨 DEPRECATED CLASS:\n"
        f"Class '{old_class}' is deprecated.\n\n"
        f"🎯 NEW SEMANTIC CLASS:\n"
        f"Use '{new_class}' instead.\n\n"
        f"🔄 MIGRATION GUIDE:\n"
        f"This class will be removed in version {version}.\n"
        f"Update your code to use the new semantic structure.\n\n"
        f"For details, see: https://flext.dev/observability/migration\n",
        FlextObservabilityDeprecationWarning,
        stacklevel=3,
    )


def warn_deprecated_function(old_func: str, new_func: str, version: str = "1.0.0") -> None:
    """Issue deprecation warning for function usage.

    Args:
        old_func: The deprecated function name
        new_func: The new recommended function
        version: Version when support will be removed

    """
    warnings.warn(
        f"\n\n🚨 DEPRECATED FUNCTION:\n"
        f"Function '{old_func}' is deprecated.\n\n"
        f"🎯 NEW SEMANTIC FUNCTION:\n"
        f"Use '{new_func}' instead.\n\n"
        f"🔄 MIGRATION GUIDE:\n"
        f"This function will be removed in version {version}.\n"
        f"Update your code to use the new semantic structure.\n\n"
        f"For details, see: https://flext.dev/observability/migration\n",
        FlextObservabilityDeprecationWarning,
        stacklevel=3,
    )


def warn_deprecated_path(old_path: str, recommendation: str, version: str = "1.0.0") -> None:
    """Issue deprecation warning for complex import paths.

    Args:
        old_path: The deprecated complex import path or pattern
        recommendation: Simple recommendation for replacement
        version: Version when support will be removed

    """
    warnings.warn(
        f"\n\n🚨 DEPRECATED COMPLEX PATH:\n"
        f"Using '{old_path}' is deprecated.\n\n"
        f"🎯 SIMPLE IMPORT SOLUTION:\n"
        f"{recommendation}\n\n"
        f"💡 PRODUCTIVITY TIP:\n"
        f"All FLEXT Observability imports are now available at root level!\n"
        f"No more complex nested paths - just import what you need directly.\n\n"
        f"🔄 MIGRATION:\n"
        f"Support for complex paths will be removed in version {version}.\n"
        f"Use simple root-level imports for better developer experience.\n\n"
        f"Examples:\n"
        f"✅ from flext_observability import get_logger\n"
        f"✅ from flext_observability import Metric, MetricsService\n"
        f"✅ from flext_observability import configure_observability\n",
        FlextObservabilityDeprecationWarning,
        stacklevel=3,
    )


# Migration mapping for automatic redirection
IMPORT_MIGRATION_MAP = {
    # Old root imports -> New semantic imports
    "flext_observability.business_metrics": "flext_observability.domain.metrics.business",
    "flext_observability.config": "flext_observability.configuration.settings",
    "flext_observability.health": "flext_observability.domain.health",
    "flext_observability.logging": "flext_observability.infrastructure.logging",
    "flext_observability.metrics": "flext_observability.domain.metrics",
    "flext_observability.simple_api": "flext_observability.application.simple_api",

    # Old domain imports -> New semantic imports
    "flext_observability.domain.entities": "flext_observability.domain.entities.core",
    "flext_observability.domain.events": "flext_observability.domain.events.core",
    "flext_observability.domain.services": "flext_observability.domain.services.core",

    # Old application imports -> New semantic imports
    "flext_observability.application.handlers": "flext_observability.application.handlers.core",
    "flext_observability.application.services": "flext_observability.application.services.core",

    # Old infrastructure imports -> New semantic imports
    "flext_observability.infrastructure.adapters": "flext_observability.infrastructure.adapters.core",
    "flext_observability.infrastructure.repositories": "flext_observability.infrastructure.persistence.repositories",
}


CLASS_MIGRATION_MAP = {
    # Old classes -> New semantic classes
    "ObservabilitySettings": "flext_observability.configuration.ObservabilityConfiguration",
    "MetricsCollector": "flext_observability.domain.metrics.MetricCollector",
    "HealthChecker": "flext_observability.domain.health.HealthMonitor",
    "EnterpriseBusinessMetrics": "flext_observability.domain.metrics.EnterpriseMetricsAggregate",

    # Application services
    "AlertService": "flext_observability.application.services.AlertingService",
    "HealthService": "flext_observability.application.services.HealthMonitoringService",
    "LoggingService": "flext_observability.application.services.LogAggregationService",
    "MetricsService": "flext_observability.application.services.MetricsCollectionService",
    "TracingService": "flext_observability.application.services.DistributedTracingService",
}


FUNCTION_MIGRATION_MAP = {
    # Old functions -> New semantic functions
    "setup_logging": "flext_observability.configuration.setup_observability_logging",
    "get_logger": "flext_observability.infrastructure.logging.get_structured_logger",
    "bind_context": "flext_observability.infrastructure.logging.bind_trace_context",
    "clear_context": "flext_observability.infrastructure.logging.clear_trace_context",
    "with_context": "flext_observability.infrastructure.logging.with_trace_context",

    # Configuration functions
    "configure_observability": "flext_observability.configuration.configure_observability_stack",
    "get_settings": "flext_observability.configuration.get_observability_settings",
    "create_development_config": "flext_observability.configuration.create_development_configuration",
    "create_production_config": "flext_observability.configuration.create_production_configuration",
    "create_testing_config": "flext_observability.configuration.create_testing_configuration",
}


def create_compatibility_wrapper(new_class: type[Any], old_name: str) -> type[Any]:
    """Create a compatibility wrapper for a deprecated class.

    Args:
        new_class: The new class implementation
        old_name: The old class name for warning

    Returns:
        A wrapper class that issues deprecation warnings

    """

    # For type safety, we dynamically create the wrapper
    def init_wrapper(self: Any, *args: Any, **kwargs: Any) -> None:
        warn_deprecated_class(
            old_name,
            f"{new_class.__module__}.{new_class.__name__}",
        )
        # Initialize using the original class
        new_class.__init__(self, *args, **kwargs)

    # Create a new class dynamically
    return type(
        old_name,
        (new_class,),
        {"__init__": init_wrapper},
    )


def create_compatibility_function(new_func: Any, old_name: str) -> Any:
    """Create a compatibility wrapper for a deprecated function.

    Args:
        new_func: The new function implementation
        old_name: The old function name for warning

    Returns:
        A wrapper function that issues deprecation warnings

    """

    def compatibility_wrapper(*args: Any, **kwargs: Any) -> Any:
        """Compatibility wrapper for deprecated function."""
        warn_deprecated_function(
            old_name,
            f"{new_func.__module__}.{new_func.__name__}",
        )
        return new_func(*args, **kwargs)

    compatibility_wrapper.__name__ = old_name
    compatibility_wrapper.__qualname__ = old_name
    compatibility_wrapper.__doc__ = getattr(new_func, "__doc__", None)

    return compatibility_wrapper
