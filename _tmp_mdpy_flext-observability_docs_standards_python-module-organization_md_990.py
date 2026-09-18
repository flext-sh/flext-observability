# from flext-observability_docs/standards/python-module-organization.md:990
from __future__ import annotations

# Test structure mirrors observability structure
tests/
├── unit/                           # Unit tests (isolated)
│   ├── test_entities.py           # Tests for entities.py (FlextMetric, FlextTrace)
│   ├── test_services.py           # Tests for services.py (FlextMetricsService)
│   ├── test_factory.py            # Tests for factory.py (FlextObservabilityMasterFactory)
│   └── test_simple_api.py          # Tests for flext_simple.py (flext_create_ functions)
├── integration/                    # Integration tests
│   ├── test_service_integration.py # Service layer integration
│   ├── test_monitoring_integration.py # Decorator integration
│   └── test_platform_integration.py # Platform orchestration
├── e2e/                           # End-to-end tests
│   └── test_observability_workflows.py # Complete observability workflows
├── conftest.py                    # Test configuration and fixtures
└── test_complete_coverage.py      # Comprehensive coverage validation
