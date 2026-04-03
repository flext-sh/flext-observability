# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_observability import (
        constants,
        integration,
        models,
        protocols,
        test_constants,
        test_factory,
        test_init,
        test_phase_11_integration,
        typings,
        unit,
        utilities,
    )
    from flext_observability.constants import (
        FlextObservabilityTestConstants,
        FlextObservabilityTestConstants as c,
    )
    from flext_observability.integration import (
        ErrorEvent,
        adv_ctx,
        advanced_ctx,
        api_result,
        api_success,
        business_result,
        correlation_id,
        ctx,
        ctx1_corr,
        custom_metrics,
        db_result,
        description,
        duration,
        error,
        error_handler,
        error_result,
        error_type,
        errors,
        escalated,
        factory,
        handler,
        json_data,
        json_snapshot,
        message,
        metric_result,
        metric_type,
        metrics,
        metrics_service,
        monitor,
        name,
        namespace,
        perf,
        perf_metrics,
        perf_monitor,
        performance,
        reg_result,
        reg_result2,
        registry,
        result,
        sampler,
        severity,
        should_alert,
        should_sample,
        snapshot,
        span_id,
        start_time,
        tags,
        test_error,
        trace_id,
    )
    from flext_observability.models import (
        FlextObservabilityTestModels,
        FlextObservabilityTestModels as m,
    )
    from flext_observability.protocols import (
        FlextObservabilityTestProtocols,
        FlextObservabilityTestProtocols as p,
    )
    from flext_observability.typings import (
        FlextObservabilityTestTypes,
        FlextObservabilityTestTypes as t,
    )
    from flext_observability.unit import (
        Testc,
        TestFlextObservabilityMasterFactoryReal,
        TestInitCoverage,
        flext_alert,
        flext_health_check,
        flext_metric,
        flext_trace,
        get_global_factory,
        reset_global_factory,
    )
    from flext_observability.utilities import (
        FlextObservabilityTestUtilities,
        FlextObservabilityTestUtilities as u,
    )

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    (
        "flext_observability.integration",
        "flext_observability.unit",
    ),
    {
        "FlextObservabilityTestConstants": "flext_observability.constants",
        "FlextObservabilityTestModels": "flext_observability.models",
        "FlextObservabilityTestProtocols": "flext_observability.protocols",
        "FlextObservabilityTestTypes": "flext_observability.typings",
        "FlextObservabilityTestUtilities": "flext_observability.utilities",
        "c": ("flext_observability.constants", "FlextObservabilityTestConstants"),
        "constants": "flext_observability.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "integration": "flext_observability.integration",
        "m": ("flext_observability.models", "FlextObservabilityTestModels"),
        "models": "flext_observability.models",
        "p": ("flext_observability.protocols", "FlextObservabilityTestProtocols"),
        "protocols": "flext_observability.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "t": ("flext_observability.typings", "FlextObservabilityTestTypes"),
        "test_constants": "flext_observability.test_constants",
        "test_factory": "flext_observability.test_factory",
        "test_init": "flext_observability.test_init",
        "test_phase_11_integration": "flext_observability.test_phase_11_integration",
        "typings": "flext_observability.typings",
        "u": ("flext_observability.utilities", "FlextObservabilityTestUtilities"),
        "unit": "flext_observability.unit",
        "utilities": "flext_observability.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
