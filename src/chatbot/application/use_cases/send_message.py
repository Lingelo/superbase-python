"""Send message use case."""
from typing import List
from uuid import UUID, uuid4

from src.chatbot.domain.entities.message import Message, MessageRole
from src.chatbot.domain.repositories.message_repository import MessageRepository
from src.chatbot.domain.repositories.conversation_repository import ConversationRepository
from src.chatbot.infrastructure.langchain.chatbot_service import ChatbotService


class SendMessageUseCase:
    """Use case for sending a message and getting a response."""

    def __init__(
        self,
        message_repository: MessageRepository,
        conversation_repository: ConversationRepository,
        chatbot_service: ChatbotService,
    ) -> None:
        """Initialize use case with repositories and services."""
        self.message_repository = message_repository
        self.conversation_repository = conversation_repository
        self.chatbot_service = chatbot_service

    async def execute(self, conversation_id: UUID, content: str) -> Message:
        """Execute the use case."""
        # Verify conversation exists
        conversation = await self.conversation_repository.get_by_id(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")

        # Get conversation history
        history = await self.message_repository.list_by_conversation(conversation_id)

        # Create and save user message
        user_message = Message(
            id=uuid4(),
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=content,
        )
        await self.message_repository.create(user_message)

        # Generate AI response
        ai_response_content = await self.chatbot_service.generate_response(
            content, history
        )

        # Create and save assistant message
        assistant_message = Message(
            id=uuid4(),
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=ai_response_content,
        )
        await self.message_repository.create(assistant_message)

        return assistant_message
