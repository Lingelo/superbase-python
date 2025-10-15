"""LangChain chatbot service implementation."""
from typing import List

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from src.chatbot.domain.entities.message import Message, MessageRole
from src.chatbot.infrastructure.config import settings


class ChatbotService:
    """Service for chatbot interactions using LangChain."""

    def __init__(self) -> None:
        """Initialize the chatbot service with OpenRouter."""
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=0.7,
            openai_api_key=settings.openrouter_api_key,
            openai_api_base=settings.openrouter_base_url,
        )

    def _convert_messages(self, messages: List[Message]) -> List:
        """Convert domain messages to LangChain messages."""
        langchain_messages = []

        for msg in messages:
            if msg.role == MessageRole.USER:
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == MessageRole.ASSISTANT:
                langchain_messages.append(AIMessage(content=msg.content))
            elif msg.role == MessageRole.SYSTEM:
                langchain_messages.append(SystemMessage(content=msg.content))

        return langchain_messages

    async def generate_response(
        self, user_message: str, conversation_history: List[Message]
    ) -> str:
        """Generate a response using the LLM."""
        # Convert conversation history to LangChain format
        messages = self._convert_messages(conversation_history)

        # Add the new user message
        messages.append(HumanMessage(content=user_message))

        # Get response from LLM
        response = await self.llm.ainvoke(messages)

        return response.content

    async def generate_conversation_title(self, first_message: str) -> str:
        """Generate a title for the conversation based on the first message."""
        prompt = f"Generate a short title (max 50 characters) for a conversation that starts with: '{first_message}'. Only return the title, nothing else."

        messages = [HumanMessage(content=prompt)]
        response = await self.llm.ainvoke(messages)

        return response.content.strip()
