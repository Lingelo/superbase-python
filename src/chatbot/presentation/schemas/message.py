"""Message API schemas."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.chatbot.domain.entities.message import MessageRole


class MessageSendRequest(BaseModel):
    """Request schema for sending a message."""

    content: str


class MessageResponse(BaseModel):
    """Response schema for message."""

    id: UUID
    conversation_id: UUID
    role: MessageRole
    content: str
    created_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True
