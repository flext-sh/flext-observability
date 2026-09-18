# from flext-observability_docs/standards/python-module-organization.md:343
from __future__ import annotations

# External interface adaptation
├── flext_simple.py          # 🎛️ Simple API functions (flext_create_*)
├── flext_monitor.py         # 🎛️ Monitoring decorators (@flext_monitor_function)
└── flext_structured.py      # 🎛️ Structured logging adapters
