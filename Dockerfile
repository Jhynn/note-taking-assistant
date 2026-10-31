FROM python:3.13-slim

# official uv binary image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# uv dependency files (pyproject.toml and uv.lock)
COPY pyproject.toml uv.lock* ./

# installing globally the py dependencies
RUN uv pip install --system -r pyproject.toml

# copying the project to the container
COPY . .

# container will use the 8000 port
EXPOSE 8000

# the command that will be executed at startup (0.0.0.0 lets uvicorn accept outside connections from the container)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
