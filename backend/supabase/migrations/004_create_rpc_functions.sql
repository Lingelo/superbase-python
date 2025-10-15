-- ============================================================================
-- RPC Functions for Chatbot API
-- These functions can be called directly from the client or Python
-- ============================================================================

-- Function: Create a new conversation and return it
CREATE OR REPLACE FUNCTION create_conversation(p_title TEXT)
RETURNS JSON AS $$
DECLARE
    v_conversation JSON;
BEGIN
    INSERT INTO conversations (title)
    VALUES (p_title)
    RETURNING json_build_object(
        'id', id,
        'title', title,
        'created_at', created_at,
        'updated_at', updated_at
    ) INTO v_conversation;

    RETURN v_conversation;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Get all conversations with pagination
CREATE OR REPLACE FUNCTION get_conversations(p_limit INTEGER DEFAULT 100, p_offset INTEGER DEFAULT 0)
RETURNS JSON AS $$
BEGIN
    RETURN (
        SELECT json_agg(
            json_build_object(
                'id', id,
                'title', title,
                'created_at', created_at,
                'updated_at', updated_at
            )
            ORDER BY created_at DESC
        )
        FROM (
            SELECT * FROM conversations
            ORDER BY created_at DESC
            LIMIT p_limit
            OFFSET p_offset
        ) AS limited_conversations
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Get a specific conversation by ID
CREATE OR REPLACE FUNCTION get_conversation_by_id(p_conversation_id UUID)
RETURNS JSON AS $$
BEGIN
    RETURN (
        SELECT json_build_object(
            'id', id,
            'title', title,
            'created_at', created_at,
            'updated_at', updated_at
        )
        FROM conversations
        WHERE id = p_conversation_id
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Create a new message in a conversation
CREATE OR REPLACE FUNCTION create_message(
    p_conversation_id UUID,
    p_role TEXT,
    p_content TEXT
)
RETURNS JSON AS $$
DECLARE
    v_message JSON;
BEGIN
    -- Verify conversation exists
    IF NOT EXISTS (SELECT 1 FROM conversations WHERE id = p_conversation_id) THEN
        RAISE EXCEPTION 'Conversation not found: %', p_conversation_id;
    END IF;

    -- Verify role is valid
    IF p_role NOT IN ('user', 'assistant', 'system') THEN
        RAISE EXCEPTION 'Invalid role: %. Must be user, assistant, or system', p_role;
    END IF;

    -- Insert message
    INSERT INTO messages (conversation_id, role, content)
    VALUES (p_conversation_id, p_role, p_content)
    RETURNING json_build_object(
        'id', id,
        'conversation_id', conversation_id,
        'role', role,
        'content', content,
        'created_at', created_at
    ) INTO v_message;

    -- Update conversation updated_at
    UPDATE conversations
    SET updated_at = NOW()
    WHERE id = p_conversation_id;

    RETURN v_message;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Get all messages for a conversation
CREATE OR REPLACE FUNCTION get_conversation_messages(
    p_conversation_id UUID,
    p_limit INTEGER DEFAULT 100,
    p_offset INTEGER DEFAULT 0
)
RETURNS JSON AS $$
BEGIN
    RETURN (
        SELECT json_agg(
            json_build_object(
                'id', id,
                'conversation_id', conversation_id,
                'role', role,
                'content', content,
                'created_at', created_at
            )
            ORDER BY created_at ASC
        )
        FROM (
            SELECT * FROM messages
            WHERE conversation_id = p_conversation_id
            ORDER BY created_at ASC
            LIMIT p_limit
            OFFSET p_offset
        ) AS limited_messages
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Get conversation with all messages (complete history)
CREATE OR REPLACE FUNCTION get_full_conversation(p_conversation_id UUID)
RETURNS JSON AS $$
BEGIN
    RETURN (
        SELECT json_build_object(
            'conversation', json_build_object(
                'id', c.id,
                'title', c.title,
                'created_at', c.created_at,
                'updated_at', c.updated_at
            ),
            'messages', COALESCE(
                (
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
                ),
                '[]'::json
            )
        )
        FROM conversations c
        WHERE c.id = p_conversation_id
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Delete a conversation and all its messages
CREATE OR REPLACE FUNCTION delete_conversation(p_conversation_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    v_deleted BOOLEAN;
BEGIN
    DELETE FROM conversations
    WHERE id = p_conversation_id;

    GET DIAGNOSTICS v_deleted = ROW_COUNT;

    RETURN v_deleted > 0;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Get conversation statistics
CREATE OR REPLACE FUNCTION get_conversation_stats(p_conversation_id UUID)
RETURNS JSON AS $$
BEGIN
    RETURN (
        SELECT json_build_object(
            'conversation_id', p_conversation_id,
            'message_count', COUNT(*),
            'user_messages', COUNT(*) FILTER (WHERE role = 'user'),
            'assistant_messages', COUNT(*) FILTER (WHERE role = 'assistant'),
            'first_message_at', MIN(created_at),
            'last_message_at', MAX(created_at)
        )
        FROM messages
        WHERE conversation_id = p_conversation_id
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Search conversations by title
CREATE OR REPLACE FUNCTION search_conversations(p_query TEXT, p_limit INTEGER DEFAULT 10)
RETURNS JSON AS $$
BEGIN
    RETURN (
        SELECT json_agg(
            json_build_object(
                'id', id,
                'title', title,
                'created_at', created_at,
                'updated_at', updated_at
            )
            ORDER BY created_at DESC
        )
        FROM (
            SELECT * FROM conversations
            WHERE title ILIKE '%' || p_query || '%'
            ORDER BY created_at DESC
            LIMIT p_limit
        ) AS search_results
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute permissions to authenticated users
GRANT EXECUTE ON FUNCTION create_conversation(TEXT) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION get_conversations(INTEGER, INTEGER) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION get_conversation_by_id(UUID) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION create_message(UUID, TEXT, TEXT) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION get_conversation_messages(UUID, INTEGER, INTEGER) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION get_full_conversation(UUID) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION delete_conversation(UUID) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION get_conversation_stats(UUID) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION search_conversations(TEXT, INTEGER) TO anon, authenticated;

-- Comments for documentation
COMMENT ON FUNCTION create_conversation(TEXT) IS 'Create a new conversation with the given title';
COMMENT ON FUNCTION get_conversations(INTEGER, INTEGER) IS 'Get all conversations with pagination';
COMMENT ON FUNCTION get_conversation_by_id(UUID) IS 'Get a specific conversation by ID';
COMMENT ON FUNCTION create_message(UUID, TEXT, TEXT) IS 'Create a new message in a conversation';
COMMENT ON FUNCTION get_conversation_messages(UUID, INTEGER, INTEGER) IS 'Get all messages for a conversation';
COMMENT ON FUNCTION get_full_conversation(UUID) IS 'Get conversation with all messages';
COMMENT ON FUNCTION delete_conversation(UUID) IS 'Delete a conversation and all its messages';
COMMENT ON FUNCTION get_conversation_stats(UUID) IS 'Get statistics about a conversation';
COMMENT ON FUNCTION search_conversations(TEXT, INTEGER) IS 'Search conversations by title';
