---
title: Securing a Docker Image
tags: [docker, security, containers]
description: How to run Docker containers as a non-root user to limit privilege escalation risk.
publish: true
---

The reason why I want a secure Docker image is because Docker runs all of its containers under the `root` user domain because it requires access to resources like network configuration, process management, and the filesystem.  What this means is that the processes running inside the containers also run as `root`. This elevated privilege is a huge security risk especially in production. Running an application as root inside of a container gives the application access that it should not have.

To fix this issue I have changed the user to a non-root user, so as the user running inside the container has access to only what is needed to run the application

```Dockerfile
FROM python:3.13-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies in a cache layer. This speeds up build time
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --locked --no-install-project --no-editable

# Copy the project into the intermediate image
COPY . /app

# Sync the project and install it, now that we have access to the source code
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked --no-editable

FROM python:3.13-alpine

# Create a non-root user and group with specific IDs
RUN addgroup -S -g 1000 app && adduser -S -u 1000 -G app app

# Copy the environment, but not the source code
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# Switch to the non-root user
USER app

# Expose the correct port
EXPOSE 22112

# Run the application
CMD ["/app/.venv/bin/study-tracker-api"]
```