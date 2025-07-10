# FLEXT Simple Logging Guide

## Overview

The `flext-observability` package provides a simplified, standardized logging interface for all FLEXT projects. This guide shows how to use it effectively.

## Installation

All FLEXT projects should add `flext-observability` as a dependency:

```toml
[tool.poetry.dependencies]
flext-observability = {path = "../flext-observability", develop = true}
```

## Quick Start

### 1. Setup Logging (Once per Application)

In your main entry point or `__init__.py`:

```python
from flext_observability import setup_logging

setup_logging(
    service_name="flext-auth",  # Your service name
    log_level="INFO",           # DEBUG, INFO, WARNING, ERROR, CRITICAL
    json_logs=True,             # True for production, False for development
    environment="production",   # Any default context you want
    version="1.0.0"
)
```

### 2. Basic Logging

```python
from flext_observability.logging import get_logger

logger = get_logger(__name__)

# Log with structured data
logger.info("User authenticated", user_id=123, method="oauth2")
logger.error("Database connection failed", host="db.example.com", port=5432)
```

### 3. Quick Logging (No Logger Instance)

```python
from flext_observability import info, error, warning

info("Service started", port=8080)
warning("Cache miss", key="user:123")
error("Request failed", status_code=500, path="/api/users")
```

### 4. Automatic Duration Logging

```python
from flext_observability import log_duration

@log_duration
def process_payment(amount: float, currency: str):
    # Function duration will be automatically logged
    return {"status": "success"}

# With custom operation name
@log_duration(operation="payment_processing")
async def async_process(data):
    # Works with async functions too
    return await external_api.process(data)
```

### 5. Contextual Logging

```python
from flext_observability import LogContext, get_logger

logger = get_logger(__name__)

def handle_request(request_id: str, user_id: str):
    # All logs within this context will include request_id and user_id
    with LogContext(request_id=request_id, user_id=user_id):
        logger.info("Processing request")
        
        # These fields are automatically included
        validate_user()  # Logs will have request_id and user_id
        process_data()   # Logs will have request_id and user_id
        
        logger.info("Request completed")
```

### 6. Error Logging with Stack Traces

```python
from flext_observability import log_error, get_logger

logger = get_logger(__name__)

try:
    risky_operation()
except Exception as e:
    # Option 1: Using log_error helper
    log_error(e, "Operation failed", operation="risky_operation", attempt=3)
    
    # Option 2: Using logger directly
    logger.exception("Operation failed", operation="risky_operation")
```

## Configuration via Environment Variables

The logging system respects these environment variables:

```bash
# Service identification
export SERVICE_NAME=flext-auth

# Logging configuration  
export LOG_LEVEL=INFO
export LOG_FORMAT=json  # or "console" for development

# These will be included in all logs if set
export ENVIRONMENT=production
export DEPLOYMENT_ID=abc123
export REGION=us-west-2
```

## Best Practices

### 1. Use Structured Logging

```python
# ❌ Bad - String concatenation
logger.info(f"User {user_id} logged in from {ip_address}")

# ✅ Good - Structured data
logger.info("User logged in", user_id=user_id, ip_address=ip_address)
```

### 2. Include Relevant Context

```python
# ❌ Bad - Missing context
logger.error("Failed to process")

# ✅ Good - Rich context
logger.error(
    "Failed to process order",
    order_id=order_id,
    error_type=type(e).__name__,
    customer_id=customer_id,
    retry_count=retry_count
)
```

### 3. Use Appropriate Log Levels

- **DEBUG**: Detailed information for diagnosing problems
- **INFO**: General informational messages
- **WARNING**: Something unexpected but not critical
- **ERROR**: Error events but application continues
- **CRITICAL**: Serious errors that may abort the program

### 4. Avoid Logging Sensitive Data

```python
# ❌ Bad - Logs password
logger.info("User login", username=username, password=password)

# ✅ Good - Masks sensitive data  
logger.info("User login", username=username, has_password=bool(password))
```

### 5. Use Log Context for Request Tracking

```python
@app.route("/api/users/<user_id>")
def get_user(user_id: str):
    request_id = str(uuid.uuid4())
    
    with LogContext(request_id=request_id, user_id=user_id, endpoint="get_user"):
        logger.info("Request started")
        
        user = fetch_user(user_id)  # All logs include context
        
        logger.info("Request completed", status="success")
        return user
```

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, Request
from flext_observability import setup_logging, get_logger, LogContext
import uuid

app = FastAPI()
logger = get_logger(__name__)

# Setup logging on startup
@app.on_event("startup")
async def startup_event():
    setup_logging(service_name="flext-api", json_logs=True)

# Middleware for request context
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    
    with LogContext(
        request_id=request_id,
        method=request.method,
        path=request.url.path
    ):
        logger.info("Request started")
        response = await call_next(request)
        logger.info("Request completed", status_code=response.status_code)
        return response
```

### Django Integration

```python
# In settings.py
from flext_observability import setup_logging

setup_logging(
    service_name="flext-web",
    log_level="INFO",
    json_logs=not DEBUG  # Human-readable in development
)

# In views.py
from flext_observability.logging import get_logger, log_duration

logger = get_logger(__name__)

@log_duration
def user_profile_view(request, user_id):
    logger.info("Fetching user profile", user_id=user_id)
    # ... view logic ...
```

### Celery Integration

```python
from celery import Celery
from flext_observability import setup_logging, get_logger, LogContext

app = Celery('tasks')
logger = get_logger(__name__)

# Setup logging when worker starts
@app.on_after_configure.connect
def setup_logging_for_worker(sender, **kwargs):
    setup_logging(service_name="flext-worker", json_logs=True)

@app.task(bind=True)
def process_order(self, order_id: str):
    with LogContext(task_id=self.request.id, order_id=order_id):
        logger.info("Processing order")
        # ... task logic ...
```

## Output Examples

### JSON Format (Production)

```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "info",
  "logger": "flext_auth.services",
  "message": "User authenticated",
  "service": "flext-auth",
  "environment": "production",
  "user_id": 123,
  "method": "oauth2",
  "duration_ms": 45.2
}
```

### Console Format (Development)

```
2024-01-15 10:30:45 [info     ] User authenticated    [flext_auth.services] duration_ms=45.2 environment=development method=oauth2 service=flext-auth user_id=123
```

## Migration from Standard Logging

### Before (Standard Logging)

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Processing user %s", user_id)
```

### After (FLEXT Logging)

```python
from flext_observability.logging import get_logger

logger = get_logger(__name__)

logger.info("Processing user", user_id=user_id)
```

## Performance Considerations

1. **Logger Caching**: Loggers are cached by name, so `get_logger(__name__)` is efficient
2. **Lazy Evaluation**: Log messages are only formatted if the log level is enabled
3. **Async Support**: The `@log_duration` decorator works with both sync and async functions
4. **Context Performance**: `LogContext` uses context variables which are thread-safe and efficient

## Troubleshooting

### Logs Not Appearing

Check that:

1. `setup_logging()` is called before any logging
2. Log level is set appropriately (not filtering out your logs)
3. For JSON logs, ensure output is not being buffered

### Missing Context Fields

Ensure you're within a `LogContext` block or have bound the fields to your logger:

```python
# Option 1: Use LogContext
with LogContext(user_id=123):
    logger.info("Action performed")  # Will include user_id

# Option 2: Bind to logger
user_logger = logger.bind(user_id=123)
user_logger.info("Action performed")  # Will include user_id
```

### Performance Impact

If logging is impacting performance:

1. Reduce log level in production (e.g., WARNING instead of INFO)
2. Avoid logging in tight loops
3. Use sampling for high-frequency events
