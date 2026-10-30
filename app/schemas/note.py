from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class NoteCreate(BaseModel):
    title: str = Field(..., max_length=256, description="The title of the note")
    content: str = Field(..., min_length=1, description="The content of the note")

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=256)
    content: Optional[str] = Field(None, min_length=1)

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, description="The user's question or search term")
    top_k: int = Field(3, ge=1, le=10, description="Number of relevant notes to retrieve")

class SearchResult(BaseModel):
    id: int
    title: str
    content: str
    distance: float = Field(..., description="Vector distance (lower is more similar)")

class AskQuery(BaseModel):
    question: str = Field(..., min_length=2, description="Question to ask the AI")

class AskResponse(BaseModel):
    question: str
    answer: str
    source_note_ids: list[int] = Field(..., description="IDs of the notes used as context")
