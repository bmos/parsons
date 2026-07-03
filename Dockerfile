FROM --platform=linux/amd64 python:3.11@sha256:4fe91343677d630977800b2b1b391c4e27109d3247c9f9eda09a60ba4791dc84

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1

###################
## Parsons setup ##
###################

WORKDIR /src
COPY pyproject.toml setup.py ./
RUN uv sync --no-editable --all-extras --no-dev --python python3.11

COPY . /src/

ENV PATH="/src/.venv/bin:$PATH"
ENV PYTHONPATH=.:/app

# The /app directory can house the scripts that will actually execute on this Docker image.
# Eg. If using this image in a Civis container script,
# Civis will install your script repo (from Github) to /app.
RUN mkdir /app
WORKDIR /app

CMD ["python3"]
