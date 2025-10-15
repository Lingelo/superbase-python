-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc', NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update updated_at on conversations
CREATE TRIGGER update_conversations_updated_at
    BEFORE UPDATE ON conversations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to get conversation with messages
CREATE OR REPLACE FUNCTION get_conversation_with_messages(conv_id UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'id', c.id,
        'title', c.title,
        'created_at', c.created_at,
        'updated_at', c.updated_at,
        'messages', (
            SELECT json_agg(
                json_build_object(
                    'id', m.id,
                    'role', m.role,
                    'content', m.content,
                    'created_at', m.created_at
                )
                ORDER BY m.created_at ASC
            )
            FROM messages m
            WHERE m.conversation_id = c.id
        )
    )
    INTO result
    FROM conversations c
    WHERE c.id = conv_id;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
