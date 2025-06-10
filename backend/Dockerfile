FROM python:3.10-slim

WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir fastapi uvicorn requests beautifulsoup4 vaderSentiment

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
