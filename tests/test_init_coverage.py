"""Test __init__.py coverage for legacy compatibility and public API."""

import warnings

from flext_core import FlextContainer


class TestInitCoverage:
    """Test coverage for __init__.py legacy facades and API functions."""

    def test_flext_health_status_function(self) -> None:
      """Test flext_health_status function coverage."""
      from flext_observability import flext_health_status

      result = flext_health_status()
      assert result["status"] == "healthy"
      assert result["service"] == "flext-observability"
      assert result["version"] == "0.9.0"

    def test_legacy_create_observability_platform(self) -> None:
      """Test legacy create_observability_platform function with deprecation warning."""
      from flext_observability import create_observability_platform

      # Capture deprecation warning
      with warnings.catch_warnings(record=True) as warning_list:
          warnings.simplefilter("always")
          factory = create_observability_platform()
          assert len(warning_list) == 1
          assert issubclass(warning_list[0].category, DeprecationWarning)
          assert "create_observability_platform is deprecated" in str(
              warning_list[0].message,
          )

      assert factory is not None

    def test_legacy_create_observability_platform_with_container(self) -> None:
      """Test legacy create_observability_platform with container parameter."""
      from flext_observability import create_observability_platform

      container = FlextContainer()

      with warnings.catch_warnings(record=True):
          warnings.simplefilter("always")
          factory = create_observability_platform(container)
          assert factory is not None
          assert factory.container is container

    def test_legacy_observability_platform(self) -> None:
      """Test legacy observability_platform function with deprecation warning."""
      from flext_observability import observability_platform

      with warnings.catch_warnings(record=True) as warning_list:
          warnings.simplefilter("always")
          factory = observability_platform()
          assert len(warning_list) == 1
          assert issubclass(warning_list[0].category, DeprecationWarning)
          assert "observability_platform is deprecated" in str(
              warning_list[0].message,
          )

      assert factory is not None

    def test_legacy_observability_platform_with_container(self) -> None:
      """Test legacy observability_platform with container parameter."""
      from flext_observability import observability_platform

      container = FlextContainer()

      with warnings.catch_warnings(record=True):
          warnings.simplefilter("always")
          factory = observability_platform(container)
          assert factory is not None
          assert factory.container is container

    def test_legacy_constants_facade(self) -> None:
      """Test legacy constants facade with deprecation warning."""
      from flext_observability import constants

      with warnings.catch_warnings(record=True) as warning_list:
          warnings.simplefilter("always")
          # Access any constant to trigger warning
          value = constants.DEFAULT_TIMEOUT
          assert len(warning_list) == 1
          assert issubclass(warning_list[0].category, DeprecationWarning)
          assert "constants.DEFAULT_TIMEOUT is deprecated" in str(
              warning_list[0].message,
          )

      # Should return something (even if "UNKNOWN")
      assert value is not None

    def test_legacy_constants_unknown_attribute(self) -> None:
      """Test legacy constants facade with unknown attribute."""
      from flext_observability import constants

      with warnings.catch_warnings(record=True):
          warnings.simplefilter("always")
          value = constants.NON_EXISTENT_CONSTANT
          assert value == "UNKNOWN"

    def test_deprecated_warning_function(self) -> None:
      """Test _deprecated_warning function directly."""
      from flext_observability import _deprecated_warning

      with warnings.catch_warnings(record=True) as warning_list:
          warnings.simplefilter("always")
          _deprecated_warning("old_function", "new_function")
          assert len(warning_list) == 1
          assert issubclass(warning_list[0].category, DeprecationWarning)
          assert "old_function is deprecated" in str(warning_list[0].message)
          assert "Use new_function instead" in str(warning_list[0].message)
          assert "Will be removed in v1.0.0" in str(warning_list[0].message)

    def test_all_public_api_imports(self) -> None:
      """Test that all __all__ exports can be imported successfully."""
      import flext_observability

      # Test all exports from __all__ list can be imported
      for export_name in flext_observability.__all__:
          assert hasattr(flext_observability, export_name), (
              f"Missing export: {export_name}"
          )
          exported_item = getattr(flext_observability, export_name)
          assert exported_item is not None, f"Null export: {export_name}"
