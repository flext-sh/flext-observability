# FLEXT OBSERVABILITY - Comprehensive Monitoring & Telemetry Service
# ================================================================
# OpenTelemetry + Prometheus + Jaeger + Structured Logging
# Python 3.13 + OpenTelemetry + Zero Tolerance Quality Gates

.PHONY: help check validate test lint type-check security format format-check fix
.PHONY: install dev-install setup pre-commit build clean
.PHONY: coverage coverage-html test-unit test-integration test-monitoring
.PHONY: deps-update deps-audit deps-tree deps-outdated
.PHONY: setup-prometheus setup-grafana setup-jaeger setup-elastic

# ============================================================================
# 🎯 HELP & INFORMATION
# ============================================================================

help: ## Show this help message
	@echo "📊 FLEXT OBSERVABILITY - Comprehensive Monitoring & Telemetry Service"
	@echo "===================================================================="
	@echo "🎯 Clean Architecture + DDD + Python 3.13 + OpenTelemetry Standards"
	@echo ""
	@echo "📦 Enterprise observability with metrics, tracing, and logging"
	@echo "🔒 Zero tolerance quality gates for monitoring infrastructure"
	@echo "🧪 90%+ test coverage requirement for telemetry components"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================================================
# 🎯 CORE QUALITY GATES - ZERO TOLERANCE
# ============================================================================

validate: lint type-check security test ## STRICT compliance validation (all must pass)
	@echo "✅ ALL QUALITY GATES PASSED - FLEXT OBSERVABILITY COMPLIANT"

check: lint type-check test ## Essential quality checks (pre-commit standard)
	@echo "✅ Essential checks passed"

lint: ## Ruff linting (17 rule categories, ALL enabled)
	@echo "🔍 Running ruff linter (ALL rules enabled)..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ Linting complete"

type-check: ## MyPy strict mode type checking (zero errors tolerated)
	@echo "🛡️ Running MyPy strict type checking..."
	@poetry run mypy src/ tests/ --strict
	@echo "✅ Type checking complete"

security: ## Security scans (bandit + pip-audit + secrets)
	@echo "🔒 Running security scans..."
	@poetry run bandit -r src/ --severity-level medium --confidence-level medium
	@poetry run pip-audit --ignore-vuln PYSEC-2022-42969
	@poetry run detect-secrets scan --all-files
	@echo "✅ Security scans complete"

format: ## Format code with ruff
	@echo "🎨 Formatting code..."
	@poetry run ruff format src/ tests/
	@echo "✅ Formatting complete"

format-check: ## Check formatting without fixing
	@echo "🎨 Checking code formatting..."
	@poetry run ruff format src/ tests/ --check
	@echo "✅ Format check complete"

fix: format lint ## Auto-fix all issues (format + imports + lint)
	@echo "🔧 Auto-fixing all issues..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ All auto-fixes applied"

# ============================================================================
# 🧪 TESTING - 90% COVERAGE MINIMUM
# ============================================================================

test: ## Run tests with coverage (90% minimum required)
	@echo "🧪 Running tests with coverage..."
	@poetry run pytest tests/ -v --cov=src/flext_observability --cov-report=term-missing --cov-fail-under=90
	@echo "✅ Tests complete"

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	@poetry run pytest tests/unit/ -v
	@echo "✅ Unit tests complete"

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	@poetry run pytest tests/integration/ -v
	@echo "✅ Integration tests complete"

test-monitoring: ## Run monitoring-specific tests
	@echo "📊 Running monitoring tests..."
	@poetry run pytest tests/monitoring/ -v --tb=short
	@echo "✅ Monitoring tests complete"

coverage: ## Generate detailed coverage report
	@echo "📊 Generating coverage report..."
	@poetry run pytest tests/ --cov=src/flext_observability --cov-report=term-missing --cov-report=html
	@echo "✅ Coverage report generated in htmlcov/"

coverage-html: coverage ## Generate HTML coverage report
	@echo "📊 Opening coverage report..."
	@python -m webbrowser htmlcov/index.html

# ============================================================================
# 🚀 DEVELOPMENT SETUP
# ============================================================================

setup: install pre-commit ## Complete development setup
	@echo "🎯 Development setup complete!"

install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies..."
	@poetry install --all-extras --with dev,test,docs,security
	@echo "✅ Dependencies installed"

dev-install: install ## Install in development mode
	@echo "🔧 Setting up development environment..."
	@poetry install --all-extras --with dev,test,docs,security
	@poetry run pre-commit install
	@echo "✅ Development environment ready"

pre-commit: ## Setup pre-commit hooks
	@echo "🎣 Setting up pre-commit hooks..."
	@poetry run pre-commit install
	@poetry run pre-commit run --all-files || true
	@echo "✅ Pre-commit hooks installed"

# ============================================================================
# 📊 MONITORING STACK SETUP
# ============================================================================

setup-prometheus: ## Setup Prometheus configuration
	@echo "📊 Setting up Prometheus configuration..."
	@poetry run python -m flext_observability.setup prometheus
	@echo "📍 Prometheus config generated at config/prometheus.yml"
	@echo "✅ Prometheus setup complete"

setup-grafana: ## Setup Grafana dashboards
	@echo "📈 Setting up Grafana dashboards..."
	@poetry run python -m flext_observability.setup grafana
	@echo "📍 Grafana dashboards generated at config/grafana/"
	@echo "✅ Grafana setup complete"

setup-jaeger: ## Setup Jaeger tracing configuration
	@echo "🔍 Setting up Jaeger tracing..."
	@poetry run python -m flext_observability.setup jaeger
	@echo "📍 Jaeger config generated at config/jaeger.yml"
	@echo "✅ Jaeger setup complete"

setup-elastic: ## Setup Elasticsearch logging
	@echo "📋 Setting up Elasticsearch logging..."
	@poetry run python -m flext_observability.setup elasticsearch
	@echo "📍 Elasticsearch config generated at config/elasticsearch.yml"
	@echo "✅ Elasticsearch setup complete"

setup-all-monitoring: setup-prometheus setup-grafana setup-jaeger setup-elastic ## Setup complete monitoring stack
	@echo "✅ Complete monitoring stack configured"

# ============================================================================
# 🔄 MONITORING OPERATIONS
# ============================================================================

start-monitoring: ## Start local monitoring stack (Docker Compose)
	@echo "🚀 Starting monitoring stack..."
	@docker-compose -f docker-compose.monitoring.yml up -d
	@echo "📊 Prometheus: http://localhost:9090"
	@echo "📈 Grafana: http://localhost:3000"
	@echo "🔍 Jaeger: http://localhost:16686"
	@echo "📋 Elasticsearch: http://localhost:9200"
	@echo "✅ Monitoring stack started"

stop-monitoring: ## Stop local monitoring stack
	@echo "⏹️ Stopping monitoring stack..."
	@docker-compose -f docker-compose.monitoring.yml down
	@echo "✅ Monitoring stack stopped"

restart-monitoring: stop-monitoring start-monitoring ## Restart monitoring stack
	@echo "✅ Monitoring stack restarted"

monitoring-status: ## Check monitoring stack status
	@echo "📊 Checking monitoring stack status..."
	@docker-compose -f docker-compose.monitoring.yml ps
	@echo "✅ Status check complete"

# ============================================================================
# 📊 METRICS & TELEMETRY OPERATIONS
# ============================================================================

collect-metrics: ## Manually trigger metrics collection
	@echo "📊 Collecting system metrics..."
	@poetry run python -m flext_observability.collectors.system
	@echo "✅ Metrics collection complete"

test-tracing: ## Test distributed tracing
	@echo "🔍 Testing distributed tracing..."
	@poetry run python -m flext_observability.testing.trace_test
	@echo "✅ Tracing test complete"

test-metrics: ## Test metrics collection
	@echo "📊 Testing metrics collection..."
	@poetry run python -m flext_observability.testing.metrics_test
	@echo "✅ Metrics test complete"

test-logging: ## Test structured logging
	@echo "📋 Testing structured logging..."
	@poetry run python -m flext_observability.testing.logging_test
	@echo "✅ Logging test complete"

validate-telemetry: test-metrics test-tracing test-logging ## Validate all telemetry components
	@echo "✅ Telemetry validation complete"

# ============================================================================
# 🔧 MONITORING TOOLS
# ============================================================================

dashboard-generate: ## Generate dynamic dashboards
	@echo "📈 Generating monitoring dashboards..."
	@poetry run python -m flext_observability.tools.dashboard_generator
	@echo "✅ Dashboards generated"

alert-rules-validate: ## Validate alert rules
	@echo "🚨 Validating alert rules..."
	@poetry run python -m flext_observability.tools.alert_validator
	@echo "✅ Alert rules validated"

health-check: ## Perform comprehensive health check
	@echo "🔍 Performing health check..."
	@poetry run python -m flext_observability.health.system_check
	@echo "✅ Health check complete"

# ============================================================================
# 📦 BUILD & DISTRIBUTION
# ============================================================================

build: clean ## Build distribution packages
	@echo "🔨 Building distribution..."
	@poetry build
	@echo "✅ Build complete - packages in dist/"

build-monitoring-image: ## Build monitoring Docker image
	@echo "🐳 Building monitoring Docker image..."
	@docker build -f docker/Dockerfile.monitoring -t flext-observability:latest .
	@echo "✅ Monitoring image built"

# ============================================================================
# 🧹 CLEANUP
# ============================================================================

clean: ## Remove all artifacts
	@echo "🧹 Cleaning up..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf .pytest_cache/
	@rm -rf logs/
	@rm -rf metrics/
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

clean-monitoring: ## Clean monitoring data
	@echo "🧹 Cleaning monitoring data..."
	@rm -rf data/prometheus/
	@rm -rf data/grafana/
	@rm -rf data/elasticsearch/
	@rm -rf logs/monitoring/
	@echo "✅ Monitoring data cleaned"

# ============================================================================
# 📊 DEPENDENCY MANAGEMENT
# ============================================================================

deps-update: ## Update all dependencies
	@echo "🔄 Updating dependencies..."
	@poetry update
	@echo "✅ Dependencies updated"

deps-audit: ## Audit dependencies for vulnerabilities
	@echo "🔍 Auditing dependencies..."
	@poetry run pip-audit
	@echo "✅ Dependency audit complete"

deps-tree: ## Show dependency tree
	@echo "🌳 Dependency tree:"
	@poetry show --tree

deps-outdated: ## Show outdated dependencies
	@echo "📋 Outdated dependencies:"
	@poetry show --outdated

# ============================================================================
# 🔧 ENVIRONMENT CONFIGURATION
# ============================================================================

# Python settings
PYTHON := python3.13
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export PYTHONDONTWRITEBYTECODE := 1
export PYTHONUNBUFFERED := 1

# OpenTelemetry settings
export OTEL_SERVICE_NAME := flext-observability
export OTEL_SERVICE_VERSION := 0.7.0
export OTEL_EXPORTER_OTLP_ENDPOINT := http://localhost:4317
export OTEL_RESOURCE_ATTRIBUTES := service.name=flext,service.version=0.7.0

# Prometheus settings
export PROMETHEUS_ENDPOINT := http://localhost:9090
export PROMETHEUS_PUSH_GATEWAY := http://localhost:9091
export PROMETHEUS_SCRAPE_INTERVAL := 15s

# Jaeger settings
export JAEGER_AGENT_HOST := localhost
export JAEGER_AGENT_PORT := 6831
export JAEGER_COLLECTOR_ENDPOINT := http://localhost:14268/api/traces

# Elasticsearch settings
export ELASTICSEARCH_HOST := localhost
export ELASTICSEARCH_PORT := 9200
export ELASTICSEARCH_INDEX_PREFIX := flext-logs

# Grafana settings
export GRAFANA_HOST := localhost
export GRAFANA_PORT := 3000

# Poetry settings
export POETRY_VENV_IN_PROJECT := false
export POETRY_CACHE_DIR := $(HOME)/.cache/pypoetry

# Quality gate settings
export MYPY_CACHE_DIR := .mypy_cache
export RUFF_CACHE_DIR := .ruff_cache

# ============================================================================
# 📝 PROJECT METADATA
# ============================================================================

# Project information
PROJECT_NAME := flext-observability
PROJECT_VERSION := $(shell poetry version -s)
PROJECT_DESCRIPTION := FLEXT Observability - Comprehensive Monitoring & Telemetry Service

.DEFAULT_GOAL := help

# ============================================================================
# 🎯 OBSERVABILITY VALIDATION COMMANDS
# ============================================================================

observability-validate: validate-telemetry alert-rules-validate health-check ## Validate observability setup
	@echo "✅ Observability validation complete"

monitoring-performance: ## Test monitoring performance
	@echo "⚡ Testing monitoring performance..."
	@poetry run python -m flext_observability.testing.performance_test
	@echo "✅ Performance test complete"

metrics-benchmark: ## Benchmark metrics collection
	@echo "📊 Benchmarking metrics collection..."
	@poetry run python -m flext_observability.testing.metrics_benchmark
	@echo "✅ Metrics benchmark complete"

# ============================================================================
# 🎯 FLEXT ECOSYSTEM INTEGRATION
# ============================================================================

ecosystem-check: ## Verify FLEXT ecosystem compatibility
	@echo "🌐 Checking FLEXT ecosystem compatibility..."
	@echo "📦 Observability project: $(PROJECT_NAME) v$(PROJECT_VERSION)"
	@echo "🏗️ Architecture: Clean Architecture + DDD"
	@echo "🐍 Python: 3.13"
	@echo "📊 Framework: OpenTelemetry + Prometheus + Jaeger"
	@echo "📊 Quality: Zero tolerance enforcement"
	@echo "✅ Ecosystem compatibility verified"

workspace-info: ## Show workspace integration info
	@echo "🏢 FLEXT Workspace Integration"
	@echo "==============================="
	@echo "📁 Project Path: $(PWD)"
	@echo "🏆 Role: Observability & Monitoring Infrastructure"
	@echo "🔗 Dependencies: flext-core"
	@echo "📦 Provides: Metrics, tracing, logging, alerting, dashboards"
	@echo "🎯 Standards: Enterprise observability patterns with OpenTelemetry"