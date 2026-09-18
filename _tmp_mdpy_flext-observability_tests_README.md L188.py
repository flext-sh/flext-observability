# from flext-observability/tests/README.md:188
from __future__ import annotations


def test_monitoring_decorator_functionality():
    """Test automatic function monitoring."""

    @flext_monitor_function("test_operation")
    def monitored_function(x: int, y: int) -> int:
        return x + y

    result = monitored_function(5, 3)
    assert result == 8
    # Monitoring data validated separately
