---
title: Projects
publish: true
---

## Kubernetes Platform Engineering on Azure
Production-grade multi-tenant Kubernetes platform built across 10 progressive phases — from VM provisioning to automated customer onboarding.

**Result:** onboarding a new customer is a 1-line Terraform change that provisions an isolated namespace, PostgreSQL database, TLS-secured ingress, daily backups to Azure Blob Storage, network policies, and alerts.

**Tech:** Azure AKS, FluxCD, Terraform, CloudNativePG, Cilium, Prometheus, Entra ID, Pod Security Standards

[View on GitHub →](https://github.com/bmacharia/kubernetes-platform-engineering)

---

## HomeLab Kubernetes Cluster (pi-cluster)
3-node K3s cluster on Raspberry Pi with full GitOps operations, observability stack, and 4 real incident postmortems.

**Result:** 4 real incidents diagnosed and written up:
- [Flux reconciliation failure: missing sops-age secret and stuck terminating namespaces](https://github.com/bmacharia/pi-cluster/blob/main/postmortem-flux-sops-stuck-namespaces-2026-05-12.md)
- [MetalLB VIP unreachable: Wi-Fi promiscuous mode](https://github.com/bmacharia/pi-cluster/blob/main/postmortem-metallb-vip-wifi-promisc-2026-05-13.md)
- [Grafana CrashLoopBackOff: duplicate default datasource](https://github.com/bmacharia/pi-cluster/blob/main/postmortem-grafana-loki-datasource-conflict-2026-05-26.md)
- [uptime-kuma VIP unreachable](https://github.com/bmacharia/pi-cluster/blob/main/postmortem-uptime-kuma-vip-2026-04-30.md)

**Tech:** K3s, FluxCD, SOPS+Age, MetalLB, Traefik, Longhorn, Prometheus/Grafana, Renovate

**Read more:** [[Building a Production-Ready K3s Control Plane on External Etcd With Full TLS]] · [[Level-Triggered vs Edge-Triggered: What Electrical Engineering Can Teach Us About Kubernetes]]

[View on GitHub →](https://github.com/bmacharia/pi-cluster)

---

## CI/CD Pipeline Automation
End-to-end CI/CD pipeline with GitHub Actions, security scanning, automated releases, and zero-downtime deployment patterns.

**Result:** 23 backend tests at 98.55% coverage, end-to-end tests in ephemeral k3d clusters on every release, and Trivy HIGH/CRITICAL image findings cut from 20 to zero.

**Tech:** GitHub Actions, Ruff, PyTest, Trivy, Release Please, DevContainers, K3d

**Read more:** [[Ephemeral Kubernetes Environments]] · [[End to End Testing to Pipeline]] · [[Scanning Container Images with Trivy]] · [[Implement Automatic Releases]]

[View on GitHub →](https://github.com/bmacharia/devops-study-app)
