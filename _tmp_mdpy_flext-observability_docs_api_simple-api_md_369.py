# from flext-observability_docs/api/simple-api.md:369
from __future__ import annotations

def flext_create_log_entry(
    level: str,
    message: str,
    context: t.StringDict | None = None,
    correlation_id: str | None = None
) -> p.Result[FlextLogEntry]
