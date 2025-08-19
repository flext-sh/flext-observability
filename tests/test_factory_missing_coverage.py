"""Test factory.py missing coverage lines to reach 95% target."""

from datetime import datetime
from unittest.mock import patch

from flext_observability import FlextObservabilityMasterFactory


class TestFactoryMissingCoverage:
    """Test specific missing lines in factory.py for complete coverage."""

    def test_service_setup_exception_handling(self) -> None:
        """Test exception handling in _setup_services method - covers lines 263-270."""
        factory = FlextObservabilityMasterFactory()

        # Mock the logger to verify exception logging
        with (
            patch.object(factory, "_logger") as mock_logger,
            patch.object(factory.container, "register") as mock_register,
        ):
            # Test ValueError exception path
            mock_register.side_effect = ValueError("Service creation error")
            factory._setup_services()
            mock_logger.exception.assert_called()

            # Test TypeError exception path
            mock_register.side_effect = TypeError("Type error")
            factory._setup_services()
            mock_logger.exception.assert_called()

            # Test AttributeError exception path
            mock_register.side_effect = AttributeError("Attribute error")
            factory._setup_services()
            mock_logger.exception.assert_called()

            # Test ImportError exception path
            mock_register.side_effect = ImportError("Import error")
            factory._setup_services()
            mock_logger.exception.assert_called()

            # Test RuntimeError exception path
            mock_register.side_effect = RuntimeError("Runtime error")
            factory._setup_services()
            mock_logger.exception.assert_called()

    def test_log_context_not_dict(self) -> None:
        """Test log when context is not a dict - covers line 324."""
        factory = FlextObservabilityMasterFactory()

        # Pass extra_data that is not a dict (should be converted to empty dict)
        result = factory.log(
            message="test message",
            service="test_service",
            extra_data="not_a_dict",  # This should trigger line 324
        )

        assert result.success
        assert result.data.extra_data == {}  # Should be converted to empty dict

    def test_log_timestamp_not_datetime(self) -> None:
        """Test log when timestamp is not datetime - covers related lines."""
        factory = FlextObservabilityMasterFactory()

        # Pass timestamp that is not datetime (should be converted)
        result = factory.log(
            message="test message",
            timestamp="not_a_datetime",  # This should trigger timestamp conversion
        )

        assert result.success
        assert isinstance(result.data.timestamp, datetime)

    def test_trace_span_attributes_not_dict(self) -> None:
        """Test trace when tags is not a dict - covers line 347."""
        factory = FlextObservabilityMasterFactory()

        result = factory.trace(
            trace_id="test_trace",
            operation="test_op",
            span_id="test_span",
            tags="not_a_dict",  # This should trigger conversion
        )

        assert result.success
        assert result.data.tags == {}

    def test_trace_timestamp_not_datetime(self) -> None:
        """Test trace when start_time is not datetime - covers related lines."""
        factory = FlextObservabilityMasterFactory()

        result = factory.trace(
            trace_id="test_trace",
            operation="test_op",
            span_id="test_span",
            start_time="not_a_datetime",  # This should trigger conversion
        )

        assert result.success
        assert isinstance(result.data.start_time, datetime)

    def test_alert_tags_not_dict(self) -> None:
        """Test alert when tags is not a dict - covers line 387."""
        factory = FlextObservabilityMasterFactory()

        result = factory.alert(
            message="Test Alert",
            service="test_service",
            tags="not_a_dict",  # This should trigger conversion
        )

        assert result.success
        assert result.data.tags == {}

    def test_alert_timestamp_not_datetime(self) -> None:
        """Test alert when timestamp is not datetime - covers related lines."""
        factory = FlextObservabilityMasterFactory()

        result = factory.alert(
            message="Test Alert",
            service="test_service",
            timestamp="not_a_datetime",  # This should trigger conversion
        )

        assert result.success
        assert isinstance(result.data.timestamp, datetime)

    def test_health_check_metrics_not_dict(self) -> None:
        """Test health_check when metrics is not a dict - covers line 431."""
        factory = FlextObservabilityMasterFactory()

        result = factory.health_check(
            service_name="test_component",
            details="not_a_dict",  # This should trigger conversion
        )

        assert result.success
        assert result.data.details == {}

    def test_health_check_timestamp_not_datetime(self) -> None:
        """Test health_check when timestamp is not datetime - covers line 460."""
        factory = FlextObservabilityMasterFactory()

        result = factory.health_check(
            service_name="test_component",
            timestamp="not_a_datetime",  # This should trigger conversion
        )

        assert result.success
        assert isinstance(result.data.timestamp, datetime)

    def test_metric_tags_not_dict(self) -> None:
        """Test metric when tags is not a dict - covers line 472."""
        factory = FlextObservabilityMasterFactory()

        result = factory.metric(
            name="test_metric",
            value=42.0,
            tags="not_a_dict",  # This should trigger conversion
        )

        assert result.success
        assert result.data.tags == {}

    def test_metric_timestamp_not_datetime(self) -> None:
        """Test metric when timestamp is not datetime - covers line 563."""
        factory = FlextObservabilityMasterFactory()

        result = factory.metric(
            name="test_metric",
            value=42.0,
            timestamp="not_a_datetime",  # This should trigger conversion
        )

        assert result.success
        assert isinstance(result.data.timestamp, datetime)

    def test_service_setup_multiple_exception_types(self) -> None:
        """Test comprehensive exception coverage in service setup."""
        factory = FlextObservabilityMasterFactory()

        with (
            patch.object(factory, "_logger") as mock_logger,
            patch.object(factory.container, "register") as mock_register,
        ):
            # Test each exception type individually to ensure all paths are covered
            exception_types = [
                ValueError("Value error"),
                TypeError("Type error"),
                AttributeError("Attribute error"),
                ImportError("Import error"),
                RuntimeError("Runtime error"),
            ]

            for exception in exception_types:
                mock_register.side_effect = exception
                factory._setup_services()
                # Verify exception was logged
                assert mock_logger.exception.called

    def test_all_factory_methods_with_invalid_inputs(self) -> None:
        """Test all factory methods with various invalid input types."""
        factory = FlextObservabilityMasterFactory()

        # Test metric with invalid tags
        result = factory.metric("test", 1.0, tags=["not", "a", "dict"])
        assert result.success
        assert result.data.tags == {}

        # Test log with invalid extra_data
        result = factory.log("test", service="test_service", extra_data=123)
        assert result.success
        assert result.data.extra_data == {}

        # Test trace with invalid tags
        result = factory.trace("id", "op", tags=123)
        assert result.success
        assert result.data.tags == {}

        # Test alert with invalid tags
        result = factory.alert("msg", "test_service", tags=123)
        assert result.success
        assert result.data.tags == {}

        # Test health_check with invalid details
        result = factory.health_check("comp", details=123)
        assert result.success
        assert result.data.details == {}
