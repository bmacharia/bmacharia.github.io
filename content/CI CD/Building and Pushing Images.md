

## Building and Pushing Docker Images from Your CI/CD Pipeline

Automating container image builds and registry pushes isn’t just about offloading repetitive work—it’s about ensuring consistency, traceability, and quick feedback when you ship features. Here’s how I structured my GitHub Actions workflow to build and push Docker images whenever I tag a new backend release, along with some lessons learned along the way.



### 1. Isolate the Feature Branch

As with any new CI/CD addition, I kicked things off on a dedicated branch:

```bash
git switch -c feat/add-docker-image-pushing
```

> **Reflection:**  
> Keeping CI changes isolated prevented accidental breaks in my main pipeline. It also let me iterate quickly on the YAML without worrying about blocking other merges.

---

### 2. Define the Workflow File

I created a new file at `.github/workflows/docker-build-push.yaml` to house my build-and-push logic:

```yaml
name: Build and Push Docker Images

on:
  push:
    # Trigger only when tags prefixed with "backend" are pushed
    tags:
      - "backend*"

env:
  REGISTRY: ghcr.io
  BACKEND_IMAGE_NAME: ${{ github.repository_owner }}/study-app-api

jobs:
  build-and-push-backend:
    name: Build and Push Backend
    runs-on: ubuntu-latest
    # Only run this job for backend tags
    if: contains(github.ref, 'backend')
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Log in to the registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract tag name
        id: tag
        run: |
          echo "TAG=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT

      - name: Build & push Backend image
        uses: docker/build-push-action@v5
        with:
          context: ./src/backend
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.BACKEND_IMAGE_NAME }}:${{ steps.tag.outputs.TAG }}
            ${{ env.REGISTRY }}/${{ env.BACKEND_IMAGE_NAME }}:latest

    outputs:
      tag: ${{ steps.tag.outputs.TAG }}
      app: backend
```

---

### 3. Understanding the Trigger

- **Event**: `push` ➔ `tags: ["backend*"]`
    
- **Logic**: Whenever I push a tag like `backend-v1.2.3`, the workflow fires.
    

> **Reflection:**  
> Using tag-based triggers means I explicitly control when an image build happens. No surprise builds on every commit—only on purposeful release events.

---

### 4. Environment Variables & Permissions

```yaml
env:
  REGISTRY: ghcr.io
  BACKEND_IMAGE_NAME: ${{ github.repository_owner }}/study-app-api
```

- **`REGISTRY`** points to GitHub Container Registry.
    
- **`BACKEND_IMAGE_NAME`** constructs the image path based on repo ownership.
    

```yaml
permissions:
  contents: read
  packages: write
```

- **`contents: read`** allows checkout.
    
- **`packages: write`** lets us push images to the registry.
    

> **Reflection:**  
> Explicitly scoping permissions keeps the pipeline principle of least privilege intact. I don’t want more access than I need.

---

### 5. Checkout, Login, and Tag Extraction

1. **Checkout**
    
    ```yaml
    uses: actions/checkout@v4
    ```
    
2. **Login to Registry**
    
    ```yaml
    uses: docker/login-action@v3
    with:
      registry: ${{ env.REGISTRY }}
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}
    ```
    
3. **Extract Tag Name**
    
    ```yaml
    run: echo "TAG=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT
    ```
    

> **Reflection:**  
> That shell expansion to strip `refs/tags/` felt a bit arcane at first—but once I tested it locally, it reliably surfaced the tag I needed for image tagging.

---

### 6. Building and Pushing the Image

```yaml
uses: docker/build-push-action@v5
with:
  context: ./src/backend
  push: true
  tags: |
    ${{ env.REGISTRY }}/${{ env.BACKEND_IMAGE_NAME }}:${{ steps.tag.outputs.TAG }}
    ${{ env.REGISTRY }}/${{ env.BACKEND_IMAGE_NAME }}:latest
```

- **Context**: Builds from the `src/backend` directory.
    
- **Tags**:
    
    - Version-specific tag (`:${{ steps.tag.outputs.TAG }}`)
        
    - Mutable `:latest` tag for quick tests.
        

> **Reflection:**  
> Pushing both a versioned and `latest` tag strikes a balance: reproducible builds when you need them, and a moving target for development or staging environments.

---

### 7. Capturing Outputs

At the end of the job, I expose:

```yaml
outputs:
  tag: ${{ steps.tag.outputs.TAG }}
  app: backend
```

This makes it easy to wire downstream jobs (e.g., deployment) to pick up exactly which version landed in the registry.

> **Reflection:**  
> Passing outputs between jobs transforms a monolithic workflow into modular building blocks. Next up: triggering a deployment job only when this build succeeds.

---

## Concluding Thoughts

By codifying the build-and-push process in GitHub Actions, I’ve eliminated manual Docker commands and ensured that every release tag automatically yields a fresh, versioned container image. Beyond the convenience, this approach guarantees that the same CI environment produces every build—no more “works on my machine” surprises.

With this foundation in place, I can focus on the next step: deploying those images in a controlled rollout. But that, as they say, is a story for another post.

---