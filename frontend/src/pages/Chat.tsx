import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { conversationsAPI, Conversation, Message } from '../lib/api'

export const Chat: React.FC = () => {
  const { user, signOut } = useAuth()
  const navigate = useNavigate()
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    loadConversations()
  }, [])

  useEffect(() => {
    if (currentConversation) {
      loadMessages(currentConversation.id)
    }
  }, [currentConversation])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const loadConversations = async () => {
    try {
      const data = await conversationsAPI.list()
      setConversations(data)
    } catch (err) {
      setError('Failed to load conversations')
    }
  }

  const loadMessages = async (conversationId: string) => {
    try {
      const data = await conversationsAPI.getMessages(conversationId)
      setMessages(data)
    } catch (err) {
      setError('Failed to load messages')
    }
  }

  const createNewConversation = async () => {
    try {
      const newConv = await conversationsAPI.create('New Conversation')
      setConversations([newConv, ...conversations])
      setCurrentConversation(newConv)
      setMessages([])
    } catch (err) {
      setError('Failed to create conversation')
    }
  }

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || !currentConversation || loading) return

    setLoading(true)
    setError('')

    try {
      const userMsg: Message = {
        id: 'temp',
        conversation_id: currentConversation.id,
        role: 'user',
        content: input,
        created_at: new Date().toISOString(),
      }
      setMessages([...messages, userMsg])
      setInput('')

      const response = await conversationsAPI.sendMessage(currentConversation.id, input)
      setMessages((prev) => [...prev.filter((m) => m.id !== 'temp'), response])
      await loadMessages(currentConversation.id)
    } catch (err) {
      setError('Failed to send message')
    } finally {
      setLoading(false)
    }
  }

  const handleSignOut = async () => {
    await signOut()
    navigate('/login')
  }

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      {/* Sidebar */}
      <div style={{ width: '250px', borderRight: '1px solid #ccc', padding: '20px', overflow: 'auto' }}>
        <div style={{ marginBottom: '20px' }}>
          <button
            onClick={createNewConversation}
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor: '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            + New Chat
          </button>
        </div>

        <div>
          {conversations.map((conv) => (
            <div
              key={conv.id}
              onClick={() => setCurrentConversation(conv)}
              style={{
                padding: '10px',
                marginBottom: '5px',
                backgroundColor: currentConversation?.id === conv.id ? '#e3f2fd' : '#f5f5f5',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              {conv.title}
            </div>
          ))}
        </div>

        <div style={{ marginTop: 'auto', paddingTop: '20px' }}>
          <div style={{ padding: '10px', backgroundColor: '#f5f5f5', borderRadius: '4px', marginBottom: '10px' }}>
            <small>{user?.email}</small>
          </div>
          <button
            onClick={handleSignOut}
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor: '#f44336',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            Sign Out
          </button>
        </div>
      </div>

      {/* Main chat area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {error && (
          <div style={{ padding: '10px', backgroundColor: '#ffebee', color: '#c62828' }}>
            {error}
          </div>
        )}

        {!currentConversation ? (
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <h2>Select a conversation or create a new one</h2>
          </div>
        ) : (
          <>
            {/* Messages */}
            <div style={{ flex: 1, overflow: 'auto', padding: '20px' }}>
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  style={{
                    marginBottom: '15px',
                    padding: '10px',
                    backgroundColor: msg.role === 'user' ? '#e3f2fd' : '#f5f5f5',
                    borderRadius: '8px',
                    maxWidth: '70%',
                    marginLeft: msg.role === 'user' ? 'auto' : '0',
                    marginRight: msg.role === 'user' ? '0' : 'auto',
                  }}
                >
                  <div style={{ fontWeight: 'bold', marginBottom: '5px', fontSize: '12px', color: '#666' }}>
                    {msg.role === 'user' ? 'You' : 'Assistant'}
                  </div>
                  <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={sendMessage} style={{ padding: '20px', borderTop: '1px solid #ccc' }}>
              <div style={{ display: 'flex', gap: '10px' }}>
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type your message..."
                  disabled={loading}
                  style={{
                    flex: 1,
                    padding: '10px',
                    fontSize: '16px',
                    border: '1px solid #ccc',
                    borderRadius: '4px',
                  }}
                />
                <button
                  type="submit"
                  disabled={loading || !input.trim()}
                  style={{
                    padding: '10px 20px',
                    backgroundColor: '#4CAF50',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
                  }}
                >
                  {loading ? 'Sending...' : 'Send'}
                </button>
              </div>
            </form>
          </>
        )}
      </div>
    </div>
  )
}
