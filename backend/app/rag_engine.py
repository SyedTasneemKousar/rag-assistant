"""
RAG Engine - Core Retrieval Augmented Generation Implementation

This module implements:
- Document processing (PDF, TXT, DOCX)
- Text chunking with LangChain
- Embedding generation using OpenAI
- Vector database (FAISS) for similarity search
- RAG query pipeline with LLM integration
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS

# Document processing imports
import PyPDF2
from docx import Document as DocxDocument

load_dotenv()


class RAGEngine:
    """
    RAG Engine that processes documents and answers questions using:
    - Document chunking
    - Embeddings (OpenAI)
    - Vector database (FAISS)
    - LLM (GPT-3.5) for answer generation
    """
    
    def __init__(self):
        """Initialize RAG Engine with embeddings and vector store"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize OpenAI embeddings (lazy initialization)
        self.embeddings = None
        self.llm = None
        
        if self.api_key:
            try:
                self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
                self.llm = ChatOpenAI(
                    model_name="gpt-3.5-turbo",
                    temperature=0,
                    openai_api_key=self.api_key
                )
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI: {e}")
        
        # Text splitter for chunking documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Vector store (FAISS)
        self.vector_store: Optional[FAISS] = None
        self.documents: List[str] = []
        self.chunks: List[Document] = []
        
    def process_document(self, file_path: str, file_type: str) -> int:
        """
        Process a document: extract text, chunk it, create embeddings, store in vector DB
        
        Args:
            file_path: Path to the document file
            file_type: File extension (pdf, txt, docx)
            
        Returns:
            Number of chunks processed
        """
        try:
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not set. Please set it in your environment or .env file")
            
            if not self.embeddings:
                self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
                self.llm = ChatOpenAI(
                    model_name="gpt-3.5-turbo",
                    temperature=0,
                    openai_api_key=self.api_key
                )
            
            # Extract text based on file type
            text = self._extract_text(file_path, file_type)
            
            if not text or len(text.strip()) < 50:
                raise ValueError("Document is too short or empty")
            
            # Split text into chunks
            chunks = self.text_splitter.create_documents([text])
            
            # Store chunks
            self.chunks.extend(chunks)
            self.documents.append(text)
            
            # Create or update vector store
            if self.vector_store is None:
                # Create new vector store
                self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            else:
                # Add to existing vector store
                self.vector_store.add_documents(chunks)
            
            return len(chunks)
            
        except Exception as e:
            raise Exception(f"Error processing document: {str(e)}")
    
    def _extract_text(self, file_path: str, file_type: str) -> str:
        """
        Extract text from different file types
        
        Args:
            file_path: Path to file
            file_type: File extension
            
        Returns:
            Extracted text content
        """
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
        Query the RAG system: retrieve relevant chunks and generate answer
        
        Args:
            question: User's question
            k: Number of chunks to retrieve
            
        Returns:
            Dictionary with answer, sources, and confidence
        """
        if self.vector_store is None or len(self.chunks) == 0:
            return {
                "answer": "No documents uploaded yet. Please upload a document first.",
                "sources": [],
                "confidence": 0.0
            }
        
        try:
            # Create retrieval chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": k}),
                return_source_documents=True
            )
            
            # Query the chain
            result = qa_chain.invoke({"query": question})
            
            # Extract answer and sources
            answer = result.get("result", "I couldn't find an answer to that question.")
            source_docs = result.get("source_documents", [])
            
            # Format sources
            sources = []
            for doc in source_docs[:k]:
                source_text = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                sources.append(source_text)
            
            # Calculate confidence (simple heuristic based on number of sources)
            confidence = min(0.9, 0.5 + (len(sources) * 0.15))
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": confidence
            }
            
        except Exception as e:
            # Fallback to simple retrieval if LLM fails
            try:
                # Simple similarity search
                docs = self.vector_store.similarity_search(question, k=k)
                sources = [doc.page_content[:200] + "..." for doc in docs]
                answer = f"Based on the document, here's what I found:\n\n" + "\n\n".join([f"• {source}" for source in sources])
                
                return {
                    "answer": answer,
                    "sources": sources,
                    "confidence": 0.6
                }
            except Exception as fallback_error:
                return {
                    "answer": f"I encountered an error: {str(fallback_error)}",
                    "sources": [],
                    "confidence": 0.0
                }
    
    def get_stats(self) -> Dict:
        """Get statistics about processed documents"""
        return {
            "total_chunks": len(self.chunks),
            "has_vector_store": self.vector_store is not None,
            "total_documents": len(self.documents)
        }
    
    def get_relevant_chunks(self, question: str, k: int = 3) -> List[Document]:
        """
        Get relevant document chunks for a question (used by agentic workflow)
        
        Args:
            question: User's question
            k: Number of chunks to retrieve
            
        Returns:
            List of relevant document chunks
        """
        if self.vector_store is None:
            return []
        
        try:
            return self.vector_store.similarity_search(question, k=k)
        except Exception:
            return []
