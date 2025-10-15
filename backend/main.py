"""Main entry point for the application."""
import uvicorn

from src.chatbot.infrastructure.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.chatbot.presentation.api.app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug,
    )
