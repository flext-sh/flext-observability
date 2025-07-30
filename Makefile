# FLEXT-OBSERVABILITY Makefile
PROJECT_NAME := flext-observability
PYTHON_VERSION := 3.13
POETRY := poetry
SRC_DIR := src
TESTS_DIR := tests

# Quality standards
MIN_COVERAGE := 90

# Observability configuration
OTEL_SERVICE_NAME := flext-observability
PROMETHEUS_ENDPOINT := http://localhost:9090
GRAFANA_PORT := 3000

# Help
help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install dependencies
	$(POETRY) install

install-dev: ## Install dev dependencies
	$(POETRY) install --with dev,test,docs

setup: install-dev ## Complete project setup
	$(POETRY) run pre-commit install

# Quality gates
validate: lint type-check security test ## Run all quality gates

check: lint type-check ## Quick health check

lint: ## Run linting
	$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR)

format: ## Format code
	$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

type-check: ## Run type checking
	$(POETRY) run mypy $(SRC_DIR) --strict

security: ## Run security scanning
	$(POETRY) run bandit -r $(SRC_DIR)
	$(POETRY) run pip-audit

fix: ## Auto-fix issues
	$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR) --fix
	$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

# Testing
test: ## Run tests with coverage
	$(POETRY) run pytest $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=term-missing --cov-fail-under=$(MIN_COVERAGE)

test-unit: ## Run unit tests
	$(POETRY) run pytest $(TESTS_DIR) -m "not integration" -v

test-integration: ## Run integration tests
	$(POETRY) run pytest $(TESTS_DIR) -m integration -v

test-monitoring: ## Run monitoring specific tests
	$(POETRY) run pytest $(TESTS_DIR) -m monitoring -v

test-fast: ## Run tests without coverage
	$(POETRY) run pytest $(TESTS_DIR) -v

coverage-html: ## Generate HTML coverage report
	$(POETRY) run pytest $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=html

# Observability operations
setup-prometheus: ## Setup Prometheus configuration
	$(POETRY) run python -c "from flext_observability import setup_prometheus; setup_prometheus()"

setup-grafana: ## Setup Grafana dashboards
	$(POETRY) run python -c "from flext_observability import setup_grafana; setup_grafana()"

setup-monitoring: setup-prometheus setup-grafana ## Setup monitoring stack

start-monitoring: ## Start monitoring stack
	@echo "Starting monitoring stack..."
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana: http://localhost:3000"
	docker-compose -f docker-compose.monitoring.yml up -d

stop-monitoring: ## Stop monitoring stack
	docker-compose -f docker-compose.monitoring.yml down

monitoring-status: ## Check monitoring status
	docker-compose -f docker-compose.monitoring.yml ps

# Telemetry testing
test-metrics: ## Test metrics collection
	$(POETRY) run python -c "from flext_observability import test_metrics; test_metrics()"

test-tracing: ## Test distributed tracing
	$(POETRY) run python -c "from flext_observability import test_tracing; test_tracing()"

test-logging: ## Test structured logging
	$(POETRY) run python -c "from flext_observability import test_logging; test_logging()"

validate-telemetry: test-metrics test-tracing test-logging ## Validate telemetry components

# Health checks
health-check: ## Perform health check
	$(POETRY) run python -c "from flext_observability import health_check; health_check()"

# Build
build: ## Build package
	$(POETRY) build

build-clean: clean build ## Clean and build

# Documentation
docs: ## Build documentation
	$(POETRY) run mkdocs build

docs-serve: ## Serve documentation
	$(POETRY) run mkdocs serve

# Dependencies
deps-update: ## Update dependencies
	$(POETRY) update

deps-show: ## Show dependency tree
	$(POETRY) show --tree

deps-audit: ## Audit dependencies
	$(POETRY) run pip-audit

# Development
shell: ## Open Python shell
	$(POETRY) run python

pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

# Maintenance
clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage .mypy_cache/ .ruff_cache/
	rm -rf logs/ metrics/ data/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

clean-all: clean ## Deep clean including venv
	rm -rf .venv/

reset: clean-all setup ## Reset project

# Diagnostics
diagnose: ## Project diagnostics
	@echo "Python: $$(python --version)"
	@echo "Poetry: $$($(POETRY) --version)"
	@echo "OpenTelemetry: $$($(POETRY) run python -c 'import opentelemetry; print(opentelemetry.__version__)' 2>/dev/null || echo 'Not available')"
	@$(POETRY) env info

doctor: diagnose check ## Health check

# Aliases
t: test
l: lint
f: format
tc: type-check
c: clean
i: install
v: validate

.DEFAULT_GOAL := help
.PHONY: help install install-dev setup validate check lint format type-check security fix test test-unit test-integration test-monitoring test-fast coverage-html setup-prometheus setup-grafana setup-monitoring start-monitoring stop-monitoring monitoring-status test-metrics test-tracing test-logging validate-telemetry health-check build build-clean docs docs-serve deps-update deps-show deps-audit shell pre-commit clean clean-all reset diagnose doctor t l f tc c i v