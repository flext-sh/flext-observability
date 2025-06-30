"""Simple monitoring service for FLEXT framework."""

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

import psutil


@dataclass
class Metric:
    """Simple metric representation."""

    name: str
    value: float
    timestamp: datetime
    tags: dict[str, str] = field(default_factory=dict)


@dataclass
class HealthCheck:
    """Health check result."""

    name: str
    status: str  # healthy, unhealthy, degraded
    message: str
    timestamp: datetime
    duration_ms: float


class MonitoringService:
    """Simple monitoring service for basic observability."""

    def __init__(self) -> None:
        self.metrics: dict[str, Metric] = {}
        self.health_checks: dict[str, HealthCheck] = {}
        self.start_time = time.time()

    def record_metric(self, name: str, value: float, tags: Optional[dict[str, str]] = None) -> None:
        """Record a metric value."""
        metric = Metric(
            name=name,
            value=value,
            timestamp=datetime.now(timezone.utc),
            tags=tags or {}
        )
        self.metrics[name] = metric

    def get_metric(self, name: str) -> Optional[Metric]:
        """Get a metric by name."""
        return self.metrics.get(name)

    def get_all_metrics(self) -> dict[str, Metric]:
        """Get all recorded metrics."""
        return self.metrics.copy()

    def record_health_check(self, name: str, status: str, message: str, duration_ms: float = 0.0) -> None:
        """Record a health check result."""
        health_check = HealthCheck(
            name=name,
            status=status,
            message=message,
            timestamp=datetime.now(timezone.utc),
            duration_ms=duration_ms
        )
        self.health_checks[name] = health_check

    def get_health_check(self, name: str) -> Optional[HealthCheck]:
        """Get a health check by name."""
        return self.health_checks.get(name)

    def get_all_health_checks(self) -> dict[str, HealthCheck]:
        """Get all health checks."""
        return self.health_checks.copy()

    def get_system_metrics(self) -> dict[str, Any]:
        """Get basic system metrics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Record as metrics
            self.record_metric("system.cpu.percent", cpu_percent)
            self.record_metric("system.memory.percent", memory.percent)
            self.record_metric("system.memory.available_gb", memory.available / (1024**3))
            self.record_metric("system.disk.percent", (disk.used / disk.total) * 100)
            self.record_metric("system.disk.free_gb", disk.free / (1024**3))

            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_percent": round((disk.used / disk.total) * 100, 2),
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "uptime_seconds": time.time() - self.start_time
            }
        except Exception as e:
            return {"error": f"Failed to get system metrics: {str(e)}"}

    def get_application_metrics(self) -> dict[str, Any]:
        """Get application-specific metrics."""
        return {
            "uptime_seconds": time.time() - self.start_time,
            "total_metrics": len(self.metrics),
            "total_health_checks": len(self.health_checks),
            "healthy_checks": len([hc for hc in self.health_checks.values() if hc.status == "healthy"]),
            "unhealthy_checks": len([hc for hc in self.health_checks.values() if hc.status == "unhealthy"])
        }

    def perform_health_check(self, name: str, check_function) -> HealthCheck:
        """Perform a health check and record the result."""
        start_time = time.time()
        try:
            result = check_function()
            duration_ms = (time.time() - start_time) * 1000

            if result:
                self.record_health_check(name, "healthy", "Check passed", duration_ms)
            else:
                self.record_health_check(name, "unhealthy", "Check failed", duration_ms)

            return self.health_checks[name]
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.record_health_check(name, "unhealthy", f"Check error: {str(e)}", duration_ms)
            return self.health_checks[name]

    def get_overall_health(self) -> dict[str, Any]:
        """Get overall system health summary."""
        healthy_count = len([hc for hc in self.health_checks.values() if hc.status == "healthy"])
        total_checks = len(self.health_checks)

        if total_checks == 0:
            status = "unknown"
        elif healthy_count == total_checks:
            status = "healthy"
        elif healthy_count == 0:
            status = "unhealthy"
        else:
            status = "degraded"

        return {
            "status": status,
            "healthy_checks": healthy_count,
            "total_checks": total_checks,
            "health_percentage": (healthy_count / total_checks * 100) if total_checks > 0 else 0,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": time.time() - self.start_time
        }


# Global monitoring instance for simple usage
_monitoring_service = MonitoringService()


def get_monitoring_service() -> MonitoringService:
    """Get the global monitoring service instance."""
    return _monitoring_service


# Convenience functions for quick usage
def record_metric(name: str, value: float, tags: Optional[dict[str, str]] = None) -> None:
    """Record a metric using the global monitoring service."""
    _monitoring_service.record_metric(name, value, tags)


def record_health_check(name: str, status: str, message: str, duration_ms: float = 0.0) -> None:
    """Record a health check using the global monitoring service."""
    _monitoring_service.record_health_check(name, status, message, duration_ms)


def get_system_metrics() -> dict[str, Any]:
    """Get system metrics using the global monitoring service."""
    return _monitoring_service.get_system_metrics()


def get_overall_health() -> dict[str, Any]:
    """Get overall health using the global monitoring service."""
    return _monitoring_service.get_overall_health()
