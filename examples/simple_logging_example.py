"""Example of using the simplified logging interface."""

from flext_observability import LogContext
from flext_observability import error
from flext_observability import get_logger
from flext_observability import info
from flext_observability import log_duration
from flext_observability import setup_logging

# 1. Setup logging once at application startup
setup_logging(
    service_name="example-service",
    log_level="INFO",
    json_logs=True,  # Set to False for human-readable output
    environment="development",
    version="1.0.0",
)

# 2. Get a logger for your module
logger = get_logger(__name__)


# 3. Use decorators for automatic duration logging
@log_duration
def process_data(data: list) -> int:
    """Process some data with automatic duration logging."""
    logger.info("Processing data", count=len(data))

    # Simulate some work
    import time

    time.sleep(0.1)

    return len(data) * 2


# 4. Use context managers for correlated logs
def handle_user_request(user_id: str, request_id: str):
    """Handle a user request with contextual logging."""
    with LogContext(user_id=user_id, request_id=request_id):
        logger.info("Handling user request")

        try:
            # All logs within this context will include user_id and request_id
            result = process_data([1, 2, 3, 4, 5])
            logger.info("Request processed successfully", result=result)
            return result

        except Exception as e:
            logger.error("Failed to process request", error=str(e), exc_info=True)
            raise


# 5. Quick logging without logger instance
def main() -> None:
    """Main application entry point."""
    info("Application starting", pid=os.getpid())

    try:
        # Example usage
        result = handle_user_request("user123", "req456")
        info("Application completed", result=result)

    except Exception as e:
        error("Application failed", error=str(e))
        raise

    finally:
        info("Application shutting down")


if __name__ == "__main__":
    import os

    main()
