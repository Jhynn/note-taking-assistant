#!/usr/bin/env bash

APP_NAME="note-taking-assistant"

docker rm -f "$APP_NAME"

docker build -t "$APP_NAME" .

docker run -d \
  --name "$APP_NAME" \
  --network host \
  --env-file .env \
  -e MODEL_PATH=/model_cache \
  -v "$(pwd)/chroma_data:/app/chroma_data" \
  -v "$(pwd)/app/core/dl_models/all-MiniLM-L6-v2:/model_cache" \
  "$APP_NAME"

docker logs -f "$APP_NAME"
