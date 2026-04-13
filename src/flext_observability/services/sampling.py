"""Sampling strategy implementation for production performance optimization.

Provides head-based sampling (sample at request entry point) to reduce observability
overhead in production while maintaining visibility into critical operations.

FLEXT Pattern:
- Single FlextObservabilitySampling class
- Configurable sampling rates per environment
- Per-service and per-operation sampling
- Context-aware sampling decisions

Key Features:
- Head-based sampling (decision made once at request start)
- Environment-based configuration (dev, staging, production)
- Per-service override capability
- Per-operation override capability
- Deterministic sampling (same request sampled consistently)
"""

from __future__ import annotations

import random
from collections.abc import MutableMapping

from flext_observability import FlextObservabilityContext, c, p, r, u


class FlextObservabilitySampling:
    """Sampling strategy for production performance optimization.

    Implements head-based sampling to reduce observability overhead while
    maintaining visibility into critical operations.

    Usage:
        ```python
        from flext_observability import FlextObservabilitySampling

        # Configure sampling
        sampler = FlextObservabilitySampling.active_sampler()
        sampler.update_environment("production")
        sampler.update_default_rate(0.1)  # 10% sampling in production

        # Make sampling decision at request entry
        should_sample = sampler.should_sample(
            operation="POST /api/users", service="user-service"
        )

        if should_sample:
            # Enable full observability for this request
            trace_handler.start_trace()
        else:
            # Minimal logging/metrics
            pass
        ```

    Nested Classes:
        Sampler: Sampling strategy configuration and decisions
    """

    _logger = u.fetch_logger(__name__)
    _sampler_instance: FlextObservabilitySampling.Sampler | None = None

    class Sampler:
        """Sampling decision engine."""

        def __init__(self) -> None:
            """Initialize sampler with default settings."""
            self._environment = "development"
            self._default_rate = 1.0
            self._environment_rates: MutableMapping[str, float] = {
                "development": 1.0,
                "staging": 0.5,
                "production": 0.1,
            }
            self._service_overrides: MutableMapping[str, float] = {}
            self._operation_overrides: MutableMapping[str, float] = {}
            self._sampled_trace_ids: set[str] = set()

        def current_rate(
            self,
            operation: str | None = None,
            service: str | None = None,
        ) -> float:
            """Return the effective sampling rate for an operation/service.

            Args:
                operation: Operation name
                service: Service name

            Returns:
                float - Effective sampling rate (0.0 to 1.0)

            """
            rate = self._default_rate
            if service and service in self._service_overrides:
                rate = self._service_overrides[service]
            if operation and operation in self._operation_overrides:
                rate = self._operation_overrides[operation]
            return rate

        def sampling_decision(
            self,
            operation: str | None = None,
            service: str | None = None,
        ) -> c.Observability.SamplingDecision:
            """Return the sampling decision as an enum.

            Args:
                operation: Operation name
                service: Service name

            Returns:
                c.Observability.SamplingDecision - SAMPLED or NOT_SAMPLED

            """
            if self.should_sample(operation=operation, service=service):
                return c.Observability.SamplingDecision.SAMPLED
            return c.Observability.SamplingDecision.NOT_SAMPLED

        def update_default_rate(self, rate: float) -> p.Result[bool]:
            """Update the default sampling rate (0.0 to 1.0).

            Args:
                rate: Sampling rate (0.0 = never sample, 1.0 = always sample)

            Returns:
                r[bool] - Ok if rate is valid

            Behavior:
                - Overrides environment-based rate
                - 0.0 = minimal observability
                - 0.1 = 10% (typical production)
                - 1.0 = 100% (full observability)

            """
            if not 0.0 <= rate <= 1.0:
                return r[bool].fail(
                    f"Invalid sampling rate: {rate}. Must be between 0.0 and 1.0",
                )
            self._default_rate = rate
            FlextObservabilitySampling._logger.debug(
                f"Default sampling rate set to {rate}",
            )
            return r[bool].ok(value=True)

        def update_environment(self, environment: str) -> p.Result[bool]:
            """Update the current environment for sampling configuration.

            Args:
                environment: Environment name (development, staging, production)

            Returns:
                r[bool] - Ok if valid environment

            Behavior:
                - Updates default sampling rate based on environment
                - Follows: dev=100%, staging=50%, prod=10%
                - Can be overridden with update_default_rate()

            """
            valid_envs = ["development", "staging", "production"]
            if environment not in valid_envs:
                return r[bool].fail(
                    f"Invalid environment: {environment}. Must be one of {valid_envs}",
                )
            self._environment = environment
            self._default_rate = self._environment_rates.get(environment, 0.1)
            FlextObservabilitySampling._logger.debug(
                f"Sampling environment set to {environment} (rate: {self._default_rate})",
            )
            return r[bool].ok(value=True)

        def update_operation_rate(self, operation: str, rate: float) -> p.Result[bool]:
            """Update the sampling rate for a specific operation.

            Args:
                operation: Operation name (e.g., "POST /api/users")
                rate: Sampling rate for this operation (0.0 to 1.0)

            Returns:
                r[bool] - Ok if rate is valid

            Behavior:
                - Per-operation rate overrides service and default rates
                - Useful for critical endpoints or expensive operations

            """
            if not 0.0 <= rate <= 1.0:
                return r[bool].fail(
                    f"Invalid sampling rate: {rate}. Must be between 0.0 and 1.0",
                )
            self._operation_overrides[operation] = rate
            FlextObservabilitySampling._logger.debug(
                f"Sampling rate for operation '{operation}' set to {rate}",
            )
            return r[bool].ok(value=True)

        def update_service_rate(self, service: str, rate: float) -> p.Result[bool]:
            """Update the sampling rate for a specific service.

            Args:
                service: Service name (e.g., "user-service")
                rate: Sampling rate for this service (0.0 to 1.0)

            Returns:
                r[bool] - Ok if rate is valid

            Behavior:
                - Per-service rate overrides default rate
                - Useful for high-traffic services (lower rate)
                - Or critical services (higher rate)

            """
            if not 0.0 <= rate <= 1.0:
                return r[bool].fail(
                    f"Invalid sampling rate: {rate}. Must be between 0.0 and 1.0",
                )
            self._service_overrides[service] = rate
            FlextObservabilitySampling._logger.debug(
                f"Sampling rate for service '{service}' set to {rate}",
            )
            return r[bool].ok(value=True)

        def should_sample(
            self,
            operation: str | None = None,
            service: str | None = None,
        ) -> bool:
            """Determine if request should be sampled (head-based decision).

            Args:
                operation: Operation name (e.g., "GET /api/users")
                service: Service name (e.g., "user-service")

            Returns:
                bool - True if request should be sampled

            Behavior:
                - Deterministic: same request_id always sampled same way
                - Priority: operation rate > service rate > default rate
                - Uses random sampling within configured rate

            """
            sampling_rate = self._default_rate
            if service and service in self._service_overrides:
                sampling_rate = self._service_overrides[service]
            if operation and operation in self._operation_overrides:
                sampling_rate = self._operation_overrides[operation]
            if sampling_rate >= 1.0:
                return True
            if sampling_rate <= 0.0:
                return False
            try:
                correlation_id = FlextObservabilityContext.correlation_id()
                hash_val = hash(correlation_id) % 100
                return hash_val / 100 < sampling_rate
            except (ValueError, TypeError, KeyError):
                return random.SystemRandom().random() < sampling_rate

    @staticmethod
    def active_sampler() -> FlextObservabilitySampling.Sampler:
        """Return the global sampler instance.

        Returns:
            Sampler - Global sampler instance

        Behavior:
            - Creates sampler on first call
            - Returns same instance for all subsequent calls
            - Thread-safe for sampling decisions

        """
        if FlextObservabilitySampling._sampler_instance is None:
            FlextObservabilitySampling._sampler_instance = (
                FlextObservabilitySampling.Sampler()
            )
        return FlextObservabilitySampling._sampler_instance

    @staticmethod
    def sampling_decision(
        operation: str | None = None,
        service: str | None = None,
    ) -> c.Observability.SamplingDecision:
        """Convenience function: return the sampling decision as an enum.

        Args:
            operation: Operation name
            service: Service name

        Returns:
            c.Observability.SamplingDecision - SAMPLED or NOT_SAMPLED

        """
        sampler = FlextObservabilitySampling.active_sampler()
        return sampler.sampling_decision(operation=operation, service=service)

    @staticmethod
    def should_sample(operation: str | None = None, service: str | None = None) -> bool:
        """Convenience function: make sampling decision.

        Args:
            operation: Operation name
            service: Service name

        Returns:
            bool - True if request should be sampled

        """
        sampler = FlextObservabilitySampling.active_sampler()
        return sampler.should_sample(operation=operation, service=service)


__all__: list[str] = ["FlextObservabilitySampling"]
