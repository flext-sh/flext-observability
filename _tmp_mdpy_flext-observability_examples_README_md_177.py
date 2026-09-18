# from flext-observability_examples/README.md:177
from __future__ import annotations

# Health check integration example
from flext_observability import flext_create_health_check, FlextHealthService


def monitor_database_health() -> p.Result[m.Dict]:
    """Monitor database connectivity and performance."""
    try:
        # Test database connection
        connection_time = test_database_connection()

        if connection_time < 100:  # milliseconds
            health_check = flext_create_health_check(
                name="postgresql_database",
                status="healthy",
                message=f"Database responding in {connection_time}ms",
                details={
                    "response_time": f"{connection_time}ms",
                    "pool_size": "10/10",
                    "active_connections": "5",
                },
            )
        else:
            health_check = flext_create_health_check(
                name="postgresql_database",
                status="degraded",
                message=f"Database slow response: {connection_time}ms",
            )

        return health_check

    except Exception as e:
        error_health = flext_create_health_check(
            name="postgresql_database",
            status="unhealthy",
            message=f"Database connection failed: {str(e)}",
        )
        return error_health
