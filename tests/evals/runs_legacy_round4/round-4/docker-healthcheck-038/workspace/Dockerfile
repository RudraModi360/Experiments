FROM python:3.12-slim AS builder

WORKDIR /app

# Upgrade pip and install any optional requirements (if any)
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    if [ -s requirements.txt ]; then /opt/venv/bin/pip install --no-cache-dir -r requirements.txt; fi

FROM python:3.12-slim AS runtime

# Create non-root system user and group for security hardening
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --create-home appuser

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
COPY service/app.py .

# Environment defaults
ENV PATH="/opt/venv/bin:$PATH"
ENV PORT=8080
ENV APP_TOKEN=demo-token-123
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=3s --retries=3 --start-period=2s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/healthz')" || exit 1

CMD ["python", "app.py"]
