# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Integration package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from flext_observability import test_phase_11_integration
    from flext_observability.test_phase_11_integration import (
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

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "ErrorEvent": "flext_observability.test_phase_11_integration",
    "adv_ctx": "flext_observability.test_phase_11_integration",
    "advanced_ctx": "flext_observability.test_phase_11_integration",
    "api_result": "flext_observability.test_phase_11_integration",
    "api_success": "flext_observability.test_phase_11_integration",
    "business_result": "flext_observability.test_phase_11_integration",
    "c": ("flext_core.constants", "FlextConstants"),
    "correlation_id": "flext_observability.test_phase_11_integration",
    "ctx": "flext_observability.test_phase_11_integration",
    "ctx1_corr": "flext_observability.test_phase_11_integration",
    "custom_metrics": "flext_observability.test_phase_11_integration",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "db_result": "flext_observability.test_phase_11_integration",
    "description": "flext_observability.test_phase_11_integration",
    "duration": "flext_observability.test_phase_11_integration",
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "error": "flext_observability.test_phase_11_integration",
    "error_handler": "flext_observability.test_phase_11_integration",
    "error_result": "flext_observability.test_phase_11_integration",
    "error_type": "flext_observability.test_phase_11_integration",
    "errors": "flext_observability.test_phase_11_integration",
    "escalated": "flext_observability.test_phase_11_integration",
    "factory": "flext_observability.test_phase_11_integration",
    "h": ("flext_core.handlers", "FlextHandlers"),
    "handler": "flext_observability.test_phase_11_integration",
    "json_data": "flext_observability.test_phase_11_integration",
    "json_snapshot": "flext_observability.test_phase_11_integration",
    "m": ("flext_core.models", "FlextModels"),
    "message": "flext_observability.test_phase_11_integration",
    "metric_result": "flext_observability.test_phase_11_integration",
    "metric_type": "flext_observability.test_phase_11_integration",
    "metrics": "flext_observability.test_phase_11_integration",
    "metrics_service": "flext_observability.test_phase_11_integration",
    "monitor": "flext_observability.test_phase_11_integration",
    "name": "flext_observability.test_phase_11_integration",
    "namespace": "flext_observability.test_phase_11_integration",
    "p": ("flext_core.protocols", "FlextProtocols"),
    "perf": "flext_observability.test_phase_11_integration",
    "perf_metrics": "flext_observability.test_phase_11_integration",
    "perf_monitor": "flext_observability.test_phase_11_integration",
    "performance": "flext_observability.test_phase_11_integration",
    "r": ("flext_core.result", "FlextResult"),
    "reg_result": "flext_observability.test_phase_11_integration",
    "reg_result2": "flext_observability.test_phase_11_integration",
    "registry": "flext_observability.test_phase_11_integration",
    "result": "flext_observability.test_phase_11_integration",
    "s": ("flext_core.service", "FlextService"),
    "sampler": "flext_observability.test_phase_11_integration",
    "severity": "flext_observability.test_phase_11_integration",
    "should_alert": "flext_observability.test_phase_11_integration",
    "should_sample": "flext_observability.test_phase_11_integration",
    "snapshot": "flext_observability.test_phase_11_integration",
    "span_id": "flext_observability.test_phase_11_integration",
    "start_time": "flext_observability.test_phase_11_integration",
    "t": ("flext_core.typings", "FlextTypes"),
    "tags": "flext_observability.test_phase_11_integration",
    "test_error": "flext_observability.test_phase_11_integration",
    "test_phase_11_integration": "flext_observability.test_phase_11_integration",
    "trace_id": "flext_observability.test_phase_11_integration",
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
