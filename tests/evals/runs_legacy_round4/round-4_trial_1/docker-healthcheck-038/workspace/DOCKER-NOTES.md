# Docker & Application Notes

## Architecture & Design

- **Service (`service/app.py`)**: A lightweight Python 3 HTTP service built entirely on standard library modules (`http.server`, `os`, `json`). It respects environment variables:
  - `PORT`: TCP port to listen on (defaults to `8080`).
  - `APP_TOKEN`: Secret token used by the application logic (e.g. endpoint displays token status/prefix).
  - `/healthz`: Endpoint returning `{"status": "ok"}` with status code `200` for health probes.
  - `/`: Root endpoint returning greeting message including token verification.

- **Multi-stage Dockerfile**:
  - **Builder Stage (`python:3.12-slim`)**: Prepares dependencies and sets up a virtual environment in `/opt/venv` using `requirements.txt`.
  - **Runtime Stage (`python:3.12-slim`)**: Lean final image containing only the runtime environment, copied virtual environment, and application code.
  - **Security (Non-Root User)**: Creates and switches to a dedicated unprivileged user (`appuser`, UID/GID 1000) to adhere to container security best practices.
  - **Layer Caching**: Orders `COPY requirements.txt .` and `RUN` instructions before copying source code to maximize build cache efficiency.
  - **Healthcheck & CMD**: Includes a native container `HEALTHCHECK` probe querying `/healthz` and uses `CMD ["python", "app.py"]` with virtualenv python path `/opt/venv/bin/python`.

- **Docker Compose (`compose.yaml`)**:
  - Exposes port `8080:8080`.
  - Passes environment variable `APP_TOKEN=demo-token-123`.
  - Configures robust container healthchecks (`interval`, `timeout`, `retries`).

- **Smoke Tests (`smoke.sh`)**:
  - Boots the service locally in the background, exercises `/healthz` and `/` endpoints, asserts expected response patterns, and cleans up.
