FROM --platform=linux/amd64 python:3.11@sha256:5062f6c22a2c3b8b3717c642af3852310d9a81c3c2c0fc72449a9a79ef09ae63

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

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
