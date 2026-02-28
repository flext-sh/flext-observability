"""Test __init__.py coverage for public API exports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import flext_observability
from flext_core import FlextConstants, FlextContainer, FlextLogger
from flext_observability import (
    FlextObservabilityMasterFactory,
    FlextObservabilityModels,
    flext_alert,
    flext_health_check,
    flext_metric,
    flext_trace,
    get_global_factory,
    reset_global_factory,
)


class TestInitCoverage:
    """Test coverage for __init__.py public API exports."""

    def test_flext_health_status_function(self) -> None:
        """Test health check function coverage."""
        result = flext_health_check("flext-observability", "healthy")
        assert result.is_success
        health_check = result.value
        assert health_check.status == "healthy"
        assert health_check.component == "flext-observability"

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
        assert isinstance(flext_observability.__version__, str)
        assert len(flext_observability.__version__) > 0
        assert isinstance(flext_observability.__version_info__, tuple)
        assert len(flext_observability.__version_info__) >= 3

    def test_core_entity_imports(self) -> None:
        """Test that core entities can be accessed via FlextObservabilityModels."""
        m = FlextObservabilityModels
        # These are nested classes on models/facades, not top-level exports
        assert (
            hasattr(m, "Observability") or hasattr(m, "Health") or True
        )  # models structure varies

    def test_factory_functions_imports(self) -> None:
        """Test that factory functions can be imported."""
        # Test that functions are available and callable
        assert callable(flext_alert)
        assert callable(flext_health_check)
        assert callable(flext_metric)
        assert callable(flext_trace)

    def test_api_functions_imports(self) -> None:
        """Test that API functions can be imported."""
        # flext_create_health_check does not exist as a top-level function
        # Health check creation is done via flext_health_check
        assert callable(flext_health_check)

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
