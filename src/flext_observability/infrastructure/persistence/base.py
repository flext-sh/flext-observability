"""Base repository classes for observability persistence.

REFACTORED: Uses flext-core patterns for repository implementations.
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
        """Save an entity."""

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> ServiceResult[T | None]:
        """Get entity by ID."""

    @abstractmethod
    async def delete(self, entity_id: UUID) -> ServiceResult[bool]:
        """Delete entity by ID."""

    @abstractmethod
    async def list(self, limit: int = 100, offset: int = 0) -> ServiceResult[list[T]]:
        """List entities with pagination."""

    @abstractmethod
    async def count(self) -> ServiceResult[int]:
        """Count total entities."""


class InMemoryRepository(BaseRepository[T]):
    """In-memory repository implementation for testing."""

    def __init__(self) -> None:
        self._entities: dict[UUID, T] = {}

    async def save(self, entity: T) -> ServiceResult[T]:
        """Save entity in memory."""
        try:
            entity_id = getattr(entity, "id", None)
            if entity_id is None:
                return ServiceResult.fail("Entity must have an ID")

            self._entities[entity_id] = entity
            return ServiceResult.ok(entity)
        except Exception as e:
            return ServiceResult.fail(f"Failed to save entity: {e}")

    async def get_by_id(self, entity_id: UUID) -> ServiceResult[T | None]:
        """Get entity by ID from memory."""
        try:
            entity = self._entities.get(entity_id)
            return ServiceResult.ok(entity)
        except Exception as e:
            return ServiceResult.fail(f"Failed to get entity: {e}")

    async def delete(self, entity_id: UUID) -> ServiceResult[bool]:
        """Delete entity from memory."""
        try:
            if entity_id in self._entities:
                del self._entities[entity_id]
                return ServiceResult.ok(True)
            return ServiceResult.ok(False)
        except Exception as e:
            return ServiceResult.fail(f"Failed to delete entity: {e}")

    async def list(self, limit: int = 100, offset: int = 0) -> ServiceResult[list[T]]:
        """List entities from memory."""
        try:
            entities = list(self._entities.values())
            paginated = entities[offset : offset + limit]
            return ServiceResult.ok(paginated)
        except Exception as e:
            return ServiceResult.fail(f"Failed to list entities: {e}")

    async def count(self) -> ServiceResult[int]:
        """Count entities in memory."""
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
DashboardRepository = BaseRepository


class EventBus(ABC):
    """Event bus interface."""

    @abstractmethod
    async def publish(self, event: Any) -> ServiceResult[None]:
        """Publish an event."""
