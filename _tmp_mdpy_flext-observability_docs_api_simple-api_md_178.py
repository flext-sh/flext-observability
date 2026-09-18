# from flext-observability_docs/api/simple-api.md:178
from __future__ import annotations

def flext_create_trace(
    operation_name: str,
    service_name: str,
    context: t.StringDict | None = None,
    parent_trace_id: str | None = None
) -> p.Result[FlextTrace]
