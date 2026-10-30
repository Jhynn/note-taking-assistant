import os

from sentence_transformers import SentenceTransformer
from app.core.config import settings


print("Downloading model from Hugging Face...")
model = SentenceTransformer('all-MiniLM-L6-v2')

os.makedirs(settings.MODEL_PATH, exist_ok=True)
model.save(settings.MODEL_PATH)
print(f"Model successfully saved to {settings.MODEL_PATH}")
