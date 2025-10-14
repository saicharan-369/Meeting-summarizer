# Deployment Guide

This guide shows simple ways to run the Meeting Summarizer publicly using Docker and common PaaS providers.

Prerequisites
- Docker and docker-compose installed locally (for building images)
- An OpenAI API key

Local with Docker Compose
1. Export your OpenAI key to environment (Linux/macOS):

   export OPENAI_API_KEY=sk-...

   Windows (PowerShell):

   $env:OPENAI_API_KEY = 'sk-...'

2. Build and run:

   docker-compose up --build -d

3. Access:
   - Backend: http://<host-ip>:8000/health
   - Streamlit: http://<host-ip>:8501/

Deploy to Render / Railway / Heroku
- Render and Railway accept Dockerfiles or simple Git repos. Recommended steps:
  1. Push repository to GitHub.
  2. Create a new service on the provider and point it at the GitHub repo.
  3. Set the `OPENAI_API_KEY` environment variable in the provider's dashboard.
  4. If deploying the backend only, use the backend/Dockerfile or point run command to `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`.

Security notes
- Never commit your `.env` file to source control. Rotate your API key if it was ever pushed.

Scaling
- For production, consider:
  - Running the backend behind a proper web server or container orchestrator (Kubernetes).
  - Using HTTPS (managed by the provider or with a reverse proxy like Traefik).
