# from flext-observability/docs/standards/python-module-organization.md:585
from __future__ import annotations

# Import for infrastructure monitoring
from flext_observability import (
    FlextHealthService,
    flext_create_health_check,
    flext_create_metric,
)


class DatabaseConnectionService:
    def __init__(self, container: FlextContainer) -> None:
        self.health_service = FlextHealthService(container)

    def check_database_connectivity(self) -> p.Result[m.Dict]:
        """Monitor database health with observability."""
        try:
            # Test connection
            connection_time = self._test_connection()

            # Create health check
            health_result = flext_create_health_check(
                name="postgresql_connection",
                status="healthy",
                message=f"Connection successful in {connection_time}ms",
            )

            # Create performance metric
            metric_result = flext_create_metric(
                name="db_connection_time",
                value=connection_time,
                unit="milliseconds",
                tags={"database": "postgresql", "host": self.host},
            )

            return r[bool].ok({"status": "healthy", "metrics": [metric_result.value]})

        except Exception as e:
            # Create failure health check
            health_result = flext_create_health_check(
                name="postgresql_connection",
                status="unhealthy",
                message=f"Connection failed: {e!s}",
            )
            return r[bool].fail(f"Database health check failed: {e!s}")
