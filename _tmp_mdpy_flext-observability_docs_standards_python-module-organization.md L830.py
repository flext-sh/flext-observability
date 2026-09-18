# from flext-observability/docs/standards/python-module-organization.md:830
from __future__ import annotations


# Comprehensive health monitoring
def monitor_service_health() -> p.Result[m.Dict]:
    """Comprehensive service health monitoring."""
    health_checks = []

    # Database health
    db_health = check_database_health()
    if db_health.success:
        health_checks.append(db_health.data)

    # Cache health
    cache_health = check_cache_health()
    if cache_health.success:
        health_checks.append(cache_health.data)

    # External API health
    api_health = check_external_api_health()
    if api_health.success:
        health_checks.append(api_health.data)

    # Aggregate health status
    overall_status = (
        "healthy"
        if all(check.status == "healthy" for check in health_checks)
        else "degraded"
    )

    # Create overall health metric
    health_metric = flext_create_metric(
        name="service_health_score",
        value=len([c for c in health_checks if c.status == "healthy"])
        / len(health_checks),
        unit="ratio",
        tags={"service": "order-service"},
    )

    return r[bool].ok({
        "overall_status": overall_status,
        "checks": health_checks,
        "health_score": health_metric.data if health_metric.success else None,
    })


def check_database_health() -> p.Result[FlextHealthCheck]:
    """Check database connectivity and performance."""
    try:
        start_time = time.time()
        # Test database query
        connection_time = (time.time() - start_time) * 1000

        status = "healthy" if connection_time < 100 else "degraded"

        return flext_create_health_check(
            name="postgresql_database",
            status=status,
            message=f"Database responding in {connection_time:.2f}ms",
            details={
                "response_time": f"{connection_time:.2f}ms",
                "connection_pool": "available",
                "last_backup": "2025-08-03T10:00:00Z",
            },
        )
    except Exception as e:
        return flext_create_health_check(
            name="postgresql_database",
            status="unhealthy",
            message=f"Database connection failed: {e!s}",
            details={"error": str(e), "retry_count": "3"},
        )
