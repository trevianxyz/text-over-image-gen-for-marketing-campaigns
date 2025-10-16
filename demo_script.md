# Creative Automation Pipeline - Demo Script

## Overview

Welcome to the **Creative Automation Pipeline**, a sophisticated FastAPI-based application that automates the generation of localized marketing campaigns for the Werkr workwear brand. This demo will showcase the backend architecture, API endpoints, Docker containerization, and the complete creative generation workflow.

---

## 🏗️ Architecture Overview

### Backend Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── routes.py            # Campaign generation endpoints
│   ├── models/
│   │   └── campaign.py      # Pydantic data models
│   └── services/
│       ├── generator.py     # AI image generation service
│       ├── embeddings.py   # Vector search with ChromaDB
│       ├── logging_db.py    # DuckDB campaign logging
│       ├── compliance.py    # Content compliance checking
│       ├── country_language.py  # Internationalization
│       └── audience_selector.py # Target audience management
```

### Key Technologies

- **FastAPI**: Modern, fast web framework with automatic OpenAPI documentation
- **Docker**: Containerized deployment with multi-stage builds
- **ChromaDB**: Vector database for semantic search of campaigns
- **DuckDB**: Analytics database for campaign logging and insights
- **OpenAI/DALL-E**: AI image generation with fallback mechanisms
- **Hugging Face**: Alternative AI image generation service
- **PIL/Pillow**: Image processing and localization

---

## 🚀 Demo Script: Backend Logic & FastAPI App

### Scene 1: Application Startup & Health Check

**Narrator**: "Let's start by examining how our FastAPI application initializes and manages its lifecycle."

```python
# From main.py - Application Lifespan Management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events"""
    # Startup
    print("🚀 Starting up Creative Automation Pipeline...")
    init_db()  # Initialize DuckDB for campaign logging
    yield
    # Shutdown
    print("🛑 Shutting down Creative Automation Pipeline...")
    close_db()  # Clean up database connections
```

**Demo Steps**:

1. **Start the application**: `uvicorn backend.app.main:app --reload`
2. **Check health endpoint**: `GET /api/health`
3. **View auto-generated docs**: `GET /docs` (Swagger UI)

**Expected Response**:

```json
{
  "status": "ok",
  "message": "Creative Automation Pipeline is running",
  "endpoints": ["/campaigns/generate"]
}
```

---

### Scene 2: Data Models & Validation

**Narrator**: "Our application uses Pydantic models for robust data validation and type safety."

```python
# From models/campaign.py
class CampaignBrief(BaseModel):
    products: List[str]      # e.g., ["safety_helmet", "work_gloves"]
    region: str             # e.g., "US", "DE", "JP"
    audience: str           # e.g., "construction_workers"
    message: str            # Marketing message
    assets: Optional[List[str]] = None

    @validator('region')
    def validate_region(cls, v):
        """Validate that the region is a valid country code"""
        from app.services.country_language import get_country_by_code
        if get_country_by_code(v):
            return v
        raise ValueError(f"Invalid region: {v}")
```

**Demo Steps**:

1. **Show model validation**: Demonstrate invalid region rejection
2. **Display type hints**: Show IDE autocompletion benefits
3. **Test validation**: Send malformed JSON to see validation errors

---

### Scene 3: Campaign Generation Workflow

**Narrator**: "The heart of our system is the campaign generation endpoint that orchestrates the entire creative pipeline."

```python
# From routes.py - Campaign Generation Endpoint
@router.post("/generate", response_model=GenerationResult)
def generate_campaign(brief: CampaignBrief):
    campaign_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create campaign directory structure
    campaign_dir = Path("assets/generated") / f"campaign_{timestamp}_{campaign_id}"
    campaign_dir.mkdir(parents=True, exist_ok=True)

    # Store embeddings for semantic search
    embed_and_store(campaign_id, brief.message, brief.model_dump())

    # Generate images for each product
    all_outputs = {}
    for product in brief.products:
        product_outputs = generate_creatives(
            prompt=f"{brief.message} for {brief.audience} in {brief.region}",
            campaign_id=campaign_id,
            product=product,
            region=brief.region,
            message=brief.message,
            campaign_dir=campaign_dir,
            audience=brief.audience
        )
        all_outputs[product] = product_outputs
```

**Demo Steps**:

1. **Send campaign request**:

```bash
curl -X POST "http://localhost:8000/campaigns/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "products": ["safety_helmet", "work_gloves"],
    "region": "US",
    "audience": "construction_workers",
    "message": "Stay safe on the job with premium workwear"
  }'
```

2. **Monitor directory creation**: Watch `assets/generated/` folder
3. **Check database logging**: Verify DuckDB entries
4. **Examine generated artifacts**: Review JSON metadata files

---

### Scene 4: AI Image Generation Service

**Narrator**: "Our image generation service uses multiple AI providers with intelligent fallback mechanisms."

```python
# From services/generator.py - Multi-Provider AI Generation
def generate_single_image(prompt: str, campaign_id: str, product: str, region: str) -> str:
    # Localize prompt for cultural relevance
    localized_prompt = localize_prompt(prompt, region)

    try:
        # Try Hugging Face first (faster, cheaper)
        image_bytes = generate_with_huggingface(localized_prompt, 1024, 1024)
        print(f"✅ Hugging Face generation successful")
    except Exception as e:
        print(f"⚠️ Hugging Face failed: {e}")
        # Fallback to OpenAI DALL-E 3
        image_bytes = generate_with_openai(localized_prompt, 1024, 1024)
        print(f"✅ OpenAI fallback successful")
```

**Key Features**:

- **Multi-provider fallback**: Hugging Face → OpenAI DALL-E 3
- **Cultural localization**: Region-specific prompt adaptation
- **Multiple aspect ratios**: 1:1, 16:9, 9:16 for different platforms
- **Brand overlay**: Automatic Werkr branding and localization
- **RTL language support**: Right-to-left text for Arabic, Hebrew, etc.

**Demo Steps**:

1. **Show prompt localization**: Compare original vs localized prompts
2. **Demonstrate fallback**: Simulate Hugging Face failure
3. **Display size variants**: Show 1:1, 16:9, 9:16 outputs
4. **Examine brand overlays**: Check localized text and branding

---

### Scene 5: Vector Search & Embeddings

**Narrator**: "We use ChromaDB for semantic search of past campaigns, enabling content reuse and inspiration."

```python
# From services/embeddings.py - Vector Search
def embed_and_store(campaign_id: str, text: str, metadata: dict):
    """Store campaign embeddings for semantic search"""
    vec = model.encode(text).tolist()
    collection.add(
        ids=[campaign_id],
        embeddings=[vec],
        metadatas=[clean_metadata],
        documents=[text]
    )

def search_similar(query: str, top_k: int = 3) -> Dict[str, Any]:
    """Find similar campaigns using vector similarity"""
    vec = model.encode(query).tolist()
    return collection.query(query_embeddings=[vec], n_results=top_k)
```

**Demo Steps**:

1. **Store campaign embeddings**: Generate a few campaigns
2. **Search similar content**: Query for "safety equipment"
3. **Show semantic matching**: Demonstrate non-exact keyword matches
4. **Display metadata**: Show stored campaign details

---

### Scene 6: Database Analytics with DuckDB

**Narrator**: "DuckDB provides fast analytics on campaign performance and compliance."

```python
# From services/logging_db.py - Campaign Analytics
def log_campaign(campaign_id: str, brief: Any, outputs: Dict[str, str], compliance: Dict):
    """Log campaign data to DuckDB for analytics"""
    conn.execute("""
        INSERT INTO campaigns VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        campaign_id, datetime.now(), str(brief.products),
        brief.region, brief.audience, brief.message,
        outputs.get("1:1", ""), outputs.get("16:9", ""), outputs.get("9:16", ""),
        compliance.get("status", "unknown"), str(compliance.get("issues", []))
    ])
```

**Demo Steps**:

1. **Show database schema**: Display campaigns table structure
2. **Query campaign analytics**: Run SQL queries on campaign data
3. **Export data**: Demonstrate DuckDB's export capabilities
4. **Performance metrics**: Show query execution times

---

## 🐳 Docker Containerization

### Scene 7: Docker Setup & Multi-Stage Build

**Narrator**: "Our Docker setup uses multi-stage builds and includes international font support for global campaigns."

```dockerfile
# From Dockerfile
FROM python:3.12-slim-bookworm

# Install uv for fast dependency management
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

# Copy application and install dependencies
COPY . /app
WORKDIR /app
RUN uv sync --locked --no-cache

# Run the application
CMD ["/app/.venv/bin/fastapi", "run", "backend/app/main.py", "--port", "80"]
```

**Key Features**:

- **Multi-stage build**: Optimized image size
- **International fonts**: Support for RTL languages and CJK scripts
- **Fast dependency management**: Using `uv` for quick installs
- **Production-ready**: Proper user permissions and security

**Demo Steps**:

1. **Build Docker image**: `docker build -t creative-automation .`
2. **Run container**: `docker run -p 8000:80 creative-automation`
3. **Show font support**: Generate campaigns in Arabic/Chinese
4. **Volume mounting**: Demonstrate persistent data storage

---

### Scene 8: Container Orchestration

**Narrator**: "For production deployment, we can orchestrate multiple services."

```yaml
# docker-compose.yml (example)
version: "3.8"
services:
  app:
    build: .
    ports:
      - "8000:80"
    volumes:
      - ./assets:/app/assets
      - ./db:/app/db
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - HF_TOKEN=${HF_TOKEN}

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

**Demo Steps**:

1. **Show container logs**: `docker logs <container_id>`
2. **Demonstrate volume persistence**: Restart container, check data
3. **Environment variables**: Show secure API key handling
4. **Health checks**: Demonstrate container health monitoring

---

## 🌍 Internationalization & Localization

### Scene 9: Multi-Language Support

**Narrator**: "Our system supports 50+ countries with automatic translation and cultural adaptation."

```python
# From services/country_language.py - Internationalization
def translate_message_with_llm(message: str, region: str, audience: str = None) -> str:
    """Use LLM to translate messages with cultural context"""
    country_code = get_legacy_region_mapping(region) or region
    target_language = get_primary_language(country_code)

    # Build audience context for better translation
    audience_context = f"Target audience: {audience_info.label} - {audience_info.description}"

    system_prompt = f"""Translate the following marketing message for the workwear brand Werkr into {target_language}, considering the cultural nuances and preferences of the target audience in {country_code}: {audience_context}. Keep it concise and impactful for advertising."""
```

**Demo Steps**:

1. **Generate US campaign**: English with American cultural context
2. **Generate German campaign**: German translation with European context
3. **Generate Japanese campaign**: Japanese with Asian cultural adaptation
4. **Show RTL support**: Arabic campaign with right-to-left text

---

## 📊 API Endpoints & Documentation

### Scene 10: Complete API Showcase

**Narrator**: "Our FastAPI application provides comprehensive endpoints with automatic documentation."

**Available Endpoints**:

- `GET /` - Frontend interface
- `GET /api/health` - Health check
- `GET /api/countries` - Available countries/regions
- `GET /api/audiences` - Target audience options
- `GET /api/master-manifest` - All campaign data
- `POST /campaigns/generate` - Generate new campaign
- `GET /docs` - Interactive API documentation

**Demo Steps**:

1. **Open Swagger UI**: Navigate to `http://localhost:8000/docs`
2. **Test all endpoints**: Use the interactive interface
3. **Show request/response schemas**: Demonstrate type safety
4. **Export OpenAPI spec**: Download API specification

---

## 🔧 Development & Testing

### Scene 11: Development Workflow

**Narrator**: "Our development setup supports hot reloading and comprehensive testing."

**Development Commands**:

```bash
# Start development server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
python -m pytest

# Build Docker image
docker build -t creative-automation .

# Run with Docker
docker run -p 8000:80 -v $(pwd)/assets:/app/assets creative-automation
```

**Demo Steps**:

1. **Show hot reloading**: Modify code, see automatic restart
2. **Run test suite**: Execute comprehensive tests
3. **Debug mode**: Show detailed error messages
4. **Performance monitoring**: Display request timing

---

## 🎯 Production Considerations

### Scene 12: Production Deployment

**Narrator**: "For production deployment, we consider scalability, security, and monitoring."

**Production Features**:

- **Database persistence**: DuckDB and ChromaDB data volumes
- **API rate limiting**: Prevent abuse and ensure fair usage
- **Error handling**: Graceful degradation and user feedback
- **Monitoring**: Health checks and performance metrics
- **Security**: API key management and input validation

**Demo Steps**:

1. **Show production config**: Environment variables and settings
2. **Demonstrate error handling**: Simulate API failures
3. **Load testing**: Show system under stress
4. **Monitoring dashboard**: Display real-time metrics

---

## 🎬 Demo Conclusion

**Narrator**: "The Creative Automation Pipeline demonstrates modern Python web development with FastAPI, containerization with Docker, and AI-powered content generation. The system scales from development to production while maintaining code quality and user experience."

**Key Takeaways**:

- **FastAPI**: Modern, fast, and automatically documented APIs
- **Docker**: Consistent deployment across environments
- **AI Integration**: Multi-provider fallback for reliability
- **Internationalization**: Global-ready with cultural adaptation
- **Database Design**: Analytics with DuckDB, search with ChromaDB
- **Development Experience**: Hot reloading, testing, and debugging

**Next Steps**:

- Deploy to cloud platforms (AWS, GCP, Azure)
- Add monitoring and alerting (Prometheus, Grafana)
- Implement user authentication and authorization
- Scale with Kubernetes orchestration
- Add advanced AI features (video generation, voice synthesis)

---

_This demo script showcases a production-ready creative automation system built with modern Python web technologies, demonstrating best practices in API design, containerization, and AI integration._
