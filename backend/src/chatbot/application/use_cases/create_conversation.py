"""Create conversation use case."""
from uuid import UUID, uuid4

from src.chatbot.domain.entities.conversation import Conversation
from src.chatbot.domain.repositories.conversation_repository import ConversationRepository


class CreateConversationUseCase:
    """Use case for creating a new conversation."""

    def __init__(self, conversation_repository: ConversationRepository) -> None:
        """Initialize use case with repositories."""
        self.conversation_repository = conversation_repository

    async def execute(self, user_id: UUID, title: str) -> Conversation:
        """Execute the use case."""
        conversation = Conversation(id=uuid4(), user_id=user_id, title=title)
        return await self.conversation_repository.create(conversation)
