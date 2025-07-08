# FLEXT-OBSERVABILITY Makefile - Enterprise Monitoring & Observability
# ====================================================================

.PHONY: help install test clean lint format build docs metrics health trace monitor dashboard

# Default target
help: ## Show this help message
	@echo "📊 FLEXT-OBSERVABILITY - Enterprise Monitoring & Observability"
	@echo "============================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'

# Installation & Setup
install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies for flext-observability..."
	poetry install --all-extras

install-dev: ## Install with dev dependencies
	@echo "🛠️  Installing dev dependencies..."
	poetry install --all-extras --group dev --group test --group monitoring

# Prometheus Metrics Server
metrics-server: ## Start Prometheus metrics server
	@echo "📊 Starting Prometheus metrics server..."
	@mkdir -p /tmp/prometheus_multiproc
	poetry run python -c "
from flext_observability.prometheus_metrics import PrometheusServer
import asyncio

async def main():
    server = PrometheusServer(port=9090)
    print('🚀 Prometheus metrics server starting on port 9090...')
    print('📊 Metrics endpoint: http://localhost:9090/metrics')
    print('Press Ctrl+C to stop')
    await server.start()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('\\n🛑 Metrics server stopped')
"

metrics-test: ## Test metrics collection
	@echo "🧪 Testing metrics collection..."
	poetry run python -c "
from flext_observability.metrics import SystemMetrics, BusinessMetrics
import time

# Test system metrics
system_metrics = SystemMetrics()
print('📊 System Metrics:')
print(f'  CPU Usage: {system_metrics.get_cpu_usage():.1f}%')
print(f'  Memory Usage: {system_metrics.get_memory_usage():.1f}%')
print(f'  Disk Usage: {system_metrics.get_disk_usage():.1f}%')

# Test business metrics
business_metrics = BusinessMetrics()
print('\\n💼 Business Metrics:')
pipeline_metrics = business_metrics.get_pipeline_metrics('test-pipeline')
print(f'  Success Rate: {pipeline_metrics[\"success_rate\"]:.1f}%')
print(f'  Avg Duration: {pipeline_metrics[\"average_duration\"]:.1f}s')

print('\\n✅ Metrics collection test complete')
"

metrics-export: ## Export current metrics to file
	@echo "📤 Exporting metrics..."
	@mkdir -p reports/metrics
	poetry run python -c "
from flext_observability.prometheus_metrics import PrometheusExporter
from datetime import datetime

exporter = PrometheusExporter()
metrics_data = exporter.collect_all_metrics()

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'reports/metrics/metrics_export_{timestamp}.txt'

with open(filename, 'w') as f:
    f.write(metrics_data)

print(f'📊 Metrics exported to {filename}')
"

# Health Monitoring
health-check: ## Run comprehensive health checks
	@echo "💓 Running health checks..."
	poetry run python -c "
from flext_observability.health import HealthChecker
import asyncio

async def main():
    checker = HealthChecker()
    
    print('💓 Running comprehensive health checks...')
    
    # Add system checks
    checker.add_check('cpu', lambda: checker.check_cpu_usage())
    checker.add_check('memory', lambda: checker.check_memory_usage())
    checker.add_check('disk', lambda: checker.check_disk_usage())
    
    # Run all checks
    results = await checker.check_all()
    
    print('\\n📋 Health Check Results:')
    for check_name, result in results.items():
        status = '✅' if result.healthy else '❌'
        print(f'  {status} {check_name}: {result.message}')
    
    overall_status = '✅ HEALTHY' if all(r.healthy for r in results.values()) else '❌ UNHEALTHY'
    print(f'\\n🏥 Overall Status: {overall_status}')

asyncio.run(main())
"

health-monitor: ## Continuous health monitoring
	@echo "👀 Starting continuous health monitoring..."
	poetry run python -c "
from flext_observability.health import HealthMonitor
import asyncio

async def main():
    monitor = HealthMonitor(interval=30)
    print('🔄 Health monitoring started (30s intervals)...')
    print('📊 Check status at http://localhost:8080/health')
    print('Press Ctrl+C to stop')
    await monitor.start()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('\\n🛑 Health monitoring stopped')
"

health-server: ## Start health check HTTP server
	@echo "🏥 Starting health check server..."
	poetry run python -c "
from flext_observability.health import HealthServer
import asyncio

async def main():
    server = HealthServer(port=8080)
    print('🚀 Health server starting on port 8080...')
    print('🏥 Health endpoint: http://localhost:8080/health')
    print('📊 Ready endpoint: http://localhost:8080/ready')
    print('Press Ctrl+C to stop')
    await server.start()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('\\n🛑 Health server stopped')
"

# Distributed Tracing
trace-setup: ## Setup OpenTelemetry tracing
	@echo "🔍 Setting up OpenTelemetry tracing..."
	poetry run python -c "
from flext_observability.tracing import TracingSetup

setup = TracingSetup()
setup.configure_tracer()

print('✅ OpenTelemetry tracing configured')
print('📡 OTLP Endpoint: \${OTEL_EXPORTER_OTLP_ENDPOINT:-http://localhost:4317}')
print('🏷️  Service Name: \${OTEL_SERVICE_NAME:-flext-observability}')
"

trace-test: ## Test tracing functionality
	@echo "🧪 Testing tracing functionality..."
	poetry run python -c "
from flext_observability.tracing import trace
from opentelemetry import trace as otel_trace
import time
import asyncio

@trace
async def test_traced_function():
    '''Test function with automatic tracing.'''
    tracer = otel_trace.get_tracer(__name__)
    
    with tracer.start_as_current_span('test_operation') as span:
        span.set_attribute('test.type', 'functionality')
        span.set_attribute('test.component', 'observability')
        
        print('🔍 Creating test trace...')
        await asyncio.sleep(0.1)  # Simulate work
        
        span.add_event('Test operation completed')
        print('✅ Test trace created successfully')

async def main():
    await test_traced_function()
    print('🎯 Tracing test complete')

asyncio.run(main())
"

# Monitoring Dashboard
dashboard-setup: ## Setup Grafana dashboard
	@echo "📊 Setting up Grafana dashboard..."
	@mkdir -p dashboards/grafana
	poetry run python -c "
import json
from pathlib import Path

# Create basic dashboard configuration
dashboard = {
    'dashboard': {
        'title': 'FLEXT Observability',
        'panels': [
            {
                'title': 'System CPU Usage',
                'type': 'stat',
                'targets': [{'expr': 'system_cpu_usage_percent'}]
            },
            {
                'title': 'Memory Usage',
                'type': 'stat', 
                'targets': [{'expr': 'system_memory_usage_percent'}]
            },
            {
                'title': 'Pipeline Success Rate',
                'type': 'stat',
                'targets': [{'expr': 'business_pipeline_success_rate'}]
            }
        ]
    }
}

dashboard_path = Path('dashboards/grafana/flext_observability.json')
dashboard_path.parent.mkdir(parents=True, exist_ok=True)
dashboard_path.write_text(json.dumps(dashboard, indent=2))

print(f'📊 Grafana dashboard created: {dashboard_path}')
"

monitor: ## Start comprehensive monitoring
	@echo "🔄 Starting comprehensive monitoring..."
	@echo "🚀 Starting all monitoring services..."
	@echo "📊 Metrics server on port 9090"
	@echo "🏥 Health server on port 8080" 
	@echo "🔍 Tracing enabled"
	@echo ""
	@echo "Use Ctrl+C to stop all services"
	@# Start services in background and wait
	@poetry run python -c "
import asyncio
from flext_observability.prometheus_metrics import PrometheusServer
from flext_observability.health import HealthServer
from flext_observability.tracing import TracingSetup

async def start_all_services():
    # Setup tracing
    tracing = TracingSetup()
    tracing.configure_tracer()
    
    # Start servers
    metrics_server = PrometheusServer(port=9090)
    health_server = HealthServer(port=8080)
    
    print('📊 All monitoring services started:')
    print('  - Metrics: http://localhost:9090/metrics')
    print('  - Health: http://localhost:8080/health')
    print('  - Tracing: Enabled')
    print('')
    print('Press Ctrl+C to stop all services')
    
    # Run both servers
    await asyncio.gather(
        metrics_server.start(),
        health_server.start()
    )

try:
    asyncio.run(start_all_services())
except KeyboardInterrupt:
    print('\\n🛑 All monitoring services stopped')
"

# Development & Testing  
test-all: ## Run all observability tests
	@echo "🧪 Running all observability tests..."
	poetry run pytest tests/ -v --tb=short --cov=src/flext_observability

test-integration: ## Run integration tests
	@echo "🔗 Running integration tests..."
	@echo "🧪 Testing Prometheus integration..."
	poetry run python -c "
from flext_observability.prometheus_metrics import PrometheusIntegration
integration = PrometheusIntegration()
if integration.test_connection():
    print('✅ Prometheus integration working')
else:
    print('❌ Prometheus integration failed')
"

performance-test: ## Run performance tests for metrics
	@echo "⚡ Running performance tests..."
	poetry run python -c "
from flext_observability.metrics import SystemMetrics
import time

metrics = SystemMetrics()
start_time = time.time()

# Collect metrics 1000 times
for i in range(1000):
    metrics.get_cpu_usage()
    metrics.get_memory_usage()
    
elapsed = time.time() - start_time
avg_time = elapsed / 1000 * 1000  # Convert to milliseconds

print(f'⚡ Performance Test Results:')
print(f'  Total time: {elapsed:.3f}s')
print(f'  Average per metric: {avg_time:.3f}ms')

if avg_time < 1.0:
    print('✅ Performance: EXCELLENT')
elif avg_time < 5.0:
    print('⚠️  Performance: ACCEPTABLE')
else:
    print('❌ Performance: NEEDS IMPROVEMENT')
"

# Testing
test: ## Run observability tests
	@echo "🧪 Running observability tests..."
	poetry run pytest tests/ -v --tb=short

test-coverage: ## Run tests with coverage
	@echo "📊 Running tests with coverage..."
	poetry run pytest tests/ --cov=src/flext_observability --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=90

# Code Quality - Maximum Strictness
lint: ## Run all linters with maximum strictness
	@echo "🔍 Running maximum strictness linting for observability..."
	poetry run ruff check . --output-format=verbose
	@echo "✅ Ruff linting complete"

format: ## Format code with strict standards
	@echo "🎨 Formatting observability code..."
	poetry run black .
	poetry run ruff check --fix .
	@echo "✅ Code formatting complete"

type-check: ## Run strict type checking
	@echo "🎯 Running strict MyPy type checking..."
	poetry run mypy src/flext_observability --strict --show-error-codes
	@echo "✅ Type checking complete"

check: lint type-check test ## Run all quality checks
	@echo "✅ All quality checks complete for flext-observability!"

# Build & Distribution
build: ## Build the observability package
	@echo "🔨 Building flext-observability package..."
	poetry build
	@echo "📦 Package built successfully"

# Documentation
docs: ## Generate observability documentation
	@echo "📚 Generating observability documentation..."
	@mkdir -p docs/generated
	poetry run python -c "
from flext_observability.metrics import SystemMetrics, BusinessMetrics
from flext_observability.health import HealthChecker
import inspect

# Generate metrics documentation
doc = '''# Observability Documentation

## System Metrics

'''
doc += inspect.getdoc(SystemMetrics) or 'System metrics collection'

doc += '''

## Business Metrics

'''
doc += inspect.getdoc(BusinessMetrics) or 'Business metrics collection'

doc += '''

## Health Checking

'''
doc += inspect.getdoc(HealthChecker) or 'Health check framework'

with open('docs/generated/observability.md', 'w') as f:
    f.write(doc)

print('✅ Observability documentation generated')
"

# Development Workflow
dev-setup: install-dev dashboard-setup ## Complete development setup
	@echo "🎯 Setting up observability development environment..."
	poetry run pre-commit install
	mkdir -p reports logs dashboards/grafana dashboards/prometheus /tmp/prometheus_multiproc
	@echo "📊 Run 'make metrics-server' to start metrics server"
	@echo "🏥 Run 'make health-check' to run health checks"
	@echo "🔍 Run 'make trace-test' to test tracing"
	@echo "🔄 Run 'make monitor' to start all services"
	@echo "✅ Development setup complete!"

# Cleanup
clean: ## Clean build artifacts and generated files
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info/
	@rm -rf reports/ logs/ .coverage htmlcov/
	@rm -rf docs/generated/
	@rm -rf /tmp/prometheus_multiproc/*
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true

# Environment variables
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export PROMETHEUS_MULTIPROC_DIR := /tmp/prometheus_multiproc
export OTEL_SERVICE_NAME := flext-observability
export FLEXT_OBSERVABILITY_DEV := true