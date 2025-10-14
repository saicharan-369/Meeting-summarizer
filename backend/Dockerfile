FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy backend files
COPY backend/ ./backend/
COPY backend/requirements.txt ./backend/requirements.txt

ENV PYTHONUNBUFFERED=1

# Install Python deps
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r backend/requirements.txt

WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Use environment variables for secrets (DO NOT bake keys into image)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
