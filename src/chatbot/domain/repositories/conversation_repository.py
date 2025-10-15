"""Conversation repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.chatbot.domain.entities.conversation import Conversation


class ConversationRepository(ABC):
    """Repository interface for Conversation entity."""

    @abstractmethod
    async def create(self, conversation: Conversation) -> Conversation:
        """Create a new conversation."""
        pass

    @abstractmethod
    async def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get a conversation by ID."""
        pass

    @abstractmethod
    async def list_all(self, limit: int = 100, offset: int = 0) -> List[Conversation]:
        """List all conversations with pagination."""
        pass

    @abstractmethod
    async def update(self, conversation: Conversation) -> Conversation:
        """Update an existing conversation."""
        pass

    @abstractmethod
    async def delete(self, conversation_id: UUID) -> bool:
        """Delete a conversation by ID."""
        pass
