# Options de Déploiement pour votre API

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VOTRE PROJET                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │   BASE DE DONNÉES │         │    API PYTHON     │         │
│  │                  │         │                  │         │
│  │    Supabase      │◄────────┤    FastAPI       │         │
│  │   (PostgreSQL)   │         │   (votre code)   │         │
│  │                  │         │                  │         │
│  └──────────────────┘         └──────────────────┘         │
│         ✅                            ❌                      │
│    Déjà configuré              À déployer                   │
└─────────────────────────────────────────────────────────────┘
```

## Supabase ne fait QUE la base de données

Supabase fournit :
- ✅ PostgreSQL hébergé
- ✅ Authentification
- ✅ Storage
- ✅ Realtime
- ❌ **NE PEUT PAS** héberger votre code Python/FastAPI

## Options pour déployer votre API Python

### Option 1: Render.com (RECOMMANDÉ - Gratuit)

**Avantages:**
- Plan gratuit disponible
- Déploiement automatique depuis GitHub
- Facile à configurer
- Supporte Python nativement

**Étapes:**

1. Allez sur https://render.com
2. Créez un compte (gratuit)
3. Cliquez sur "New +" → "Web Service"
4. Connectez votre repo GitHub: `Lingelo/superbase-python`
5. Configurez:
   - **Name**: supabase-chatbot-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.chatbot.presentation.api.app:app --host 0.0.0.0 --port $PORT`
6. Ajoutez les variables d'environnement:
   - `PYTHONPATH` = `.`
   - `SUPABASE_URL` = `https://vyadvnjnwpwzysqhbplz.supabase.co`
   - `SUPABASE_KEY` = `eyJhbGci...` (votre clé)
   - `OPENROUTER_API_KEY` = `sk-or-v1-...` (votre clé)
7. Cliquez "Create Web Service"

**Résultat:** Votre API sera disponible sur `https://votre-app.onrender.com`

### Option 2: Railway.app (Très simple)

**Avantages:**
- Déploiement en 1 clic
- Plan gratuit (500h/mois)
- Auto-détecte Python

**Étapes:**

1. Allez sur https://railway.app
2. Cliquez "Start a New Project"
3. Choisissez "Deploy from GitHub repo"
4. Sélectionnez `Lingelo/superbase-python`
5. Ajoutez les variables d'environnement dans Settings
6. Railway déploie automatiquement !

### Option 3: Fly.io (Pour production)

**Avantages:**
- Bon pour production
- Déploiement global
- Gratuit jusqu'à 3 apps

**Étapes:**

```bash
# Installer Fly CLI
curl -L https://fly.io/install.sh | sh

# Se connecter
fly auth login

# Lancer l'app
fly launch

# Définir les secrets
fly secrets set SUPABASE_URL=https://vyadvnjnwpwzysqhbplz.supabase.co
fly secrets set SUPABASE_KEY=eyJhbG...
fly secrets set OPENROUTER_API_KEY=sk-or-v1-...

# Déployer
fly deploy
```

### Option 4: Google Cloud Run (Enterprise)

**Avantages:**
- Très scalable
- Gratuit jusqu'à 2M requêtes/mois
- Paiement à l'usage

**Étapes:**

```bash
# Build Docker image
docker build -t gcr.io/PROJECT_ID/chatbot-api .

# Push to registry
docker push gcr.io/PROJECT_ID/chatbot-api

# Deploy
gcloud run deploy chatbot-api \
  --image gcr.io/PROJECT_ID/chatbot-api \
  --platform managed \
  --region europe-west1 \
  --set-env-vars SUPABASE_URL=xxx,SUPABASE_KEY=xxx
```

## Configuration des Migrations Automatiques

Pour que les migrations se déploient automatiquement avec GitHub Actions:

### 1. Installer Supabase CLI localement

```bash
npm install -g supabase
```

### 2. Obtenir vos tokens Supabase

Allez sur https://supabase.com/dashboard/account/tokens et créez un token.

### 3. Ajouter les secrets GitHub

Dans GitHub → Settings → Secrets, ajoutez:

- `SUPABASE_ACCESS_TOKEN`: Token depuis le dashboard
- `SUPABASE_DB_PASSWORD`: Password de votre DB (dans Settings → Database)

### 4. Push et c'est fait !

À chaque push sur `main`, GitHub Actions va:
1. ✅ Appliquer les migrations sur Supabase
2. ✅ Déployer l'API (si configuré avec Render/Railway)

## Ma Recommandation

**Pour commencer rapidement (aujourd'hui):**

1. ✅ Utilisez **Render.com** (gratuit, 5 minutes de setup)
2. ✅ Configurez les **GitHub Secrets** pour Supabase
3. ✅ Push sur GitHub → tout se déploie automatiquement

**Pour plus tard (production):**

1. Migrez vers **Fly.io** ou **Google Cloud Run**
2. Ajoutez un CDN (Cloudflare)
3. Configurez des alertes et monitoring

## Prochaines Étapes Concrètes

1. **Maintenant:** Choisissez Render.com ou Railway.app
2. **5 minutes:** Créez le service et connectez GitHub
3. **2 minutes:** Ajoutez les variables d'environnement
4. **Résultat:** Votre API est en ligne !

Quelle option voulez-vous que je configure pour vous ?
