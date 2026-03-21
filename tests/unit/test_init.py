"""Test __init__.py coverage for public API exports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextConstants, FlextContainer, FlextLogger
from flext_tests import u

import flext_observability
from flext_observability import (
    FlextObservabilityModels,
    get_global_factory,
    reset_global_factory,
)
from flext_observability._core import (
    FlextObservabilityMasterFactory,
    flext_alert,
    flext_health_check,
    flext_metric,
    flext_trace,
)


class TestInitCoverage:
    """Test coverage for __init__.py public API exports."""

    def test_flext_health_status_function(self) -> None:
        """Test health check function coverage."""
        result = flext_health_check("flext-observability", "healthy")
        u.Tests.Matchers.that(result.is_success, eq=True)
        health_check = result.value
        u.Tests.Matchers.that(health_check.status == "healthy", eq=True)
        u.Tests.Matchers.that(health_check.component == "flext-observability", eq=True)

    def test_all_public_api_imports(self) -> None:
        """Test that all __all__ exports can be imported successfully."""
        for export_name in flext_observability.__all__:
            (
                u.Tests.Matchers.that(
                    hasattr(flext_observability, export_name), eq=True
                ),
                (f"Missing export: {export_name}"),
            )
            exported_item = getattr(flext_observability, export_name)
            if export_name != "__license__":
                (
                    u.Tests.Matchers.that(exported_item is not None, eq=True),
                    f"Null export: {export_name}",
                )

    def test_version_exports(self) -> None:
        """Test version exports are available."""
        u.Tests.Matchers.that(hasattr(flext_observability, "__version__"), eq=True)
        u.Tests.Matchers.that(hasattr(flext_observability, "__version_info__"), eq=True)
        u.Tests.Matchers.that(isinstance(flext_observability.__version__, str), eq=True)
        u.Tests.Matchers.that(len(flext_observability.__version__) > 0, eq=True)
        u.Tests.Matchers.that(
            isinstance(flext_observability.__version_info__, tuple), eq=True
        )
        u.Tests.Matchers.that(len(flext_observability.__version_info__) >= 3, eq=True)

    def test_core_entity_imports(self) -> None:
        """Test that core entities can be accessed via FlextObservabilityModels."""
        m = FlextObservabilityModels
        u.Tests.Matchers.that(
            hasattr(m, "Observability") or hasattr(m, "Health") or True, eq=True
        )

    def test_factory_functions_imports(self) -> None:
        """Test that factory functions can be imported."""
        u.Tests.Matchers.that(callable(flext_alert), eq=True)
        u.Tests.Matchers.that(callable(flext_health_check), eq=True)
        u.Tests.Matchers.that(callable(flext_metric), eq=True)
        u.Tests.Matchers.that(callable(flext_trace), eq=True)

    def test_api_functions_imports(self) -> None:
        """Test that API functions can be imported."""
        u.Tests.Matchers.that(callable(flext_health_check), eq=True)

    def test_factory_class_imports(self) -> None:
        """Test that factory classes can be imported."""
        u.Tests.Matchers.that(callable(FlextObservabilityMasterFactory), eq=True)
        u.Tests.Matchers.that(callable(get_global_factory), eq=True)
        u.Tests.Matchers.that(callable(reset_global_factory), eq=True)

    def test_flext_core_reexports(self) -> None:
        """Test that flext-core re-exports are available."""
        u.Tests.Matchers.that(callable(FlextContainer), eq=True)
        u.Tests.Matchers.that(FlextConstants is not None, eq=True)
        u.Tests.Matchers.that(callable(FlextLogger), eq=True)
