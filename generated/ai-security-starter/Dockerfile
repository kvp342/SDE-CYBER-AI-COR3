# secrag image. Build: docker build -t secrag .
# Offline suites:  docker run --rm secrag                       (attack suite with the stub model)
#                  docker run --rm secrag python3 -m unittest discover -s tests -v
# With Claude:     docker run --rm -e ANTHROPIC_API_KEY secrag python3 attacks/run_attacks.py --llm anthropic
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd --create-home appuser
USER appuser
CMD ["python3", "attacks/run_attacks.py"]
