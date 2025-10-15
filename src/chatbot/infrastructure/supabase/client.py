"""Supabase client configuration."""
from supabase import create_client, Client

from src.chatbot.infrastructure.config import settings


def get_supabase_client() -> Client:
    """Get configured Supabase client."""
    return create_client(settings.supabase_url, settings.supabase_key)


# Global client instance
supabase_client = get_supabase_client()
