# from flext-observability/docs/api/simple-api.md:330
from __future__ import annotations

from flext_observability import flext_create_health_check

# Basic health check
result = flext_create_health_check(
    name="database_connection",
    status="healthy",
    message="PostgreSQL connection active and responsive",
)

# Unhealthy service check
result = flext_create_health_check(
    name="external_api",
    status="unhealthy",
    message="Third-party API returning 503 errors",
    details={
        "endpoint": "https://api.external.com/v1/status",
        "last_success": "2025-08-03T10:30:00Z",
        "error_rate": "95%",
    },
)

# Degraded performance check
result = flext_create_health_check(
    name="cache_performance",
    status="degraded",
    message="Redis cache showing increased latency",
    details={"avg_latency": "150ms", "threshold": "50ms", "hit_rate": "85%"},
)
