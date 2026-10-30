import datetime

from app.models.notes import Note
from app.schemas.note import NoteCreate, NoteUpdate
from app.core.database import vector_collection
from app.core.config import settings

from sentence_transformers import SentenceTransformer
from peewee import DoesNotExist


print(f"Loading local embedding model from: {settings.MODEL_PATH}")
embedder = SentenceTransformer(settings.MODEL_PATH) 

class NoteService:
    @staticmethod
    def get_all_notes(
        skip: int = 0, 
        limit: int = 10, 
        title_contains: str|None=None,
        order_by: str = "desc"
    ) -> list[Note]:

        query = Note.select()

        if title_contains:
            query = query.where(Note.title.contains(title_contains))

        if order_by == "desc":
            query = query.order_by(Note.created_at.desc())
        else:
            query = query.order_by(Note.created_at.asc())

        query = query.offset(skip).limit(limit)
        return list(query)

    @staticmethod
    def create_note(data: NoteCreate) -> Note:
        note = Note.create(title=data.title, content=data.content)

        text_to_embed = f"Title: {note.title}. Content: {note.content}"
        vector = embedder.encode(text_to_embed).tolist()

        vector_collection.add(
            ids=[str(note.id)],
            embeddings=[vector],
            metadatas=[{"title": note.title, "created_at": str(note.created_at)}]
        )

        return note

    @staticmethod
    def get_note(note_id: int) -> Note:
        return Note.get_by_id(note_id)

    @staticmethod
    def update_note(note_id: int, data: NoteUpdate) -> Note:
        note = Note.get_by_id(note_id)

        # Update the fields passed on the request
        if data.title is not None:
            note.title = data.title
        if data.content is not None:
            note.content = data.content

        note.updated_at = datetime.datetime.now()
        note.save()

        # Updates the vector their vector on ChromaDB
        text_to_embed = f"Title: {note.title}. Content: {note.content}"
        vector = embedder.encode(text_to_embed).tolist()

        vector_collection.update(
            ids=[str(note.id)],
            embeddings=[vector],
            metadatas=[{"title": note.title, "created_at": str(note.created_at)}]
        )

        return note

    @staticmethod
    def delete_note(note_id: int) -> None:
        note = Note.get_by_id(note_id)
        note.delete_instance()

        # Also removes their embeddings.
        vector_collection.delete(ids=[str(note_id)])

    @staticmethod
    def search_notes(query_text: str, top_k: int = 3) -> list[dict]:
        # 1. Convert the user's question into a mathematical vector
        query_vector = embedder.encode(query_text).tolist()

        # 2. Search ChromaDB for the closest vectors (Nearest Neighbors)
        # By default, ChromaDB uses Squared L2 distance
        results = vector_collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )

        if not results['ids'] or not results['ids'][0]:
            return []

        search_results = []

        # 3. Zip the results and fetch the full content from MariaDB
        # results['ids'][0] contains the matched string IDs we saved earlier
        # results['distances'][0] contains the mathematical distance
        for doc_id_str, distance in zip(results['ids'][0], results['distances'][0]): # type: ignore
            try:
                # We query MariaDB to get the actual content 
                # (since we only stored title and date in ChromaDB's metadata)
                note = Note.get_by_id(int(doc_id_str))
                search_results.append({
                    "id": note.id,
                    "title": note.title,
                    "content": note.content,
                    "distance": distance
                })
            except DoesNotExist:
                continue

        return search_results
