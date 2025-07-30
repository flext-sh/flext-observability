#!/usr/bin/env python3

"""Debug script to understand test failure."""

from unittest.mock import Mock
from flext_core import FlextContainer, FlextResult
from flext_observability import FlextMetricsService

def test_debug() -> None:
    """Debug the test failure."""
    print("=== Debug Test ===")
    
    # Create container and service
    container = FlextContainer()
    metrics_service = FlextMetricsService(container=container)
    
    # Create mock metric
    sample_metric = Mock()
    sample_metric.name = "test_metric"
    sample_metric.value = 42.0
    sample_metric.unit = "count"
    
    # Create mock repository
    mock_repository = Mock()
    mock_repository.save.return_value = FlextResult.ok(sample_metric)
    
    print(f"Mock repository: {mock_repository}")
    print(f"Mock repository.save: {mock_repository.save}")
    
    # Register repository
    container.register("metrics_repository", mock_repository)
    
    # Verify registration worked
    get_result = container.get("metrics_repository")
    print(f"Get result is_success: {get_result.is_success}")
    print(f"Get result data: {get_result.data}")
    print(f"Get result data == mock_repository: {get_result.data == mock_repository}")
    print(f"Get result data is mock_repository: {get_result.data is mock_repository}")
    
    # Test domain service (should not exist)
    domain_result = container.get("metrics_domain_service")
    print(f"Domain service result is_success: {domain_result.is_success}")
    
    # Execute the service method
    print("\n=== Executing record_metric ===")
    result = metrics_service.record_metric(sample_metric)
    
    print(f"Result is_success: {result.is_success}")
    print(f"Result data: {result.data}")
    print(f"Result error: {result.error if hasattr(result, 'error') else 'No error attr'}")
    
    # Check if save was called
    print(f"Save call count: {mock_repository.save.call_count}")
    print(f"Save call args: {mock_repository.save.call_args_list}")

if __name__ == "__main__":
    test_debug()