import os
import chromadb

from dotenv import load_dotenv
from peewee import MySQLDatabase
from .config import settings

load_dotenv()


# Relational Database (MariaDB)
db = MySQLDatabase(
    database=settings.DB_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    port=settings.DB_PORT,
    host=settings.HOST,
)

# Vector Database (ChromaDB)
chroma_client = chromadb.PersistentClient(path="./chroma_data")
vector_collection = chroma_client.get_or_create_collection(name="notes_embeddings")
