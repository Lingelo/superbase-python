# Database Migrations

This directory contains SQL migration files for the Supabase database.

## How to Apply Migrations

### Option 1: Using Supabase Dashboard

1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Copy and paste each migration file in order (001, 002, 003)
4. Execute each script

### Option 2: Using Supabase CLI

If you have the Supabase CLI installed:

```bash
supabase db push
```

### Manual Execution Order

Execute the migrations in this order:

1. `001_create_conversations_table.sql` - Creates the conversations table
2. `002_create_messages_table.sql` - Creates the messages table with foreign key to conversations
3. `003_create_functions.sql` - Creates helper functions and triggers

## Schema Overview

### Tables

- **conversations**: Stores conversation metadata
  - `id` (UUID, primary key)
  - `title` (TEXT)
  - `created_at` (TIMESTAMP)
  - `updated_at` (TIMESTAMP)

- **messages**: Stores individual messages within conversations
  - `id` (UUID, primary key)
  - `conversation_id` (UUID, foreign key)
  - `role` (TEXT: 'user', 'assistant', 'system')
  - `content` (TEXT)
  - `created_at` (TIMESTAMP)

### Functions

- `update_updated_at_column()`: Automatically updates the `updated_at` timestamp
- `get_conversation_with_messages(conv_id UUID)`: Retrieves a conversation with all its messages
