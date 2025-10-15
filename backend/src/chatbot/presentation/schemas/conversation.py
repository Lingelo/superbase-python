"""Conversation API schemas."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ConversationCreateRequest(BaseModel):
    """Request schema for creating a conversation."""

    title: str


class ConversationResponse(BaseModel):
    """Response schema for conversation."""

    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True
