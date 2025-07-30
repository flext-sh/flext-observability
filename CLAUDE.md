# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLEXT Observability is a foundation library within the FLEXT ecosystem providing comprehensive monitoring, metrics, tracing, and health check capabilities. Built with Python 3.13+ and implementing Clean Architecture patterns, it integrates with OpenTelemetry, Prometheus, Jaeger, and structured logging to deliver enterprise-grade observability infrastructure.

This project serves as the centralized observability layer for all FLEXT ecosystem components, providing consistent monitoring patterns and telemetry collection across the entire distributed data integration platform.

## Core Architecture

### Domain Structure
- **Entities**: Core observability models (FlextMetric, FlextTrace, FlextAlert, FlextLogEntry, FlextHealthCheck)
- **Services**: Business logic for metrics, tracing, logging, alerting, and health monitoring
- **Factories**: Creation patterns for observability components with dependency injection
- **Monitors**: Decorators and utilities for automatic monitoring integration
- **Platform**: Unified observability platform orchestrating all monitoring components

### Key Components
- **FlextObservabilityPlatformV2**: Main platform orchestrating all observability services
- **FlextObservabilityMasterFactory**: Central factory for creating observability entities
- **FlextObservabilityMonitor**: Function decorators for automatic monitoring
- **Simple API**: Easy-to-use functions for quick observability integration

### Dependencies
- **flext-core**: Foundation library providing FlextEntity, FlextResult, FlextContainer patterns
- **OpenTelemetry**: Distributed tracing and metrics collection
- **Prometheus**: Metrics storage and alerting
- **Structured Logging**: JSON-structured logging with correlation IDs

## Development Commands

### Essential Commands
```bash
# Quick quality check (run before committing)
make check                   # Lint + type check + test

# Complete validation (zero tolerance)
make validate               # Lint + type + security + test (90% coverage)

# Individual quality gates
make lint                   # Ruff linting (ALL rules enabled)
make type-check             # MyPy strict mode (zero errors tolerated)
make test                   # Pytest with 90% coverage requirement
make security               # Bandit + pip-audit + secrets scan
```

### Testing Commands
```bash
# Run specific test types
make test-unit              # Unit tests only
make test-integration       # Integration tests only
make test-monitoring        # Monitoring-specific tests

# Coverage reporting
make coverage               # Generate detailed coverage report
make coverage-html          # Generate HTML coverage report

# Test specific components
pytest tests/test_entities_simple.py -v        # Test entities
pytest tests/test_services_simple.py -v        # Test services
pytest tests/test_factory_complete.py -v       # Test factory patterns
```

### Development Setup
```bash
# Complete development setup
make setup                  # Install dependencies + pre-commit hooks
make dev-install           # Development environment setup
make install               # Install dependencies only

# Development tools
make format                # Format code with ruff
make fix                   # Auto-fix all issues (format + lint)
```

### Observability Operations
```bash
# Monitoring stack setup
make setup-prometheus      # Configure Prometheus
make setup-grafana         # Configure Grafana dashboards
make setup-jaeger          # Configure Jaeger tracing
make setup-elastic         # Configure Elasticsearch logging
make setup-all-monitoring  # Complete monitoring stack

# Stack operations
make start-monitoring      # Start monitoring stack (Docker Compose)
make stop-monitoring       # Stop monitoring stack
make monitoring-status     # Check stack status

# Telemetry testing
make test-metrics          # Test metrics collection
make test-tracing          # Test distributed tracing
make test-logging          # Test structured logging
make validate-telemetry    # Validate all telemetry components
```

### Health & Diagnostics
```bash
# System diagnostics
make diagnose              # Complete system diagnostics
make health-check          # Comprehensive health check
make info                  # Project information

# Performance testing
make monitoring-performance # Test monitoring performance
make metrics-benchmark     # Benchmark metrics collection
```

## Architecture Patterns

### Entity Creation
Use factory functions for consistent entity creation:
```python
# Simple API (recommended for basic usage)
from flext_observability import flext_create_metric, flext_create_trace

metric_result = flext_create_metric("cpu_usage", 85.2, "percent")
trace_result = flext_create_trace("user_request", "processing_order")

# Factory pattern (for advanced usage)
from flext_observability import get_global_factory
factory = get_global_factory()
metric_result = factory.create_metric("memory_usage", 1024, "MB")
```

### Service Integration
Services follow flext-core patterns with FlextResult:
```python
from flext_observability import FlextMetricsService
from flext_core import FlextContainer

# Initialize with dependency injection
container = FlextContainer()
metrics_service = FlextMetricsService(container)

# All operations return FlextResult
result = metrics_service.record_metric(metric)
if result.is_success:
    print(f"Recorded: {result.value.name}")
```

### Monitoring Decorators
Use `@flext_monitor_function` for automatic function monitoring:
```python
from flext_observability import flext_monitor_function

@flext_monitor_function("data_processing")
def process_data(data):
    # Function automatically monitored for:
    # - Execution time metrics
    # - Success/failure traces
    # - Structured logging
    return processed_data
```

## Testing Strategy

### Test Organization
- **Unit Tests**: `/tests/unit/` - Test individual components in isolation
- **Integration Tests**: `/tests/integration/` - Test service interactions
- **E2E Tests**: `/tests/e2e/` - Test complete observability workflows
- **Coverage Tests**: Multiple coverage test files ensuring 90%+ coverage

### Test Fixtures
The `conftest.py` provides comprehensive fixtures:
- OpenTelemetry tracing setup with in-memory exporters
- Prometheus metrics registry
- Health checkers and metrics collectors
- Async test utilities

### Coverage Requirements
- **Minimum**: 90% test coverage (enforced by `make test`)
- **Target**: 95%+ coverage for critical observability components
- **Reports**: HTML coverage reports generated in `htmlcov/`

## Code Quality Standards

### Zero Tolerance Quality Gates
All code must pass strict quality gates:
- **Ruff**: ALL rule categories enabled (17+ categories)
- **MyPy**: Strict mode with zero errors tolerated
- **Bandit**: Security scanning for vulnerabilities
- **Pre-commit**: Automated hooks prevent bad commits

### Type Safety
- Python 3.13 with full type hints
- Strict MyPy configuration (no `Any` types allowed)
- Pydantic models for runtime type validation
- Generic types for FlextResult patterns

## Integration with FLEXT Ecosystem

### Dependency Flow
- **Depends on**: `flext-core` (foundation patterns)
- **Used by**: All FLEXT services and applications
- **Provides**: Centralized observability for the entire ecosystem

### Telemetry Standards
- **Metrics**: Prometheus-compatible metrics with consistent naming
- **Tracing**: OpenTelemetry spans with correlation IDs
- **Logging**: Structured JSON logs with contextual information
- **Health**: Standardized health check endpoints

## Common Workflows

### Adding New Observability Entities
1. Define entity in `src/flext_observability/entities.py`
2. Extend base `FlextEntity` from flext-core
3. Implement `validate_domain_rules()` method
4. Add factory methods to `factory.py`
5. Create corresponding service in `services.py`
6. Add comprehensive tests with 90%+ coverage

### Integrating Observability in FLEXT Services
1. Import observability components: `from flext_observability import ...`
2. Use simple API for quick integration: `flext_create_metric()`
3. Use services for advanced scenarios: `FlextMetricsService`
4. Apply monitoring decorators: `@flext_monitor_function`
5. Test telemetry integration thoroughly

### Debugging Observability Issues
1. Check service health: `make health-check`
2. Validate telemetry: `make validate-telemetry`  
3. Run diagnostics: `make diagnose`
4. Check monitoring stack: `make monitoring-status`
5. Review logs and metrics in Grafana/Prometheus

## Environment Configuration

### Required Environment Variables
```bash
# OpenTelemetry settings
export OTEL_SERVICE_NAME=flext-observability
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus settings  
export PROMETHEUS_ENDPOINT=http://localhost:9090
export PROMETHEUS_PUSH_GATEWAY=http://localhost:9091

# Jaeger settings
export JAEGER_COLLECTOR_ENDPOINT=http://localhost:14268/api/traces
```

### Docker Integration
- **Base Image**: python:3.13-slim
- **Exposed Port**: 9090 (metrics endpoint)
- **Health Check**: Built-in metrics endpoint health check
- **Security**: Non-root user execution

## Troubleshooting

### Common Issues
- **Import Errors**: Ensure `flext-core` dependency is installed
- **Type Errors**: Run `make type-check` for detailed MyPy output
- **Test Failures**: Check coverage with `make coverage-html`
- **Monitoring Stack**: Verify Docker Compose services are running

### Performance Optimization
- Use efficient metric collection patterns
- Implement sampling for high-volume tracing
- Optimize logging levels for production
- Monitor observability overhead with built-in benchmarks

## TODO: GAPS DE ARQUITETURA IDENTIFICADOS - PRIORIDADE ALTA

### 🚨 GAP 1: Monitoring Stack Integration Gap
**Status**: ALTO - Stack de monitoramento não integrado com deployment ecosystem
**Problema**:
- Prometheus, Grafana, Jaeger setup manual não integrado com Docker Compose workspace
- Monitoring stack não configurado automaticamente para todos os 32 services
- Dashboards não auto-gerados para ecosystem services

**TODO**:
- [ ] Integrar monitoring stack com workspace Docker Compose
- [ ] Criar auto-discovery de services para monitoring
- [ ] Implementar dashboard templates para cada tipo de service FLEXT
- [ ] Documentar monitoring integration patterns para novos services

### 🚨 GAP 2: Cross-Service Correlation Missing
**Status**: ALTO - Correlation IDs não propagados entre services
**Problema**:
- Correlation IDs mencionados mas sem cross-service propagation
- Distributed tracing não conecta FlexCore (Go) ↔ FLEXT (Python) ↔ outros services
- Request tracking não end-to-end

**TODO**:
- [ ] Implementar correlation ID propagation via HTTP headers
- [ ] Criar tracing integration entre Go e Python services
- [ ] Documentar distributed tracing patterns para ecosystem
- [ ] Implementar request flow visualization tools

### 🚨 GAP 3: Metrics Standardization Inconsistent
**Status**: ALTO - Métricas não padronizadas entre services
**Problema**:
- Naming conventions não definidas para ecosystem metrics
- Business metrics não diferenciadas de system metrics
- SLA/SLO tracking não implementado

**TODO**:
- [ ] Definir metric naming conventions para ecosystem
- [ ] Criar business metrics framework
- [ ] Implementar SLA/SLO tracking e alerting
- [ ] Documentar metrics best practices para development teams