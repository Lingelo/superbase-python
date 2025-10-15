"""API routes."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.chatbot.domain.entities.user import User
from src.chatbot.infrastructure.auth.supabase_auth import get_current_user
from src.chatbot.presentation.schemas.conversation import (
    ConversationCreateRequest,
    ConversationResponse,
)
from src.chatbot.presentation.schemas.message import MessageSendRequest, MessageResponse
from src.chatbot.presentation.api.dependencies import (
    get_create_conversation_use_case,
    get_get_conversation_use_case,
    get_list_conversations_use_case,
    get_send_message_use_case,
    get_get_conversation_messages_use_case,
)
from src.chatbot.application.use_cases.create_conversation import CreateConversationUseCase
from src.chatbot.application.use_cases.get_conversation import GetConversationUseCase
from src.chatbot.application.use_cases.list_conversations import ListConversationsUseCase
from src.chatbot.application.use_cases.send_message import SendMessageUseCase
from src.chatbot.application.use_cases.get_conversation_messages import (
    GetConversationMessagesUseCase,
)

router = APIRouter()


@router.post("/conversations", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    request: ConversationCreateRequest,
    current_user: User = Depends(get_current_user),
    use_case: CreateConversationUseCase = Depends(get_create_conversation_use_case),
) -> ConversationResponse:
    """Create a new conversation."""
    conversation = await use_case.execute(current_user.id, request.title)
    return ConversationResponse.model_validate(conversation)


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    current_user: User = Depends(get_current_user),
    limit: int = 100,
    offset: int = 0,
    use_case: ListConversationsUseCase = Depends(get_list_conversations_use_case),
) -> List[ConversationResponse]:
    """List all conversations for the authenticated user."""
    conversations = await use_case.execute(current_user.id, limit=limit, offset=offset)
    return [ConversationResponse.model_validate(c) for c in conversations]


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: GetConversationUseCase = Depends(get_get_conversation_use_case),
) -> ConversationResponse:
    """Get a conversation by ID."""
    conversation = await use_case.execute(conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationResponse.model_validate(conversation)


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=201,
)
async def send_message(
    conversation_id: UUID,
    request: MessageSendRequest,
    current_user: User = Depends(get_current_user),
    use_case: SendMessageUseCase = Depends(get_send_message_use_case),
) -> MessageResponse:
    """Send a message to a conversation and get AI response."""
    try:
        message = await use_case.execute(conversation_id, current_user.id, request.content)
        return MessageResponse.model_validate(message)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/conversations/{conversation_id}/messages", response_model=List[MessageResponse]
)
async def get_conversation_messages(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    limit: int = 100,
    offset: int = 0,
    use_case: GetConversationMessagesUseCase = Depends(
        get_get_conversation_messages_use_case
    ),
) -> List[MessageResponse]:
    """Get all messages for a conversation."""
    # Note: RLS policies will ensure user can only access their own conversations
    messages = await use_case.execute(conversation_id, limit=limit, offset=offset)
    return [MessageResponse.model_validate(m) for m in messages]
