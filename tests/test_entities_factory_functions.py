"""Test entity factory functions for complete coverage."""

from decimal import Decimal

from flext_observability import (
    flext_alert,
    flext_health_check,
    flext_metric,
    flext_trace,
)


class TestEntityFactoryFunctions:
    """Test entity factory functions to improve coverage."""

    def test_flext_alert_with_id_and_version(self) -> None:
      """Test flext_alert with both id and version provided."""
      alert = flext_alert(
          "Test Title",
          "Test Message",
          severity="high",
          id="custom_id",
          version=2,
          tags={"test": "value"},
      )
      assert alert.id == "custom_id"
      assert alert.version == 2
      assert alert.title == "Test Title"
      assert alert.severity == "high"

    def test_flext_alert_with_id_only(self) -> None:
      """Test flext_alert with only id provided."""
      alert = flext_alert(
          "Test Title",
          "Test Message",
          id="custom_id_only",
          tags={"test": "value"},
      )
      assert alert.id == "custom_id_only"
      assert alert.version == 1  # Default version
      assert alert.title == "Test Title"

    def test_flext_alert_without_id(self) -> None:
      """Test flext_alert without id (auto-generated)."""
      alert = flext_alert(
          "Test Title",
          "Test Message",
          tags={"test": "value"},
      )
      assert alert.id is not None
      assert len(alert.id) > 0
      assert alert.version == 1

    def test_flext_trace_with_id(self) -> None:
      """Test flext_trace with id provided."""
      trace = flext_trace(
          "trace_123",
          "test_operation",
          "span_456",
          id="custom_trace_id",
          span_attributes={"test": "value"},
          duration_ms=100,
      )
      assert trace.id == "custom_trace_id"
      assert trace.trace_id == "trace_123"
      assert trace.operation == "test_operation"
      assert trace.span_id == "span_456"

    def test_flext_trace_without_id(self) -> None:
      """Test flext_trace without id (auto-generated)."""
      trace = flext_trace(
          "trace_789",
          "another_operation",
          "span_012",
          span_attributes={"test": "value"},
      )
      assert trace.id is not None
      assert len(trace.id) > 0
      assert trace.trace_id == "trace_789"

    def test_flext_metric_with_id_and_version(self) -> None:
      """Test flext_metric with both id and version provided."""
      result = flext_metric(
          "test_metric",
          42.5,
          unit="seconds",
          id="custom_metric_id",
          version=3,
          tags={"env": "test"},
      )
      assert result.success
      metric = result.data
      assert metric.id == "custom_metric_id"
      assert metric.version == 3
      assert metric.name == "test_metric"
      assert metric.value == 42.5

    def test_flext_metric_with_id_only(self) -> None:
      """Test flext_metric with only id provided."""
      result = flext_metric(
          "test_metric",
          100.0,
          id="metric_id_only",
          tags={"test": "value"},
      )
      assert result.success
      metric = result.data
      assert metric.id == "metric_id_only"
      assert metric.version == 1

    def test_flext_metric_without_id(self) -> None:
      """Test flext_metric without id (auto-generated)."""
      result = flext_metric(
          "auto_metric",
          75.0,
          unit="percent",
          tags={"auto": "generated"},
      )
      assert result.success
      metric = result.data
      assert metric.id is not None
      assert len(metric.id) > 0

    def test_flext_metric_with_decimal_value(self) -> None:
      """Test flext_metric with Decimal value."""
      result = flext_metric(
          "decimal_metric",
          Decimal("123.456"),
          unit="currency",
      )
      assert result.success
      metric = result.data
      assert isinstance(metric.value, Decimal)
      assert metric.value == Decimal("123.456")

    def test_flext_metric_creation_error(self) -> None:
      """Test flext_metric error handling."""
      # Force an error by providing invalid arguments
      result = flext_metric(
          "",  # Empty name should cause validation error
          42.0,
      )
      assert result.is_failure
      assert "Invalid metric name" in result.error

    def test_flext_health_check_with_id(self) -> None:
      """Test flext_health_check with id provided."""
      health = flext_health_check(
          "test_component",
          status="healthy",
          message="All good",
          id="custom_health_id",
          metrics={"cpu": 50.0},
      )
      assert health.id == "custom_health_id"
      assert health.component == "test_component"
      assert health.status == "healthy"
      assert health.message == "All good"

    def test_flext_health_check_without_id(self) -> None:
      """Test flext_health_check without id (auto-generated)."""
      health = flext_health_check(
          "auto_component",
          metrics={"memory": 75.0},
      )
      assert health.id is not None
      assert len(health.id) > 0
      assert health.component == "auto_component"

    def test_flext_metric_exception_handling(self) -> None:
      """Test flext_metric exception handling to cover lines 880-881."""
      from unittest.mock import patch

      # Force a TypeError during FlextGenerators.generate_entity_id() to hit exception handler
      with patch(
          "flext_observability.entities.FlextGenerators.generate_entity_id",
          side_effect=TypeError("Forced error"),
      ):
          result = flext_metric("test_metric", 42.0)
          assert result.is_failure
          assert "Failed to create metric: Forced error" in result.error
