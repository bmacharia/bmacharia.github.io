---
title: Decision Records
publish: true
description: "Architecture decision records for Babu Macharia's Kubernetes platform projects: what was chosen, the alternatives, and the tradeoffs accepted."
---

Short records of significant technical decisions. 002 was my own call; 001, 003, and 004 come from the KubeCraft program's reference design, which I implemented and operated. Each covers the context, what was chosen, what it was chosen over, and what it costs. Each links to the project it shaped.

| # | Decision | Project |
|---|---|---|
| 001 | [CloudNativePG instead of managed Azure PostgreSQL](#001-cloudnativepg-instead-of-managed-azure-postgresql) | [[Case Study - Multi-Tenant AKS Platform\|AKS platform]] |
| 002 | [Flux CD instead of Argo CD](#002-flux-cd-instead-of-argo-cd) | [[Case Study - Multi-Tenant AKS Platform\|AKS platform]] |
| 003 | [Traefik instead of NGINX Ingress](#003-traefik-instead-of-nginx-ingress) | [[Case Study - Multi-Tenant AKS Platform\|AKS platform]] |
| 004 | [Terraform generates the GitOps manifests](#004-terraform-generates-the-gitops-manifests) | [[Case Study - Multi-Tenant AKS Platform\|AKS platform]] |

---

## 001: CloudNativePG instead of managed Azure PostgreSQL

**Context:** every customer needs a dedicated PostgreSQL database with high availability, continuous backups, and point-in-time recovery.

**Decision:** run PostgreSQL in the cluster with the CloudNativePG (CNPG) operator, backing up to Azure Blob Storage with Barman.

**Alternatives:** Azure Database for PostgreSQL (managed), one per customer or shared.

**Why:** lower cost per tenant, the same setup runs on any Kubernetes cluster, and the operator handles failover and WAL archiving natively, declared in Git alongside everything else.

**Consequences:** we own database operations: operator upgrades, backup verification, and recovery. That is why recovery was [tested in a DR lab](https://github.com/bmacharia/kubernetes-platform-engineering/blob/main/mercury-workflows-sanitized/phase-6-cnpg/DR-LAB.md) rather than assumed.

## 002: Flux CD instead of Argo CD

**Context:** the cluster must be reconciled continuously from Git, with infrastructure applied before configuration, and configuration before applications.

**Decision:** Flux CD, installed through the AKS Flux extension.

**Alternatives:** Argo CD.

**Why (my call):** Flux keeps me on the CLI, where I already work. Its pull-based model needs no inbound access to the cluster, the AKS extension simplifies bootstrap, and Kustomization `dependsOn` chains map cleanly to the infra → config → apps layering.

**Consequences:** no built-in web UI; reconciliation status comes from the `flux` CLI and Grafana. That isn't a lock-in: Flux and Argo CD can run side by side, so the platform team keeps Flux while developers who prefer a UI use Argo CD. A wrong `GitRepository` URL fails quietly until you look, which is [one of the incidents I debugged](https://github.com/bmacharia/kubernetes-platform-engineering/blob/main/mercury-workflows-sanitized/phase-5-gitops/mercury-gitops/infrastructure/controllers/base/TROUBLESHOOTING.md).

## 003: Traefik instead of NGINX Ingress

**Context:** new customer hostnames are added continuously, each needing automatic HTTPS.

**Decision:** Traefik as the ingress controller, with cert-manager issuing Let's Encrypt certificates.

**Alternatives:** NGINX Ingress Controller.

**Why:** dynamic configuration discovery and straightforward Let's Encrypt integration reduce work in a multi-tenant setup where ingress rules change often.

**Consequences:** a smaller ecosystem than NGINX, and Helm naming defaults matter: the release generated an IngressClass called `traefik-traefik`, so certificates were never served until the class name was set explicitly. [Write-up](https://github.com/bmacharia/kubernetes-platform-engineering/blob/main/mercury-workflows-sanitized/phase-5-gitops/mercury-gitops/TROUBLESHOOTING-certificates.md).

## 004: Terraform generates the GitOps manifests

**Context:** each customer needs a matching set of Azure resources and Kubernetes manifests, and they must never drift apart.

**Decision:** Terraform's `local_file` resource writes each customer's manifests during `terraform apply`; Flux picks them up from Git.

**Alternatives:** hand-written per-customer YAML; a templating tool such as Helm or Kustomize overlays per tenant; a small onboarding CLI.

**Why:** one command and one list (`customers.tf`) drive both the cloud resources and the cluster state, so onboarding is a 1-line change.

**Consequences:** Terraform state and Git content are coupled; a bad apply can write bad manifests, and Terraform now has a job beyond infrastructure. A Python onboarding CLI is the planned v2: not every developer knows Terraform, and it would leave Terraform managing infrastructure only.
