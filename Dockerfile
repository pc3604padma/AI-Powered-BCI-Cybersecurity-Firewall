FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables for faster builds
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false \
    STREAMLIT_LOGGER_LEVEL=warning \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy ONLY requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with optimized flags
RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create .streamlit directory and config
RUN mkdir -p .streamlit && \
    echo "[runner]\nmagicEnabled = true\nfastReruns = true\n\n[cache]\nmaxEntries = 1000" > .streamlit/config.toml

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0", "--logger.level", "warning", "--client.showErrorDetails", "false"]
