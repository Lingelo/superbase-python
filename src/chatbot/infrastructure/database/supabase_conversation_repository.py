"""Supabase implementation of ConversationRepository."""
from typing import List, Optional
from uuid import UUID

from supabase import Client

from src.chatbot.domain.entities.conversation import Conversation
from src.chatbot.domain.repositories.conversation_repository import ConversationRepository


class SupabaseConversationRepository(ConversationRepository):
    """Supabase implementation of conversation repository."""

    def __init__(self, client: Client) -> None:
        """Initialize repository with Supabase client."""
        self.client = client
        self.table_name = "conversations"

    async def create(self, conversation: Conversation) -> Conversation:
        """Create a new conversation."""
        data = {
            "id": str(conversation.id),
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
        }

        result = self.client.table(self.table_name).insert(data).execute()

        if not result.data:
            raise Exception("Failed to create conversation")

        return Conversation(**result.data[0])

    async def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get a conversation by ID."""
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("id", str(conversation_id))
            .execute()
        )

        if not result.data:
            return None

        return Conversation(**result.data[0])

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[Conversation]:
        """List all conversations with pagination."""
        result = (
            self.client.table(self.table_name)
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .offset(offset)
            .execute()
        )

        return [Conversation(**item) for item in result.data]

    async def update(self, conversation: Conversation) -> Conversation:
        """Update an existing conversation."""
        data = {
            "title": conversation.title,
            "updated_at": conversation.updated_at.isoformat(),
        }

        result = (
            self.client.table(self.table_name)
            .update(data)
            .eq("id", str(conversation.id))
            .execute()
        )

        if not result.data:
            raise Exception("Failed to update conversation")

        return Conversation(**result.data[0])

    async def delete(self, conversation_id: UUID) -> bool:
        """Delete a conversation by ID."""
        result = (
            self.client.table(self.table_name)
            .delete()
            .eq("id", str(conversation_id))
            .execute()
        )

        return len(result.data) > 0
