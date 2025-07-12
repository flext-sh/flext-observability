"""Base repository classes for observability persistence.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar

from flext_core.domain.types import ServiceResult

if TYPE_CHECKING:
    from uuid import UUID

T = TypeVar("T")


class BaseRepository[T](ABC):
    """Base repository interface for observability entities."""

    @abstractmethod
    async def save(self, entity: T) -> ServiceResult[T]:
        """Save entity to repository."""
        ...

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> ServiceResult[T | None]:
        """Get entity by ID."""
        ...

    @abstractmethod
    async def delete(self, entity_id: UUID) -> ServiceResult[bool]:
        """Delete entity by ID."""
        ...

    @abstractmethod
    async def list(self, limit: int = 100, offset: int = 0) -> ServiceResult[list[T]]:
        """List entities with pagination."""
        ...

    @abstractmethod
    async def count(self) -> ServiceResult[int]:
        """Count total entities."""
        ...


class InMemoryRepository(BaseRepository[T]):
    """In-memory repository implementation for testing."""

    def __init__(self) -> None:
        """Initialize empty repository."""
        self._entities: dict[UUID, T] = {}

    async def save(self, entity: T) -> ServiceResult[T]:
        """Save entity to in-memory storage.

        Args:
            entity: Entity to save (must have ID attribute).

        Returns:
            ServiceResult with saved entity or error.

        """
        try:
            entity_id = getattr(entity, "id", None)
            if entity_id is None:
                return ServiceResult.fail("Entity must have an ID")

            self._entities[entity_id] = entity
            return ServiceResult.ok(entity)
        except Exception as e:
            return ServiceResult.fail(f"Failed to save entity: {e}")

    async def get_by_id(self, entity_id: UUID) -> ServiceResult[T | None]:
        """Get entity from storage by ID.

        Args:
            entity_id: Unique identifier of entity to retrieve.

        Returns:
            ServiceResult with entity if found, None if not found, or error.

        """
        try:
            entity = self._entities.get(entity_id)
            return ServiceResult.ok(entity)
        except Exception as e:
            return ServiceResult.fail(f"Failed to get entity: {e}")

    async def delete(self, entity_id: UUID) -> ServiceResult[bool]:
        """Delete entity from storage by ID.

        Args:
            entity_id: Unique identifier of entity to delete.

        Returns:
            ServiceResult with True if deleted, False if not found.

        """
        try:
            if entity_id in self._entities:
                del self._entities[entity_id]
                return ServiceResult.ok(True)
            return ServiceResult.ok(False)
        except Exception as e:
            return ServiceResult.fail(f"Failed to delete entity: {e}")

    async def list(self, limit: int = 100, offset: int = 0) -> ServiceResult[list[T]]:
        """List entities with pagination.

        Args:
            limit: Maximum number of entities to return.
            offset: Number of entities to skip.

        Returns:
            ServiceResult with list of entities.

        """
        try:
            entities = list(self._entities.values())
            paginated = entities[offset : offset + limit]
            return ServiceResult.ok(paginated)
        except Exception as e:
            return ServiceResult.fail(f"Failed to list entities: {e}")

    async def count(self) -> ServiceResult[int]:
        """Count total number of entities in storage.

        Returns:
            ServiceResult with count of entities or error.

        """
        try:
            return ServiceResult.ok(len(self._entities))
        except Exception as e:
            return ServiceResult.fail(f"Failed to count entities: {e}")


# Create type aliases for the repository interfaces
AlertRepository = BaseRepository
MetricsRepository = BaseRepository
LogRepository = BaseRepository
TraceRepository = BaseRepository
HealthRepository = BaseRepository
DashboardRepository = BaseRepository  # Type alias


class EventBus(ABC):
    """Event bus interface."""

    @abstractmethod
    async def publish(self, event: Any) -> None:
        """Publish event to bus."""
        ...

    @abstractmethod
    async def subscribe(self, event_type: type[Any], handler: Any) -> None:
        """Subscribe to events of specific type."""
        ...

    @abstractmethod
    async def unsubscribe(self, event_type: type[Any], handler: Any) -> None:
        """Unsubscribe from events of specific type."""
        ...
