# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

**FLEXT-Observability - Enterprise Observability and Monitoring Foundation**
**Version**: 0.9.0 | **Updated**: 2025-10-10
**Status**: Active development with comprehensive observability patterns · 100% coverage requirement

**References**: See [../CLAUDE.md](../CLAUDE.md) for FLEXT ecosystem standards and [README.md](README.md) for project overview.

**Hierarchy**: This document provides project-specific standards based on workspace-level patterns defined in [../CLAUDE.md](../CLAUDE.md). For architectural principles, quality gates, and MCP server usage, reference the main workspace standards.

## 🔗 MCP SERVER INTEGRATION (MANDATORY)

As defined in [../CLAUDE.md](../CLAUDE.md), all FLEXT development MUST use:

| MCP Server              | Purpose                                                     | Status          |
| ----------------------- | ----------------------------------------------------------- | --------------- |
| **serena**              | Semantic code analysis, symbol manipulation, refactoring    | **MANDATORY**   |
| **sequential-thinking** | Observability architecture and metrics problem solving     | **RECOMMENDED** |
| **context7**            | Third-party library documentation (OpenTelemetry, Pydantic) | **RECOMMENDED** |
| **github**              | Repository operations and observability PRs                | **ACTIVE**      |

**Usage**: Reference [~/.claude/commands/flext.md](~/.claude/commands/flext.md) for MCP workflows. Use `/flext` command for module optimization.

**Copyright (c) 2025 FLEXT Team. All rights reserved.**
**License**: MIT

---

## 🎯 FLEXT-OBSERVABILITY PURPOSE

**ROLE**: flext-observability provides enterprise-grade observability, monitoring, and metrics patterns for the FLEXT ecosystem using flext-core foundation exclusively.

**CURRENT CAPABILITIES**:

- ✅ **Domain Entities**: FlextMetric, FlextTrace, FlextAlert, FlextHealthCheck with full validation
- ✅ **Service Layer**: Enterprise-grade observability services with dependency injection
- ✅ **Simple API**: Easy-to-use factory functions (flext_create_metric, flext_create_trace, flext_create_alert)
- ✅ **Monitoring Decorators**: Function decorators for automatic instrumentation (@flext_monitor_function)
- ✅ **Type Safety**: Pydantic v2 models with Python 3.13+ type annotations
- ✅ **FLEXT Integration**: Complete flext-core 1.0.0 integration (FlextResult, FlextContainer)
- ✅ **Railway Pattern**: All operations return FlextResult[T] for composable error handling
- ⚠️ **Import Issues**: Current import compatibility issues with flext-core (T not exported)

**ECOSYSTEM USAGE**:

- **Foundation Component**: Provides observability patterns for all FLEXT projects
- **Clean Architecture**: Domain → Application → Infrastructure layers
- **Domain-Driven Design**: Rich domain models with business logic validation
- **Zero Tolerance**: No custom observability implementations allowed

**QUALITY STANDARDS**:

- **Type Safety**: Pyrefly strict mode compliance (currently blocked by import issues)
- **Test Coverage**: 100% minimum requirement (481 test functions across 40 files)
- **Code Quality**: Ruff linting and formatting (100% compliance)
- **FLEXT Integration**: Complete flext-core patterns usage

## 🛑 ZERO TOLERANCE ENFORCEMENT (OBSERVABILITY & MONITORING FOUNDATION)

### ⛔ ABSOLUTELY FORBIDDEN OBSERVABILITY VIOLATIONS

#### 1. **DIRECT OBSERVABILITY LIBRARY IMPORTS (ECOSYSTEM VIOLATION)**

```python
# ❌ ABSOLUTELY FORBIDDEN - Direct observability library imports
import opentelemetry.trace              # VIOLATION: Use flext-observability foundation
from prometheus_client import Counter   # VIOLATION: Use flext-observability metrics
import logging                          # VIOLATION: Use FlextLogger from flext-core
from opentelemetry import metrics       # VIOLATION: Architecture breach

# ✅ CORRECT - FLEXT Ecosystem Foundation Only
from flext_observability import FlextMetricsService, FlextTracingService
from flext_observability import flext_create_metric, flext_create_trace
from flext_observability import FlextObservabilityMasterFactory, flext_monitor_function
from flext_core import FlextResult, FlextLogger, get_logger
```

#### 2. **CUSTOM OBSERVABILITY IMPLEMENTATIONS (ARCHITECTURE VIOLATION)**

- **FORBIDDEN**: Custom metrics implementations outside flext-observability patterns
- **FORBIDDEN**: Direct OpenTelemetry tracing setup - Use FlextTracingService
- **FORBIDDEN**: Custom Prometheus metrics collectors - Use FlextMetricsService
- **FORBIDDEN**: Manual logging implementations - Use FlextLogger from flext-core
- **FORBIDDEN**: Custom observability error handling - Use FlextResult[T] railway pattern

#### 3. **MONITORING CONFIGURATION VIOLATIONS**

- **FORBIDDEN**: Direct OpenTelemetry configuration without flext-observability validation
- **FORBIDDEN**: Prometheus metrics registration outside flext-observability management
- **FORBIDDEN**: Custom health check implementations bypassing FlextHealthService
- **FORBIDDEN**: Alert configurations without flext-observability alert management

### ⛔ PRODUCTION OBSERVABILITY STANDARDS (ZERO DEVIATION)

1. **ALL observability operations** through flext-observability foundation exclusively
2. **ALL metrics collection** via FlextMetricsService and FlextMetric entities
3. **ALL distributed tracing** through FlextTracingService and FlextTrace entities
4. **ALL alerting** through FlextAlertService and FlextAlert entities
5. **ALL health monitoring** through FlextHealthService and FlextHealthCheck entities
6. **ALL observability error handling** with FlextResult[T] railway pattern

## 🚀 ENTERPRISE DEVELOPMENT COMMANDS (PRODUCTION OBSERVABILITY FOUNDATION)

### Essential Commands

```bash
# Setup and installation
make setup                   # Complete setup with Poetry dependencies
make install                 # Install dependencies
make install-dev             # Install with dev dependencies

# Quality gates (MANDATORY before commit)
make validate                # Full validation: lint + type-check + security + test
make check                   # Quick check: lint + type-check
make lint                    # Ruff linting (ZERO violations)
make type-check              # Pyrefly type checking (ZERO errors)
make security                # Bandit + pip-audit security scanning
make test                    # Full test suite (100% coverage requirement)

# Testing categories
make test-unit               # Unit tests only
make test-integration        # Integration tests only
make test-fast               # Tests without coverage

# Code quality
make format                  # Auto-format with Ruff
make fix                     # Auto-fix issues

# Build and distribution
make build                   # Build package
make clean                   # Clean artifacts
```

### 📊 OBSERVABILITY FOUNDATION OPERATIONS

```bash
# Core observability infrastructure lifecycle
make observability-init      # Initialize observability stack with FLEXT standards
make monitoring-setup        # Setup monitoring services (Prometheus, Grafana)
make observability-validate  # Validate complete observability configuration
make observability-test      # Test observability stack with real systems

# Monitoring operations (production patterns)
make metrics-collect         # Collect metrics with FlextMetricsService
make traces-start           # Start distributed tracing with FlextTracingService
make alerts-configure       # Configure alerting with FlextAlertService
make health-monitor         # Monitor system health with FlextHealthService

# Observability stack operations
make prometheus-start       # Start Prometheus metrics collection
make grafana-setup          # Setup Grafana dashboards
make jaeger-start          # Start Jaeger distributed tracing
make alertmanager-config   # Configure alert manager integration
```

### 🧪 ENTERPRISE TESTING STANDARDS (REAL OBSERVABILITY VALIDATION)

```bash
# Comprehensive observability testing (NO MOCKS - Real monitoring systems)
make test                    # Full suite: 90%+ coverage with real observability integration
make test-fast              # Tests without coverage (development speed)
make test-unit              # Unit tests with FlextResult pattern validation
make test-integration       # Integration tests with real OpenTelemetry/Prometheus APIs
make test-observability     # Observability-specific tests with monitoring validation
make test-monitoring        # Complete monitoring stack testing
make coverage-html          # Generate HTML coverage report with observability metrics

# Production observability validation
make test-metrics-e2e       # End-to-end metrics collection testing
make test-tracing-distributed # Distributed tracing validation
make test-alerts-integration  # Alerting system integration testing
make test-health-monitoring   # Health monitoring system validation
```

## 🏗️ ARCHITECTURE

### Design Philosophy

**Clean Architecture + Domain-Driven Design**: flext-observability implements enterprise observability patterns with clear separation between domain, application, and infrastructure layers.

**Railway-Oriented Programming**: All operations return `FlextResult[T]` for composable error handling.

**FLEXT Integration**: Complete flext-core 1.0.0 integration with dependency injection and service patterns.

### Module Organization

```
src/flext_observability/
├── __init__.py              # Public API exports (58 classes/functions)
├── __version__.py           # Version metadata
├── py.typed                 # Type marker for ecosystem
│
├── models.py                # FlextMetric, FlextTrace, FlextAlert, FlextHealthCheck
├── fields.py                # Pydantic field definitions and validation
├── constants.py             # Domain constants and enumerations
├── exceptions.py            # Exception hierarchy
├── typings.py               # Type definitions and protocols
├── protocols.py             # Interface definitions
│
├── services.py              # Core service implementations
├── factories.py             # Factory functions and master factory
├── monitoring.py            # Monitoring decorators and utilities
├── config.py                # Configuration management
│
├── alerting.py              # Alert management
├── health.py                # Health check utilities
├── logging.py               # Logging utilities
├── metrics.py               # Metrics collection
├── tracing.py               # Distributed tracing
├── utilities.py             # Helper functions
│
└── README.md                # Module documentation
```

**Key Module Dependencies**:
- `models.py` → Core domain entities (FlextMetric, FlextTrace, etc.)
- `services.py` → Business logic services with FlextResult patterns
- `factories.py` → Factory functions for easy API usage
- `monitoring.py` → Decorators and monitoring utilities
- All modules → Extend flext-core patterns (FlextResult, FlextContainer)

### Core Classes (Public API)

```python
from flext_observability import (
    # Domain Entities
    FlextMetric, FlextTrace, FlextAlert, FlextHealthCheck,

    # Services
    FlextObservabilityServices,

    # Factories & APIs
    flext_create_metric, flext_create_trace, flext_create_alert,
    flext_create_health_check, flext_create_log_entry,

    # Monitoring
    flext_monitor_function, FlextObservabilityMonitor,

    # Configuration
    FlextObservabilityConfig, FlextObservabilityConstants,

    # Types & Protocols
    FlextObservabilityTypes, FlextObservabilityProtocols,
)
```

### Design Patterns

#### 1. Railway Pattern with FlextResult[T]

ALL operations return `FlextResult[T]` for composable error handling:

```python
from flext_core import FlextResult
from flext_observability import flext_create_metric

# All operations return FlextResult
result = flext_create_metric("cpu_usage", 85.2, "percent")
if result.is_success:
    metric = result.unwrap()
else:
    print(f"Error: {result.error}")
```

#### 2. Domain Library Pattern

Each module exports exactly ONE main class with `Flext` prefix:

```python
# ✅ CORRECT - Single class per module
from flext_observability import FlextObservabilityServices

# Access nested functionality
metrics_service = FlextObservabilityServices.MetricsService()
```

#### 3. Factory Function API

Simple factory functions for easy integration:

```python
from flext_observability import (
    flext_create_metric,
    flext_create_trace,
    flext_create_alert,
)

# Easy-to-use factory functions
metric = flext_create_metric("api_requests", 42, "count")
trace = flext_create_trace("user_login", "auth-service")
alert = flext_create_alert("high_cpu", "warning", "CPU usage > 80%")
```

#### 4. Monitoring Decorator Pattern

Automatic instrumentation with decorators:

```python
from flext_observability import flext_monitor_function

@flext_monitor_function("business_operation")
def process_data(data: dict) -> dict:
    # Function automatically monitored for:
    # - Execution time metrics
    # - Success/failure traces
    # - Structured logging
    return {"processed": True}
```

## 🔗 OBSERVABILITY IMPORT STANDARDS (ECOSYSTEM COMPLIANCE)

### ✅ MANDATORY OBSERVABILITY IMPORT PATTERNS (ZERO TOLERANCE ENFORCEMENT)

**CORRECT - FLEXT Ecosystem Foundation Imports Only:**

```python
# ✅ FLEXT-OBSERVABILITY Foundation Imports (MANDATORY)
from flext_observability import FlextMetricsService, FlextTracingService
from flext_observability import FlextAlertService, FlextHealthService
from flext_observability import flext_create_metric, flext_create_trace
from flext_observability import FlextObservabilityMasterFactory, flext_monitor_function

# ✅ FLEXT Ecosystem Integration (REQUIRED)
from flext_core import FlextResult, FlextDomainService, get_logger
from flext_core import FlextContainer, FlextUtilities
from flext_cli import CLICommand, FlextCliApi
```

### ❌ ABSOLUTELY FORBIDDEN OBSERVABILITY IMPORTS (ECOSYSTEM VIOLATION)

**PROHIBITED - Direct Observability Library Imports:**

```python
# ❌ ZERO TOLERANCE VIOLATIONS - Direct observability library imports
import opentelemetry                    # FORBIDDEN: Use flext-observability foundation
import opentelemetry.trace             # FORBIDDEN: Use FlextTracingService
from opentelemetry import metrics      # FORBIDDEN: Use FlextMetricsService
from prometheus_client import Counter  # FORBIDDEN: Use FlextMetric entities
import logging                         # FORBIDDEN: Use FlextLogger from flext-core
import structlog                       # FORBIDDEN: Use flext-core logging patterns

# ❌ ARCHITECTURAL BOUNDARY VIOLATIONS
from flext_observability.services import FlextMetricsService  # WRONG: Use root imports
from flext_observability.models import FlextMetric           # WRONG: Use root imports
from flext_core.internal.logging import Logger              # WRONG: Internal modules
```

### 🏢 ENTERPRISE DEPENDENCY ARCHITECTURE (LEVEL-BASED CONSTRAINTS)

**ALLOWED Dependencies (Level 1 Foundation Only):**

**MANDATORY FLEXT Ecosystem Dependencies:**

- `flext-core>=0.9.9` - Foundation patterns, FlextResult, service base classes, logging
- `flext-cli>=0.9.9` - CLI patterns, command processing, and user interface

**EXTERNAL Observability Dependencies (Abstracted Through FLEXT):**

- `opentelemetry-api>=1.20.0` - OpenTelemetry tracing (INTERNAL USE ONLY - wrapped by FlextTracingService)
- `opentelemetry-sdk>=1.20.0` - OpenTelemetry SDK (INTERNAL USE ONLY - wrapped by observability services)
- `prometheus-client>=0.19.0` - Prometheus metrics (INTERNAL USE ONLY - wrapped by FlextMetricsService)
- `pydantic>=2.0.0` - Data validation and modeling for observability configurations

**ABSOLUTELY PROHIBITED Dependencies:**

- ❌ Same level (other Level 2) or higher level modules
- ❌ Direct OpenTelemetry/Prometheus usage for observability operations
- ❌ Custom logging implementations bypassing flext-core patterns
- ❌ Custom observability implementations bypassing flext-observability foundation

## 🏆 OBSERVABILITY QUALITY STANDARDS (ENTERPRISE AUTHORITY)

### Type Safety Standards

- **Pyrefly Strict Mode**: Required for all `src/` code (currently blocked by import issues)
- **Complete Type Annotations**: All public APIs fully typed with Python 3.13+ syntax
- **FlextResult[T] Pattern**: ALL operations return FlextResult for composable error handling
- **Pydantic v2 Models**: Data validation and type safety for all domain entities

```python
# ✅ CORRECT - Complete type annotations
from typing import Dict, List, Optional
from flext_core import FlextResult
from flext_observability import FlextMetric

async def collect_system_metrics(
    metric_names: List[str],
    collection_interval: float = 60.0
) -> FlextResult[List[FlextMetric]]:
    """Collect system metrics with complete type safety."""
    pass

# ❌ WRONG - Missing type annotations
def monitor_service(service, metrics):  # Missing types
    pass
```

### Code Quality Standards

- **Ruff Linting**: ZERO violations (currently not verified due to import issues)
- **Line Length**: 88 characters (Ruff default)
- **Import Organization**: Automatic sorting and organization
- **Complexity Limits**: Functions with complexity >10 require refactoring

### Testing Philosophy

**COMPREHENSIVE TEST SUITE** (481 test functions across 40 files):

- **Unit Tests**: Individual component testing with dependency injection
- **Integration Tests**: End-to-end observability pipeline testing
- **Domain Entity Tests**: Pydantic model validation and business logic
- **Factory Function Tests**: Simple API functionality verification
- **Service Layer Tests**: Business logic with FlextResult patterns

**Quality Targets**:
- **Coverage**: 100% requirement (currently untestable due to import issues)
- **Test Categories**: unit, integration, e2e, monitoring, metrics, tracing
- **Real Integration**: Tests use actual patterns, not excessive mocking

## 🎯 OBSERVABILITY DEVELOPMENT PATTERNS (ZERO TOLERANCE ENFORCEMENT)

### 📊 Observability Metrics Pattern (ENTERPRISE MONITORING AUTHORITY)

**CRITICAL**: These patterns demonstrate how FLEXT-OBSERVABILITY provides enterprise observability operations using MANDATORY FLEXT ecosystem integration for ALL monitoring needs.

### FlextResult Observability Pattern (ENTERPRISE ERROR HANDLING)

```python
# ✅ CORRECT - Observability operations with FlextResult from flext-core
from flext_core import FlextResult, get_logger
from flext_observability import FlextMetricsService, FlextMetric
import asyncio

async def enterprise_metrics_collection(service_name: str, metrics_config: Dict[str, object]) -> FlextResult[List[FlextMetric]]:
    """Enterprise metrics collection with proper error handling - NO try/except fallbacks."""
    logger = get_logger("observability_operations")

    # Input validation with early return
    if not service_name or not metrics_config:
        return FlextResult[List[FlextMetric]].fail("Invalid metrics collection configuration")

    # Use flext-observability exclusively for metrics operations - NO custom implementations
    metrics_service = FlextMetricsService()
    collected_metrics = []

    # Collect metrics through flext-observability foundation
    for metric_name, metric_config in metrics_config.items():
        from flext_observability import flext_create_metric
        metric_result = flext_create_metric(
            name=metric_name,
            value=metric_config.get("value", 0.0),
            unit=metric_config.get("unit", "count")
        )
        if metric_result.is_failure:
            return FlextResult[List[FlextMetric]].fail(f"Metric creation failed: {metric_result.error}")

        metric = metric_result.unwrap()

        # Record metric through flext-observability
        record_result = await metrics_service.record_metric(metric)
        if record_result.is_failure:
            return FlextResult[List[FlextMetric]].fail(f"Metric recording failed: {record_result.error}")

        collected_metrics.append(metric)

    return FlextResult[List[FlextMetric]].ok(collected_metrics)

# ❌ ABSOLUTELY FORBIDDEN - Custom observability implementations in ecosystem projects
# import prometheus_client  # ZERO TOLERANCE VIOLATION
# import opentelemetry.trace  # ZERO TOLERANCE VIOLATION
# custom_counter = prometheus_client.Counter(...)  # FORBIDDEN - use FlextMetricsService
```

### Distributed Tracing Pattern (ENTERPRISE OBSERVABILITY)

```python
# ✅ CORRECT - Distributed tracing using FLEXT observability foundation
from flext_core import FlextDomainService, FlextResult, get_logger
from flext_observability import FlextTracingService, FlextTrace
from flext_observability import flext_create_trace, flext_monitor_function
import asyncio
from typing import Dict, object, List

class EnterpriseObservabilityService(FlextDomainService):
    """Enterprise observability service using FLEXT foundation - NO custom implementations."""

    def __init__(self, service_name: str) -> None:
        super().__init__()
        self._logger = get_logger("enterprise_observability")
        self._service_name = service_name
        self._tracing_service = FlextTracingService()

    async def create_distributed_trace(self, operation_name: str, trace_context: Dict[str, object]) -> FlextResult[FlextTrace]:
        """Create distributed trace using flext-observability foundation exclusively."""

        # Distributed tracing through flext-observability
        try:
            trace_result = flext_create_trace(
                name=operation_name,
                operation=f"{self._service_name}.{operation_name}",
                context=trace_context
            )
            if trace_result.is_failure:
                return FlextResult[FlextTrace].fail(f"Trace creation failed: {trace_result.error}")

            trace = trace_result.unwrap()

            # Start tracing through flext-observability patterns
            start_result = await self._tracing_service.start_trace(trace)
            if start_result.is_failure:
                return FlextResult[FlextTrace].fail(f"Trace start failed: {start_result.error}")

            return FlextResult[FlextTrace].ok(trace)
        except Exception as e:
            return FlextResult[FlextTrace].fail(f"Distributed tracing creation failed: {e}")

    @flext_monitor_function("service_processing")
    async def process_monitored_operation(self, operation_data: Dict[str, object]) -> FlextResult[Dict[str, object]]:
        """Process operation with automatic monitoring using flext-observability patterns."""

        # Create trace for operation
        trace_result = await self.create_distributed_trace("process_operation", operation_data)
        if trace_result.is_failure:
            return FlextResult[Dict[str, object]].fail(f"Trace creation failed: {trace_result.error}")

        trace = trace_result.unwrap()

        try:
            # Business logic with distributed tracing
            processing_result = await self._process_business_logic(operation_data)

            # Record metrics through flext-observability
            from flext_observability import flext_create_metric
            metric_result = flext_create_metric(
                name=f"{self._service_name}.operations",
                value=1.0,
                unit="count"
            )
            if metric_result.is_success:
                metric = metric_result.unwrap()
                await FlextMetricsService().record_metric(metric)

            # Complete trace through flext-observability
            complete_result = await self._tracing_service.complete_trace(trace)
            if complete_result.is_failure:
                self._logger.warning(f"Trace completion failed: {complete_result.error}")

            return FlextResult[Dict[str, object]].ok({
                "operation": operation_data.get("operation", "unknown"),
                "result": processing_result,
                "trace_id": trace.trace_id,
                "success": True
            })
        except Exception as e:
            # Error trace through flext-observability
            error_result = await self._tracing_service.error_trace(trace, str(e))
            if error_result.is_failure:
                self._logger.warning(f"Error trace failed: {error_result.error}")

            return FlextResult[Dict[str, object]].fail(f"Monitored operation failed: {e}")

    async def _process_business_logic(self, data: Dict[str, object]) -> object:
        """Business logic processing."""
        # Simulate processing
        await asyncio.sleep(0.1)
        return {"processed": True, "data": data}

# ❌ ABSOLUTELY FORBIDDEN - Custom tracing implementations bypassing FLEXT
# from opentelemetry import trace  # ZERO TOLERANCE VIOLATION - use FlextTracingService
# tracer = trace.get_tracer(__name__)  # FORBIDDEN - use flext-observability
```

### Alerting and Health Monitoring Pattern (ENTERPRISE ALERTING)

```python
# ✅ CORRECT - Alerting using flext-observability alerting foundation
from flext_core import FlextResult, get_logger
from flext_observability import FlextAlertService, FlextHealthService
from flext_observability import flext_create_alert, FlextAlert, FlextHealthCheck
import asyncio
from typing import Dict, List, Optional

class EnterpriseAlertingService:
    """Enterprise alerting service using flext-observability alerting foundation."""

    def __init__(self) -> None:
        self._logger = get_logger("enterprise_alerting")
        self._alert_service = FlextAlertService()
        self._health_service = FlextHealthService()

    async def create_system_alert(self, alert_config: Dict[str, object]) -> FlextResult[FlextAlert]:
        """Create system alert using flext-observability alerting patterns."""

        try:
            # Use flext-observability alerting factory - NO direct alerting systems
            alert_result = flext_create_alert(
                name=alert_config["name"],
                severity=alert_config.get("severity", "warning"),
                message=alert_config["message"],
                source=alert_config.get("source", "system")
            )
            if alert_result.is_failure:
                return FlextResult[FlextAlert].fail(f"Alert creation failed: {alert_result.error}")

            alert = alert_result.unwrap()

            return FlextResult[FlextAlert].ok(alert)
        except Exception as e:
            return FlextResult[FlextAlert].fail(f"System alert creation failed: {e}")

    async def monitor_system_health(self, health_checks: List[str]) -> FlextResult[List[FlextHealthCheck]]:
        """Monitor system health using flext-observability health patterns."""

        health_results = []

        try:
            # Start health monitoring through flext-observability
            for check_name in health_checks:
                from flext_observability import flext_create_health_check

                health_result = flext_create_health_check(
                    name=check_name,
                    status="healthy",
                    details={"checked_at": "now", "component": check_name}
                )
                if health_result.is_failure:
                    self._logger.warning(f"Health check creation failed: {health_result.error}")
                    continue

                health_check = health_result.unwrap()

                # Execute health check through flext-observability
                check_result = await self._health_service.execute_health_check(health_check)
                if check_result.is_failure:
                    self._logger.warning(f"Health check execution failed: {check_result.error}")
                    continue

                executed_check = check_result.unwrap()
                health_results.append(executed_check)

            return FlextResult[List[FlextHealthCheck]].ok(health_results)
        except Exception as e:
            return FlextResult[List[FlextHealthCheck]].fail(f"System health monitoring failed: {e}")

    async def process_alert_escalation(self, alert: FlextAlert, escalation_config: Dict[str, object]) -> FlextResult[Dict[str, object]]:
        """Process alert escalation using flext-observability alert management."""

        try:
            # Process alert through flext-observability
            process_result = await self._alert_service.process_alert(alert)
            if process_result.is_failure:
                return FlextResult[Dict[str, object]].fail(f"Alert processing failed: {process_result.error}")

            processed_alert = process_result.unwrap()

            # Handle escalation through flext-observability patterns
            escalation_result = await self._alert_service.escalate_alert(
                processed_alert,
                escalation_config
            )
            if escalation_result.is_failure:
                return FlextResult[Dict[str, object]].fail(f"Alert escalation failed: {escalation_result.error}")

            escalated_alert = escalation_result.unwrap()

            return FlextResult[Dict[str, object]].ok({
                "alert_id": alert.alert_id,
                "escalated": True,
                "escalation_level": escalation_config.get("level", 1),
                "processed_at": "now",
                "success": True
            })
        except Exception as e:
            return FlextResult[Dict[str, object]].fail(f"Alert escalation processing failed: {e}")

# Usage pattern for enterprise alerting
async def create_enterprise_alerting_service() -> FlextResult[EnterpriseAlertingService]:
    """Create enterprise alerting service using flext-observability patterns."""
    alerting_service = EnterpriseAlertingService()

    return FlextResult[EnterpriseAlertingService].ok(alerting_service)

# ❌ ABSOLUTELY FORBIDDEN - Custom alerting implementations bypassing flext-observability
# import smtplib  # ZERO TOLERANCE VIOLATION - use flext-observability alerting
# def send_custom_alert(message):  # FORBIDDEN - use FlextAlertService
#     pass
```

## 📊 CURRENT STATUS (v0.9.0)

### What Works

- ✅ **Complete Module Architecture**: 21 Python modules with clean separation
- ✅ **Domain Entities**: FlextMetric, FlextTrace, FlextAlert, FlextHealthCheck with validation
- ✅ **Service Layer**: Comprehensive services with dependency injection
- ✅ **Factory Functions**: Simple API (flext_create_*) for easy integration
- ✅ **Monitoring Decorators**: @flext_monitor_function for automatic instrumentation
- ✅ **Type Safety**: Pydantic v2 models with Python 3.13+ annotations
- ✅ **Railway Pattern**: All operations return FlextResult[T]
- ✅ **Test Suite**: 481 test functions across 40 test files (comprehensive coverage)
- ✅ **Documentation**: Complete docs structure with API guides

### Current Issues

- ⚠️ **Import Compatibility**: flext-core import issues (T not exported from __init__.py)
- ⚠️ **Test Execution**: All tests failing due to import errors (33 errors during collection)
- ⚠️ **Type Checking**: Blocked by import issues (cannot run Pyrefly)
- ⚠️ **Integration Testing**: Cannot execute due to import failures

### Quality Metrics

- **Test Functions**: 481 (across 40 files)
- **Modules**: 21 Python files in src/flext_observability/
- **Coverage Requirement**: 100% (currently untestable)
- **Type Safety**: Complete annotations (currently uncheckable)
- **Linting**: Ruff compliance (not verified due to import issues)

### Development Priorities

#### Phase 1: Fix Import Issues (CRITICAL)
- Fix flext-core import compatibility (T export issue)
- Resolve circular import dependencies
- Enable test execution and type checking

#### Phase 2: Quality Validation
- Achieve 100% test coverage
- Complete Pyrefly strict mode compliance
- Zero Ruff linting violations

#### Phase 3: Feature Completion
- Complete monitoring stack integration
- Add real OpenTelemetry/Prometheus integration
- Implement distributed tracing

## 🚀 OBSERVABILITY DEVELOPMENT WORKFLOW (ENTERPRISE PRODUCTION STANDARDS)

### 🔍 PRE-DEVELOPMENT VALIDATION (MANDATORY FIRST STEPS)

**1. Observability Ecosystem Status Check:**

```bash
# MANDATORY - Verify current observability foundation status
make check                    # Quick validation (lint + type + observability-config)
make observability-validate   # Observability stack configuration validation
make test-fast               # Observability functionality verification without coverage
```

**2. Enterprise Observability Architecture Understanding:**

```bash
# Review FLEXT ecosystem observability dependencies
grep -r "from flext_" src/ --include="*.py" | sort | uniq

# Understand observability integration patterns
cat src/flext_observability/services.py | head -50

# Review monitoring abstractions
cat src/flext_observability/monitoring.py | head -50

# Check factory implementations
cat src/flext_observability/factories.py | head -50
```

**3. Production Observability Environment Verification:**

```bash
# Verify monitoring stack components
docker ps | grep -E "(prometheus|grafana|jaeger)"  # Check running monitoring services
ls -la docker-compose.monitoring.yml             # Monitoring stack configuration

# Test observability integration
make prometheus-start         # Start Prometheus metrics collection
make grafana-setup           # Setup Grafana dashboards
make test-observability      # Observability stack validation
```

### ⚡ DURING OBSERVABILITY DEVELOPMENT (PRODUCTION PATTERNS)

**1. FlextResult Observability Pattern Compliance (MANDATORY):**

```python
# ✅ CORRECT - ALL observability operations use FlextResult pattern
from flext_core import FlextResult
from flext_observability import FlextMetricsService, FlextTracingService

async def collect_monitor_alert(
    service_name: str,
    metrics_config: Dict[str, object],
    alert_thresholds: Dict[str, float]
) -> FlextResult[Dict[str, object]]:
    """Complete observability pipeline with railway-oriented programming."""
    metrics_service = FlextMetricsService()
    tracing_service = FlextTracingService()

    # Metrics collection phase with FlextResult chaining
    metrics_result = await metrics_service.collect_metrics(service_name, metrics_config)
    if metrics_result.is_failure:
        return FlextResult[Dict[str, object]].fail(f"Metrics collection failed: {metrics_result.error}")

    # Distributed tracing phase with FlextResult chaining
    tracing_result = await tracing_service.start_trace(f"{service_name}_monitoring")
    if tracing_result.is_failure:
        return FlextResult[Dict[str, object]].fail(f"Tracing failed: {tracing_result.error}")

    # Alert evaluation phase with FlextResult chaining
    alert_result = await evaluate_alert_thresholds(metrics_result.unwrap(), alert_thresholds)
    if alert_result.is_failure:
        return FlextResult[Dict[str, object]].fail(f"Alert evaluation failed: {alert_result.error}")

    return FlextResult[Dict[str, object]].ok({
        "collected_metrics": metrics_result.unwrap(),
        "trace_id": tracing_result.unwrap(),
        "alerts_triggered": alert_result.unwrap()
    })

# ❌ WRONG - Try/except fallbacks for observability operations
try:
    result = collect_metrics()  # FORBIDDEN - use FlextResult
except Exception as e:
    return {"error": str(e)}  # FORBIDDEN - use FlextResult.fail()
```

**2. Real Observability Integration (PRODUCTION REQUIREMENT):**

```python
# ✅ CORRECT - Direct observability integration through FLEXT abstractions
from flext_observability import FlextMetricsService, FlextTracingService, flext_monitor_function

@flext_monitor_function("critical_business_operation")
async def monitored_business_operation(operation_data: Dict[str, object]) -> FlextResult[object]:
    """Business operation with comprehensive observability."""
    metrics_service = FlextMetricsService()

    # Real observability operations
    await metrics_service.record_metric("operation_start", 1.0, "count")
    result = await execute_business_logic(operation_data)
    await metrics_service.record_metric("operation_success", 1.0, "count")

    return FlextResult[object].ok(result)

# ❌ WRONG - Mocked observability operations
@patch('prometheus_client.Counter')  # FORBIDDEN - use real observability
def test_fake_monitoring(): pass
```

**3. Incremental Observability Quality Validation:**

```bash
# Run after each significant change
make lint                     # Ruff validation with observability-specific rules
make type-check              # MyPy strict mode validation
make test-unit               # Unit tests for observability components
make observability-validate  # Observability configuration validation
```

### ✅ PRE-COMMIT OBSERVABILITY VALIDATION (ZERO TOLERANCE QUALITY GATES)

**MANDATORY Pre-Commit Checklist (100% PASS REQUIRED):**

```bash
# PHASE 1: Complete Observability Validation Pipeline (CRITICAL)
make validate                 # Complete: lint + type + security + test + observability

# PHASE 2: Observability-Specific Validation (MANDATORY)
echo "=== OBSERVABILITY FOUNDATION VALIDATION ==="

# 1. Verify ZERO custom OpenTelemetry/Prometheus imports
custom_imports=$(find src/ -name "*.py" -exec grep -l "import opentelemetry\|import prometheus_client\|import logging" {} \; 2>/dev/null)
if [ -n "$custom_imports" ]; then
    echo "❌ CRITICAL: Custom observability imports found - use flext-observability foundation"
    echo "$custom_imports"
    exit 1
fi

# 2. Validate observability services integration
python -c "
from flext_observability import FlextMetricsService, FlextTracingService, FlextAlertService
metrics = FlextMetricsService()
tracing = FlextTracingService()
alerts = FlextAlertService()
print('✅ Observability services creation successful')
"

# 3. Verify monitoring factory functionality
python -c "
from flext_observability import FlextObservabilityMasterFactory, get_global_factory
from flext_observability import flext_create_metric, flext_create_trace
factory = get_global_factory()
metric_result = flext_create_metric('test_metric', 1.0, 'count')
trace_result = flext_create_trace('test_trace', 'test_operation')
print('✅ Observability factory functionality validated')
"

# 4. Validate monitoring decorators
python -c "
from flext_observability import flext_monitor_function
@flext_monitor_function('test_function')
def test_func():
    return 'monitored'
print('✅ Monitoring decorators validated')
"

echo "✅ Observability foundation validation COMPLETED"

# PHASE 3: Observability Test Coverage Validation (90%+ REQUIRED)
make test                    # 90%+ coverage with real observability APIs
pytest --cov=src/flext_observability --cov-fail-under=90

# PHASE 4: Architecture Compliance (ENTERPRISE STANDARDS)
# No internal imports - use only root module imports
internal_imports=$(find src/ -name "*.py" -exec grep -l "from flext_observability\.[a-z]" {} \; 2>/dev/null)
if [ -n "$internal_imports" ]; then
    echo "❌ ARCHITECTURE VIOLATION: Internal module imports found"
    echo "$internal_imports"
    echo "RESOLUTION: Use root imports - from flext_observability import ClassName"
    exit 1
fi
```

## 🌐 PRODUCTION OBSERVABILITY ENVIRONMENT SETUP

### 🔧 ESSENTIAL OBSERVABILITY ENVIRONMENT VARIABLES (PRODUCTION CONFIGURATION)

```bash
# MANDATORY Observability Environment Configuration
export OTEL_SERVICE_NAME=flext-observability          # OpenTelemetry service name
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317  # OTLP endpoint
export PROMETHEUS_PUSH_GATEWAY=http://localhost:9091     # Prometheus push gateway

# FLEXT Ecosystem Integration
export PYTHONPATH=$(PWD)/src:$(PYTHONPATH)           # Python path for development
export FLEXT_LOG_LEVEL=INFO                          # FLEXT ecosystem logging
export FLEXT_ENVIRONMENT=development                 # FLEXT environment mode

# Monitoring Stack Configuration
export GRAFANA_URL=http://localhost:3000             # Grafana dashboard URL
export JAEGER_AGENT_HOST=localhost                   # Jaeger tracing agent
export JAEGER_AGENT_PORT=6831                        # Jaeger agent port
export ALERTMANAGER_URL=http://localhost:9093        # Alert Manager URL
```

### 🏗️ ENTERPRISE VIRTUAL ENVIRONMENT (FLEXT WORKSPACE INTEGRATION)

```bash
# MANDATORY - Use FLEXT workspace virtual environment
cd ..                          # Navigate to FLEXT workspace
source .venv/bin/activate                        # Activate shared virtual environment
cd flext-observability                          # Navigate to observability project

# Enterprise development setup
make install-dev                                # Install development dependencies
make setup                                      # Complete environment setup
make observability-init                         # Initialize observability stack
```

### 📊 MONITORING STACK SETUP (PRODUCTION OBSERVABILITY)

```bash
# MANDATORY - Production monitoring stack deployment
make prometheus-start                            # Start Prometheus metrics collection
make grafana-setup                              # Setup Grafana dashboards and data sources
make jaeger-start                               # Start Jaeger distributed tracing
make alertmanager-config                        # Configure alert manager integration

# Verify monitoring stack health
curl http://localhost:9090/api/v1/query?query=up  # Prometheus health
curl http://localhost:3000/api/health             # Grafana health
curl http://localhost:16686/api/services          # Jaeger health
```

### 📚 CRITICAL OBSERVABILITY DEVELOPMENT FILES (UNDERSTANDING FOUNDATION)

**MANDATORY Reading for Observability Development:**

**Foundation Architecture:**

- `src/flext_observability/__init__.py` - Complete module exports and FLEXT ecosystem integration
- `src/flext_observability/services.py` - FlextMetricsService, FlextTracingService, FlextAlertService
- `src/flext_observability/models.py` - FlextMetric, FlextTrace, FlextAlert, FlextHealthCheck entities

**Observability Implementations:**

- `src/flext_observability/factories.py` - FlextObservabilityMasterFactory (monitoring creation)
- `src/flext_observability/monitoring.py` - FlextObservabilityMonitor, flext_monitor_function
- `src/flext_observability/api.py` - Simple API (flext_create_metric, flext_create_trace)

**Production Testing:**

- `tests/test_*_complete.py` - Comprehensive real observability API tests
- `tests/integration/` - Integration tests with real OpenTelemetry/Prometheus operations
- `tests/e2e/` - End-to-end observability stack testing

**Monitoring Configuration:**

- `docker-compose.monitoring.yml` - Complete monitoring stack (Prometheus, Grafana, Jaeger)
- `grafana/dashboards/` - Production Grafana dashboards for FLEXT ecosystem
- `prometheus/prometheus.yml` - Prometheus configuration for FLEXT services

---

## 📚 KEY DEVELOPMENT FILES

**MANDATORY Reading for flext-observability Development:**

**Core Architecture:**
- `src/flext_observability/__init__.py` - Complete public API exports (58 items)
- `src/flext_observability/models.py` - Domain entities (FlextMetric, FlextTrace, etc.)
- `src/flext_observability/services.py` - Service layer implementations
- `src/flext_observability/factories.py` - Factory functions and simple API

**Development Patterns:**
- `src/flext_observability/monitoring.py` - Monitoring decorators and utilities
- `tests/test_simple.py` - Basic functionality verification (89 test functions)
- `examples/01_functional.py` - Working examples and usage patterns

**Configuration:**
- `pyproject.toml` - Poetry dependencies and build configuration
- `Makefile` - Complete development workflow and quality gates

## 🎯 SUMMARY

**FLEXT-OBSERVABILITY v0.9.0** - Enterprise observability foundation with comprehensive patterns and domain-driven design.

**CURRENT STATUS**: Complete architecture with import compatibility issues blocking validation.

**CRITICAL NEXT STEPS**:
1. **Fix Import Issues**: Resolve flext-core compatibility (T export)
2. **Enable Testing**: Achieve 100% test coverage with 481 test functions
3. **Complete Integration**: Add real OpenTelemetry/Prometheus monitoring stack

**ARCHITECTURAL STRENGTHS**:
- ✅ Complete Clean Architecture implementation
- ✅ Railway-oriented programming with FlextResult[T]
- ✅ Domain-Driven Design with rich domain entities
- ✅ Type safety with Python 3.13+ annotations
- ✅ Comprehensive test suite (481 functions across 40 files)

**QUALITY STANDARDS**:
- **Type Safety**: Pyrefly strict mode (currently blocked)
- **Test Coverage**: 100% requirement (currently untestable)
- **Code Quality**: Ruff compliance (currently unverified)
- **FLEXT Integration**: Complete flext-core patterns usage

---

**FLEXT-OBSERVABILITY AUTHORITY**: Enterprise observability foundation for the FLEXT ecosystem with zero tolerance for custom implementations.

**DEVELOPMENT STATUS**: Architecture complete, validation blocked by import issues, comprehensive test suite ready for execution.

---

## Pydantic v2 Compliance Standards

**Status**: ✅ Fully Pydantic v2 Compliant
**Verified**: October 22, 2025 (Phase 7 Ecosystem Audit)

### Verification

```bash
make audit-pydantic-v2     # Expected: Status: PASS, Violations: 0
```

### Reference

- **Complete Guide**: `../flext-core/docs/pydantic-v2-modernization/PYDANTIC_V2_STANDARDS_GUIDE.md`
- **Phase 7 Report**: `../flext-core/docs/pydantic-v2-modernization/PHASE_7_COMPLETION_REPORT.md`
