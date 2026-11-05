# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from examples import (
        ExamplesFlextObservabilityConstants,
        ExamplesFlextObservabilityModels,
        ExamplesFlextObservabilityProtocols,
        ExamplesFlextObservabilityTypes,
        ExamplesFlextObservabilityUtilities,
    )
    from flext_tests import api, d, e, h, r, td, tf, tk, tm, x

    from flext_observability import (
        FlextObservability,
        FlextObservabilityCli,
        FlextObservabilityConfig,
        FlextObservabilityConstants,
        FlextObservabilityModels,
        FlextObservabilityModelsConfig,
        FlextObservabilityProtocols,
        FlextObservabilityServiceBase,
        FlextObservabilitySettings,
        FlextObservabilityTypes,
        FlextObservabilityUtilities,
        FlextObservabilityVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
        config,
        main,
        observability,
        settings,
    )
    from tests.base import TestsFlextObservabilityServiceBase, s
    from tests.constants import TestsFlextObservabilityConstants, c
    from tests.models import TestsFlextObservabilityModels, m
    from tests.protocols import TestsFlextObservabilityProtocols, p
    from tests.settings import TestsFlextObservabilitySettings
    from tests.typings import TestsFlextObservabilityTypes, t
    from tests.utilities import TestsFlextObservabilityUtilities, u


__all__: tuple[str, ...] = (
    "ExamplesFlextObservabilityConstants",
    "ExamplesFlextObservabilityModels",
    "ExamplesFlextObservabilityProtocols",
    "ExamplesFlextObservabilityTypes",
    "ExamplesFlextObservabilityUtilities",
    "FlextObservability",
    "FlextObservabilityCli",
    "FlextObservabilityConfig",
    "FlextObservabilityConstants",
    "FlextObservabilityModels",
    "FlextObservabilityModelsConfig",
    "FlextObservabilityProtocols",
    "FlextObservabilityServiceBase",
    "FlextObservabilitySettings",
    "FlextObservabilityTypes",
    "FlextObservabilityUtilities",
    "FlextObservabilityVersion",
    "TestsFlextObservabilityConstants",
    "TestsFlextObservabilityModels",
    "TestsFlextObservabilityProtocols",
    "TestsFlextObservabilityServiceBase",
    "TestsFlextObservabilitySettings",
    "TestsFlextObservabilityTypes",
    "TestsFlextObservabilityUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "api",
    "c",
    "config",
    "d",
    "e",
    "h",
    "m",
    "main",
    "observability",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "ExamplesFlextObservabilityConstants": "examples",
        "ExamplesFlextObservabilityModels": "examples",
        "ExamplesFlextObservabilityProtocols": "examples",
        "ExamplesFlextObservabilityTypes": "examples",
        "ExamplesFlextObservabilityUtilities": "examples",
        "FlextObservability": "flext_observability",
        "FlextObservabilityCli": "flext_observability",
        "FlextObservabilityConfig": "flext_observability",
        "FlextObservabilityConstants": "flext_observability",
        "FlextObservabilityModels": "flext_observability",
        "FlextObservabilityModelsConfig": "flext_observability",
        "FlextObservabilityProtocols": "flext_observability",
        "FlextObservabilityServiceBase": "flext_observability",
        "FlextObservabilitySettings": "flext_observability",
        "FlextObservabilityTypes": "flext_observability",
        "FlextObservabilityUtilities": "flext_observability",
        "FlextObservabilityVersion": "flext_observability",
        "TestsFlextObservabilityConstants": ".constants",
        "TestsFlextObservabilityModels": ".models",
        "TestsFlextObservabilityProtocols": ".protocols",
        "TestsFlextObservabilityServiceBase": ".base",
        "TestsFlextObservabilitySettings": ".settings",
        "TestsFlextObservabilityTypes": ".typings",
        "TestsFlextObservabilityUtilities": ".utilities",
        "__author__": "flext_observability",
        "__author_email__": "flext_observability",
        "__description__": "flext_observability",
        "__license__": "flext_observability",
        "__title__": "flext_observability",
        "__url__": "flext_observability",
        "__version__": "flext_observability",
        "__version_info__": "flext_observability",
        "api": "flext_tests",
        "c": ".constants",
        "config": "flext_observability",
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "m": ".models",
        "main": "flext_observability",
        "observability": "flext_observability",
        "p": ".protocols",
        "r": "flext_tests",
        "s": ".base",
        "settings": "flext_observability",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_tests",
    },
    public_exports=__all__,
)
