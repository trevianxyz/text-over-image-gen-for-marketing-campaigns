# Creative Automation Pipeline - Stack Outline

## 🏗️ Technology Stack

### **Backend Framework**

- **FastAPI** - Modern Python web framework
  - Async/await support for high performance
  - Automatic OpenAPI/Swagger documentation
  - Type safety with Pydantic models
  - Built-in validation and serialization

### **AI/ML Services**

- **Hugging Face** (Primary) - Stable Diffusion XL
  - Cost-effective image generation
  - Fast inference API
  - High-quality outputs
- **OpenAI DALL-E 3** (Fallback) - Reliable backup
  - Automatic failover on HF errors
  - Enterprise-grade reliability
  - Multi-provider resilience

### **Databases**

- **ChromaDB** - Vector database
  - Semantic search for campaigns
  - Sentence transformers embeddings
  - Content similarity matching
- **DuckDB** - Analytics database
  - Fast SQL queries
  - Campaign tracking and logging
  - Embedded, no setup required

### **Frontend**

- **Jinja2 Templates** - Server-side rendering
  - Dynamic HTML generation
  - Template inheritance
  - Context-aware rendering
- **Vanilla JavaScript** - Client-side interactivity
  - Country/region selector
  - Audience selector
  - Form validation and submission
- **CSS3** - Modern styling
  - Dark navy theme
  - Responsive design
  - CSS variables for theming

### **Containerization**

- **Docker** - Application packaging
  - Python 3.12 slim base image
  - Multi-stage builds
  - International font support (RTL, CJK)
  - Volume mounting for persistence

### **Dependency Management**

- **uv** - Fast Python package installer
  - Lightning-fast dependency resolution
  - Lock file for reproducibility
  - Minimal image size

### **Image Processing**

- **Pillow (PIL)** - Image manipulation
  - Brand overlay and watermarking
  - Smart cropping and resizing
  - Multiple aspect ratios (1:1, 16:9, 9:16)
  - Text rendering with international fonts

### **Internationalization**

- **OpenAI GPT-5** - Translation service
  - Cultural adaptation
  - Context-aware translations
  - 50+ countries supported
- **RTL Language Support**
  - Arabic, Hebrew, Persian, Urdu
  - Right-to-left text rendering
  - International font families

## 🔄 Architecture Pattern

### **Microservices-Ready Design**

```
FastAPI Application
├── Routes Layer (API endpoints)
├── Services Layer (business logic)
│   ├── generator.py (AI image generation)
│   ├── embeddings.py (vector search)
│   ├── logging_db.py (analytics)
│   ├── compliance.py (content validation)
│   ├── country_language.py (i18n)
│   └── audience_selector.py (targeting)
├── Models Layer (Pydantic schemas)
└── Frontend Layer (templates + static)
```

### **Data Flow**

```
User Request → FastAPI → Validation (Pydantic)
    ↓
Campaign Generation Service
    ↓
AI Image Generation (HF → OpenAI fallback)
    ↓
Image Processing (Pillow)
    ↓
Translation (GPT-4) + Localization
    ↓
Storage (ChromaDB + DuckDB)
    ↓
Response (JSON + Images)
```

## 🚀 Key Features

### **Performance**

- Async request handling
- Connection pooling
- Embedded databases (no network overhead)
- Multi-provider AI failover

### **Scalability**

- Stateless application design
- Horizontal scaling ready
- Container-native architecture
- Volume-based data persistence

### **Reliability**

- Multi-provider AI fallback
- Graceful error handling
- Health check endpoints
- Comprehensive logging

### **Developer Experience**

- Hot reloading in development
- Auto-generated API docs
- Type hints throughout
- Clear separation of concerns

### **Global Ready**

- 50+ countries supported
- RTL language rendering
- Cultural adaptation
- Multi-language translations

## 📦 Dependencies

### **Core**

- `fastapi[standard]>=0.112.1` - Web framework
- `uvicorn` - ASGI server
- `python-dotenv>=1.0.1` - Environment variables

### **AI/ML**

- `openai>=2.3.0` - OpenAI API client
- `sentence-transformers>=5.1.1` - Embeddings
- `chromadb>=1.1.1` - Vector database

### **Data**

- `duckdb>=1.4.1` - Analytics database
- `pydantic` - Data validation

### **Image Processing**

- `pillow>=10.0.0` - Image manipulation
- `httpx` - HTTP client for API calls

## 🎯 Production Considerations

### **Deployment**

- Docker containerization
- Environment-based configuration
- Volume mounting for data persistence
- Multi-stage builds for optimization

### **Security**

- API key management via environment variables
- Input validation with Pydantic
- CORS middleware for API access
- Content compliance checking

### **Monitoring**

- Health check endpoints
- Structured logging
- Campaign analytics
- Error tracking

### **Cost Optimization**

- Primary use of Hugging Face (cheaper)
- Fallback to OpenAI only when needed
- Embedded databases (no cloud costs)
- Efficient image processing

---

**Stack Philosophy**: Modern, performant, globally-scalable, and cost-effective creative automation platform built with production-ready technologies and best practices.
