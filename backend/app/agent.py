"""
Agentic AI Workflow - Multi-step Reasoning with LangChain Agents

This module implements:
- LangChain agents for complex query handling
- Multiple tools (document search, summarization, stats)
- Multi-step reasoning workflow
"""

from typing import Optional, List, Dict
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv()


class AgenticWorkflow:
    """
    Agentic AI workflow that uses LangChain agents to:
    - Break down complex queries
    - Use multiple tools
    - Perform multi-step reasoning
    """
    
    def __init__(self, rag_engine):
        """
        Initialize agentic workflow
        
        Args:
            rag_engine: RAGEngine instance for document access
        """
        self.rag_engine = rag_engine
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize LLM for agent (lazy initialization)
        self.llm = None
        self.agent = None
        self.tools = []
        
        if self.api_key:
            try:
                self.llm = ChatOpenAI(
                    model_name="gpt-3.5-turbo",
                    temperature=0,
                    openai_api_key=self.api_key
                )
                # Define tools for the agent
                self.tools = self._create_tools()
                # Initialize agent
                self.agent = initialize_agent(
                    tools=self.tools,
                    llm=self.llm,
                    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                    verbose=True,
                    handle_parsing_errors=True
                )
            except Exception as e:
                print(f"Warning: Could not initialize agent: {e}")
    
    def _create_tools(self) -> List[Tool]:
        """
        Create tools that the agent can use
        
        Returns:
            List of Tool objects
        """
        def document_query(query: str) -> str:
            """Search documents using RAG"""
            try:
                result = self.rag_engine.query(query, k=3)
                return result.get("answer", "No answer found")
            except Exception as e:
                return f"Error querying documents: {str(e)}"
        
        def summarize_text(text: str) -> str:
            """Summarize text using LLM"""
            try:
                prompt = f"Please provide a concise summary of the following text:\n\n{text[:2000]}"
                response = self.llm.invoke(prompt)
                return response.content if hasattr(response, 'content') else str(response)
            except Exception as e:
                return f"Error summarizing: {str(e)}"
        
        def get_document_stats() -> str:
            """Get statistics about processed documents"""
            try:
                stats = self.rag_engine.get_stats()
                return f"Total chunks: {stats['total_chunks']}, Documents: {stats['total_documents']}, Has vector store: {stats['has_vector_store']}"
            except Exception as e:
                return f"Error getting stats: {str(e)}"
        
        tools = [
            Tool(
                name="DocumentQuery",
                func=document_query,
                description="Use this tool to search and query uploaded documents. Input should be a question about the documents."
            ),
            Tool(
                name="Summarize",
                func=summarize_text,
                description="Use this tool to summarize text or document content. Input should be the text to summarize."
            ),
            Tool(
                name="GetStats",
                func=lambda x: get_document_stats(),
                description="Use this tool to get statistics about processed documents. Input can be anything, it will return stats."
            )
        ]
        
        return tools
    
    def process_query(self, question: str) -> Dict:
        """
        Process a query using the agentic workflow
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer and metadata
        """
        if not self.api_key:
            return {
                "answer": "OPENAI_API_KEY not set. Please set it in your environment or .env file.",
                "sources": [],
                "confidence": 0.0,
                "agentic": False
            }
        
        if not self.rag_engine.vector_store:
            return {
                "answer": "No documents uploaded yet. Please upload a document first.",
                "sources": [],
                "confidence": 0.0,
                "agentic": True
            }
        
        if not self.agent:
            # Initialize agent if not already done
            try:
                if not self.llm:
                    self.llm = ChatOpenAI(
                        model_name="gpt-3.5-turbo",
                        temperature=0,
                        openai_api_key=self.api_key
                    )
                self.tools = self._create_tools()
                self.agent = initialize_agent(
                    tools=self.tools,
                    llm=self.llm,
                    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                    verbose=True,
                    handle_parsing_errors=True
                )
            except Exception as e:
                return {
                    "answer": f"Error initializing agent: {str(e)}",
                    "sources": [],
                    "confidence": 0.0,
                    "agentic": False
                }
        
        try:
            # Use agent to process query
            result = self.agent.run(question)
            
            # Get relevant chunks for sources
            relevant_chunks = self.rag_engine.get_relevant_chunks(question, k=3)
            sources = [chunk.page_content[:200] + "..." for chunk in relevant_chunks]
            
            return {
                "answer": result,
                "sources": sources,
                "confidence": 0.8,
                "agentic": True
            }
            
        except Exception as e:
            # Fallback to simple RAG if agent fails
            try:
                return {
                    **self.rag_engine.query(question),
                    "agentic": False,
                    "error": f"Agent failed, using simple RAG: {str(e)}"
                }
            except Exception as fallback_error:
                return {
                    "answer": f"I encountered an error processing your query: {str(fallback_error)}",
                    "sources": [],
                    "confidence": 0.0,
                    "agentic": False
                }
