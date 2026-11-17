PROJECTS · DOCKER AND CI

# Docker and GitHub Actions for both starters

Both starters now have a `Dockerfile`, a `.dockerignore` and `.github/workflows/tests.yml`. Copy a starter folder into its own GitHub repository and every push runs the tests and builds the image: a green tick on your commits is something recruiters notice.

## Dockerfile, line by line (backend starter)

|                                                    |                                                                                                                    |
|----------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| `FROM python:3.12-slim`                            | Start from a small official Python image.                                                                          |
| `ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1` | No .pyc files; logs appear immediately.                                                                            |
| `WORKDIR /app`                                     | All later paths are relative to /app.                                                                              |
| `COPY requirements.txt . / RUN pip install …`      | Install dependencies first, so Docker can reuse this layer when only your code changes.                            |
| `COPY app ./app`                                   | Then copy the code (the .dockerignore keeps .venv, caches and databases out).                                      |
| `RUN useradd … / USER appuser`                     | Run as a non-root user: a bug in the app cannot act as root inside the container.                                  |
| `VOLUME ["/data"] and DB_PATH`                     | Keep the SQLite file outside the image so it survives restarts.                                                    |
| `EXPOSE 8000 / CMD ["uvicorn", …]`                 | Document the port and start the server; secrets such as JWT_SECRET come from -e at run time, never from the image. |
| `HEALTHCHECK …`                                    | Docker marks the container unhealthy if /health stops answering.                                                   |

## Workflow, step by step

|                                                                |                                                            |
|----------------------------------------------------------------|------------------------------------------------------------|
| `on: push, pull_request`                                       | Run on every push and every pull request.                  |
| `runs-on: ubuntu-latest`                                       | A fresh Linux machine from GitHub for each job.            |
| `actions/checkout@v4`                                          | Get your code.                                             |
| `actions/setup-python@v5 (python-version 3.12, cache: pip)`    | Install Python and cache downloaded packages between runs. |
| `pip install / pytest -q (or the unittest and suite commands)` | Install and test; a failing test turns the commit red.     |
| `docker job, needs: test`                                      | Only after tests pass, check that the image still builds.  |

## Commands

``` bash
docker build -t study-tracker generated/backend-starter
docker run -p 8000:8000 -e JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))") -v study-data:/data study-tracker
docker build -t secrag generated/ai-security-starter && docker run --rm secrag
```

**Checked.** Both images were built and run with Docker 29: the backend's 10 tests pass inside the image, the API answers /health and refuses to start without a strong JWT_SECRET; secrag's tests pass and its suite reports 12/12 baseline and 0/12 defended. Both run as a non-root user. Workflow files were parsed and checked as YAML; they have not yet run on GitHub.
