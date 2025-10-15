# Supabase Chatbot API

A production-ready chatbot API built with **FastAPI**, **Supabase**, and **LangChain** using **Clean Architecture** principles.

## Features

- Clean Architecture with clear separation of concerns
- REST API with FastAPI
- Supabase for database and authentication
- LangChain integration with OpenRouter support
- Conversation and message management
- AI-powered chatbot responses
- Async/await throughout
- Type hints with Pydantic

## Project Structure

```
supabase-python/
├── src/
│   └── chatbot/
│       ├── domain/              # Business logic & entities
│       │   ├── entities/        # Domain entities (Conversation, Message)
│       │   └── repositories/    # Repository interfaces
│       ├── application/         # Use cases
│       │   └── use_cases/       # Business use cases
│       ├── infrastructure/      # External services
│       │   ├── database/        # Supabase repository implementations
│       │   ├── langchain/       # LangChain chatbot service
│       │   ├── supabase/        # Supabase client configuration
│       │   └── config.py        # Application configuration
│       └── presentation/        # API layer
│           ├── api/             # FastAPI routes & dependencies
│           └── schemas/         # Request/Response schemas
├── migrations/                  # Database migrations
├── scripts/                     # Utility scripts
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
└── .env                         # Environment variables

```

## Prerequisites

- Python 3.11+
- Supabase account
- OpenRouter API key (or OpenAI API key)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd supabase-python
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# OpenRouter Configuration (for LangChain)
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-3.5-turbo

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
```

### 5. Apply database migrations

Go to your Supabase dashboard → SQL Editor and run the following migrations in order:

1. `migrations/001_create_conversations_table.sql`
2. `migrations/002_create_messages_table.sql`
3. `migrations/003_create_functions.sql`

Or use the migration script to see the instructions:

```bash
PYTHONPATH=. python scripts/apply_migrations.py
```

## Running the Application

### Development mode

```bash
PYTHONPATH=. python main.py
```

The API will be available at `http://localhost:8000`

### Using uvicorn directly

```bash
PYTHONPATH=. uvicorn src.chatbot.presentation.api.app:app --reload --host 0.0.0.0 --port 8000
```

### Using uvx (recommended)

```bash
uvx uvicorn src.chatbot.presentation.api.app:app --reload
```

## API Documentation

Once the application is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health Check

```bash
GET /health
```

### Conversations

#### Create a new conversation

```bash
POST /api/v1/conversations
Content-Type: application/json

{
  "title": "My First Conversation"
}
```

#### List all conversations

```bash
GET /api/v1/conversations?limit=100&offset=0
```

#### Get a specific conversation

```bash
GET /api/v1/conversations/{conversation_id}
```

### Messages

#### Send a message (and get AI response)

```bash
POST /api/v1/conversations/{conversation_id}/messages
Content-Type: application/json

{
  "content": "Hello, how are you?"
}
```

This endpoint will:
1. Save the user message
2. Generate an AI response using LangChain
3. Save the AI response
4. Return the AI message

#### Get conversation messages

```bash
GET /api/v1/conversations/{conversation_id}/messages?limit=100&offset=0
```

## Example Usage

### Using cURL

```bash
# Create a conversation
CONV_ID=$(curl -X POST http://localhost:8000/api/v1/conversations \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Chat"}' | jq -r '.id')

# Send a message
curl -X POST http://localhost:8000/api/v1/conversations/$CONV_ID/messages \
  -H "Content-Type: application/json" \
  -d '{"content":"What is the capital of France?"}'

# Get all messages
curl http://localhost:8000/api/v1/conversations/$CONV_ID/messages
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Create a conversation
response = requests.post(
    f"{BASE_URL}/conversations",
    json={"title": "Python Test Chat"}
)
conversation = response.json()
conv_id = conversation["id"]

# Send a message
response = requests.post(
    f"{BASE_URL}/conversations/{conv_id}/messages",
    json={"content": "Tell me a joke about programming"}
)
ai_message = response.json()
print(f"AI: {ai_message['content']}")
```

## Architecture

This project follows **Clean Architecture** principles:

### Domain Layer
- **Entities**: Core business objects (Conversation, Message)
- **Repository Interfaces**: Define contracts for data access

### Application Layer
- **Use Cases**: Business logic operations (CreateConversation, SendMessage, etc.)

### Infrastructure Layer
- **Database**: Supabase repository implementations
- **LangChain**: AI chatbot service
- **Config**: Environment configuration

### Presentation Layer
- **API Routes**: FastAPI endpoints
- **Schemas**: Request/Response validation with Pydantic
- **Dependencies**: Dependency injection setup

## Technologies

- **FastAPI**: Modern, fast web framework
- **Supabase**: Open-source Firebase alternative
- **LangChain**: LLM framework for building AI applications
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI web server

## Development

### Run tests

```bash
PYTHONPATH=. pytest tests/
```

### Code formatting

```bash
black src/
ruff check src/
```

### Type checking

```bash
mypy src/
```

## Troubleshooting

### ModuleNotFoundError: No module named 'src'

Always run Python commands with `PYTHONPATH=.`:

```bash
PYTHONPATH=. python main.py
```

### Supabase connection errors

- Verify your `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Ensure migrations have been applied
- Check RLS policies if authentication is enabled

### LangChain API errors

- Verify your `OPENROUTER_API_KEY` in `.env`
- Check the `LLM_MODEL` is valid for your OpenRouter account
- Ensure you have sufficient credits/quota

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
