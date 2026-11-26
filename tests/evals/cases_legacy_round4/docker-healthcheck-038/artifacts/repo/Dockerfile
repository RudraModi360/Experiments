FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN python -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
FROM python:3.12-slim AS runtime
RUN groupadd --gid 1000 appgroup && useradd --uid 1000 --gid appgroup appuser
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY service/app.py .
ENV PORT=8080
ENV APP_TOKEN=
USER appuser
EXPOSE 8080
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/healthz')" || exit 1
CMD ["python","app.py"]
