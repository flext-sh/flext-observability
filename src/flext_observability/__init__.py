# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Observability package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from flext_cli import d as d
    from flext_cli import e as e
    from flext_cli import h as h
    from flext_cli import r as r
    from flext_cli import s as s
    from flext_cli import x as x

    from ._config import FlextObservabilityConfig as FlextObservabilityConfig
    from ._config import config as config
    from ._settings import FlextObservabilitySettings as FlextObservabilitySettings
    from ._settings import settings as settings
    from .api import FlextObservability as FlextObservability
    from .api import observability as observability
    from .constants import FlextObservabilityConstants as FlextObservabilityConstants

    c: type[FlextObservabilityConstants]
    from .models import FlextObservabilityModels as FlextObservabilityModels

    m: type[FlextObservabilityModels]
    from .protocols import FlextObservabilityProtocols as FlextObservabilityProtocols

    p: type[FlextObservabilityProtocols]
    from .typings import FlextObservabilityTypes as FlextObservabilityTypes

    t: type[FlextObservabilityTypes]
    from .utilities import FlextObservabilityUtilities as FlextObservabilityUtilities

    u: type[FlextObservabilityUtilities]

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextObservabilityConfig", "config"),
    "._settings": ("FlextObservabilitySettings", "settings"),
    ".api": ("FlextObservability", "observability"),
    ".constants": ("FlextObservabilityConstants", "c"),
    ".models": ("FlextObservabilityModels", "m"),
    ".protocols": ("FlextObservabilityProtocols", "p"),
    ".typings": ("FlextObservabilityTypes", "t"),
    ".utilities": ("FlextObservabilityUtilities", "u"),
    "flext_cli": ("d", "e", "h", "r", "s", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextObservability",
    "FlextObservabilityConfig",
    "FlextObservabilityConstants",
    "FlextObservabilityModels",
    "FlextObservabilityProtocols",
    "FlextObservabilitySettings",
    "FlextObservabilityTypes",
    "FlextObservabilityUtilities",
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
    "observability",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
