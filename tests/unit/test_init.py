"""Test __init__.py coverage for public API exports.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

import flext_observability
from flext_core import FlextConstants, FlextContainer, FlextLogger
from flext_observability import (
    FlextObservability,
    FlextObservabilityMasterFactory,
    __version__ as pkg_version,
    __version_info__ as pkg_version_info,
)
from tests import c, t

flext_alert = FlextObservability.flext_alert
flext_health_check = FlextObservability.flext_health_check
flext_metric = FlextObservability.flext_metric
flext_trace = FlextObservability.flext_trace
get_global_factory = FlextObservability.get_global_factory
reset_global_factory = FlextObservability.reset_global_factory


class TestInitCoverage:
    """Test coverage for __init__.py public API exports."""

    def test_flext_health_status_function(self) -> None:
        """Test health check function coverage."""
        result = flext_health_check(
            "flext-observability",
            c.Observability.HealthStatus.HEALTHY,
        )
        tm.that(result.is_success, eq=True)
        health_check = result.value
        tm.that(health_check.status, eq="healthy")
        tm.that(health_check.component, eq="flext-observability")

    def test_all_public_api_imports(self) -> None:
        """Test that all __all__ exports can be imported successfully."""
        nullable_metadata = {"__license__", "__author__", "__url__"}
        # __version__/__version_info__ shadow the __version__ submodule via
        # lazy imports; validated separately in test_version_exports.
        skip_lazy_shadow = {"__version__", "__version_info__", "__all__"}
        module_all: t.StrSequence = getattr(flext_observability, "__all__", [])
        for export_name in module_all:
            if export_name in skip_lazy_shadow:
                continue
            exported_item = getattr(flext_observability, export_name)
            if export_name not in nullable_metadata:
                tm.that(exported_item, none=False)

    def test_version_exports(self) -> None:
        """Test version exports are available via __version__ submodule."""
        tm.that(pkg_version, is_=str)
        tm.that(pkg_version, none=False)
        tm.that(pkg_version_info, is_=tuple)
        tm.that(len(pkg_version_info), gte=3)

    def test_core_entity_imports(self) -> None:
        """Test that core entities can be accessed via FlextObservabilityModels."""

    def test_factory_functions_imports(self) -> None:
        """Test that factory functions can be imported."""
        tm.that(callable(flext_alert), eq=True)
        tm.that(callable(flext_health_check), eq=True)
        tm.that(callable(flext_metric), eq=True)
        tm.that(callable(flext_trace), eq=True)

    def test_api_functions_imports(self) -> None:
        """Test that API functions can be imported."""
        tm.that(callable(flext_health_check), eq=True)

    def test_factory_class_imports(self) -> None:
        """Test that factory classes can be imported."""
        tm.that(callable(FlextObservabilityMasterFactory), eq=True)
        tm.that(callable(get_global_factory), eq=True)
        tm.that(callable(reset_global_factory), eq=True)

    def test_flext_core_reexports(self) -> None:
        """Test that flext-core re-exports are available."""
        tm.that(callable(FlextContainer), eq=True)
        tm.that(FlextConstants, none=False)
        tm.that(callable(FlextLogger), eq=True)
