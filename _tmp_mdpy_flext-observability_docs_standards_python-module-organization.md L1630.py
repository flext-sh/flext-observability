# from flext-observability/docs/standards/python-module-organization.md:1630
from __future__ import annotations

# ✅ Consistent monitoring across ecosystem services
from flext_observability import flext_monitor_function


class FlextAPIService:
    """API service with ecosystem-standard monitoring."""

    @flext_monitor_function("api_endpoint")
    def handle_user_request(self, request_data: dict) -> p.Result[m.Dict]:
        """Handle API request with automatic monitoring."""
        # Automatically gets:
        # - Request latency metrics
        # - Success/failure tracking
        # - Distributed tracing
        # - Structured logging with correlation IDs

        return self._process_request(request_data)

    @flext_monitor_function("database_operation")
    def query_user_data(self, user_id: str) -> p.Result[m.Dict]:
        """Database query with monitoring."""
        # Database-specific observability patterns
        return self._execute_database_query(user_id)


class FlextOracleService:
    """Oracle service with ecosystem-standard monitoring."""

    @flext_monitor_function("oracle_query")
    def execute_wms_query(self, query: str) -> p.Result[Sequence[m.Dict]]:
        """Execute Oracle WMS query with monitoring."""
        # Oracle-specific observability patterns
        return self._execute_oracle_query(query)


class FlextLdapService:
    """LDAP service with ecosystem-standard monitoring."""

    @flext_monitor_function("ldap_operation")
    def search_users(self, search_filter: str) -> p.Result[Sequence[m.Dict]]:
        """LDAP search with monitoring."""
        # LDAP-specific observability patterns
        return self._execute_ldap_search(search_filter)
