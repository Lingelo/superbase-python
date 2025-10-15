"""User entity."""
from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    """User entity representing an authenticated user."""

    id: UUID
    email: str
