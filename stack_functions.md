# Creative Automation Pipeline - API Endpoints & Functions Documentation

## Overview

This document provides a comprehensive overview of all API endpoints and service functions in the Creative Automation Pipeline application. The system is designed to generate localized marketing creatives for the WERKR work apparel brand across different countries, audiences, and products.

## Application Architecture

### Main Application (`backend/app/main.py`)

- **FastAPI Application**: Core web framework with CORS middleware
- **Static File Serving**: Serves frontend assets and generated images
- **Template Rendering**: Jinja2 templates for HTML responses
- **Database Lifecycle**: Manages DuckDB connection initialization and cleanup

---

## API Endpoints

### Core Application Endpoints

#### `GET /`

- **Purpose**: Serves the main HTML frontend interface
- **Response**: Rendered `index.html` template
- **Usage**: Entry point for the web application

#### `GET /api/health`

- **Purpose**: Health check endpoint for monitoring
- **Response**: Application status and available endpoints
- **Usage**: Verify application is running and responsive

---

### Campaign Management Endpoints (`/campaigns`)

#### `POST /campaigns/generate`

- **Purpose**: Generate creative campaign assets for multiple products
- **Input**: `CampaignBrief` (products, country, audience, message, assets, generation parameters)
- **Process**:
  1. Creates campaign directory structure
  2. Stores embeddings for semantic search
  3. Generates images for each product using AI models
  4. Creates multiple aspect ratios (1:1, 16:9, 9:16)
  5. Adds brand overlay and localized text
  6. Runs compliance checks
  7. Logs campaign data to database
- **Output**: `GenerationResult` with campaign ID, image paths, compliance status, and metadata
- **Features**: Multi-model fallback (Hugging Face → OpenAI), cost calculation, error handling

#### `POST /campaigns/search`

- **Purpose**: Semantic search for similar campaigns using vector embeddings
- **Input**: `SearchQuery` (query text, top_k results)
- **Process**:
  1. Converts query to vector embedding
  2. Searches ChromaDB for similar campaigns
  3. Enriches results with full campaign data from master manifest
  4. Calculates similarity scores
- **Output**: List of similar campaigns with metadata and similarity scores

#### `GET /campaigns/master-manifest`

- **Purpose**: Retrieve the master manifest containing all campaign history
- **Response**: Complete campaign manifest with metadata
- **Usage**: Frontend dashboard and campaign management

---

### Analytics Endpoints (`/campaigns/analytics`)

#### `GET /campaigns/analytics/overview`

- **Purpose**: Comprehensive analytics dashboard data
- **Response**: Campaign metrics, recent campaigns, compliance status, top regions/audiences
- **Usage**: Main dashboard overview

#### `GET /campaigns/analytics/campaigns/recent`

- **Purpose**: Get recent campaigns with optional limit
- **Parameters**: `limit` (default: 10)
- **Response**: List of recent campaigns with full details

#### `GET /campaigns/analytics/campaigns/search`

- **Purpose**: Search campaigns with multiple filters
- **Parameters**: `country`, `audience`, `product`, `compliance_status`, `limit`
- **Response**: Filtered campaign results

#### `GET /campaigns/analytics/geographic`

- **Purpose**: Geographic distribution analytics
- **Response**: Campaign distribution by region and regional performance metrics

#### `GET /campaigns/analytics/audience`

- **Purpose**: Audience distribution and performance analytics
- **Response**: Campaign distribution by audience and audience performance metrics

#### `GET /campaigns/analytics/compliance`

- **Purpose**: Compliance and quality analytics
- **Response**: Compliance status distribution and campaigns with issues

#### `GET /campaigns/analytics/temporal`

- **Purpose**: Time-based analytics
- **Response**: Today's campaigns and hourly activity patterns

#### `GET /campaigns/analytics/products`

- **Purpose**: Product analysis and categorization
- **Response**: Popular products, safety equipment campaigns, construction gear campaigns

#### `GET /campaigns/analytics/database/stats`

- **Purpose**: Database statistics and schema information
- **Response**: Database schema, total campaigns, date range

#### `GET /campaigns/analytics/campaigns/{campaign_id}`

- **Purpose**: Get detailed information for a specific campaign
- **Parameters**: `campaign_id` (path parameter)
- **Response**: Complete campaign details

---

### Data Service Endpoints

#### `GET /api/countries`

- **Purpose**: Get all available countries for the country selector
- **Response**: Countries list with language mappings and regions
- **Usage**: Frontend country selection dropdown

#### `GET /api/audiences`

- **Purpose**: Get all available audiences for the audience selector
- **Response**: Audience options with categories and metadata
- **Usage**: Frontend audience selection interface

#### `GET /api/master-manifest`

- **Purpose**: Get the master manifest containing all campaign data
- **Response**: Complete manifest with campaign history
- **Usage**: Campaign management and asset discovery

---

## Service Modules

### 1. Campaign Models (`backend/app/models/campaign.py`)

#### `CampaignBrief`

- **Purpose**: Input validation model for campaign generation requests
- **Fields**:
  - `products`: List of product names
  - `country_name`: Target country (validated against country database)
  - `audience`: Target audience identifier
  - `message`: Campaign message text
  - `assets`: Optional asset references
  - `noise_scheduler`, `unet_backbone`, `vae`: AI generation parameters
  - `guidance_scale`, `num_inference_steps`, `seed`: Generation control parameters
- **Validation**: Country name validation against country/language database

#### `GenerationResult`

- **Purpose**: Response model for campaign generation
- **Fields**:
  - `campaign_id`: Unique campaign identifier
  - `outputs`: Dictionary mapping products to aspect ratios to file paths
  - `compliance`: Compliance check results
  - `metadata`: Generation metadata including costs and token usage

---

### 2. Audience Selector Service (`backend/app/services/audience_selector.py`)

#### `AudienceOption`

- **Purpose**: Data model for audience selection options
- **Fields**: `id`, `label`, `description`, `age_group`, `gender`, `interests`, `category`

#### Key Functions:

- **`get_audience_selector_data()`**: Returns formatted audience data for frontend
- **`get_audience_by_id(audience_id)`**: Retrieves specific audience option
- **`validate_audience(audience_id)`**: Validates audience ID exists

#### Audience Categories:

- **Demographics**: Age-based groups (Young Adults, Millennials, Gen X, Boomers)
- **Professions**: Industry-specific groups (Construction, Healthcare, Office, Retail, etc.)
- **Interests**: Interest-based targeting (Safety-conscious, Tech enthusiasts, etc.)
- **Gender-specific**: Male/Female professionals
- **Industry-specific**: Warehouse, Maintenance, Security personnel

---

### 3. Compliance Service (`backend/app/services/compliance.py`)

#### Key Functions:

- **`check_compliance(message, image_paths)`**: Main compliance checking function
  - Validates message content for inappropriate language
  - Checks for excessive capitalization
  - Ensures minimum message length
  - Verifies brand overlay on generated images
- **`verify_brand_overlay(image_path, brand_reference_path)`**: Brand overlay verification (placeholder implementation)

#### Compliance Checks:

- **Content Filtering**: Inappropriate language detection
- **Quality Standards**: Message length and formatting validation
- **Brand Consistency**: Brand overlay verification on images

---

### 4. Country & Language Service (`backend/app/services/country_language.py`)

#### `CountryInfo`

- **Purpose**: Comprehensive country information with language mappings
- **Fields**: `name`, `code`, `primary_language`, `languages`, `region`

#### Key Functions:

- **`get_country_by_code(country_code)`**: Get country info by ISO code
- **`get_country_by_name(country_name)`**: Get country info by name
- **`get_legacy_region_mapping(region)`**: Convert legacy region names to country codes
- **`get_primary_language(country_code)`**: Get primary language for country
- **`get_supported_languages(country_code)`**: Get all supported languages
- **`get_countries_by_region(region)`**: Get countries in specific region
- **`get_all_countries()`**: Get complete country list
- **`search_countries(query)`**: Search countries by name/code/language
- **`get_country_selector_data()`**: Formatted data for frontend selector

#### Coverage:

- **200+ Countries**: Complete global coverage with ISO codes
- **Language Mapping**: Primary and secondary language support
- **Regional Grouping**: Geographic region categorization
- **Legacy Support**: Backward compatibility for region names

---

### 5. Embeddings Service (`backend/app/services/embeddings.py`)

#### Key Functions:

- **`embed_and_store(campaign_id, text, metadata)`**: Store campaign embeddings
  - Creates rich text combining message, country, audience, and products
  - Generates embeddings using SentenceTransformer
  - Stores in ChromaDB with metadata
- **`search_similar(query, top_k)`**: Semantic search for similar campaigns
  - Converts query to vector embedding
  - Performs cosine similarity search
  - Returns similar campaigns with distances and metadata

#### Technology Stack:

- **ChromaDB**: Vector database for embeddings storage
- **SentenceTransformer**: `all-MiniLM-L6-v2` model for embeddings
- **Cosine Distance**: Similarity scoring (0-2 range, 0 = identical)

---

### 6. Generator Service (`backend/app/services/generator.py`)

#### Core Generation Functions:

- **`generate_creatives(prompt, ...)`**: Main creative generation function
  - Generates base image using AI models
  - Creates multiple aspect ratio variants
  - Adds brand overlay and localization
- **`generate_single_image(prompt, ...)`**: Generate single base image
- **`create_size_variants(base_image_path, ...)`**: Create aspect ratio variants
- **`add_brand_overlay(image_path, ...)`**: Add brand overlay and localized text

#### AI Model Integration:

- **Primary**: Hugging Face Stable Diffusion XL
- **Fallback**: OpenAI DALL-E 3
- **Parameters**: Noise scheduler, UNet backbone, VAE, guidance scale, inference steps

#### Localization Features:

- **`translate_message_with_llm(message, country_name, audience)`**: LLM-based translation
- **`localize_prompt(prompt, country_name)`**: Cultural prompt localization
- **RTL Support**: Right-to-left language support
- **Font Selection**: International font support for different scripts

#### Text Overlay Features:

- **`wrap_text(text, font, max_width)`**: Smart text wrapping
- **`add_brand_overlay(image_path, ...)`**: Brand logo and text overlay
- **Responsive Design**: Adaptive font sizes and positioning
- **Multi-language Support**: CJK, Arabic/Hebrew, Cyrillic, Latin scripts

---

### 7. Logging Database Service (`backend/app/services/logging_db.py`)

#### Key Functions:

- **`init_db()`**: Initialize DuckDB tables and schema
- **`close_db()`**: Close database connections
- **`log_campaign(campaign_id, brief, outputs, compliance)`**: Log campaign data
- **`get_connection()`**: Get database connection with pooling

#### Database Schema:

- **Table**: `campaigns`
- **Fields**: `campaign_id`, `created_at`, `products`, `country_name`, `audience`, `message`, `output_square`, `output_landscape`, `output_portrait`, `compliance_status`, `compliance_issues`
- **Migration**: Automatic schema migration from legacy `region` to `country_name`

---

### 8. View Database Service (`backend/app/services/view_db.py`)

#### `CampaignViewer` Class:

Context manager for database viewing and analytics operations.

#### Basic Queries:

- **`get_recent_campaigns(limit)`**: Recent campaigns with full details
- **`get_database_stats()`**: Database schema and statistics

#### Geographic Analysis:

- **`get_campaigns_by_region()`**: Campaign distribution by region
- **`get_campaigns_by_country(country_code, limit)`**: Country-specific campaigns
- **`get_regional_performance(min_campaigns)`**: Regional performance metrics

#### Audience Analysis:

- **`get_campaigns_by_audience()`**: Campaign distribution by audience
- **`get_campaigns_by_audience_type(audience_pattern, limit)`**: Pattern-based audience search
- **`get_audience_performance(min_campaigns)`**: Audience performance metrics

#### Compliance & Quality:

- **`get_compliance_status()`**: Compliance status distribution with percentages
- **`get_campaigns_with_issues()`**: Campaigns with compliance problems

#### Time-based Analysis:

- **`get_todays_campaigns()`**: Today's campaign activity
- **`get_campaigns_by_hour()`**: Hourly activity patterns
- **`get_campaigns_by_date_range(start_date, end_date)`**: Date range queries

#### Product Analysis:

- **`get_product_analysis(limit)`**: Most popular products
- **`get_campaigns_by_product_type(product_pattern, limit)`**: Product-specific campaigns

#### Advanced Analytics:

- **`get_campaign_metrics()`**: Comprehensive campaign metrics
- **`search_campaigns(country, audience, product, compliance_status, limit)`**: Multi-filter search

#### Convenience Functions:

- **`get_recent_campaigns(limit)`**: Direct access to recent campaigns
- **`get_campaign_metrics()`**: Direct access to metrics
- **`search_campaigns(**kwargs)`\*\*: Direct search functionality

---

## Data Flow

### Campaign Generation Flow:

1. **Input Validation**: `CampaignBrief` model validation
2. **Directory Creation**: Campaign-specific directory structure
3. **Embedding Storage**: Vector storage for semantic search
4. **Image Generation**: AI model-based creative generation
5. **Localization**: Translation and cultural adaptation
6. **Brand Overlay**: Logo and text overlay application
7. **Compliance Check**: Content and quality validation
8. **Database Logging**: Campaign data persistence
9. **Response Generation**: Structured response with metadata

### Search Flow:

1. **Query Processing**: Natural language query input
2. **Vector Conversion**: Query to embedding conversion
3. **Similarity Search**: ChromaDB vector search
4. **Result Enrichment**: Full campaign data retrieval
5. **Score Calculation**: Similarity scoring and ranking

---

## Technology Stack

### Backend:

- **FastAPI**: Web framework with automatic API documentation
- **Pydantic**: Data validation and serialization
- **DuckDB**: Analytics database for campaign logging
- **ChromaDB**: Vector database for semantic search
- **SentenceTransformer**: Embedding generation

### AI/ML:

- **Hugging Face**: Primary image generation (Stable Diffusion XL)
- **OpenAI**: Fallback image generation (DALL-E 3) and translation (GPT-4)
- **PIL/Pillow**: Image processing and manipulation

### Frontend:

- **Jinja2**: Template rendering
- **Static Files**: CSS, JavaScript, and image assets

### Infrastructure:

- **Docker**: Containerization
- **Volume Mounting**: Persistent data storage
- **CORS**: Cross-origin resource sharing

---

## Error Handling

### API Level:

- **HTTP Exceptions**: Proper status codes and error messages
- **Validation Errors**: Pydantic model validation
- **Service Failures**: Graceful degradation and fallbacks

### Service Level:

- **Model Fallbacks**: Hugging Face → OpenAI fallback chain
- **Database Errors**: Connection pooling and error recovery
- **File System**: Directory creation and cleanup on failures

### Compliance:

- **Content Filtering**: Automatic content validation
- **Quality Checks**: Message length and formatting validation
- **Brand Consistency**: Overlay verification (placeholder)

---

This documentation provides a complete overview of the Creative Automation Pipeline's API endpoints and service functions, enabling developers to understand and integrate with the system effectively.
