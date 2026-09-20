"""Observability protocols for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import p

from ._protocols.base import FlextObservabilityProtocolsBase
from ._protocols.domains import FlextObservabilityProtocolsDomains


class FlextObservabilityProtocols(p, FlextObservabilityProtocolsBase):
    """Unified observability protocols following FLEXT domain extension pattern.

    Extends p to inherit all foundation protocols (Result, Service, etc.)
    and adds observability-specific protocols in the Observability namespace.

    Architecture:
    - EXTENDS: p (inherits Foundation, Domain, Application, etc.)
    - ADDS: Observability-specific protocols in Observability namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_core import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Service[str]

    # Observability-specific protocols
    service: p.Observability.ObservabilityService
    request: p.Observability.Http.Request
    """

    class Observability(
        FlextObservabilityProtocolsBase, FlextObservabilityProtocolsDomains
    ):
        """Observability domain-specific protocols.

        Provides the observability service contract plus HTTP framework
        instrumentation protocols.
        """


p = FlextObservabilityProtocols

__all__: list[str] = ["FlextObservabilityProtocols", "p"]
