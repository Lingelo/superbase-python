"""FastAPI dependencies."""
from src.chatbot.infrastructure.supabase.client import supabase_client
from src.chatbot.infrastructure.database.supabase_conversation_repository import (
    SupabaseConversationRepository,
)
from src.chatbot.infrastructure.database.supabase_message_repository import (
    SupabaseMessageRepository,
)
from src.chatbot.infrastructure.langchain.chatbot_service import ChatbotService
from src.chatbot.application.use_cases.create_conversation import CreateConversationUseCase
from src.chatbot.application.use_cases.get_conversation import GetConversationUseCase
from src.chatbot.application.use_cases.list_conversations import ListConversationsUseCase
from src.chatbot.application.use_cases.send_message import SendMessageUseCase
from src.chatbot.application.use_cases.get_conversation_messages import (
    GetConversationMessagesUseCase,
)


# Repositories
def get_conversation_repository() -> SupabaseConversationRepository:
    """Get conversation repository instance."""
    return SupabaseConversationRepository(supabase_client)


def get_message_repository() -> SupabaseMessageRepository:
    """Get message repository instance."""
    return SupabaseMessageRepository(supabase_client)


# Services
def get_chatbot_service() -> ChatbotService:
    """Get chatbot service instance."""
    return ChatbotService()


# Use cases
def get_create_conversation_use_case() -> CreateConversationUseCase:
    """Get create conversation use case."""
    return CreateConversationUseCase(get_conversation_repository())


def get_get_conversation_use_case() -> GetConversationUseCase:
    """Get conversation use case."""
    return GetConversationUseCase(get_conversation_repository())


def get_list_conversations_use_case() -> ListConversationsUseCase:
    """Get list conversations use case."""
    return ListConversationsUseCase(get_conversation_repository())


def get_send_message_use_case() -> SendMessageUseCase:
    """Get send message use case."""
    return SendMessageUseCase(
        get_message_repository(),
        get_conversation_repository(),
        get_chatbot_service(),
    )


def get_get_conversation_messages_use_case() -> GetConversationMessagesUseCase:
    """Get conversation messages use case."""
    return GetConversationMessagesUseCase(get_message_repository())
