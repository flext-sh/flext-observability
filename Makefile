# flext-observability - Observability Framework
PROJECT_NAME := flext-observability
# Coverage temporarily reduced while test suite is rebuilt (was testing non-existent APIs)
include ../base.mk

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: test-unit test-integration build shell

.DEFAULT_GOAL := help
