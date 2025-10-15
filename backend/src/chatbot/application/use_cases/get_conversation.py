"""Get conversation use case."""
from typing import Optional
from uuid import UUID

from src.chatbot.domain.entities.conversation import Conversation
from src.chatbot.domain.repositories.conversation_repository import ConversationRepository


class GetConversationUseCase:
    """Use case for retrieving a conversation."""

    def __init__(self, conversation_repository: ConversationRepository) -> None:
        """Initialize use case with repositories."""
        self.conversation_repository = conversation_repository

    async def execute(self, conversation_id: UUID, user_id: UUID) -> Optional[Conversation]:
        """Execute the use case."""
        return await self.conversation_repository.get_by_id(conversation_id, user_id)
