# FLEXT Observability - C4 Model Architecture

**C4 Model Documentation for Enterprise Observability Foundation**

Based on the C4 Model by Simon Brown, this documentation provides multiple architectural views of the FLEXT Observability system, showing how it fits into the broader FLEXT ecosystem and its internal structure.

## 📋 C4 Model Overview

The C4 Model provides four levels of architectural abstraction:

1. **Context** (Level 1): System in its environment
2. **Container** (Level 2): High-level technology choices
3. **Component** (Level 3): Major building blocks
4. **Code** (Level 4): Implementation details

---

## 🌍 Level 1: System Context

### System Purpose

FLEXT Observability is the enterprise monitoring and metrics foundation library for the entire FLEXT ecosystem, providing consistent observability patterns across 33+ projects.

### Context Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           FLEXT Ecosystem                               │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    External Systems & Users                    │    │
│  │                                                                 │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │    │
│  │  │  Enterprise │  │   DevOps    │  │ Monitoring  │  │  Data   │ │    │
│  │  │  Applications│  │   Teams    │  │   Systems  │  │  Teams  │ │    │
│  │  │             │  │             │  │             │  │         │ │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│               │              │              │              │            │
│               └──────────────┼──────────────┼──────────────┘            │
│                              │              │                           │
│                    ┌─────────┴─────────┐    │                           │
│                    │ FLEXT Observability │  │                           │
│                    │   Foundation       │    │                           │
│                    │                    │    │                           │
│                    └────────────────────┘    │                           │
│                              │              │                           │
│               ┌──────────────┼──────────────┼──────────────┐            │
│               │              │              │              │            │
│  ┌────────────▼────┐ ┌───────▼─────┐ ┌──────▼─────┐ ┌─────▼────┐       │
│  │   Prometheus    │ │   Grafana   │ │   Jaeger   │ │ OpenTelemetry│     │
│  │   Metrics DB    │ │   Dashboards│ │   Tracing  │ │   SDK      │     │
│  └─────────────────┘ └─────────────┘ └─────────────┘ └──────────┘       │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    FLEXT Ecosystem Projects                     │    │
│  │                                                                 │    │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌─────┐  │ │
│  │  │flext-│ │flext-│ │flext-│ │flext-│ │flext-│ │flext-│ │ ... │  │ │
│  │  │ core │ │  api │ │ auth │ │ ldap │ │  cli │ │meltano│ │     │  │ │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └─────┘  │ │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### External Interfaces

#### Primary Users

- **Enterprise Application Developers**: Use FLEXT Observability for consistent monitoring
- **DevOps Teams**: Configure and maintain observability infrastructure
- **Monitoring Teams**: Access metrics, traces, and alerts through dashboards
- **Data Teams**: Analyze observability data for insights

#### External Systems

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Jaeger**: Distributed tracing backend
- **OpenTelemetry**: Telemetry data collection standard

---

## 🏗️ Level 2: Container Architecture

### Container Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      FLEXT Observability System                          │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    User Interfaces (APIs)                        │    │
│  │                                                                 │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │ │
│  │  │   Simple API    │  │   Monitoring    │  │   REST API      │   │ │
│  │  │   Functions     │  │   Decorators    │  │   (Future)      │   │ │
│  │  │                 │  │                 │  │                 │   │ │
│  │  │ • flext_create_ │  │ • @flext_monitor│  │ • HTTP Endpoints│   │ │
│  │  │   metric()      │  │   _function     │  │ • Metrics Export│   │ │
│  │  │ • flext_create_ │  │ • Auto-tracing  │  │ • Health Checks │   │ │
│  │  │   trace()       │  │ • Auto-metrics │  │                 │   │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                   Core Application Services                       │    │
│  │                                                                 │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │ │
│  │  │   Metrics       │  │   Tracing       │  │   Alerting      │   │ │
│  │  │   Service       │  │   Service       │  │   Service       │   │ │
│  │  │                 │  │                 │  │                 │   │ │
│  │  │ • Counter/Gauge │  │ • Trace Creation│  │ • Alert Rules   │   │ │
│  │  │ • Histograms    │  │ • Span Context  │  │ • Notifications  │   │ │
│  │  │ • Aggregation   │  │ • Correlation   │  │ • Escalation    │   │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     Domain Layer (Core)                          │    │
│  │                                                                 │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │ │
│  │  │   Domain        │  │   Business      │  │   Validation    │   │ │
│  │  │   Entities      │  │   Logic         │  │   Rules         │   │ │
│  │  │                 │  │                 │  │                 │   │ │
│  │  │ • FlextMetric   │  │ • Domain Rules  │  │ • Pydantic v2   │   │ │
│  │  │ • FlextTrace    │  │ • Constraints   │  │ • Type Safety   │   │ │
│  │  │ • FlextAlert    │  │ • Invariants    │  │ • Business Rules│   │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                 Infrastructure & External Systems                 │    │
│  │                                                                 │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │ │
│  │  │   Storage       │  │   External      │  │   Configuration │   │ │
│  │  │   Layer         │  │   Systems       │  │   Management    │   │ │
│  │  │                 │  │                 │  │                 │   │ │
│  │  │ • In-Memory     │  │ • Prometheus    │  │ • Pydantic      │   │ │
│  │  │ • Future: Redis │  │ • Jaeger        │  │ • Settings      │   │ │
│  │  │ • Future: DB    │  │ • OpenTelemetry │  │ • Environment   │   │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### Container Descriptions

#### **Simple API Container**

- **Technology**: Python Functions
- **Purpose**: Easy-to-use factory functions for quick integration
- **Interfaces**: `flext_create_metric()`, `flext_create_trace()`, `flext_create_alert()`
- **Users**: Application developers needing simple observability integration

#### **Monitoring Decorators Container**

- **Technology**: Python Decorators
- **Purpose**: Automatic instrumentation of functions and methods
- **Interfaces**: `@flext_monitor_function`, `@flext_monitor_method`
- **Users**: Framework and library developers

#### **Core Application Services Container**

- **Technology**: Python Classes with Railway Pattern
- **Purpose**: Business logic orchestration and service coordination
- **Interfaces**: `FlextObservabilityServices` unified service class
- **Dependencies**: Domain entities, storage layer

#### **Domain Layer Container**

- **Technology**: Pydantic v2 Models, Domain Entities
- **Purpose**: Core business logic and domain rules
- **Interfaces**: `FlextMetric`, `FlextTrace`, `FlextAlert`, `FlextHealthCheck`
- **Characteristics**: Immutable entities, business rule validation

#### **Infrastructure Layer Container**

- **Technology**: External APIs, Storage Abstractions
- **Purpose**: External system integrations and persistence
- **Interfaces**: Prometheus client, OpenTelemetry SDK, Storage adapters
- **Characteristics**: Pluggable implementations, abstraction layers

---

## 🔧 Level 3: Component Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   FLEXT Observability Components                        │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    Interface Adapters                            │    │
│  │                                                                 │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐  │ │
│  │  │Simple API   │  │Factory Func │  │Monitor Dec │  │REST API │  │ │
│  │  │Functions    │  │tions        │  │orators     │  │(Future) │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘  │ │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                 Application Service Components                   │    │
│  │                                                                 │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐  │ │
│  │  │Metrics Svc  │  │Tracing Svc │  │Alert Svc   │  │Health Svc│  │ │
│  │  │Components   │  │Components   │  │Components  │  │Components│  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘  │ │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                   Domain Model Components                        │    │
│  │                                                                 │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐  │ │
│  │  │Metric Entity│  │Trace Entity│  │Alert Entity│  │Health Ent│  │ │
│  │  │& Value Obj  │  │& Value Obj  │  │& Value Obj │  │ity       │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘  │ │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │               Infrastructure Components                          │    │
│  │                                                                 │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐  │ │
│  │  │Storage Impl │  │External API│  │Config Mgmt │  │Logging   │  │ │
│  │  │(In-Memory)  │  │Clients      │  │            │  │Framework │  │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘  │ │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Components

#### **Metrics Service Components**

- **Counter Recorder**: Thread-safe counter increment operations
- **Gauge Recorder**: Real-time value recording with metadata
- **Histogram Recorder**: Statistical distribution tracking
- **Metrics Aggregator**: Data aggregation and statistical calculations
- **Export Formatter**: Prometheus/OpenMetrics format conversion

#### **Tracing Service Components**

- **Trace Creator**: Distributed trace initialization and context management
- **Span Manager**: Individual operation tracking within traces
- **Context Propagator**: Trace context passing between services
- **Trace Correlator**: Linking related operations across services
- **Trace Exporter**: OpenTelemetry protocol export

#### **Alerting Service Components**

- **Alert Rule Engine**: Condition evaluation and threshold checking
- **Alert Manager**: Alert lifecycle management and state tracking
- **Notification Dispatcher**: Multi-channel alert delivery
- **Escalation Manager**: Alert priority handling and routing
- **Alert History**: Alert persistence and audit trail

#### **Domain Entities**

- **FlextMetric**: Immutable metric data with validation
- **FlextTrace**: Trace context and span hierarchy
- **FlextAlert**: Alert definition with severity and routing
- **FlextHealthCheck**: Health status with dependency tracking

---

## 💻 Level 4: Code Architecture

### Code Package Structure

```
src/flext_observability/
├── __init__.py                 # Public API exports (58 items)
├── __version__.py              # Version metadata
├── py.typed                    # Type marker
│
├── models.py                   # Domain Models facade
│   ├── alerting.py             # Alert domain models
│   ├── health.py               # Health check models
│   ├── logging.py              # Logging entry models
│   ├── metrics.py              # Metrics domain models
│   └── tracing.py              # Tracing domain models
│
├── services.py                 # Unified service implementations
├── factories.py                # Factory functions and master factory
├── monitoring.py               # Monitoring decorators and utilities
│
├── config.py                   # Configuration management
├── constants.py                # Domain constants
├── exceptions.py               # Custom exceptions
│
├── fields.py                   # Pydantic field definitions
├── protocols.py                # Interface definitions
├── typings.py                  # Type definitions and aliases
│
└── utilities.py                # Helper functions
```

### Key Classes and Relationships

#### **Domain Layer Classes**

```python
# Core Domain Entities
class FlextMetric(FlextModels.Entity):
    """Immutable metric entity with domain validation."""
    name: str
    value: float
    unit: str
    timestamp: datetime
    tags: dict[str, str]

class FlextTrace(FlextModels.Entity):
    """Distributed trace entity with span hierarchy."""
    trace_id: str
    spans: list[Span]
    context: TraceContext

class FlextAlert(FlextModels.Entity):
    """Alert entity with severity and routing."""
    name: str
    severity: AlertLevel
    message: str
    condition: AlertCondition
```

#### **Service Layer Classes**

```python
class FlextObservabilityServices(FlextUtilities):
    """Unified service class with all observability operations."""

    @classmethod
    def record_counter(cls, name: str, value: float = 1.0) -> FlextResult[None]:
        """Record counter metric with thread safety."""

    @classmethod
    def create_trace(cls, operation: str) -> FlextResult[FlextTrace]:
        """Create new distributed trace."""

    @classmethod
    def evaluate_alert(cls, alert: FlextAlert) -> FlextResult[bool]:
        """Evaluate alert conditions."""
```

#### **Factory Classes**

```python
class FlextObservabilityMasterFactory:
    """Central factory for all observability entities."""

    def create_metric(self, name: str, value: float, unit: str) -> FlextResult[FlextMetric]:
        """Create validated metric entity."""

    def create_trace(self, operation: str, context: dict) -> FlextResult[FlextTrace]:
        """Create validated trace entity."""
```

---

## 🔄 Dynamic Behavior

### Observability Data Flow

```
User Request
     ↓
Simple API / Decorators
     ↓ (Validation)
Domain Entity Creation
     ↓ (Business Logic)
Application Service Processing
     ↓ (Storage)
Infrastructure Layer Persistence
     ↓ (Export)
External Monitoring Systems
```

### Error Handling Flow

```
Domain Validation Failure
     ↓
FlextResult[T].fail(error_message)
     ↓
Service Layer Error Handling
     ↓
Interface Adapter Error Response
     ↓
Structured Error Logging
     ↓
External System Notification
```

---

## 🏛️ Architectural Decisions

### ADRs Referenced

- **ADR-001**: Railway-oriented Programming with FlextResult[T]
- **ADR-002**: Clean Architecture Layer Separation
- **ADR-003**: Domain-Driven Design with Pydantic Entities
- **ADR-004**: Unified Service Class Pattern
- **ADR-005**: Factory Function API Design

### Key Architectural Principles

1. **Railway Pattern**: All operations return `FlextResult[T]` for composable error handling
2. **Clean Architecture**: Strict layer separation (Domain → Application → Infrastructure)
3. **Domain-Driven Design**: Rich domain entities with business logic validation
4. **Type Safety**: Complete Python 3.13+ type annotations throughout
5. **Unified API**: Single service class with flattened method structure
6. **Factory Pattern**: Consistent entity creation through factory functions
7. **Thread Safety**: All shared state protected with appropriate locking
8. **Pluggable Architecture**: External system integrations through abstraction layers

---

**C4 Model Views**: This documentation provides comprehensive architectural views at all four C4 levels, showing how FLEXT Observability serves as the foundation for enterprise observability across the entire FLEXT ecosystem.
