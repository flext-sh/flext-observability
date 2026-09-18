# from flext-observability/docs/standards/python-module-organization.md:907
from __future__ import annotations

# Business rule-based alerting
def create_business_alert(metric_name: str, current_value: float, threshold: float) -> p.Result[bool]:
    """Create business rule alert based on metric thresholds."""

    if current_value <= threshold:
        return r[bool].| ok(value=True)  # No alert needed

    # Determine severity based on threshold breach
    severity_ratio = current_value / threshold
    if severity_ratio > 2.0:
        severity = "critical"
    elif severity_ratio > 1.5:
        severity = "error"
    else:
        severity = "warning"

    # Create contextual alert
    alert_result = flext_create_alert(
        name=f"{metric_name}_threshold_breach",
        severity=severity,
        message=f"{metric_name} exceeded threshold: {current_value} > {threshold}",
        details={
            "metric_name": metric_name,
            "current_value": str(current_value),
            "threshold": str(threshold),
            "breach_ratio": str(severity_ratio),
            "timestamp": datetime.now(UTC).isoformat()
        }
    )

    if alert_result.failure:
        return r[bool].fail(f"Failed to create alert: {alert_result.error}")

    # Create alert metric for monitoring
    alert_metric_result = flext_create_metric(
        name="alerts_created",
        value=1,
        unit="count",
        tags={"severity": severity, "metric": metric_name},
        metric_type="counter"
    )

    return r[bool].| ok(value=True)

# Alert escalation patterns
def escalate_alert_if_needed(alert: FlextAlert, duration_minutes: int) -> p.Result[bool]:
    """Escalate alert based on duration and severity."""

    escalation_thresholds = {
        "warning": 60,    # 1 hour
        "error": 30,      # 30 minutes
        "critical": 15    # 15 minutes
    }

    threshold = escalation_thresholds.get(alert.severity, 60)

    if duration_minutes >= threshold:
        escalated_alert_result = flext_create_alert(
            name=f"{alert.name}_escalated",
            severity="critical",
            message=f"Alert escalated: {alert.message} (duration: {duration_minutes}m)",
            details={
                "original_alert_id": alert.id,
                "original_severity": alert.severity,
                "escalation_duration": str(duration_minutes),
                "escalation_threshold": str(threshold)
            }
        )

        return escalated_alert_result.map(lambda _: None)

    return r[bool].| ok(value=True)
