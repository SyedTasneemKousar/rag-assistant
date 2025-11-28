"""
Demo RAG Engine - Works WITHOUT OpenAI API (Free Mode)

This version uses simple text matching instead of embeddings/LLM
Perfect for testing the system structure without API costs
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

# LangChain imports for text splitting
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Document processing imports
import PyPDF2
from docx import Document as DocxDocument

load_dotenv()


class RAGEngineDemo:
    """
    Demo RAG Engine that works WITHOUT OpenAI:
    - Processes documents (extracts text, chunks it)
    - Uses simple keyword matching instead of embeddings
    - Returns relevant chunks based on text similarity
    - No API costs!
    """
    
    def __init__(self):
        """Initialize Demo RAG Engine"""
        # Text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Simple storage (no vector DB needed)
        self.documents: List[str] = []
        self.chunks: List[Document] = []
        self.chunk_texts: List[str] = []
        
    def process_document(self, file_path: str, file_type: str) -> int:
        """
        Process a document: extract text, chunk it (NO embeddings needed)
        
        Args:
            file_path: Path to the document file
            file_type: File extension (pdf, txt, docx)
            
        Returns:
            Number of chunks processed
        """
        try:
            # Extract text based on file type
            text = self._extract_text(file_path, file_type)
            
            if not text or len(text.strip()) < 50:
                raise ValueError("Document is too short or empty")
            
            # Split text into chunks
            chunks = self.text_splitter.create_documents([text])
            
            # Store chunks
            self.chunks.extend(chunks)
            self.chunk_texts.extend([chunk.page_content for chunk in chunks])
            self.documents.append(text)
            
            return len(chunks)
            
        except Exception as e:
            raise Exception(f"Error processing document: {str(e)}")
    
    def _extract_text(self, file_path: str, file_type: str) -> str:
        """Extract text from different file types"""
        if file_type == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        
        elif file_type == "pdf":
            text = ""
            with open(file_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        
        elif file_type == "docx":
            doc = DocxDocument(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def query(self, question: str, k: int = 3) -> Dict:
        """
        Query using simple keyword matching (NO OpenAI needed)
        
        Args:
            question: User's question
            k: Number of chunks to retrieve
            
        Returns:
            Dictionary with answer, sources, and confidence
        """
        if len(self.chunks) == 0:
            return {
                "answer": "No documents uploaded yet. Please upload a document first.",
                "sources": [],
                "confidence": 0.0
            }
        
        try:
            # Simple keyword matching
            question_lower = question.lower()
            question_words = set(question_lower.split())
            
            # Score chunks based on keyword matches
            scored_chunks = []
            for i, chunk_text in enumerate(self.chunk_texts):
                chunk_lower = chunk_text.lower()
                chunk_words = set(chunk_lower.split())
                
                # Calculate simple similarity (word overlap)
                common_words = question_words.intersection(chunk_words)
                score = len(common_words) / max(len(question_words), 1)
                
                scored_chunks.append((score, chunk_text, i))
            
            # Sort by score and get top k
            scored_chunks.sort(reverse=True, key=lambda x: x[0])
            top_chunks = scored_chunks[:k]
            
            # Build answer from top chunks
            sources = []
            answer_parts = []
            
            for score, chunk_text, idx in top_chunks:
                # Truncate for display
                source_text = chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text
                sources.append(source_text)
                
                # Add to answer
                answer_parts.append(chunk_text)
            
            # Create simple answer
            answer = f"Based on the document, here's what I found:\n\n"
            answer += "\n\n".join([f"• {part[:300]}..." if len(part) > 300 else f"• {part}" 
                                  for part in answer_parts[:3]])
            
            # Calculate confidence based on match score
            confidence = min(0.9, 0.5 + (top_chunks[0][0] * 0.4) if top_chunks else 0.5)
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": confidence
            }
            
        except Exception as e:
            return {
                "answer": f"I encountered an error: {str(e)}",
                "sources": [],
                "confidence": 0.0
            }
    
    def get_stats(self) -> Dict:
        """Get statistics about processed documents"""
        return {
            "total_chunks": len(self.chunks),
            "has_vector_store": False,
            "total_documents": len(self.documents),
            "mode": "DEMO (No OpenAI required)"
        }
    
    def get_relevant_chunks(self, question: str, k: int = 3) -> List[Document]:
        """Get relevant document chunks (for agentic workflow)"""
        if len(self.chunks) == 0:
            return []
        
        # Use same simple matching
        question_lower = question.lower()
        question_words = set(question_lower.split())
        
        scored_chunks = []
        for i, chunk in enumerate(self.chunks):
            chunk_lower = chunk.page_content.lower()
            chunk_words = set(chunk_lower.split())
            common_words = question_words.intersection(chunk_words)
            score = len(common_words) / max(len(question_words), 1)
            scored_chunks.append((score, chunk, i))
        
        scored_chunks.sort(reverse=True, key=lambda x: x[0])
        return [chunk for _, chunk, _ in scored_chunks[:k]]

