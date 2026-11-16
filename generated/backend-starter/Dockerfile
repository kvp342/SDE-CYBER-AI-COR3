# Study tracker API image. Build: docker build -t study-tracker .
# Run:   docker run -p 8000:8000 -e JWT_SECRET=$(python3 -c "import secrets;print(secrets.token_hex(32))") study-tracker
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DB_PATH=/data/study.db
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY tests ./tests
# Run as an unprivileged user; the database lives in a writable volume.
RUN useradd --create-home appuser && mkdir /data && chown appuser /data
USER appuser
VOLUME ["/data"]
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
