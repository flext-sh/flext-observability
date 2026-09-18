# from flext-observability/docs/standards/python-module-organization.md:1248
from __future__ import annotations

from flext_observability import flext_monitor_function
import time


def test_function_monitoring_decorator():
    """Test automatic function monitoring."""

    @flext_monitor_function("test_operation")
    def monitored_function(x: int, y: int) -> int:
        """Test function with monitoring."""
        time.sleep(0.1)  # Simulate work
        return x + y

    # Execute monitored function
    result = monitored_function(5, 3)

    # Verify function result
    assert result == 8

    # Verify monitoring data was created (in a real implementation,
    # you would check the metrics service or factory for created metrics)


def test_function_monitoring_with_exception():
    """Test monitoring decorator with function exceptions."""

    @flext_monitor_function("error_prone_operation")
    def failing_function() -> int:
        """Function that raises an exception."""
        raise ValueError("Test error")

    # Execute function and expect exception
    with pytest.raises(ValueError, match="Test error"):
        failing_function()

    # In a real implementation, verify that error metrics were created
    # and failure traces were recorded
