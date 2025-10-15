# Supabase Chatbot Application

Une application de chatbot complète construite avec **Clean Architecture**, comprenant:
- **Backend**: FastAPI + Supabase + LangChain + OpenRouter
- **Frontend**: React + Vite + TypeScript + Supabase Auth

## Fonctionnalités

- Architecture propre (Clean Architecture) avec séparation des responsabilités
- Authentification utilisateur complète avec Supabase Auth
- API REST sécurisée avec validation JWT
- Interface de chat moderne et responsive
- Gestion des conversations par utilisateur
- Réponses IA alimentées par LangChain et OpenRouter
- Row Level Security (RLS) dans Supabase
- Async/await pour de meilleures performances

## Structure du Projet

```
supabase-python/
├── backend/
│   ├── src/chatbot/
│   │   ├── domain/              # Logique métier & entités
│   │   │   ├── entities/        # User, Conversation, Message
│   │   │   └── repositories/    # Interfaces de repository
│   │   ├── application/         # Use cases
│   │   ├── infrastructure/      # Services externes
│   │   │   ├── auth/            # Middleware d'authentification JWT
│   │   │   ├── database/        # Implémentations Supabase
│   │   │   ├── langchain/       # Service chatbot LangChain
│   │   │   └── config.py        # Configuration
│   │   └── presentation/        # Couche API
│   │       ├── api/             # Routes FastAPI
│   │       └── schemas/         # Schémas de validation
│   ├── supabase/migrations/     # Migrations de base de données
│   ├── main.py                  # Point d'entrée
│   └── requirements.txt         # Dépendances Python
│
└── frontend/
    ├── src/
    │   ├── components/          # Composants React
    │   ├── contexts/            # AuthContext
    │   ├── lib/                 # Supabase client & API
    │   └── pages/               # Login, SignUp, Chat
    ├── package.json             # Dépendances Node
    └── .env                     # Variables d'environnement
```

## Prérequis

- Python 3.11+
- Node.js 18+
- Compte Supabase
- Clé API OpenRouter (ou OpenAI)

## Installation

### 1. Configuration de Supabase

1. Créez un nouveau projet sur [supabase.com](https://supabase.com)
2. Récupérez votre URL de projet et vos clés API (anon et JWT secret)
3. Appliquez les migrations SQL dans le Supabase Dashboard → SQL Editor:
   - `backend/supabase/migrations/001_create_conversations_table.sql`
   - `backend/supabase/migrations/002_create_messages_table.sql`

### 2. Installation du Backend

```bash
cd backend

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
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

**Note importante**: Le `SUPABASE_JWT_SECRET` se trouve dans votre dashboard Supabase sous Settings → API → JWT Settings → JWT Secret

### 3. Installation du Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Configurer les variables d'environnement
cp .env.example .env
```

Éditez `frontend/.env`:

```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Lancement de l'Application

### Démarrer le Backend

```bash
cd backend
PYTHONPATH=. python main.py
```

L'API sera disponible sur `http://localhost:8000`
Documentation API: `http://localhost:8000/docs`

### Démarrer le Frontend

```bash
# Dans le dossier frontend
npm run dev
```

L'application web sera disponible sur `http://localhost:5173`

## Utilisation

1. Ouvrez `http://localhost:5173` dans votre navigateur
2. Créez un compte (Sign Up)
3. Vérifiez votre email (configuration Supabase Auth)
4. Connectez-vous
5. Créez une nouvelle conversation
6. Commencez à discuter avec l'IA!

## API Endpoints

Toutes les routes nécessitent une authentification via Bearer token (JWT).

### Conversations

```bash
# Créer une conversation
POST /api/v1/conversations
Authorization: Bearer <token>
Content-Type: application/json
{"title": "Ma conversation"}

# Lister les conversations de l'utilisateur
GET /api/v1/conversations
Authorization: Bearer <token>

# Récupérer une conversation
GET /api/v1/conversations/{conversation_id}
Authorization: Bearer <token>
```

### Messages

```bash
# Envoyer un message et recevoir une réponse IA
POST /api/v1/conversations/{conversation_id}/messages
Authorization: Bearer <token>
Content-Type: application/json
{"content": "Bonjour!"}

# Récupérer les messages d'une conversation
GET /api/v1/conversations/{conversation_id}/messages
Authorization: Bearer <token>
```

## Architecture

### Backend (Clean Architecture)

**Domain Layer**
- Entités: User, Conversation, Message
- Interfaces de repository

**Application Layer**
- Use cases: CreateConversation, SendMessage, etc.
- Logique métier isolée

**Infrastructure Layer**
- Authentification JWT avec Supabase
- Repositories Supabase
- Service LangChain pour l'IA
- Configuration

**Presentation Layer**
- Routes FastAPI avec middleware d'authentification
- Schémas Pydantic
- Injection de dépendances

### Frontend

**Contextes**
- `AuthContext`: Gestion de l'authentification Supabase

**Pages**
- `Login`: Connexion utilisateur
- `SignUp`: Inscription
- `Chat`: Interface principale de conversation

**Services**
- `supabase.ts`: Client Supabase
- `api.ts`: Client API avec intercepteurs d'authentification

## Sécurité

- Row Level Security (RLS) activé sur toutes les tables
- Validation JWT côté backend
- Les utilisateurs ne voient que leurs propres conversations
- Tokens d'authentification stockés de manière sécurisée
- CORS configuré correctement

## Technologies

### Backend
- **FastAPI**: Framework web moderne et rapide
- **Supabase**: Base de données PostgreSQL + Auth
- **LangChain**: Framework pour applications IA
- **OpenRouter**: Gateway pour modèles LLM
- **Pydantic**: Validation de données
- **PyJWT**: Validation des tokens JWT

### Frontend
- **React**: Bibliothèque UI
- **Vite**: Build tool ultra-rapide
- **TypeScript**: Typage statique
- **React Router**: Navigation
- **Supabase JS**: Client Supabase
- **Axios**: Client HTTP

## Développement

### Backend

```bash
cd backend

# Lancer les tests
PYTHONPATH=. pytest tests/

# Formatage du code
black src/
ruff check src/

# Vérification des types
mypy src/
```

### Frontend

```bash
cd frontend

# Lancer en mode développement
npm run dev

# Build de production
npm run build

# Preview du build
npm run preview
```

## Dépannage

### Backend

**Erreur: ModuleNotFoundError**
```bash
# Toujours utiliser PYTHONPATH=.
PYTHONPATH=. python main.py
```

**Erreur: Invalid JWT**
- Vérifiez que `SUPABASE_JWT_SECRET` est correct
- Le secret JWT se trouve dans Supabase Dashboard → Settings → API → JWT Secret

**Erreur de connexion Supabase**
- Vérifiez `SUPABASE_URL` et `SUPABASE_KEY`
- Vérifiez que les migrations sont appliquées

### Frontend

**Erreur: Cannot connect to API**
- Vérifiez que le backend est lancé
- Vérifiez `VITE_API_BASE_URL` dans `.env`

**Erreur d'authentification**
- Vérifiez que Supabase Auth est activé
- Vérifiez `VITE_SUPABASE_URL` et `VITE_SUPABASE_ANON_KEY`

## Prochaines Améliorations

- [ ] Streaming des réponses IA en temps réel
- [ ] Modification et suppression de conversations
- [ ] Support du markdown dans les messages
- [ ] Mode sombre
- [ ] Export des conversations
- [ ] Avatars utilisateurs
- [ ] Notifications en temps réel
- [ ] Support multilingue

## Contribution

Les contributions sont les bienvenues! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence

MIT License
