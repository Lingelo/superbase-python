"""Conversation entity."""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Conversation(BaseModel):
    """Conversation domain entity."""

    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""

        from_attributes = True
