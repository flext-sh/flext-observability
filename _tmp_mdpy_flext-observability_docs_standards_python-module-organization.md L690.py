# from flext-observability/docs/standards/python-module-organization.md:690
from __future__ import annotations

# Dependencies flow inward (Clean Architecture)
Interface Adapters  →  Application Services  →  Domain Layer
        ↓                      ↓                   ↓
Infrastructure Layer  →  Foundation Layer  →  flext-core
