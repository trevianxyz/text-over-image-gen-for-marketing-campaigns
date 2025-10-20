# Creative Automation Pipeline - Developer Setup Guide

## 🚀 Quick Start for New Developers

### Prerequisites

- **Docker** (latest version)
- **Git** (for cloning the repository)
- **API Keys** (Hugging Face and OpenAI - see setup below)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd for-adobe

# Create environment file
cp .env.example .env
```

2. Start Python environment & sync dependencies.
   This repo is a fork of [https://github.com/astral-sh/uv-fastapi-example](https://github.com/astral-sh/uv-fastapi-example) from the py package manager `uv`, so the application ships with without need to init uv. Don't run `uv init`.

You should start a py env with the cmd:

```bash
uv venv
```

once the venv is started, you need to sync the dependencies:

```bash
uv sync
```

### 3. Configure & export API Keys

Edit `.env` file with your API keys:

```bash
# Required: OpenAI API Key (for LLM translation and fallback image generation)
OPENAI_API_KEY=sk-proj-your-openai-key-here

# Optional: Hugging Face API Key (for primary image generation; fallback to openai dall-e-3)
HF_TOKEN=hf_your-huggingface-token-here
```

**Get API Keys:**

- **OpenAI**: https://platform.openai.com/api-keys
- **Hugging Face**: https://huggingface.co/settings/tokens

Export API keys and env variables

```bash
# Required: OpenAI API Key (for LLM translation and fallback image generation)
export OPENAI_API_KEY=sk-proj-your-openai-key-here
# Optional: Hugging Face API Key (for primary image generation; fallback to openai dall-e-3)
export HF_TOKEN=hf_your-huggingface-token-here
```

### 4. Build and Run

NOTE:
** You must have [Docker Desktop](https://docs.docker.com/desktop/) or a Docker Engine (daemon) running to launch this container. **

```bash
# Build the Docker image
docker build -t adobe-fastapi-app .

# Run the container with persistent storage
docker run -d -p 8080:80 --name adobe-fastapi-container \
  -v "$(pwd)/assets:/app/assets" \
  -v "$(pwd)/db:/app/db" \
  -v "$(pwd)/.env:/app/.env" \
  adobe-fastapi-app
```

### 5. Verify Installation

```bash
# Check container is running
docker ps --filter name=adobe-fastapi-container

# Test the API
curl http://localhost:8080/api/health
```

6.

# View the frontend

### Open the web interface

```bash
open http://localhost:8080
```

## 🌍 Features Overview

### **AI-Powered Campaign Generation**

- **Multi-Product Support**: Generate images for multiple products in one campaign
- **3 Size Variants**: Square (1:1), Landscape (16:9), Portrait (9:16)
- **Dual AI Providers**: Hugging Face (primary) + OpenAI DALL-E (fallback)
- **Smart Fallback**: Automatic failover if primary service is unavailable
- **Cultural Localization**: Region-specific prompts and cultural adaptation
- **Brand Overlay**: Automatic Werkr branding with translated text

### **Localization & Translation**

- **50+ Countries**: Support for international markets with country-specific localization
- **RTL Language Support**: Right-to-left text for Arabic, Hebrew, Persian, Urdu
- **Cultural Context**: Region-specific prompts for better relevance
- **LLM Translation**: GPT-4 powered translation with cultural adaptation
- **Brand Overlay**: Werkr logo with localized text and regional branding

### **Enterprise Features**

- **Vector Search**: ChromaDB for campaign similarity and content reuse
- **Analytics**: DuckDB for campaign tracking and performance insights
- **Compliance**: Automated content validation and safety checks
- **Persistent Storage**: All data survives container restarts
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Health Monitoring**: Built-in health checks and status endpoints

## 📁 Project Structure

```
for-adobe/
├── backend/                    # FastAPI application
│   └── app/
│       ├── main.py           # FastAPI app with lifespan events
│       ├── routes.py         # Campaign generation endpoints
│       ├── models/           # Pydantic data models
│       └── services/         # Business logic
│           ├── generator.py  # AI image generation + localization
│           ├── embeddings.py # ChromaDB vector search
│           ├── logging_db.py # DuckDB analytics
│           └── compliance.py # Content validation
├── frontend/                  # Web interface
│   ├── templates/           # Jinja2 HTML templates
│   └── static/             # CSS, JS, images
├── assets/                   # Generated content
│   ├── generated/           # Campaign outputs
│   ├── inputs/             # Input images and manifests
│   └── werkr_brand_image.png # Brand logo for overlays
├── db/                      # Databases
│   ├── chroma/             # ChromaDB vector store
│   └── campaigns.duckdb    # DuckDB analytics
├── generate_master_manifest.py # Campaign manifest generator
├── Dockerfile              # Container configuration
├── pyproject.toml          # Python dependencies
└── .env                    # API keys (create from .env.example)
```

## 🎯 Usage Examples

### Web Interface

1. Open http://localhost:8080
2. Fill out the campaign form:
   - **Products**: "safety helmet, work boots"
   - **Region**: "Mexico" (auto-translates to Spanish)
   - **Audience**: "construction workers"
   - **Message**: "Professional safety equipment"
3. Click "Generate Campaign"
4. View results with translated text and brand overlay

### API Usage

```bash
# Generate campaign via API
curl -X POST http://localhost:8080/campaigns/generate \
  -H "Content-Type: application/json" \
  -d '{
    "products": ["safety helmet", "work boots"],
    "region": "Germany",
    "audience": "construction workers",
    "message": "Professional safety equipment"
  }'
```

**Response:**

```json
{
  "campaign_id": "uuid-here",
  "outputs": {
    "1:1": "assets/generated/campaign_20251015_153700_uuid/safety_helmet/1x1/image_1x1.png",
    "16:9": "assets/generated/campaign_20251015_153700_uuid/safety_helmet/16x9/image_16x9.png",
    "9:16": "assets/generated/campaign_20251015_153700_uuid/safety_helmet/9x16/image_9x16.png"
  },
  "compliance": {
    "status": "approved",
    "issues": [],
    "message": "No compliance issues detected"
  }
}
```

## 🔧 Development Workflow

### Making Changes

```bash
# Stop container
docker stop adobe-fastapi-container

# Remove container
docker rm adobe-fastapi-container

# Rebuild with changes
docker build -t adobe-fastapi-app .

# Run updated container
docker run -d -p 8080:80 --name adobe-fastapi-container \
  -v "$(pwd)/assets:/app/assets" \
  -v "$(pwd)/db:/app/db" \
  -v "$(pwd)/.env:/app/.env" \
  adobe-fastapi-app
```

### Viewing Logs

```bash
# Container logs
docker logs adobe-fastapi-container

# Follow logs in real-time
docker logs -f adobe-fastapi-container

# Check specific services
docker logs adobe-fastapi-container | grep -E "(🚀|🔄|✅|⚠️|🌍|🏷️)"
```

### Database Access

```bash
# Query DuckDB analytics
docker exec adobe-fastapi-container /app/.venv/bin/python -c "
import duckdb
conn = duckdb.connect('db/campaigns.duckdb', read_only=True)
print(conn.execute('SELECT campaign_id, created_at, region, compliance_status FROM campaigns ORDER BY created_at DESC LIMIT 5').fetchall())
"

# Check ChromaDB collections
docker exec adobe-fastapi-container /app/.venv/bin/python -c "
import chromadb
client = chromadb.Client()
print(client.list_collections())
"
```

## 🐛 Troubleshooting

### Common Issues

**1. Container won't start:**

```bash
# Check logs
docker logs adobe-fastapi-container

# Common fixes:
# - Missing .env file
# - Invalid API keys
# - Port conflicts
```

**2. Images not displaying:**

```bash
# Check if assets are accessible
curl -I http://localhost:8080/assets/generated/campaign_*/product_name/1x1/image_1x1.png

# Verify volume mounts
docker inspect adobe-fastapi-container | grep -A 10 "Mounts"
```

**3. Translation not working:**

```bash
# Check OpenAI API key
docker exec adobe-fastapi-container printenv OPENAI_API_KEY

# Test translation manually
docker exec adobe-fastapi-container /app/.venv/bin/python -c "
from app.services.generator import translate_message_with_llm
print(translate_message_with_llm('Safety first', 'Mexico'))
"
```

**4. Port conflicts:**

```bash
# Check what's using port 8080
lsof -i :8080

# Use different port
docker run -d -p 8081:80 --name adobe-fastapi-container ...
```

### Performance Optimization

**For faster generation:**

- Use OpenAI DALL-E 3 (set `HF_TOKEN=""` to skip Hugging Face)
- Reduce image quality in `generator.py`
- Use smaller image sizes

**For better translations:**

- Upgrade to GPT-4 in `translate_message_with_llm()`
- Add more language mappings in `region_languages`

## 📊 Monitoring

### Health Checks

```bash
# API health
curl http://localhost:8080/api/health

# Container status
docker ps --filter name=adobe-fastapi-container

# Resource usage
docker stats adobe-fastapi-container
```

### Analytics Queries

```bash
# Campaign success rate
docker exec adobe-fastapi-container /app/.venv/bin/python -c "
import duckdb
conn = duckdb.connect('db/campaigns.duckdb', read_only=True)
result = conn.execute('SELECT compliance_status, COUNT(*) FROM campaigns GROUP BY compliance_status').fetchall()
print('Compliance Status:', result)
"

# Most popular regions
docker exec adobe-fastapi-container /app/.venv/bin/python -c "
import duckdb
conn = duckdb.connect('db/campaigns.duckdb', read_only=True)
result = conn.execute('SELECT region, COUNT(*) as campaigns FROM campaigns GROUP BY region ORDER BY campaigns DESC LIMIT 10').fetchall()
print('Top Regions:', result)
"
```

## 🚀 Production Deployment

### Environment Variables

```bash
# Production .env
OPENAI_API_KEY=sk-proj-your-production-key
HF_TOKEN=hf_your-production-token
```

### Docker Compose (Optional)

```yaml
# docker-compose.yml
version: "3.8"
services:
  creative-pipeline:
    build: .
    ports:
      - "8080:80"
    volumes:
      - ./assets:/app/assets
      - ./db:/app/db
      - ./.env:/app/.env
    restart: unless-stopped
```

### Security Considerations

- Rotate API keys regularly
- Use environment-specific keys
- Monitor API usage and costs
- Implement rate limiting for production

## 📚 API Documentation

- **Interactive Docs**: http://localhost:8080/docs
- **OpenAPI Spec**: http://localhost:8080/openapi.json
- **Health Check**: http://localhost:8080/api/health
- **Countries API**: http://localhost:8080/api/countries
- **Audiences API**: http://localhost:8080/api/audiences
- **Master Manifest**: http://localhost:8080/api/master-manifest

## 🎬 Demo & Learning Resources

### Comprehensive Demo Script

- **📋 Demo Script**: `demo_script.md` - 12-scene narrative demo covering:
  - FastAPI application architecture
  - Docker containerization
  - AI image generation pipeline
  - Vector search and analytics
  - Internationalization features
  - Production deployment considerations

### Key Demo Scenes

1. **Application Startup** - Lifespan management and health checks
2. **Data Models** - Pydantic validation and type safety
3. **Campaign Generation** - Complete creative pipeline workflow
4. **AI Image Generation** - Multi-provider fallback system
5. **Vector Search** - Semantic search with ChromaDB
6. **Database Analytics** - Campaign logging with DuckDB
7. **Docker Setup** - Multi-stage builds with international fonts
8. **Container Orchestration** - Production deployment
9. **Internationalization** - 50+ countries with cultural adaptation
10. **API Documentation** - Interactive Swagger UI
11. **Development Workflow** - Hot reloading and testing
12. **Production Deployment** - Scalability and monitoring

## 🛠️ Development Tools

### Master Manifest Generation

```bash
# Generate master manifest of all campaigns
python generate_master_manifest.py

# Access via API
curl http://localhost:8080/api/master-manifest
```

### Testing & Validation

```bash
# Run test suite
python -m pytest

# Test specific components
python test_country_selector_final.py
python test_server_routes.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with the demo script
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

---

**Need help?**

- Check the logs first: `docker logs adobe-fastapi-container`
- Follow the demo script: `demo_script.md`
- Review API docs: http://localhost:8080/docs

<!-- Hard stop and rebuild docker container.
Stop. Remove. Build. Run.  -->

```bash
docker stop adobe-fastapi-container && docker rm adobe-fastapi-container && docker build -t adobe-fastapi-app . && docker run -d -p 8080:8080 --name adobe-fastapi-container -v "$(pwd)/assets:/app/assets" -v "$(pwd)/db:/app/db" adobe-fastapi-app
```
