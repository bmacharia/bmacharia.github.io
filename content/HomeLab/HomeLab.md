# My Kubernetes Homelab Journey

In this blog, I’ll document my journey setting up a Kubernetes home lab. This reflective exploration balances technical detail with insights gained along the way, structured into clear, manageable sections.

---

## Choosing a Kubernetes Distribution

When embarking on my Kubernetes home lab, I faced numerous choices. Kubernetes itself is simply a collection of binaries running on Linux, but distributions bundle and optimize components differently, impacting installation, management, and ease of use.

### Popular Distribution Options:

- **Kubeadm**: Common in certification contexts (e.g., CKA), providing excellent learning depth but demanding substantial manual management (certificates, CNI, updates).
- **MicroK8S**: Canonical’s user-friendly distribution, easy to install but somewhat opinionated with limited configuration flexibility.
- **Talos Linux**: Secure, immutable OS with no SSH access, entirely API-driven, appealing to advanced users.

### Why I Chose K3s

K3s hit the sweet spot between ease and flexibility:

- Single binary installation suitable for existing Linux setups
- Lightweight (great for Raspberry Pi)
- Flexible networking plugins
- Rancher-backed, useful in enterprise environments
- Excellent for exploring OS-level troubleshooting

Future explorations will involve more advanced distributions, like Talos Linux, using GitOps principles to ease migration.

---

## Installing and Configuring K3s on Raspberry Pi

### System Preparation

Before K3s installation, I prepared the Raspberry Pi:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install vim -y
```

I then enabled necessary cgroup parameters:

```bash
sudo vim /boot/firmware/cmdline.txt
```

Appending:

```
cgroup_memory=1 cgroup_enable=memory
```

Rebooted and verified:

```bash
sudo reboot
cat /proc/cmdline
```

### K3s Installation

Ran the simple installation script:

```bash
sudo su -
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable=helm-controller" sh
sudo systemctl status k3s.service
```

### Remote Access

Copied K3s config to local for easier management:

```bash
cd
sudo cp /etc/rancher/k3s/k3s.yaml .
scp <username>@<Raspberry_Pi_IP>:/home/<username>/k3s.yaml .
```

Configured `kubectl` locally:

```bash
vim k3s.yaml
mkdir -p ~/.kube
mv k3s.yaml ~/.kube/config
```

### Verifying Installation

Checked nodes and pods to verify the cluster:

```bash
kubectl get nodes
kubectl get pods --all-namespaces
```

---

## GitOps with Flux

Implementing GitOps means using Git as a single source of truth for infrastructure, easing migration and cluster management.

### Key GitOps Principles

- Declarative system descriptions
- Version-controlled system state
- Automated change application
- Continuous state reconciliation

### Choosing Flux

Flux is ideal due to its:

- Simpler CLI-centric workflow
- Seamless integration with Kubernetes and Kustomize
- Easy adoption for personal labs

I set up Flux with the following bootstrap command:

```bash
flux bootstrap github \
  --owner=$GITHUB_USER \
  --repository=pi-cluster \
  --branch=main \
  --path=./clusters/staging \
  --personal
```

---

## Deploying Applications: Linkding Example

Using GitOps, I deployed Linkding (bookmark manager) declaratively:

Defined Kubernetes manifests (`namespace.yaml`, `deployment.yaml`) and a Kustomization for Flux auto-deployment.

Deployment verification:

```bash
kubectl get pods -n linkding
kubectl port-forward pod/linkding 8080:9090 -n linkding
```

### Security Enhancements

I further enhanced security:

- Added Security Context (`runAsUser`, `fsGroup`)
- Set non-root execution (`www-data`, UID 33)
- Disabled privilege escalation

---

## Secure Exposure with Cloudflare Tunnel

Cloudflare Tunnels securely expose services without direct public internet exposure.

Steps:

- Generated tunnel credentials securely using `cloudflared`
- Deployed Cloudflare Tunnel as Kubernetes manifests (Deployment, ConfigMap, Secret)
- Managed secrets securely using SOPS encryption

---

## Secrets Management with SOPS

Secure secret handling in public repositories is crucial. I leveraged SOPS and `age` encryption:

```bash
kubectl create secret generic test-secret \
--from-literal=user=admin --from-literal=password=mischa \
--dry-run=client -o yaml > test-secret.yaml

sops --age=$AGE_PUBLIC --encrypt --encrypted-regex '^(data|stringData)$' --in-place test-secret.yaml
```

---

## Monitoring with Kube-Prometheus-Stack

Flux automated deployment of monitoring stack (`kube-prometheus-stack`) using HelmRelease objects:

- Grafana dashboard accessed via port-forwarding

---

## Automating Dependency Updates: Renovate

Configured Renovate in Kubernetes as a CronJob for automated dependency updates:

- Used encrypted secrets and ConfigMaps for secure, declarative management
- Scheduled CronJobs hourly to create PRs for dependencies updates

---

## Audiobookshelf Deployment

Deployed Audiobookshelf with persistent storage and secure access via Cloudflare Tunnel:

- ConfigMaps and persistent volumes (PVCs)
- High availability through replicated Cloudflared deployments

---

## Reflections

My Kubernetes home lab has been an enriching journey. It deepened my understanding of Kubernetes distributions, GitOps, security practices, and cloud-native tools like Flux, SOPS, Cloudflare, and Renovate. The iterative process reinforced the importance of automation, declarative configurations, and security in modern DevOps workflows.

Looking ahead, I'll continue exploring advanced distributions like Talos Linux and refining my GitOps approach to achieve greater flexibility and robustness.
