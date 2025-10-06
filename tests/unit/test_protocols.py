"""Unit tests for flext_observability.protocols module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from flext_observability import FlextObservabilityProtocols


class TestFlextObservabilityProtocols:
    """Test the FlextObservabilityProtocols class."""

    def test_inherits_from_flext_protocols(self) -> None:
        """Test that FlextObservabilityProtocols inherits from FlextProtocols."""
        from flext_core import FlextProtocols

        assert issubclass(FlextObservabilityProtocols, FlextProtocols)

    def test_protocol_definitions(self) -> None:
        """Test that protocol definitions exist."""
        protocols = [
            "MetricProtocol",
            "TraceProtocol",
            "AlertProtocol",
            "HealthCheckProtocol",
            "LogEntryProtocol",
            "ObservabilityServiceProtocol",
        ]
        for protocol in protocols:
            assert hasattr(FlextObservabilityProtocols, protocol)

    def test_metric_protocol_methods(self) -> None:
        """Test MetricProtocol has required methods."""
        protocol = FlextObservabilityProtocols.MetricProtocol
        methods = ["record", "get_value", "get_metadata"]
        for method in methods:
            assert hasattr(protocol, method)

    def test_trace_protocol_methods(self) -> None:
        """Test TraceProtocol has required methods."""
        protocol = FlextObservabilityProtocols.TraceProtocol
        methods = ["start", "complete", "add_span", "get_spans"]
        for method in methods:
            assert hasattr(protocol, method)

    def test_alert_protocol_methods(self) -> None:
        """Test AlertProtocol has required methods."""
        protocol = FlextObservabilityProtocols.AlertProtocol
        methods = ["trigger", "resolve", "escalate", "get_status"]
        for method in methods:
            assert hasattr(protocol, method)

    def test_health_check_protocol_methods(self) -> None:
        """Test HealthCheckProtocol has required methods."""
        protocol = FlextObservabilityProtocols.HealthCheckProtocol
        methods = ["execute", "get_status", "get_last_execution_time"]
        for method in methods:
            assert hasattr(protocol, method)

    def test_log_entry_protocol_methods(self) -> None:
        """Test LogEntryProtocol has required methods."""
        protocol = FlextObservabilityProtocols.LogEntryProtocol
        methods = ["write", "format", "get_level", "get_timestamp"]
        for method in methods:
            assert hasattr(protocol, method)
