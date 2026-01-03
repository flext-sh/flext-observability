# flext-observability - Observability Framework
PROJECT_NAME := flext-observability
COV_DIR := flext_observability
# Coverage temporarily reduced while test suite is rebuilt (was testing non-existent APIs)
MIN_COVERAGE := 49

include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: test-unit test-integration build shell

.DEFAULT_GOAL := help
