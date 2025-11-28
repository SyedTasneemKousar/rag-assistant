/**
 * Document Upload Component
 * 
 * Allows users to upload PDF, TXT, or DOCX files
 * Sends file to FastAPI backend for processing
 */

import React, { useState } from 'react';
import axios from 'axios';
import './DocumentUpload.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function DocumentUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const ext = selectedFile.name.split('.').pop().toLowerCase();
      if (['pdf', 'txt', 'docx'].includes(ext)) {
        setFile(selectedFile);
        setMessage('');
      } else {
        setMessage('⚠️ Please upload PDF, TXT, or DOCX files only');
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('⚠️ Please select a file first');
      return;
    }

    setUploading(true);
    setMessage('');

    try {
      // Create FormData to send file
      const formData = new FormData();
      formData.append('file', file);

      // Send to FastAPI backend
      const response = await axios.post(`${API_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setMessage(`✅ ${response.data.message} (${response.data.chunks_processed} chunks processed)`);
      onUploadSuccess(file.name);
      setFile(null);
      
      // Reset file input
      document.getElementById('file-input').value = '';
    } catch (error) {
      setMessage(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="document-upload">
      <h2>📄 Upload Document</h2>
      <p className="upload-description">
        Upload a PDF, TXT, or DOCX file to start asking questions
      </p>

      <div className="upload-controls">
        <label htmlFor="file-input" className="file-label">
          Choose File
        </label>
        <input
          id="file-input"
          type="file"
          accept=".pdf,.txt,.docx"
          onChange={handleFileChange}
          className="file-input"
        />
        {file && (
          <div className="file-info">
            📎 {file.name} ({(file.size / 1024).toFixed(2)} KB)
          </div>
        )}
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="upload-button"
        >
          {uploading ? '⏳ Uploading...' : '🚀 Upload & Process'}
        </button>
      </div>

      {message && (
        <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}
    </div>
  );
}

export default DocumentUpload;


