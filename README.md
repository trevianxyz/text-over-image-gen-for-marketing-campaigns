# Creative Automation Pipeline

A [FastAPI](https://github.com/fastapi/fastapi) application for automated campaign creative generation, managed with [uv](https://github.com/astral-sh/uv).

## Features

- **AI Image Generation** - Generate campaign creatives via Hugging Face API
- **Vector Search** - ChromaDB for campaign similarity search
- **Analytics Logging** - DuckDB for campaign tracking and analytics
- **Compliance Checking** - Automated content validation
- **Docker Ready** - Containerized with persistent storage
- **Lifecycle Management** - FastAPI lifespan events for clean startup/shutdown

## Requirements

- Docker
- `.env` file with `HF_TOKEN` for Hugging Face API (optional for testing)

## Quick Start

### 1. Build the Docker Image

```bash
docker build -t adobe-fastapi-app .
```

### 2. Run the Container

```bash
# Run with volume mounts for persistent storage (assets + DuckDB + ChromaDB)
docker run -d -p 8080:80 --name adobe-fastapi-container \
  -v "$(pwd)/assets:/app/assets" \
  -v "$(pwd)/db:/app/db" \
  $([ -f .env ] && echo "-v $(pwd)/.env:/app/.env" || echo "") \
  adobe-fastapi-app
```

### 3. Verify the API is Running

```bash
curl http://localhost:8080/
# Response:
# {"status":"ok","message":"Creative Automation Pipeline is running","endpoints":["/campaigns/generate"]}
```

## API Endpoints

- **API Root**: http://localhost:8080/
- **Interactive Docs**: http://localhost:8080/docs
- **OpenAPI Spec**: http://localhost:8080/openapi.json
- **Generate Campaign**: `POST /campaigns/generate`

### Example API Request

```bash
curl -X POST http://localhost:8080/campaigns/generate \
  -H "Content-Type: application/json" \
  -d '{
    "products": ["Running Shoes", "Sportswear"],
    "region": "North America",
    "audience": "Athletes and fitness enthusiasts",
    "message": "Run faster, push harder with our new performance gear"
  }'
```

**Response:**

```json
{
  "campaign_id": "uuid-here",
  "outputs": {
    "1:1": "assets/generated/gen_123_1024x1024.png",
    "16:9": "assets/generated/gen_123_1024x576.png",
    "9:16": "assets/generated/gen_123_576x1024.png"
  },
  "compliance": {
    "status": "approved",
    "issues": [],
    "message": "No compliance issues detected"
  }
}
```

## Asset Storage Locations

Generated images and data are stored in the following locations:

### Generated Images

- **Host Machine**: `./assets/generated/`
- **Container**: `/app/assets/generated/`
- **Naming**: `gen_{process_id}_{width}x{height}.png`

Example output from API:

```json
{
  "campaign_id": "b79ad02a-3ce1-4ae9-b7d4-042926b4dd74",
  "outputs": {
    "1:1": "assets/generated/gen_123_1024x1024.png",
    "16:9": "assets/generated/gen_123_1024x576.png",
    "9:16": "assets/generated/gen_123_576x1024.png"
  }
}
```

### ChromaDB Vector Database

- **Host Machine**: `./db/chroma/`
- **Container**: `/app/db/chroma/`
- Stores campaign embeddings for similarity search
- Persists across container restarts

### DuckDB Analytics Database

- **Host Machine**: `./db/campaigns.duckdb`
- **Container**: `/app/db/campaigns.duckdb`
- Logs all campaign generation events for analytics
- **Initialization**: Uses FastAPI lifespan events for proper startup/shutdown
- **Connection**: Single pooled connection reused across requests

**Schema:**

```sql
CREATE TABLE campaigns (
    campaign_id VARCHAR PRIMARY KEY,
    created_at TIMESTAMP,
    products VARCHAR,
    region VARCHAR,
    audience VARCHAR,
    message TEXT,
    output_square VARCHAR,
    output_landscape VARCHAR,
    output_portrait VARCHAR,
    compliance_status VARCHAR,
    compliance_issues TEXT
)
```

**Example Queries:**

```bash
# Connect from inside the container
docker exec adobe-fastapi-container /app/.venv/bin/python -c "
import duckdb
conn = duckdb.connect('db/campaigns.duckdb')
print(conn.execute('SELECT campaign_id, created_at, region, compliance_status FROM campaigns ORDER BY created_at DESC LIMIT 5').fetchall())
"
```

**Note**: Both volume mounts (`assets` and `db`) ensure your data persists on the host machine and survives container restarts/removals.

## Architecture & Data Flow

When you POST to `/campaigns/generate`:

1. ** Vector Embeddings** → Campaign text is embedded and stored in ChromaDB for similarity search
2. ** Image Generation** → Three images generated via Hugging Face API (square, landscape, portrait)
3. ** Compliance Check** → Message is validated for compliance issues
4. ** Analytics Logging** → Full campaign details logged to DuckDB
5. ** Response** → Returns campaign ID, file paths, and compliance status

### Lifecycle Management

The application uses **FastAPI lifespan events** for proper resource management:

- **Startup** (`app/main.py`):
  - DuckDB connection initialized
  - Tables created if not exist
  - Connection pooled for reuse
- **Shutdown** (`app/main.py`):
  - DuckDB connection closed gracefully
  - No data loss on container stop

### troubleshooting

`double check you've exported api keys from .env file.`

1. remove the docker container

```bash
docker rm adobe-fastapi-container
```

2. check docker logs

```bash
docker logs adobe-fastapi
```

3. potential issues
   a. Be certain Chromadb is lazy loaded
   b. port conflict with chroma and fastapi; check port conflict

```bash
lsof -i :8000
```

## Tech Stack

- **FastAPI** - Modern Python web framework
- **DuckDB** - Analytics database for campaign logging
- **ChromaDB** - Vector database for similarity search
- **Sentence Transformers** - Text embeddings
- **Hugging Face** - AI image generation API
- **Docker** - Containerization
- **uv** - Fast Python package manager

## License

MIT

---

<div align="center">
  <a target="_blank" href="https://astral.sh" style="background:none">
    <img src="https://raw.githubusercontent.com/astral-sh/uv/main/assets/svg/Astral.svg" alt="Made by Astral" width="120">
  </a>
</div>
