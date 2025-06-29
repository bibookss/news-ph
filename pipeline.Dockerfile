FROM python:3.12-slim-bookworm

# Install curl and CA certificates
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Set path for uv
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /opt/dagster

# Copy pyproject first (for caching during build)
COPY ./news_ph/pyproject.toml ./news_ph/

# Install dependencies
RUN uv pip install --system ./news_ph

# Copy source code
COPY ./news_ph ./news_ph
COPY ./abs_cbn_dbt ./abs_cbn_dbt

# Dagster environment variables
ENV DAGSTER_HOME=/opt/dagster/dagster_home
ENV PYTHONPATH=/opt/dagster/dagster_home

# Expose GRPC port
EXPOSE 4000

# Start GRPC server
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-m", "news_ph"]
