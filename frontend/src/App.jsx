/**
 * Main App Component
 * 
 * This is the main React component that:
 * 1. Shows document upload interface
 * 2. Displays chat interface for Q&A
 * 3. Connects to FastAPI backend
 */

import React, { useState } from 'react';
import './App.css';
import DocumentUpload from './components/DocumentUpload';
import ChatInterface from './components/ChatInterface';

function App() {
  const [documentUploaded, setDocumentUploaded] = useState(false);
  const [documentName, setDocumentName] = useState('');

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 RAG Assistant</h1>
        <p>Intelligent Document Q&A with RAG & Agentic AI</p>
      </header>

      <main className="App-main">
        {/* Document Upload Section */}
        <section className="upload-section">
          <DocumentUpload 
            onUploadSuccess={(filename) => {
              setDocumentUploaded(true);
              setDocumentName(filename);
            }}
          />
          {documentUploaded && (
            <div className="success-message">
              ✅ Document "{documentName}" uploaded successfully!
            </div>
          )}
        </section>

        {/* Chat Interface Section */}
        <section className="chat-section">
          <ChatInterface disabled={!documentUploaded} />
        </section>
      </main>

      <footer className="App-footer">
        <p>Built with FastAPI, LangChain, LlamaIndex, and React</p>
      </footer>
    </div>
  );
}

export default App;


