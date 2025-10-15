"""Supabase implementation of MessageRepository."""
from typing import List, Optional
from uuid import UUID

from supabase import Client

from src.chatbot.domain.entities.message import Message
from src.chatbot.domain.repositories.message_repository import MessageRepository


class SupabaseMessageRepository(MessageRepository):
    """Supabase implementation of message repository."""

    def __init__(self, client: Client) -> None:
        """Initialize repository with Supabase client."""
        self.client = client
        self.table_name = "messages"

    async def create(self, message: Message) -> Message:
        """Create a new message."""
        data = {
            "id": str(message.id),
            "conversation_id": str(message.conversation_id),
            "role": message.role.value,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
        }

        result = self.client.table(self.table_name).insert(data).execute()

        if not result.data:
            raise Exception("Failed to create message")

        return Message(**result.data[0])

    async def get_by_id(self, message_id: UUID) -> Optional[Message]:
        """Get a message by ID."""
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("id", str(message_id))
            .execute()
        )

        if not result.data:
            return None

        return Message(**result.data[0])

    async def list_by_conversation(
        self, conversation_id: UUID, limit: int = 100, offset: int = 0
    ) -> List[Message]:
        """List all messages for a conversation."""
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("conversation_id", str(conversation_id))
            .order("created_at", desc=False)
            .limit(limit)
            .offset(offset)
            .execute()
        )

        return [Message(**item) for item in result.data]

    async def delete(self, message_id: UUID) -> bool:
        """Delete a message by ID."""
        result = (
            self.client.table(self.table_name)
            .delete()
            .eq("id", str(message_id))
            .execute()
        )

        return len(result.data) > 0
