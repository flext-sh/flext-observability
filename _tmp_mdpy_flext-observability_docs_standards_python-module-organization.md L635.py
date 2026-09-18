# from flext-observability/docs/standards/python-module-organization.md:635
from __future__ import annotations

# ❌ Don't import everything
from flext_observability import *

# ❌ Don't import internal implementations

# ❌ Don't bypass simple API without reason
from flext_observability import FlextObservabilityMasterFactory

factory = FlextObservabilityMasterFactory()
metric = factory.create_metric("test", 1.0)  # Use flext_create_metric instead


# ❌ Don't create custom observability types
class MyCustomMetric:  # Use FlextMetric instead
    pass


# ❌ Don't ignore r error handling
result = flext_create_metric("test", 1.0)
metric = result.value  # Should check result.success first
