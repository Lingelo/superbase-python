"""List conversations use case."""
from typing import List
from uuid import UUID

from src.chatbot.domain.entities.conversation import Conversation
from src.chatbot.domain.repositories.conversation_repository import ConversationRepository


class ListConversationsUseCase:
    """Use case for listing conversations."""

    def __init__(self, conversation_repository: ConversationRepository) -> None:
        """Initialize use case with repositories."""
        self.conversation_repository = conversation_repository

    async def execute(self, user_id: UUID, limit: int = 100, offset: int = 0) -> List[Conversation]:
        """Execute the use case."""
        return await self.conversation_repository.list_all(user_id=user_id, limit=limit, offset=offset)
