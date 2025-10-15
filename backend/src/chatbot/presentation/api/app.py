"""FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.chatbot.presentation.api.routes import router
from src.chatbot.infrastructure.config import settings

app = FastAPI(
    title="Supabase Chatbot API",
    description="A chatbot API using Supabase, LangChain, and FastAPI",
    version="0.1.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api/v1", tags=["chatbot"])


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "message": "Welcome to Supabase Chatbot API",
        "docs": "/docs",
        "version": "0.1.0",
    }


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}
