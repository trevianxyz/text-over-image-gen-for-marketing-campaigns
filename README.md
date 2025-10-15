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
docker run -d -p 8000:80 --name adobe-fastapi-container adobe-fastapi-app
```

API Endpoint: http://localhost:8080/
Interactive Docs: http://localhost:8080/docs
OpenAPI Spec: http://localhost:8080/openapi.json

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
