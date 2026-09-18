# from flext-observability_docs/api/simple-api.md:240
from __future__ import annotations

def flext_create_alert(
    name: str,
    severity: str,
    message: str,
    details: t.StringDict | None = None
) -> p.Result[FlextAlert]
