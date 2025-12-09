# flext-observability - FLEXT Infrastructure

**Hierarchy**: PROJECT
**Parent**: [../CLAUDE.md](../CLAUDE.md) - Workspace standards
**Last Update**: 2025-12-07

---

## Project Overview

**FLEXT-Observability** is the enterprise observability and monitoring foundation for the FLEXT ecosystem.

**Version**: 0.9.0  
**Status**: Active development  
**Python**: 3.13+  
**Coverage Target**: 100%

---

## Essential Commands

```bash
# Setup and validation
make setup                    # Complete development environment setup
make validate                 # Complete validation (lint + type + security + test)
make check                    # Quick check (lint + type)

# Quality gates
make lint                     # Ruff linting
make type-check               # Pyrefly type checking
make security                 # Bandit security scan
make test                     # Run tests
```

---

## Key Patterns

### Observability Integration

```python
from flext_core import FlextResult
from flext_observability import FlextObservability

obs = FlextObservability()

# Record metrics
result = obs.record_metric("operation.duration", 1.5)
if result.is_success:
    print("Metric recorded")
```

---

## Critical Development Rules

### ZERO TOLERANCE Policies

**ABSOLUTELY FORBIDDEN**:
- ❌ Exception-based error handling (use FlextResult)
- ❌ Type ignores or `Any` types
- ❌ Mockpatch in tests

**MANDATORY**:
- ✅ Use `FlextResult[T]` for all operations
- ✅ Complete type annotations
- ✅ Zero Ruff violations
- ✅ 100% test coverage

---

**See Also**:
- [Workspace Standards](../CLAUDE.md)
- [flext-core Patterns](../flext-core/CLAUDE.md)
- [flext-quality Patterns](../flext-quality/CLAUDE.md)
