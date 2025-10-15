-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Create index on created_at for faster queries
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);

-- Add RLS policies
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

-- Allow all operations for now (you can customize this based on your auth requirements)
CREATE POLICY "Allow all operations on conversations" ON conversations
    FOR ALL
    USING (true)
    WITH CHECK (true);
