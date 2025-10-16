FROM python:3.12-slim-bookworm

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install fonts for international text support (RTL, non-Latin scripts)
RUN apt-get update && apt-get install -y \
    fonts-liberation \
    fonts-dejavu-core \
    fonts-noto-core \
    fonts-noto-cjk \
    fonts-arabeyes \
    fonts-khmeros \
    fonts-thai-tlwg \
    fonts-takao \
    && rm -rf /var/lib/apt/lists/*

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --locked --no-cache

# Run the application.
# (No, this does NOT directly affect the frontend Jinja2 templates. This line only specifies the process to run, i.e., starting the FastAPI backend server.)
CMD ["/app/.venv/bin/fastapi", "run", "backend/app/main.py", "--port", "8080"]

