"""Unit tests for flext_observability.typings module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_observability.typings import FlextObservabilityTypes, t


class TestFlextObservabilityTypes:
    """Test the FlextObservabilityTypes class."""

    def test_inherits_from_flext_types(self) -> None:
        """Test that FlextObservabilityTypes inherits from t."""
        assert issubclass(FlextObservabilityTypes, dict[str, t.GeneralValueType])

    def test_nested_type_classes(self) -> None:
        """Test that nested type classes exist."""
        assert hasattr(FlextObservabilityTypes, "ObservabilityCore")
        assert hasattr(FlextObservabilityTypes, "Metrics")
        assert hasattr(FlextObservabilityTypes, "Tracing")
        assert hasattr(FlextObservabilityTypes, "Alerting")
        assert hasattr(FlextObservabilityTypes, "Health")
        assert hasattr(FlextObservabilityTypes, "Logging")

    def test_observability_core_types(self) -> None:
        """Test ObservabilityCore type definitions."""
        core = t.ObservabilityCore
        types = [
            "CountersDict",
            "GaugesDict",
            "HistogramsDict",
            "MetadataDict",
            "TracesDict",
            "AlertsDict",
            "HealthChecksDict",
        ]
        for type_name in types:
            assert hasattr(core, type_name)

    def test_metrics_types(self) -> None:
        """Test Metrics type definitions."""
        metrics = t.Metrics
        types = ["MetricValue", "MetricName", "MetricUnit", "MetricType", "MetricTags"]
        for type_name in types:
            assert hasattr(metrics, type_name)

    def test_tracing_types(self) -> None:
        """Test Tracing type definitions."""
        tracing = t.Tracing
        types = [
            "TraceId",
            "SpanId",
            "TraceName",
            "SpanName",
            "TraceStatus",
            "SpanContext",
        ]
        for type_name in types:
            assert hasattr(tracing, type_name)

    def test_alerting_types(self) -> None:
        """Test Alerting type definitions."""
        alerting = t.Alerting
        types = ["AlertLevel", "AlertMessage", "AlertId", "AlertStatus"]
        for type_name in types:
            assert hasattr(alerting, type_name)

    def test_health_types(self) -> None:
        """Test Health type definitions."""
        health = t.Health
        types = [
            "HealthStatus",
            "HealthCheckId",
            "HealthCheckName",
            "HealthCheckResult",
        ]
        for type_name in types:
            assert hasattr(health, type_name)

    def test_logging_types(self) -> None:
        """Test Logging type definitions."""
        logging_types = t.Logging
        types = ["LogLevel", "LogMessage", "LogEntryId", "LogTimestamp"]
        for type_name in types:
            assert hasattr(logging_types, type_name)


class TestFlextObservabilityTypesAlias:
    """Test the FlextObservabilityTypes type aliases."""

    def test_type_aliases_exist(self) -> None:
        """Test that key type aliases are defined."""
        aliases = [
            "MetricValue",
            "TagsDict",
            "LogLevel",
            "AlertLevel",
            "TraceStatus",
            "HealthStatus",
        ]
        for alias in aliases:
            # These aliases should be available as attributes or types within FlextObservabilityTypes
            assert hasattr(FlextObservabilityTypes, alias) or hasattr(t, alias)
