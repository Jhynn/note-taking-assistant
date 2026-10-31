import time

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.core.logger import logger

from app.api.endpoints import notes
from app.core.database import db
from app.models.notes import Note

app = FastAPI(title="Second Brain API", version="1.0.0")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(f"Method: {request.method} Path: {request.url.path} Status: {response.status_code} Latency: {process_time:.4f}s")

    return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Startup: Code before the yield runs before the app starts taking requests
    print("Starting up...")

    db.connect()
    db.create_tables([Note])

    yield

    # 2. Shutdown: Code after the yield runs after the app finishes handling requests
    print("Shutting down...")

    if not db.is_closed():
        db.close()

@app.get('/')
def root():
    return {
        'message': 'Welcome to the Second brain app!'
    }

# Register routes (like registering controllers in Laravel routes/api.php)
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
