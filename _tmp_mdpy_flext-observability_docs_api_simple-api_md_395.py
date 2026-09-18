# from flext-observability_docs/api/simple-api.md:395
from __future__ import annotations

from flext_observability import flext_create_log_entry

# Basic log entry
result = flext_create_log_entry(level="info", message="User authentication successful")

# Log with context
result = flext_create_log_entry(
    level="warning",
    message="Database query taking longer than expected",
    context={
        "query": "SELECT * FROM users WHERE active = true",
        "duration": "5.2s",
        "threshold": "2.0s",
    },
)

# Correlated log entry
result = flext_create_log_entry(
    level="error",
    message="Payment processing failed",
    context={
        "user_id": "user123",
        "order_id": "order456",
        "error": "INSUFFICIENT_FUNDS",
    },
    correlation_id="req_789xyz",
)
