# =============================================================================
# FLEXT-OBSERVABILITY - Monitoring & Telemetry Platform Makefile
# =============================================================================
# Python 3.13+ Observability Framework - Clean Architecture + DDD + Zero Tolerance
# =============================================================================

# Project Configuration
PROJECT_NAME := flext-observability
PYTHON_VERSION := 3.13
POETRY := poetry
SRC_DIR := src
TESTS_DIR := tests
COV_DIR := flext_observability

# Quality Standards
MIN_COVERAGE := 100

# Observability Configuration
OTEL_SERVICE_NAME := flext-observability
PROMETHEUS_ENDPOINT := http://localhost:9090
PROMETHEUS_PUSH_GATEWAY := http://localhost:9091
GRAFANA_PORT := 3000
JAEGER_ENDPOINT := http://localhost:14268

# Export Configuration
export PROJECT_NAME PYTHON_VERSION MIN_COVERAGE OTEL_SERVICE_NAME PROMETHEUS_ENDPOINT PROMETHEUS_PUSH_GATEWAY GRAFANA_PORT JAEGER_ENDPOINT

# =============================================================================
# HELP & INFORMATION
# =============================================================================

.PHONY: help
help: ## Show available commands
	@echo "FLEXT-OBSERVABILITY - Monitoring & Telemetry Platform"
	@echo "===================================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \\033[36m%-15s\\033[0m %s\\n", $$1, $$2}'

.PHONY: info
info: ## Show project information
	@echo "Project: $(PROJECT_NAME)"
	@echo "Python: $(PYTHON_VERSION)+"
	@echo "Poetry: $(POETRY)"
	@echo "Coverage: $(MIN_COVERAGE)% minimum (MANDATORY)"
	@echo "OTEL Service: $(OTEL_SERVICE_NAME)"
	@echo "Prometheus: $(PROMETHEUS_ENDPOINT)"
	@echo "Grafana: http://localhost:$(GRAFANA_PORT)"
	@echo "Architecture: Clean Architecture + DDD + OpenTelemetry"

# =============================================================================
# SETUP & INSTALLATION
# =============================================================================

.PHONY: install
install: ## Install dependencies
	$(POETRY) install

.PHONY: install-dev
install-dev: ## Install dev dependencies
	$(POETRY) install --with dev,test,docs

.PHONY: setup
setup: install-dev ## Complete project setup
	$(POETRY) run pre-commit install

# =============================================================================
# QUALITY GATES (MANDATORY - ZERO TOLERANCE)
# =============================================================================

.PHONY: validate
validate: lint type-check security test ## Run all quality gates (MANDATORY ORDER)

.PHONY: check
check: lint type-check ## Quick health check

.PHONY: lint
lint: ## Run linting (ZERO TOLERANCE)
	$(POETRY) run ruff check .

.PHONY: format
format: ## Format code
	$(POETRY) run ruff format .

.PHONY: type-check
type-check: ## Run type checking with Pyrefly (ZERO TOLERANCE)
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pyrefly check .

.PHONY: security
security: ## Run security scanning
	$(POETRY) run bandit -r $(SRC_DIR)
	$(POETRY) run pip-audit

.PHONY: fix
fix: ## Auto-fix issues
	$(POETRY) run ruff check . --fix
	$(POETRY) run ruff format .

# =============================================================================
# TESTING (MANDATORY - 100% COVERAGE)
# =============================================================================

.PHONY: test
test: ## Run tests with 100% coverage (MANDATORY)
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -q --maxfail=10000 --cov=$(COV_DIR) --cov-report=term-missing:skip-covered --cov-fail-under=$(MIN_COVERAGE)

.PHONY: test-unit
test-unit: ## Run unit tests
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -m "not integration" -v

.PHONY: test-integration
test-integration: ## Run integration tests with Docker
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -m integration -v

.PHONY: test-monitoring
test-monitoring: ## Run monitoring specific tests
	$(POETRY) run pytest $(TESTS_DIR) -m monitoring -v

.PHONY: test-metrics
test-metrics: ## Run metrics tests
	$(POETRY) run pytest $(TESTS_DIR) -m metrics -v

.PHONY: test-tracing
test-tracing: ## Run tracing tests
	$(POETRY) run pytest $(TESTS_DIR) -m tracing -v

.PHONY: test-logging
test-logging: ## Run logging tests
	$(POETRY) run pytest $(TESTS_DIR) -m logging -v

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests
	$(POETRY) run pytest $(TESTS_DIR) -m e2e -v

.PHONY: test-fast
test-fast: ## Run tests without coverage
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -v

.PHONY: coverage-html
coverage-html: ## Generate HTML coverage report
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest --cov=$(COV_DIR) --cov-report=html

# =============================================================================
# BUILD & DISTRIBUTION
# =============================================================================

.PHONY: build
build: ## Build package
	$(POETRY) build

.PHONY: build-clean
build-clean: clean build ## Clean and build

# =============================================================================
# OBSERVABILITY OPERATIONS
# =============================================================================

.PHONY: otel-test
otel-test: ## Test OpenTelemetry connectivity
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_observability import flext_create_metric; print('OpenTelemetry test passed')"

.PHONY: prometheus-test
prometheus-test: ## Test Prometheus metrics
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_observability import flext_create_metric; result = flext_create_metric('test_metric', 1.0, 'test'); print('Prometheus test passed' if result.success else 'Failed')"

.PHONY: grafana-test
grafana-test: ## Test Grafana dashboard connectivity
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "import requests; response = requests.get('$(PROMETHEUS_ENDPOINT)/api/v1/status/buildinfo', timeout=5); print('Grafana backend OK' if response.status_code == 200 else 'Failed')" 2>/dev/null || echo "Grafana/Prometheus not available"

.PHONY: jaeger-test
jaeger-test: ## Test Jaeger tracing
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_observability import flext_create_trace; result = flext_create_trace('test_trace', 'test_operation'); print('Jaeger test passed' if result.success else 'Failed')"

.PHONY: setup-prometheus
setup-prometheus: ## Setup Prometheus configuration
	@echo "⚠️  Prometheus setup not implemented - see CLAUDE.md for details"
	@echo "To implement: Create setup_prometheus function in flext_observability/__init__.py"

.PHONY: setup-grafana
setup-grafana: ## Setup Grafana dashboards
	@echo "⚠️  Grafana setup not implemented - see CLAUDE.md for details"
	@echo "To implement: Create setup_grafana function in flext_observability/__init__.py"

.PHONY: setup-monitoring
setup-monitoring: setup-prometheus setup-grafana ## Setup monitoring stack

.PHONY: start-monitoring
start-monitoring: ## Start monitoring stack
	@echo "⚠️  Docker Compose monitoring file not found"
	@echo "To implement: Create docker-compose.monitoring.yml with Prometheus, Grafana, and Jaeger"
	@if [ -f docker-compose.monitoring.yml ]; then \
		echo "Starting monitoring stack..."; \
		echo "Prometheus: $(PROMETHEUS_ENDPOINT)"; \
		echo "Grafana: http://localhost:$(GRAFANA_PORT)"; \
		echo "Jaeger: $(JAEGER_ENDPOINT)"; \
		docker-compose -f docker-compose.monitoring.yml up -d; \
	fi

.PHONY: stop-monitoring
stop-monitoring: ## Stop monitoring stack
	@if [ -f docker-compose.monitoring.yml ]; then \
		docker-compose -f docker-compose.monitoring.yml down; \
	else \
		echo "⚠️  docker-compose.monitoring.yml not found"; \
	fi

.PHONY: monitoring-status
monitoring-status: ## Check monitoring status
	@if [ -f docker-compose.monitoring.yml ]; then \
		docker-compose -f docker-compose.monitoring.yml ps; \
	else \
		echo "⚠️  docker-compose.monitoring.yml not found"; \
	fi

.PHONY: validate-telemetry
validate-telemetry: otel-test prometheus-test jaeger-test ## Validate telemetry components

.PHONY: health-check
health-check: ## Perform health check
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_observability import get_global_factory; factory = get_global_factory(); print('Health check: Observatory factory OK')"

.PHONY: observability-operations
observability-operations: otel-test prometheus-test jaeger-test health-check ## Run all observability validations

# =============================================================================
# DOCUMENTATION
# =============================================================================

.PHONY: docs
docs: ## Build documentation
	$(POETRY) run mkdocs build

.PHONY: docs-serve
docs-serve: ## Serve documentation
	$(POETRY) run mkdocs serve

# =============================================================================
# DEPENDENCIES
# =============================================================================

.PHONY: deps-update
deps-update: ## Update dependencies
	$(POETRY) update

.PHONY: deps-show
deps-show: ## Show dependency tree
	$(POETRY) show --tree

.PHONY: deps-audit
deps-audit: ## Audit dependencies
	$(POETRY) run pip-audit

# =============================================================================
# DEVELOPMENT
# =============================================================================

.PHONY: shell
shell: ## Open Python shell
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

# =============================================================================
# MAINTENANCE
# =============================================================================

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage .mypy_cache/ .pyrefly_cache/ .ruff_cache/
	rm -rf logs/ metrics/ data/ traces/ spans/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

.PHONY: clean-all
clean-all: clean ## Deep clean including venv
	rm -rf .venv/

.PHONY: reset
reset: clean-all setup ## Reset project

# =============================================================================
# DIAGNOSTICS
# =============================================================================

.PHONY: diagnose
diagnose: ## Project diagnostics
	@echo "Python: $$(python --version)"
	@echo "Poetry: $$($(POETRY) --version)"
	@echo "OpenTelemetry: $$(PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c 'import opentelemetry; print(opentelemetry.__version__)' 2>/dev/null || echo 'Not available')"
	@echo "Prometheus Client: $$(PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c 'import prometheus_client; print(prometheus_client.__version__)' 2>/dev/null || echo 'Not available')"
	@$(POETRY) env info

.PHONY: doctor
doctor: diagnose check ## Health check

# =============================================================================

# =============================================================================

.PHONY: t l f tc c i v
t: test
l: lint
f: format
tc: type-check
c: clean
i: install
v: validate

# =============================================================================
# CONFIGURATION
# =============================================================================

.DEFAULT_GOAL := help
