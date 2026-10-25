# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, x

    from flext_observability.__version__ import (
        FlextObservabilityVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_observability._config import FlextObservabilityConfig, config
    from flext_observability._settings import FlextObservabilitySettings, settings
    from flext_observability.api import FlextObservability, observability
    from flext_observability.base import FlextObservabilityServiceBase, s
    from flext_observability.cli import FlextObservabilityCli, main
    from flext_observability.constants import FlextObservabilityConstants, c
    from flext_observability.models import FlextObservabilityModels, m
    from flext_observability.protocols import FlextObservabilityProtocols, p
    from flext_observability.typings import FlextObservabilityTypes, t
    from flext_observability.utilities import FlextObservabilityUtilities, u


__all__: tuple[str, ...] = (
    "FlextObservability",
    "FlextObservabilityCli",
    "FlextObservabilityConfig",
    "FlextObservabilityConstants",
    "FlextObservabilityModels",
    "FlextObservabilityProtocols",
    "FlextObservabilityServiceBase",
    "FlextObservabilitySettings",
    "FlextObservabilityTypes",
    "FlextObservabilityUtilities",
    "FlextObservabilityVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
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
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextObservability": ".api",
        "FlextObservabilityCli": ".cli",
        "FlextObservabilityConfig": "._config",
        "FlextObservabilityConstants": ".constants",
        "FlextObservabilityModels": ".models",
        "FlextObservabilityProtocols": ".protocols",
        "FlextObservabilityServiceBase": ".base",
        "FlextObservabilitySettings": "._settings",
        "FlextObservabilityTypes": ".typings",
        "FlextObservabilityUtilities": ".utilities",
        "FlextObservabilityVersion": ".__version__",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version_info__": ".__version__",
        "c": ".constants",
        "config": "._config",
        "d": "flext_cli",
        "e": "flext_cli",
        "h": "flext_cli",
        "m": ".models",
        "main": ".cli",
        "observability": ".api",
        "p": ".protocols",
        "r": "flext_cli",
        "s": ".base",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_cli",
    }),
    public_exports=__all__,
)

if not TYPE_CHECKING:
    from flext_observability.__version__ import __version__
