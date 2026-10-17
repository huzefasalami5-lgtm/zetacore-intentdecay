# ==============================================================================
# Dockerfile: ZetaCore IntentDecay Sidecar & Operations Dashboard
# Multi-Arch Support: linux/s390x (IBM LinuxONE) & linux/amd64
# Base Image: Red Hat UBI (Universal Base Image) or Debian Slim
# ==============================================================================
FROM python:3.11-slim

# Prevent interactive prompts & bufferless output
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install minimal OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose ports:
# 8000: FastAPI Sidecar REST API (Microservice)
# 8501: Streamlit Operations Dashboard (Web UI)
EXPOSE 8000 8501

# Healthcheck for IBM LinuxONE OpenShift / Podman
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/v1/health || exit 1

# Default command: launch both the Sidecar REST API and Streamlit UI
CMD ["sh", "-c", "python -m uvicorn api:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]
