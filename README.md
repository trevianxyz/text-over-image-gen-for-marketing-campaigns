# uv-fastapi-example

An example of a [FastAPI](https://github.com/fastapi/fastapi) application managed as a
[uv](https://github.com/astral-sh/uv) project.

Based on the [multi-file example](https://fastapi.tiangolo.com/tutorial/bigger-applications/) from
the FastAPI documentation.

## License

MIT

<div align="center">
  <a target="_blank" href="https://astral.sh" style="background:none">
    <img src="https://raw.githubusercontent.com/astral-sh/uv/main/assets/svg/Astral.svg" alt="Made by Astral">
  </a>
</div>

```bash
docker build -t adobe-fastapi-app .
```

```bash
# Run with volume mounts for persistent asset storage
docker run -d -p 8080:80 --name adobe-fastapi-container \
  -v "$(pwd)/assets:/app/assets" \
  $([ -f .env ] && echo "-v $(pwd)/.env:/app/.env" || echo "") \
  adobe-fastapi-app
```

confirm with curl

```bash
curl http://localhost:8080/
# Response:
# {"status":"ok","message":"Creative Automation Pipeline is running","endpoints":["/campaigns/generate"]}
```

API Endpoint: http://localhost:8080/
Interactive Docs: http://localhost:8080/docs
OpenAPI Spec: http://localhost:8080/openapi.json

## 📁 Asset Storage Locations

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
- **Container**: `/app/db/chroma/`
- Stores campaign embeddings for similarity search

**Note**: The volume mount ensures generated images persist on your host machine and survive container restarts.

### troubleshooting

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
