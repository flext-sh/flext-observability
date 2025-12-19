# flext-observability - Observability Framework
PROJECT_NAME := flext-observability
COV_DIR := flext_observability
MIN_COVERAGE := 90

include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: test-unit test-integration build shell

.DEFAULT_GOAL := help
