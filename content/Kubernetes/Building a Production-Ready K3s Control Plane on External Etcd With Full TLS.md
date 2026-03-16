---
title: Building a Production-Ready K3s Control Plane on External Etcd With Full TLS
tags: [kubernetes, k3s, etcd, tls, homelab]
description: A complete guide to setting up K3s with an external etcd cluster and mutual TLS authentication.
publish: true
---

## **Building a Production-Ready K3s Control Plane on External Etcd With Full TLS**

This artifact documents the complete process I followed to design, build, secure, and troubleshoot a highly available **external etcd cluster** and integrate it with a **K3s Kubernetes control plane**, using:

- Mutual TLS authentication
- Static IP addressing
- Explicit PKI lifecycle management
- Etcd cluster health validation
- K3s server bootstrapping via external datastore
- Disaster recovery–aligned configuration
- Real troubleshooting of degraded raft nodes and certificate failures

This mirrors the real-world operational skills expected from DevOps, SRE, and Platform Engineering roles.

---

## **1. Architecture Summary**

### **Nodes**

| Node    | Role                       | IP         |
| ------- | -------------------------- | ---------- |
| node-01 | etcd-1                     | 172.16.0.2 |
| node-02 | etcd-2                     | 172.16.0.3 |
| node-03 | etcd-3                     | 172.16.0.4 |
| node-04 | K3s server (control plane) | 172.16.0.5 |

### **Topology**

```
+------------------+        +------------------+
|     etcd-1       |<------>|     etcd-2       |
| 172.16.0.2:2380  |<------>| 172.16.0.3:2380  |
+--------^---------+        +---------^--------+
         |                           |
         |                           |
         v                           v
                  +------------------+
                  |     etcd-3       |
                  | 172.16.0.4:2380  |
                  +--------^---------+
                           |
                           |
                           v
                 +------------------+
                 |   K3s Server     |
                 | 172.16.0.5       |
                 | External Etcd     |
                 +------------------+
```

The control plane depends on external etcd via:

```
etcd://172.16.0.2:2379,172.16.0.3:2379,172.16.0.4:2379
```

---

## **2. Skills Demonstrated**

### ✔ **Distributed Systems**

- Built a 3-node etcd cluster with full Raft consensus.
- Validated cluster health, election behavior, and endpoint availability.

### ✔ **PKI + Mutual TLS Authentication**

- Generated:

  - Cluster CA
  - Per-node private keys
  - Per-node signed certificates with correct SAN entries

- Investigated and resolved TLS failures due to incorrect IP SANs.

### ✔ **Linux Systems Engineering**

- Managed systemd units for etcd and k3s.
- Corrected file ownership and secure permissions (`600`, `644`).
- Used journald logs for deep debugging.

### ✔ **K3s Control Plane Bootstrapping**

- Integrated external etcd into K3s using `config.yaml`.
- Corrected datastore URI formats (`etcd://`).
- Ensured k3s-server successfully registered itself as a Kubernetes node.

### ✔ **Troubleshooting & Root Cause Analysis**

- Diagnosed “tls: bad certificate” errors.
- Compared CSR SAN values against real host IPs.
- Re-issued and redeployed certificates.
- Validated fix by checking Raft health and Kubernetes readiness.

### ✔ **Real DevOps Discipline**

- Iterated systematically:

  1. Observe failure
  2. Interpret logs
  3. Form hypothesis
  4. Validate
  5. Apply fix
  6. Re-run tests

Exactly how production outages are handled.

---

## **3. What I Built (Step-by-Step Summary)**

### **3.1. Created PKI Infrastructure**

Generated a CA, node CSRs, and signed certificates:

```bash
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key -subj "/CN=etcd-ca" -days 3650 -out ca.crt
```

Each etcd node received its own unique cert + key with SAN entries matching:

```
DNS:etcd-X
IP:172.16.0.X
```

### **3.2. Deployed TLS-Secured Etcd Cluster**

Each node received:

```
/etc/etcd/tls/ca.crt
/etc/etcd/tls/etcd-N.crt
/etc/etcd/tls/etcd-N.key
```

Correct permissions enforced:

```
600  private keys
644  public certs
```

### **3.3. Brought up the cluster & validated health**

```bash
etcdctl --endpoints="https://172.16.0.2:2379,https://172.16.0.3:2379" \
  --cacert=/etc/etcd/tls/ca.crt \
  --cert=/etc/etcd/tls/etcd-1.crt \
  --key=/etc/etcd/tls/etcd-1.key \
  endpoint health -w table
```

Final expected output:

```
| https://172.16.0.2:2379 | true |
| https://172.16.0.3:2379 | true |
| https://172.16.0.4:2379 | true |
```

### **3.4. Integrated K3s with External Etcd**

Created `/etc/rancher/k3s/config.yaml`:

```yaml
datastore-endpoint: "etcd://172.16.0.2:2379,172.16.0.3:2379,172.16.0.4:2379"
etcd-cafile: "/etc/rancher/k3s/ca.crt"
etcd-certfile: "/etc/rancher/k3s/etcd-1.crt"
etcd-keyfile: "/etc/rancher/k3s/etcd-1.key"
```

Installed K3s:

```bash
curl -sfL https://get.k3s.io | sudo sh -s - server
```

### **3.5. Validated Kubernetes Control Plane**

```bash
sudo k3s kubectl get nodes
```

Result:

```
NAME      STATUS   ROLES                  AGE   VERSION
node-04   Ready    control-plane,master   57s   v1.33.6+k3s1
```

---

## **4. Root Cause Analysis (Major Learning)**

During the build, I intentionally kept logs, mistakes, and resolutions.
One real production-grade issue occurred:

### ❌ **etcd peers rejected connections: `tls: bad certificate`**

### **Cause**

A certificate SAN contained the wrong IP:

```
IP Address:176.16.0.3   # incorrect
```

### **Fix**

- Regenerated CSR
- Reissued certificate
- Deployed correct cert bundle
- Restarted etcd
- Revalidated health

### **Lesson**

\*\*99% of etcd TLS failures are caused by incorrect SAN values.
Always verify SANs before signing certificates.
