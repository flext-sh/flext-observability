# from flext-observability/docs/api/simple-api.md:265
from __future__ import annotations

from flext_observability import flext_create_alert

# Basic alert
result = flext_create_alert(
    name="high_cpu_usage",
    severity="warning",
    message="CPU usage exceeded 80% threshold",
)

# Alert with detailed context
result = flext_create_alert(
    name="database_connection_failure",
    severity="critical",
    message="Unable to connect to primary database",
    details={
        "host": "db-primary.example.com",
        "port": "5432",
        "database": "production",
        "error_code": "CONNECTION_TIMEOUT",
    },
)

# Business logic alert
result = flext_create_alert(
    name="payment_processing_delay",
    severity="error",
    message="Payment processing taking longer than expected",
    details={"queue_size": "1500", "avg_processing_time": "45s", "threshold": "30s"},
)
