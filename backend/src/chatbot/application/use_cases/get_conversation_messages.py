"""Get conversation messages use case."""
from typing import List
from uuid import UUID

from src.chatbot.domain.entities.message import Message
from src.chatbot.domain.repositories.message_repository import MessageRepository


class GetConversationMessagesUseCase:
    """Use case for retrieving conversation messages."""

    def __init__(self, message_repository: MessageRepository) -> None:
        """Initialize use case with repositories."""
        self.message_repository = message_repository

    async def execute(
        self, conversation_id: UUID, limit: int = 100, offset: int = 0
    ) -> List[Message]:
        """Execute the use case."""
        return await self.message_repository.list_by_conversation(
            conversation_id, limit=limit, offset=offset
        )
