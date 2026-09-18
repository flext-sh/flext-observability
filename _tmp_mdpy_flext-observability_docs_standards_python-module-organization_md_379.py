# from flext-observability_docs/standards/python-module-organization.md:379
from __future__ import annotations

from flext_observability import flext_monitor_function


@flext_monitor_function("user_processing")
def process_user_data(user_data: dict) -> t.JsonMapping:
    """Function automatically monitored for execution time and errors."""
    # Business logic here
    return {"status": "processed", "user": user_data}


# Decorator automatically:
# - Creates execution time metrics
# - Creates trace spans with operation context
# - Handles success/failure tracking
# - Logs structured entries with correlation IDs
