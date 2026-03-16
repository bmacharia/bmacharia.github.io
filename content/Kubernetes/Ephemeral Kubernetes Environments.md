---
title: Ephemeral Kubernetes Environments
tags: [kubernetes, k3d, devops, testing]
description: How to spin up disposable Kubernetes clusters with k3d for development and testing workflows.
publish: true
---

As a DevOps engineer, nothing gives me more satisfaction than smoothing out the path for developers. My mantra is simple: if I can make it effortless for someone to spin up a dev environment and start coding, we’ve already won half the battle.

## Spinning Up a Cluster in Seconds

Not long ago, I discovered **k3d**, a wrapper around [k3s](https://k3s.io/) that lets you create disposable Kubernetes clusters inside Docker containers—ideal for local development and rapid testing. In fact, every time I demo k3d, I like to remind folks how magical it feels:

```bash
k3d cluster create
```

With that one line, you get a single-node cluster…no YAML editing, no cloud accounts, no waiting. It hums to life, ready to accept workloads, and when you’re done you can tear it down just as quickly.

## Declarative Deployments: Let Kubernetes Do the Heavy Lifting

I’m a stickler for declarative infrastructure—tell Kubernetes _what_ you want, and let it handle the _how_. Every application I deploy starts life as a set of manifest files:

- **Deployment** specs to define pods, replicas, and container images
    
- **Service** specs to expose those pods inside (or outside) the cluster
    

This approach frees me from brittle scripts and manual steps. I simply commit my desired state, and Kubernetes’s control loop drives the cluster toward that state.

## A Real-World Example: My DevOps-Study-App

For illustration, lets's use **devops-study-app**, an example service that tracks weekly study hours toward DevOps mastery. While the app’s internals aren’t our focus here, the workflow is:

1. **Local Testing:** Spin up k3d, apply manifests, poke around in the browser
    
2. **Iterate Quickly:** Tweak code and manifests, re-apply, watch rolling updates
    
3. **Promote to Production:** Push tags and let our GitOps pipeline do the rest
    

This cycle keeps me in the zone, writing code and refining my deployment, without ever wrestling with environment drift or manual CI/CD hacks.

## Embracing GitOps with Flux

That “push-and-pray” approach to deployments belongs in the past. Enter **GitOps**—a model where your Git repository is the single source of truth for both code and infrastructure. All you need to do to roll out changes is update your repo; an automated controller takes care of applying them.

> **GitOps**  
> Versioned CI/CD on declarative infrastructure—stop scripting and start shipping.  
> — [Kelsey Hightower](https://twitter.com/kelseyhightower/status/953638870888849408)

I use [Flux](https://fluxcd.io/) to implement this. Flux continuously watches one or more Git repositories (and even OCI registries or S3 buckets), then reconciles your cluster’s state to match what’s declared. No more “It worked on my machine”—if it’s in Git, Flux makes it real.

### Behind the Scenes: Reconciliation

Flux defines several reconciliation primitives, but the one I lean on is **Kustomization**:

- **HelmRelease** reconciliation for Helm charts
    
- **Bucket** reconciliation for artifact snapshots
    
- **Kustomization** reconciliation for plain-YAML deployments
    

Whenever Flux polls your repo, it compares the _observed_ state in the cluster with the _desired_ state in Git. If they differ—say you bumped an image tag in `kustomization.yaml`—Flux applies the change automatically, giving you a push-button rollout.

## Project Layout: Keeping Things Organized

Here’s what my directory structure looks like:

```bash
.
├── k3d-config.yaml           # Custom cluster settings
├── manifests/
│   ├── base/
│   │   ├── backend/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── kustomization.yaml
│   │   ├── frontend/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── kustomization.yaml
│   │   └── kustomization.yaml
│   └── dev/
│       ├── backend/
│       │   └── kustomization.yaml
│       ├── frontend/
│       │   └── kustomization.yaml
│       ├── kustomization.yaml
│       └── namespace.yaml
├── setup_cluster_local       # Helper scripts for k3d
└── setup_cluster_minimal     # Minimal-cluster setup
```

Each `kustomization.yaml` wires together logical layers: a **base** that describes core workloads, and an **overlay** (like `dev/`) that injects environment-specific tweaks—namespaces, replica counts, feature flags, you name it.

---

That’s the heart of my local-to-production journey: **k3d** for instant clusters, **YAML manifests** for declarative workloads, and **Flux** for hands-free, Git-driven deployments. It’s a workflow that keeps my focus where it belongs—building features and delighting developers—rather than babysitting infrastructure.

Peace, happy hacking, and may your clusters always reconcile. 🙌

[[Introduction to K3D]]
