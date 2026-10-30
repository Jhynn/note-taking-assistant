from fastapi import APIRouter, HTTPException, Query, Path
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse, SearchQuery, SearchResult, AskQuery, AskResponse
from app.services.note_service import NoteService
from app.services.llm_service import LLMService
from peewee import DoesNotExist


router = APIRouter()

@router.get("/", response_model=list[NoteResponse])
def list_notes(
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Limit for pagination"),
    title_contains: str = Query(None, description="Filter by title"),
    order_by: str = Query("desc", pattern="^(asc|desc)$", description="Sort order by created_at")
):
    return NoteService.get_all_notes(skip, limit, title_contains, order_by)

@router.post("/", response_model=NoteResponse)
def create_note(note_in: NoteCreate):
    return NoteService.create_note(note_in)

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int = Path(..., description="The ID of the note")):
    try:
        return NoteService.get_note(note_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Note not found")

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_in: NoteUpdate, note_id: int = Path(...)):
    try:
        return NoteService.update_note(note_id, note_in)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Note not found")

@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int = Path(...)):
    try:
        NoteService.delete_note(note_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Note not found")

@router.post("/search", response_model=list[SearchResult])
def search_notes_endpoint(search_in: SearchQuery):
    """
    Performs semantic search across all notes using vector embeddings.
    """
    results = NoteService.search_notes(search_in.query, search_in.top_k)
    return results

@router.post("/ask", response_model=AskResponse)
def ask_second_brain(query_in: AskQuery):
    """
    RAG Endpoint: Retrieves relevant notes and asks the LLM to generate an answer.
    """
    # 1. Retrieval (Busca Semântica)
    relevant_notes = NoteService.search_notes(query_in.question, top_k=3)

    # 2. In case the DB is empty
    if not relevant_notes:
        return AskResponse(
            question=query_in.question,
            answer="I couldn't find any relevant notes to answer your question.",
            source_note_ids=[]
        )

    # 3. Generation with LLM
    answer = LLMService.generate_rag_answer(query_in.question, relevant_notes)

    # 4. The notes used as sources
    source_ids = [note["id"] for note in relevant_notes]

    return AskResponse(
        question=query_in.question,
        answer=answer,
        source_note_ids=source_ids
    )
