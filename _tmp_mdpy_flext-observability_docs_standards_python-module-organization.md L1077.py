# from flext-observability/docs/standards/python-module-organization.md:1077
from __future__ import annotations

from flext_observability import FlextMetric, FlextTrace
from decimal import Decimal


class TestFlextMetric:
    """Test observability metric entity behavior."""

    def test_metric_validation_success(self):
        """Test successful metric validation."""
        metric = FlextMetric(
            name="response_time",
            value=150.5,
            unit="milliseconds",
            tags={"service": "api", "endpoint": "/users"},
        )

        validation_result = metric.validate_business_rules()

        assert validation_result.success
        assert metric.name == "response_time"
        assert metric.value == 150.5
        assert metric.unit == "milliseconds"
        assert metric.tags["service"] == "api"

    def test_metric_validation_invalid_name(self):
        """Test metric validation with invalid name."""
        metric = FlextMetric(name="", value=100.0, unit="count")

        validation_result = metric.validate_business_rules()

        assert validation_result.failure
        assert "Invalid metric name" in validation_result.error

    def test_metric_decimal_value_support(self):
        """Test metric with Decimal value for financial precision."""
        metric = FlextMetric(
            name="transaction_amount", value=Decimal("1234.56"), unit="USD"
        )

        validation_result = metric.validate_business_rules()

        assert validation_result.success
        assert metric.value == Decimal("1234.56")
        assert isinstance(metric.value, Decimal)


class TestFlextTrace:
    """Test observability trace entity behavior."""

    def test_trace_creation_with_context(self):
        """Test trace creation with operation context."""
        trace = FlextTrace(
            operation_name="process_payment",
            service_name="payment-service",
            context={"user_id": "123", "amount": "100.00"},
        )

        assert trace.operation_name == "process_payment"
        assert trace.service_name == "payment-service"
        assert trace.context["user_id"] == "123"
        assert trace.context["amount"] == "100.00"
        assert trace.start_time is not None

    def test_trace_parent_child_relationship(self):
        """Test parent-child trace relationships."""
        parent_trace = FlextTrace(
            operation_name="api_request", service_name="api-gateway"
        )

        child_trace = FlextTrace(
            operation_name="database_query",
            service_name="user-service",
            parent_trace_id=parent_trace.id,
        )

        assert child_trace.parent_trace_id == parent_trace.id
        assert child_trace.operation_name == "database_query"
        assert child_trace.service_name == "user-service"
