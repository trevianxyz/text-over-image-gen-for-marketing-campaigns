# Frontend - Creative Automation Pipeline

Web interface for the Creative Automation Pipeline.

## Structure

```
frontend/
├── templates/          # Jinja2 HTML templates
│   ├── base.html      # Base template with navbar and footer
│   └── index.html     # Main campaign generation form
└── static/            # Static assets
    ├── css/
    │   └── style.css  # Application styles
    └── js/
        └── main.js    # Form handling and API interaction
```

## Features

- **Campaign Form**: Input form for products, region, audience, and message
- **Real-time Generation**: Shows loading state during image generation
- **Results Display**: Grid layout showing all three aspect ratios (1:1, 16:9, 9:16)
- **Error Handling**: User-friendly error messages
- **Responsive Design**: Mobile-friendly layout

## Technology Stack

- **Templating**: Jinja2 (served by FastAPI)
- **Styling**: Vanilla CSS with CSS Grid and Flexbox
- **JavaScript**: Vanilla JS (no framework dependencies)
- **API Communication**: Fetch API

## API Integration

The frontend communicates with these endpoints:

- `POST /campaigns/generate` - Generate campaign creatives
- `GET /api/health` - Health check endpoint
- `GET /api/docs` - API documentation (Swagger UI)

## Development

Templates are automatically served by FastAPI. Any changes require rebuilding the Docker container:

```bash
docker build -t adobe-fastapi-app .
docker run -d -p 8080:80 --name adobe-fastapi-container \
  -v "$(pwd)/assets:/app/assets" \
  -v "$(pwd)/db:/app/db" \
  adobe-fastapi-app
```

Access at: **http://localhost:8080/**

## Customization

### Styling
Edit `static/css/style.css` to customize:
- Color scheme (CSS variables in `:root`)
- Layout and spacing
- Component styles

### Behavior
Edit `static/js/main.js` to customize:
- Form validation
- API request handling
- Results display logic

### Templates
Edit templates to modify:
- `base.html` - Navigation, footer, overall layout
- `index.html` - Form fields and results display

