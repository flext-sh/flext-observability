# from flext-observability/docs/standards/python-module-organization.md:666
from __future__ import annotations

# Observability architecture with clear boundaries
┌─────────────────────────────────────┐
│       Interface Adapters            │  # flext_simple.py, flext_monitor.py
│   (Simple API, Decorators, Export)  │  # flext_structured.py
├─────────────────────────────────────┤
│       Application Services          │  # services.py, obs_platform.py
│   (Business Logic, Coordination)    │  # health.py
├─────────────────────────────────────┤
│         Domain Layer                │  # entities.py (FlextMetric, FlextTrace)
│   (Observability Entities)          │  # validation.py (Domain rules)
├─────────────────────────────────────┤
│       Infrastructure Layer          │  # repos.py, metrics.py
│   (Storage, Utilities, Collection)  │  # flext_metrics.py
├─────────────────────────────────────┤
│         Foundation Layer            │  # constants.py, exceptions.py
│   (Constants, Base Patterns)        │  # validation.py (Base validation)
└─────────────────────────────────────┘
