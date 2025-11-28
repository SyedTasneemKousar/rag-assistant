"""
Pydantic Models for API Request/Response
These define the structure of data sent to and received from the API
"""

from pydantic import BaseModel
from typing import Optional, List


class QueryRequest(BaseModel):
    """Request model for asking questions"""
    question: str
    chat_history: Optional[List[dict]] = []


class QueryResponse(BaseModel):
    """Response model for answers"""
    answer: str
    sources: Optional[List[str]] = []
    confidence: Optional[float] = None


class UploadResponse(BaseModel):
    """Response after uploading a document"""
    message: str
    document_id: str
    chunks_processed: int
