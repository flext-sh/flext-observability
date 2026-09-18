# from flext-observability/docs/standards/python-module-organization.md:181
from __future__ import annotations

# Core observability foundation
src/flext_observability/
├── __init__.py              # 🎯 Public API gateway - observability exports
├── constants.py             # 🎯 Observability constants and defaults
├── exceptions.py            # 🎯 Observability-specific exceptions
└── validation.py            # 🎯 Domain validation utilities
