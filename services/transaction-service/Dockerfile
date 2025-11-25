FROM python:3.11-slim

WORKDIR /app

COPY docker-requirements.txt .
RUN pip install --no-cache-dir -r docker-requirements.txt

# Copy app code
COPY ./app ./app

# Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003", "--lifespan", "on"]
