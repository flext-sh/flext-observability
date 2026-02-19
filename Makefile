# flext-observability - Observability Framework
PROJECT_NAME := flext-observability
# Coverage temporarily reduced while test suite is rebuilt (was testing non-existent APIs)
ifneq ("$(wildcard ../base.mk)", "")
include ../base.mk
else
include base.mk
endif

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: test-unit test-integration build shell

.DEFAULT_GOAL := help
