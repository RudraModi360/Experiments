# Docker Notes & Container Architecture

## Overview
This repository contains a lightweight Python HTTP service (`service/app.py`) built using Python's standard library (`http.server`). It is containerized using a production-ready, secure, multi-stage Dockerfile and orchestrated via Docker Compose (`compose.yaml`).

---

## Architecture & Multi-Stage Build

The `Dockerfile` employs a **multi-stage build** strategy:
1. **Builder Stage (`python:3.12-slim`)**:
   - Installs build essentials and Python dependencies (if any listed in `requirements.txt`) into an isolated virtual environment (`/opt/venv`).
   - Keeps build artifacts separate from the final deployment footprint.
2. **Runtime Stage (`python:3.12-slim`)**:
   - Copies over only the clean virtual environment (`/opt/venv`) and application source code (`service/app.py`).
   - Eliminates unnecessary compiler toolchains, reducing image size and potential attack surface.

---

## Security Hardening
- **Non-Root User**: Creates a dedicated system user and group (`appuser:appgroup`, UID/GID 1000) so that the application does not run with root privileges.
- **Minimal Base Image**: Uses Debian-slim Python images to minimize installed packages and known CVE vulnerabilities.
- **No Cache**: Leverages `--no-cache-dir` during pip installation to keep image layers lean.

---

## Environment Variables
- `PORT`: The HTTP server listening port (default: `8080`).
- `APP_TOKEN`: Authentication / configuration token for the service (default: `demo-token-123`).
- `PYTHONUNBUFFERED`: Ensures stdout and stderr streams are flushed immediately without buffering.

---

## Healthchecks & Reliability
- **Docker HEALTHCHECK & Compose Healthcheck**:
  - Periodically executes an HTTP request (`http://localhost:8080/healthz`) using Python's `urllib.request`.
  - Configured with `interval: 10s`, `timeout: 3s`, `retries: 3`, and `start-period: 2s`.
- **Restart Policy**: `restart: unless-stopped` ensures high availability under normal operations.

---

## Usage & Commands

### Running Smoke Tests Locally
```bash
bash smoke.sh
```

### Building the Docker Image Manually
```bash
docker build -t python-http-service:latest .
```

### Running with Docker Compose
```bash
docker compose up --build
```
