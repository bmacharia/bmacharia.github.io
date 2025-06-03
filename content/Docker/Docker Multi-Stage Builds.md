In a previous post I wrote Scanning Container Images with [Trivy](https://trivy.dev/latest/), I went through the process of reducing the size of my container image, just by changing the container base image.  My current `Dockerfile` is below

```Dockerfile

FROM python:3.13-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . /app

RUN uv sync --locked --no-editable

CMD ["uv", "run", "study-tracker-api"]
```

A quick look at my current `Dockerfile` one can see that I am just copying everything into the directory. For further optimization, I will be implementing Multi-Stage builds and a cache mount, to make the container image as small as possible


## Multi-stage Builds 

From the official Docker documentation on [Multi-stage-Builds](https://docs.docker.com/build/building/multi-stage/) 

With multi-stage builds, you use multiple `FROM` statements in your Dockerfile. Each `FROM` instruction can use a different base, and each of them begins a new stage of the build. You can selectively copy artifacts from one stage to another, leaving behind everything you don't want in the final image. Below is a Dockerfile with multiple `FROM` statements which means it has two separate stages, one for building a binary, and the other stage is for where the binary gets copied from the first state into the next stage.

Below is my new Dockerfile with each line explained

```Dockerfile

# Stage 1: Builder the first stage of the build process
# Use the official Python 3.13 image based on Alpine Linux as the base.
# Alpine is chosen for its small size.
# Name this stage "builder" for later reference.
FROM python:3.13-alpine AS builder

  

# Copy the 'uv' and 'uvx' executables (Python package installer/resolver)
# from a specific public image into the /bin/ directory of the builder stage.
# This makes 'uv' available for installing dependencies.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

  

# Set the working directory within the builder stage to /app.
# All subsequent commands (RUN, COPY, etc.) will be executed from this directory.
WORKDIR /app

  

# Install project dependencies. This layer is cached to speed up subsequent builds
# if dependencies haven't changed.
# --mount=type=cache,target=/root/.cache/uv: Mounts a Docker build cache for uv.
# This persists the uv cache across builds, speeding up dependency resolution/downloads.
# --mount=type=bind,source=uv.lock,target=uv.lock: Mounts the uv.lock file from the
# build context (your project directory) into the container at /app/uv.lock.
# This file specifies exact versions of all dependencies.
# --mount=type=bind,source=pyproject.toml,target=pyproject.toml: Mounts the pyproject.toml
# file from the build context into the container at /app/pyproject.toml.
# This file defines project metadata and direct dependencies.
# uv sync --locked --no-install-project --no-editable: Uses uv to install dependencies.
# --locked: Ensures only versions from uv.lock are installed.
# --no-install-project: Installs only the dependencies listed in pyproject.toml,
# not the project itself at this stage. This helps in caching dependencies separately.
# --no-editable: Installs packages normally, not in editable mode.

RUN --mount=type=cache,target=/root/.cache/uv \
--mount=type=bind,source=uv.lock,target=uv.lock \
--mount=type=bind,source=pyproject.toml,target=pyproject.toml \
uv sync --locked --no-install-project --no-editable

  

# Copy all files and directories from the current directory (build context,
# which is src/backend/ when building this Dockerfile) into the /app directory
# inside the builder stage. This includes your application's source code.
COPY . /app

  

# Install the project itself along with its dependencies into the virtual environment.
# This uses the previously cached dependencies if possible.
# --mount=type=cache,target=/root/.cache/uv: Uses the same uv cache.
# uv sync --locked --no-editable: Installs the project (defined in pyproject.toml)
# and its dependencies. Since --no-install-project is omitted, the project itself is installed.
RUN --mount=type=cache,target=/root/.cache/uv \
uv sync --locked --no-editable

  

# Stage 2: Final image
# Start a new, clean stage using the same python:3.13-alpine base image.
# This helps create a smaller final image by not including build tools or
# intermediate files from the "builder" stage unless explicitly copied.
FROM python:3.13-alpine

  

# Copy the Python virtual environment (created by uv and containing all dependencies
# and the installed project) from the "builder" stage to the /app/.venv directory
# in the final image.
# --from=builder: Specifies that the source of the copy is the "builder" stage.
# --chown=app:app: Sets the owner and group of the copied files to "app".
# This is a security best practice to run the application as a non-root user.
# It assumes an "app" user and group exist or will be created in the base image
# or through other Dockerfile instructions (though not explicitly created here).
COPY --from=builder --chown=app:app /app/.venv /app/.venv

  

# Set the default command to run when a container is started from this image.
# It executes the 'study-tracker-api' script, which is an entry point
# defined in your project's pyproject.toml ([`src/backend/pyproject.toml`](src/backend/pyproject.toml)).
# This script, located in the virtual environment's bin directory,
# will start the FastAPI application (defined in [`src/backend/src/backend/main.py`](src/backend/src/backend/main.py)).

CMD ["/app/.venv/bin/study-tracker-api"]
```


Now with my new Dockerfile, I will build the image and of course I would like my docker image to be as small as possible

```shell
 docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
backend      03        e2905e16ea5c   4 seconds ago   56.5MB
backend      02        a381a5f768d1   3 hours ago     114MB
backend      01        ae9b526becd0   3 hours ago     189MB
backend      00        e48cc776d20c   4 hours ago     1.09GB

```

As one can see that my new docker image went form 114MB from a previous build down to 56MB. What this shows is that my new Docker image only contains what I need to run the application.


That is all for now

Peace!





