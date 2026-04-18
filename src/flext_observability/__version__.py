# AUTO-GENERATED FILE — Regenerate with: make gen
"""Package version and metadata for flext-observability.

Subclass of ``FlextVersion`` — overrides only ``_metadata``.
All derived attributes (``__version__``, ``__title__``, etc.) are
computed automatically via ``FlextVersion.__init_subclass__``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import PackageMetadata, metadata

from flext_core import FlextVersion


class FlextObservabilityVersion(FlextVersion):
    """flext-observability version — MRO-derived from FlextVersion."""

    _metadata: PackageMetadata = metadata("flext-observability")


__version__ = FlextObservabilityVersion.__version__
__version_info__ = FlextObservabilityVersion.__version_info__
__title__ = FlextObservabilityVersion.__title__
__description__ = FlextObservabilityVersion.__description__
__author__ = FlextObservabilityVersion.__author__
__author_email__ = FlextObservabilityVersion.__author_email__
__license__ = FlextObservabilityVersion.__license__
__url__ = FlextObservabilityVersion.__url__
__all__: list[str] = [
    "FlextObservabilityVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
]
