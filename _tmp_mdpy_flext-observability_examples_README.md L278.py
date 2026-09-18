# from flext-observability/examples/README.md:278
from __future__ import annotations

# Example Singer tap with observability
from flext_observability import flext_monitor_function, flext_create_metric


class FlextTapOracle:
    """Example Singer tap with integrated observability."""

    @flext_monitor_function("tap_oracle_extract")
    def extract_records(self, table_name: str) -> t.SequenceOf[m.Dict]:
        """Extract records with automatic monitoring."""

        # Extract data (business logic)
        records = self._query_oracle_table(table_name)

        # Business metrics
        flext_create_metric(
            name="records_extracted",
            value=len(records),
            unit="count",
            tags={"table": table_name, "tap": "oracle"},
        )

        flext_create_metric(
            name="extraction_time",
            value=self._last_extraction_time,
            unit="seconds",
            tags={"table": table_name},
        )

        return records
