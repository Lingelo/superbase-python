# Configuration des Secrets GitHub pour Supabase

Ce guide explique comment configurer les secrets GitHub pour le déploiement automatique des migrations Supabase.

## Secrets Requis

Vous devez ajouter ces secrets dans **GitHub Repository Settings** → **Secrets and variables** → **Actions**:

### 1. SUPABASE_ACCESS_TOKEN

**Où le trouver:**
1. Allez sur [https://supabase.com/dashboard/account/tokens](https://supabase.com/dashboard/account/tokens)
2. Cliquez sur **Generate new token**
3. Donnez-lui un nom (ex: "GitHub Actions")
4. Copiez le token généré

**Ajouter dans GitHub:**
- Name: `SUPABASE_ACCESS_TOKEN`
- Value: Le token copié

### 2. SUPABASE_PROJECT_ID

**Où le trouver:**
1. Allez dans votre projet Supabase Dashboard
2. Cliquez sur **Settings** → **General**
3. Copiez le **Reference ID**

**Ajouter dans GitHub:**
- Name: `SUPABASE_PROJECT_ID`
- Value: Le Reference ID (ex: `abcdefghijklmnop`)

### 3. SUPABASE_DB_PASSWORD

**Où le trouver:**
1. Allez dans votre projet Supabase Dashboard
2. Cliquez sur **Settings** → **Database**
3. Sous **Connection string**, cliquez sur le bouton pour révéler le mot de passe
4. Ou utilisez le mot de passe que vous avez défini lors de la création du projet

**Ajouter dans GitHub:**
- Name: `SUPABASE_DB_PASSWORD`
- Value: Votre mot de passe de base de données

## Comment Ajouter les Secrets

1. Allez dans votre dépôt GitHub
2. Cliquez sur **Settings** (en haut à droite)
3. Dans le menu de gauche, cliquez sur **Secrets and variables** → **Actions**
4. Cliquez sur **New repository secret**
5. Ajoutez chaque secret (nom et valeur)
6. Cliquez sur **Add secret**

## Tester le Déploiement

### Déploiement Automatique

Le workflow se déclenche automatiquement quand:
- Vous poussez des modifications dans `backend/supabase/migrations/`
- Vous poussez sur la branche `main`

### Déploiement Manuel

1. Allez dans l'onglet **Actions** de votre dépôt GitHub
2. Sélectionnez le workflow **Deploy to Supabase**
3. Cliquez sur **Run workflow**
4. Sélectionnez la branche `main`
5. Cliquez sur **Run workflow**

## Vérification

Après le déploiement:
1. Allez dans l'onglet **Actions** de votre dépôt
2. Vérifiez que le workflow s'est exécuté avec succès (✅ vert)
3. Dans Supabase Dashboard → **Table Editor**, vérifiez que vos tables existent
4. Dans Supabase Dashboard → **Database** → **Policies**, vérifiez les politiques RLS

## Sécurité

⚠️ **Important:**
- Ne commitez JAMAIS ces secrets dans votre code
- Les secrets GitHub sont cryptés et sécurisés
- Seules les GitHub Actions peuvent y accéder
- Vous pouvez révoquer/changer les tokens à tout moment

## Troubleshooting

### Erreur: "Invalid access token"
→ Régénérez un nouveau token sur supabase.com/dashboard/account/tokens

### Erreur: "Project not found"
→ Vérifiez que le `SUPABASE_PROJECT_ID` est correct

### Erreur: "Authentication failed"
→ Vérifiez que le `SUPABASE_DB_PASSWORD` est correct
