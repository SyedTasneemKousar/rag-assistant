/**
 * Chat Interface Component
 * 
 * Main chat interface for asking questions about uploaded documents
 * Uses RAG + Agentic AI to provide intelligent answers
 */

import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatInterface.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function ChatInterface({ disabled }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading || disabled) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message to chat
    const newMessages = [...messages, { role: 'user', content: userMessage }];
    setMessages(newMessages);
    setLoading(true);

    try {
      // Send query to FastAPI backend
      const response = await axios.post(`${API_URL}/query`, {
        question: userMessage,
        chat_history: messages.map(m => ({
          role: m.role,
          content: m.content
        }))
      });

      // Add assistant response to chat
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: response.data.answer,
          sources: response.data.sources || []
        }
      ]);
    } catch (error) {
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: `❌ Error: ${error.response?.data?.detail || error.message}`,
          sources: []
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-interface">
      <h2>💬 Ask Questions</h2>
      
      {disabled && (
        <div className="disabled-message">
          ⚠️ Please upload a document first to start asking questions
        </div>
      )}

      <div className="chat-messages">
        {messages.length === 0 && !disabled && (
          <div className="welcome-message">
            <p>👋 Welcome! Ask me anything about your uploaded document.</p>
            <p className="example-questions">
              Try asking:
              <br />• "What is this document about?"
              <br />• "Summarize the main points"
              <br />• "What are the key findings?"
            </p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.content}
            </div>
            {msg.sources && msg.sources.length > 0 && (
              <div className="sources">
                <strong>Sources:</strong>
                {msg.sources.map((source, i) => (
                  <div key={i} className="source-item">
                    {source}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="message assistant">
            <div className="message-content">
              <span className="typing-indicator">🤔 Thinking...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={disabled ? "Upload a document first..." : "Ask a question about your document..."}
          disabled={disabled || loading}
          className="chat-input"
          rows="2"
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || loading || disabled}
          className="send-button"
        >
          {loading ? '⏳' : '📤'}
        </button>
      </div>
    </div>
  );
}

export default ChatInterface;


