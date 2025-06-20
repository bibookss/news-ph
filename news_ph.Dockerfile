FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /opt/dagster

COPY ./news_ph/pyproject.toml ./news_ph/

RUN uv pip install --system ./news_ph

COPY ./news_ph ./news_ph
COPY ./abs_cbn_dbt ./abs_cbn_dbt

ENV DAGSTER_HOME=/opt/dagster
ENV PYTHONPATH=/opt/dagster

EXPOSE 4000

CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-m", "news_ph"]
