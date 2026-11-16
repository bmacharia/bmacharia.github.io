---
title: Babu Macharia for DevOps Engineer Roles
publish: true
description: "Babu Macharia for DevOps Engineer roles: Terraform, Kubernetes, GitOps with Flux, and CI/CD with security gates, with the projects that prove each one. Remote U.S. or hybrid in the San Francisco Bay Area."
---

**Hiring a DevOps Engineer?** This page maps what the role usually asks for to the work I've done, with a link to each piece of evidence.

| | |
|---|---|
| **Role** | DevOps Engineer |
| **Location** | Tracy, California (San Francisco Bay Area) |
| **Work arrangement** | Remote anywhere in the U.S., or hybrid in the Bay Area |
| **Availability** | Open to new roles now |

## What the role asks for, and where I've done it

| The job asks for | What I've done | Evidence |
|---|---|---|
| **Infrastructure as code** | Built a multi-tenant AKS platform with Terraform modules, where onboarding a customer is a 1-line change to `customers.tf` | [[HomeLab/Case Study - Multi-Tenant AKS Platform\|AKS case study]] |
| **CI/CD pipelines** | GitHub Actions pipeline with 23 backend tests at 98.55% coverage, end-to-end tests in ephemeral k3d clusters, and automated releases | [CI/CD repo](https://github.com/bmacharia/devops-study-app) |
| **Security in the pipeline** | Trivy image scanning gate; HIGH/CRITICAL findings cut from 20 to zero. Restricted Pod Security Standards and Cilium network policies per tenant | [CI/CD repo](https://github.com/bmacharia/devops-study-app) · [[HomeLab/Case Study - Multi-Tenant AKS Platform\|AKS case study]] |
| **Kubernetes and GitOps** | Flux CD reconciling an AKS platform and a 3-node Raspberry Pi K3s cluster from Git; secrets encrypted with SOPS and Age | [pi-cluster repo](https://github.com/bmacharia/pi-cluster) |
| **Monitoring and incident response** | Prometheus and Grafana with Telegram alerts; 4 real incidents diagnosed and written up as postmortems | [pi-cluster repo](https://github.com/bmacharia/pi-cluster) |
| **Backups and recovery** | Daily PostgreSQL backups to Azure Blob Storage, and a restore tested end to end in a DR lab | [DR lab write-up](https://github.com/bmacharia/kubernetes-platform-engineering/blob/main/mercury-workflows-sanitized/phase-6-cnpg/DR-LAB.md) |
| **Documented decisions** | Each major choice recorded with the alternatives and the tradeoffs accepted | [[decisions\|Decision records]] |

## Background

U.S. Navy veteran (avionics electronics technician), then 10+ years in regulated healthcare diagnostics operations at Genomic Health / Exact Sciences, where following procedures exactly and documenting every deviation was the job. I bring that same habit to infrastructure: runbooks, postmortems, and changes made through Git.

**Core stack:** Kubernetes (AKS, k3s, k3d) · Terraform · FluxCD · GitHub Actions · AWS · Azure · Docker · Prometheus / Grafana · Python · Bash

## Next step

- **Email:** [babu.macharia@protonmail.com](mailto:babu.macharia@protonmail.com) (résumé available on request)
- **LinkedIn:** [linkedin.com/in/babu-macharia](https://www.linkedin.com/in/babu-macharia/)
- **Quick facts for recruiters:** [[recruiters|the 60-second version]]
- **Referring me?** [[refer|Here's a blurb you can paste]]
