"""Message repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.chatbot.domain.entities.message import Message


class MessageRepository(ABC):
    """Repository interface for Message entity."""

    @abstractmethod
    async def create(self, message: Message) -> Message:
        """Create a new message."""
        pass

    @abstractmethod
    async def get_by_id(self, message_id: UUID) -> Optional[Message]:
        """Get a message by ID."""
        pass

    @abstractmethod
    async def list_by_conversation(
        self, conversation_id: UUID, limit: int = 100, offset: int = 0
    ) -> List[Message]:
        """List all messages for a conversation."""
        pass

    @abstractmethod
    async def delete(self, message_id: UUID) -> bool:
        """Delete a message by ID."""
        pass
