"""Test __init__.py coverage for public API exports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import flext_observability
from flext_observability import (
    FlextAlert,
    FlextConstants,
    FlextContainer,
    FlextHealthCheck,
    FlextLogEntry,
    FlextLogger,
    FlextMetric,
    FlextObservabilityMasterFactory,
    FlextTrace,
    flext_alert,
    flext_create_alert,
    flext_create_health_check,
    flext_create_log_entry,
    flext_create_metric,
    flext_create_trace,
    flext_health_check,
    flext_health_status,
    flext_metric,
    flext_trace,
    get_global_factory,
    reset_global_factory,
)


class TestInitCoverage:
    """Test coverage for __init__.py public API exports."""

    def test_flext_health_status_function(self) -> None:
        """Test flext_health_status function coverage."""
        result = flext_health_status()
        assert result["status"] == "healthy"
        assert result["service"] == "flext-observability"
        assert result["version"] == "0.9.0"

    def test_all_public_api_imports(self) -> None:
        """Test that all __all__ exports can be imported successfully."""
        # Test all exports from __all__ list can be imported
        for export_name in flext_observability.__all__:
            assert hasattr(flext_observability, export_name), (
                f"Missing export: {export_name}"
            )
            exported_item = getattr(flext_observability, export_name)
            assert exported_item is not None, f"Null export: {export_name}"

    def test_version_exports(self) -> None:
        """Test version exports are available."""
        assert hasattr(flext_observability, "__version__")
        assert hasattr(flext_observability, "__version_info__")
        assert flext_observability.__version__ == "0.9.0"
        assert flext_observability.__version_info__ == (0, 9, 0)

    def test_core_entity_imports(self) -> None:
        """Test that core entities can be imported and instantiated."""
        # Test that classes are available and callable
        assert callable(FlextAlert)
        assert callable(FlextHealthCheck)
        assert callable(FlextLogEntry)
        assert callable(FlextMetric)
        assert callable(FlextTrace)

    def test_factory_functions_imports(self) -> None:
        """Test that factory functions can be imported."""
        # Test that functions are available and callable
        assert callable(flext_alert)
        assert callable(flext_health_check)
        assert callable(flext_metric)
        assert callable(flext_trace)

    def test_api_functions_imports(self) -> None:
        """Test that API functions can be imported."""
        # Test that functions are available and callable
        assert callable(flext_create_alert)
        assert callable(flext_create_health_check)
        assert callable(flext_create_log_entry)
        assert callable(flext_create_metric)
        assert callable(flext_create_trace)

    def test_factory_class_imports(self) -> None:
        """Test that factory classes can be imported."""
        # Test that classes and functions are available
        assert callable(FlextObservabilityMasterFactory)
        assert callable(get_global_factory)
        assert callable(reset_global_factory)

    def test_flext_core_reexports(self) -> None:
        """Test that flext-core re-exports are available."""
        # Test that re-exported classes are available
        assert callable(FlextContainer)
        assert FlextConstants is not None
        assert callable(FlextLogger)
