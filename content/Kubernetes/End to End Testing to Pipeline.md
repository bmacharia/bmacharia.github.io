---
title: End-to-End Testing in a CI/CD Pipeline
tags: [kubernetes, testing, ci-cd, k3d]
description: Adding end-to-end Kubernetes tests to a CI/CD pipeline using k3d and Python.
publish: true
---

### End to End Testing with k3d and Python

In a previous post [[Ephemeral Kubernetes Environments]] I explained a method for creating ephemeral Kubernetes Environments. Now it is time to see what kind of cool stuff we can do with our clusters.

Lets say we want to do some end to end testing. For example, say we want to define a bunch of test cases, when an application is running in Kubernetes. An example of that is to `curl`  a health end point to see if a container is actually running and not having any problems.

For this scenario I already have End to End setup, what I want to do is add End to End testing to a CI/CD pipeline. There are many ways to accomplish this. I can create a template and call it from a different workflow, or can just add it to an existing testing pipeline.  Those are just some options.


What I am going to do is utilize a template and call end to end testing from a different workflow. The question is how am I going to trigger this

```bash

 tree
.
├── backend-tests.yaml
├── docker-build-push.yaml
└── release-please.yaml

1 directory, 3 file
```

I already have some tests setup, and those tests are path based triggered. Meaning when there are changes within a certain directory, that alone triggers the workflow.  What U can do is trigger end to end testing whenever there is a change or update to backend of frontend code.

 The way to this is to create a `trigger` in the `backend-tests.yaml`, and what this basically is, is a new job.

Here is how it looks like. 

```yaml
# in order for this to run, it needs the job test to return successful
# Then it calls the workflow ./.github/workflows/e2e-tests.yaml
  trigger_e2e:
    name: Trigger E2E Tests
    needs: test
    if: success()
    uses: ./.github/workflows/e2e-tests.yaml
```

The idea is the run end to end testing in the pipeline when the testing of the code passes all tests and when test coverage is above a certain threshold. If they do not pass, then there is no reason to run end to end testing. So end to end testing is dependent on test before it being run with all test successful.

Oh yeah the workflow for end to end testing looks like below.
The trigger is on `workflow_call`

```yaml

name: End-to-End Tests

# This workflow is triggered by other workflows, not directly from PRs
on:
  workflow_call:

jobs:
  e2e_test:
    name: End-to-End Tests
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./kubernetes

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install K3d
        uses: nolar/setup-k3d-k3s@v1
        with:
          version: "latest"
          skip-creation: true

      - name: Install kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: "latest"

      - name: Install UV
        uses: astral-sh/setup-uv@v5

      - name: Set up Python
        run: uv python install

      - name: Run E2E tests
        run: |
          uv run python e2e_test.py

```

Thanks and that is all Peace!