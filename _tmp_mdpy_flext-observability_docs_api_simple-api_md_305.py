# from flext-observability_docs/api/simple-api.md:305
from __future__ import annotations

def flext_create_health_check(
    name: str,
    status: str,
    message: str = "",
    details: t.StringDict | None = None
) -> p.Result[FlextHealthCheck]
