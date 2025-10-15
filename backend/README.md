# Backend - Supabase Chatbot API

Backend API pour l'application de chatbot, construit avec FastAPI, Supabase, et LangChain.

## Technologies

- **FastAPI**: Framework web moderne et rapide
- **Supabase**: Base de données PostgreSQL + Authentification
- **LangChain**: Framework pour applications IA
- **OpenRouter**: Gateway pour modèles LLM
- **Pydantic**: Validation de données
- **PyJWT**: Validation des tokens JWT

## Architecture (Clean Architecture)

### Domain Layer (`src/chatbot/domain/`)
- **Entities**: User, Conversation, Message
- **Repositories**: Interfaces abstraites pour l'accès aux données

### Application Layer (`src/chatbot/application/`)
- **Use Cases**: Logique métier (CreateConversation, SendMessage, etc.)

### Infrastructure Layer (`src/chatbot/infrastructure/`)
- **Auth**: Middleware JWT pour Supabase
- **Database**: Implémentations Supabase des repositories
- **LangChain**: Service de chatbot IA
- **Config**: Configuration de l'application

### Presentation Layer (`src/chatbot/presentation/`)
- **API Routes**: Endpoints FastAPI
- **Schemas**: Validation Pydantic
- **Dependencies**: Injection de dépendances

## Installation

### 1. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Éditez `.env`:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_JWT_SECRET=your-supabase-jwt-secret

# OpenRouter Configuration
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-3.5-turbo

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
```

**Important**: Le `SUPABASE_JWT_SECRET` se trouve dans votre dashboard Supabase:
Settings → API → JWT Settings → JWT Secret

### 4. Appliquer les migrations Supabase

Allez dans votre Supabase Dashboard → SQL Editor et exécutez:

1. `supabase/migrations/001_create_conversations_table.sql`
2. `supabase/migrations/002_create_messages_table.sql`

## Lancement

```bash
PYTHONPATH=. python main.py
```

L'API sera disponible sur `http://localhost:8000`

Documentation interactive: `http://localhost:8000/docs`

## API Endpoints

Toutes les routes nécessitent un token JWT dans le header `Authorization: Bearer <token>`.

### Health Check

```bash
GET /health
```

### Conversations

```bash
# Créer une conversation
POST /api/v1/conversations
{"title": "Ma conversation"}

# Lister les conversations de l'utilisateur
GET /api/v1/conversations?limit=100&offset=0

# Récupérer une conversation spécifique
GET /api/v1/conversations/{conversation_id}
```

### Messages

```bash
# Envoyer un message et recevoir une réponse IA
POST /api/v1/conversations/{conversation_id}/messages
{"content": "Bonjour!"}

# Récupérer les messages d'une conversation
GET /api/v1/conversations/{conversation_id}/messages?limit=100&offset=0
```

## Développement

### Lancer les tests

```bash
PYTHONPATH=. pytest tests/
```

### Formatage du code

```bash
black src/
ruff check src/
```

### Vérification des types

```bash
mypy src/
```

## Structure des Dossiers

```
backend/
├── src/chatbot/
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── user.py
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   └── repositories/
│   │       ├── conversation_repository.py
│   │       └── message_repository.py
│   ├── application/
│   │   └── use_cases/
│   │       ├── create_conversation.py
│   │       ├── get_conversation.py
│   │       ├── list_conversations.py
│   │       ├── send_message.py
│   │       └── get_conversation_messages.py
│   ├── infrastructure/
│   │   ├── auth/
│   │   │   └── supabase_auth.py
│   │   ├── database/
│   │   │   ├── supabase_conversation_repository.py
│   │   │   └── supabase_message_repository.py
│   │   ├── langchain/
│   │   │   └── chatbot_service.py
│   │   ├── supabase/
│   │   │   └── client.py
│   │   └── config.py
│   └── presentation/
│       ├── api/
│       │   ├── routes.py
│       │   ├── dependencies.py
│       │   └── app.py
│       └── schemas/
│           ├── conversation.py
│           └── message.py
├── supabase/migrations/
├── main.py
├── requirements.txt
└── .env.example
```

## Sécurité

- **JWT Authentication**: Validation des tokens Supabase
- **Row Level Security**: Politiques RLS sur toutes les tables
- **User Isolation**: Chaque utilisateur ne voit que ses données
- **Type Safety**: Validation stricte avec Pydantic

## Dépannage

### ModuleNotFoundError

Toujours utiliser `PYTHONPATH=.`:

```bash
PYTHONPATH=. python main.py
```

### Invalid JWT Error

- Vérifiez que `SUPABASE_JWT_SECRET` est correct
- Le secret se trouve dans Settings → API → JWT Secret de Supabase

### Erreur de connexion Supabase

- Vérifiez `SUPABASE_URL` et `SUPABASE_KEY`
- Vérifiez que les migrations sont appliquées
- Vérifiez que les politiques RLS sont activées

## Licence

MIT License
