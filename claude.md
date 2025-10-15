# Claude.md - Project Context

## Project Overview

This is a **Supabase Chatbot API** built with Clean Architecture principles, combining FastAPI, Supabase, and LangChain to create a production-ready conversational AI system.

## Tech Stack

- **Backend Framework**: FastAPI (async Python web framework)
- **Database**: Supabase (PostgreSQL-based backend-as-a-service)
- **AI/LLM**: LangChain + OpenRouter (flexible LLM provider)
- **Language**: Python 3.11+
- **Architecture**: Clean Architecture (Domain, Application, Infrastructure, Presentation)

## Architecture Layers

### 1. Domain Layer (`src/chatbot/domain/`)
Pure business logic with no external dependencies.

**Entities:**
- `Conversation`: Represents a chat conversation with id, title, timestamps
- `Message`: Individual messages with role (user/assistant/system), content, and conversation reference

**Repository Interfaces:**
- `ConversationRepository`: Abstract interface for conversation data operations
- `MessageRepository`: Abstract interface for message data operations

### 2. Application Layer (`src/chatbot/application/`)
Business use cases orchestrating domain entities and repositories.

**Use Cases:**
- `CreateConversationUseCase`: Creates new conversations
- `GetConversationUseCase`: Retrieves conversation by ID
- `ListConversationsUseCase`: Lists all conversations with pagination
- `SendMessageUseCase`: Processes user messages and generates AI responses
- `GetConversationMessagesUseCase`: Retrieves message history

### 3. Infrastructure Layer (`src/chatbot/infrastructure/`)
External service implementations and configuration.

**Components:**
- `config.py`: Pydantic settings loading from .env
- `supabase/client.py`: Supabase client initialization
- `database/`: Concrete Supabase repository implementations
- `langchain/chatbot_service.py`: LangChain integration for AI responses

### 4. Presentation Layer (`src/chatbot/presentation/`)
API endpoints and request/response schemas.

**Components:**
- `api/routes.py`: FastAPI REST endpoints
- `api/dependencies.py`: Dependency injection setup
- `schemas/`: Pydantic models for API validation

## Database Schema

### Tables

**conversations**
```sql
- id: UUID (primary key)
- title: TEXT
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

**messages**
```sql
- id: UUID (primary key)
- conversation_id: UUID (foreign key)
- role: TEXT (user/assistant/system)
- content: TEXT
- created_at: TIMESTAMP
```

### Key Features
- Row Level Security (RLS) enabled
- Automatic updated_at trigger on conversations
- Helper function for fetching conversations with messages
- Indexed for performance on common queries

## API Endpoints

### Base URL: `/api/v1`

#### Conversations
- `POST /conversations` - Create new conversation
- `GET /conversations` - List all conversations (paginated)
- `GET /conversations/{id}` - Get specific conversation

#### Messages
- `POST /conversations/{id}/messages` - Send message & get AI response
- `GET /conversations/{id}/messages` - Get conversation message history

## Environment Configuration

Required environment variables (`.env`):

```env
# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJxxx...

# OpenRouter (LLM provider)
OPENROUTER_API_KEY=sk-or-v1-xxx...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-3.5-turbo

# Application
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
```

## Key Design Decisions

1. **Clean Architecture**: Separation of concerns, testability, and maintainability
2. **Async/Await**: Non-blocking I/O for better performance
3. **Type Hints**: Full type coverage with Pydantic and mypy
4. **Repository Pattern**: Abstract data access for flexibility
5. **Dependency Injection**: Loose coupling through FastAPI's DI system
6. **OpenRouter**: Flexible LLM provider supporting multiple models

## Running the Project

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # then edit with your credentials
```

### Apply Migrations
Go to Supabase Dashboard → SQL Editor and run files in `migrations/` folder in order.

### Start Server
```bash
PYTHONPATH=. python main.py
```

Access API docs at: http://localhost:8000/docs

## Development Workflow

### Adding a New Feature

1. **Domain**: Define entities and repository interfaces
2. **Application**: Create use case implementing business logic
3. **Infrastructure**: Implement repository with Supabase
4. **Presentation**: Add API endpoint and schemas
5. **Test**: Write tests for each layer

### Example: Adding User Authentication

1. Create `User` entity in domain
2. Add `UserRepository` interface
3. Implement `SupabaseUserRepository`
4. Create `LoginUseCase` and `RegisterUseCase`
5. Add `/api/v1/auth` endpoints
6. Update RLS policies in Supabase

## Testing Strategy

- **Unit Tests**: Test use cases with mocked repositories
- **Integration Tests**: Test repositories with test database
- **E2E Tests**: Test API endpoints with FastAPI TestClient
- **Run**: `PYTHONPATH=. pytest tests/`

## Common Issues & Solutions

### Issue: ModuleNotFoundError
**Solution**: Always use `PYTHONPATH=.` when running Python commands

### Issue: Supabase connection errors
**Solution**: Check `.env` credentials and verify migrations are applied

### Issue: LangChain API errors
**Solution**: Verify OpenRouter API key and model availability

## Project Structure
```
supabase-python/
├── src/chatbot/           # Main application code
│   ├── domain/            # Business entities & interfaces
│   ├── application/       # Use cases
│   ├── infrastructure/    # External services
│   └── presentation/      # API layer
├── migrations/            # SQL migrations
├── scripts/               # Utility scripts
├── tests/                 # Test files
├── main.py               # Entry point
├── requirements.txt      # Dependencies
├── pyproject.toml        # Project config
├── .env.example          # Environment template
└── README.md             # Documentation
```

## Future Enhancements

- [ ] User authentication with Supabase Auth
- [ ] Streaming responses for real-time chat
- [ ] LangGraph for complex conversation flows
- [ ] Vector database for semantic search
- [ ] Rate limiting and API keys
- [ ] Conversation summarization
- [ ] Export conversation history
- [ ] WebSocket support for real-time updates

## Contributing

When contributing to this project:
1. Follow Clean Architecture principles
2. Maintain type hints throughout
3. Write tests for new features
4. Update documentation
5. Use async/await for I/O operations

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
