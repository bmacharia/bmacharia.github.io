

---

# ✅ **Artifact #1 (Markdown File) — K3s + External Etcd Prerequisites Checklist**

**Here is the fully self-contained Markdown file** — copy/paste this as-is:

---

````markdown
# K3s + External Etcd — Prerequisites Checklist

This checklist ensures your external etcd cluster and K3s node are ready for installation.

---

## 1. Verify External Etcd Cluster Health

```bash
export ETCDCTL_API=3

etcdctl --endpoints="https://172.16.0.2:2379,https://172.16.0.3:2379" \
  --cacert=/etc/etcd/tls/ca.crt \
  --cert=/etc/etcd/tls/etcd-1.crt \
  --key=/etc/etcd/tls/etcd-1.key \
  endpoint health -w table
````

Expected Output:

|ENDPOINT|HEALTH|
|---|---|
|[https://172.16.0.2](https://172.16.0.2/)|true|
|[https://172.16.0.3](https://172.16.0.3/)|true|

---

## 2. Verify Node-04 Can Reach Etcd Endpoints

```bash
curl -k https://172.16.0.2:2379/health
curl -k https://172.16.0.3:2379/health
```

---

## 3. Ensure TLS Files Exist on Etcd Nodes

Required files:

```
/etc/etcd/tls/ca.crt
/etc/etcd/tls/etcd-1.crt
/etc/etcd/tls/etcd-1.key
/etc/etcd/tls/etcd-2.crt
/etc/etcd/tls/etcd-2.key
/etc/etcd/tls/etcd-3.crt
/etc/etcd/tls/etcd-3.key
```

---

## 4. Copy TLS Certificates to the K3s Server Node (node-04)

Create directory:

```bash
sudo mkdir -p /etc/rancher/k3s/etcd/
```

Copy from node-01:

```bash
scp /etc/etcd/tls/ca.crt node-04:/etc/rancher/k3s/etcd/

scp /etc/etcd/tls/etcd-1.crt node-04:/etc/rancher/k3s/etcd/client.crt
scp /etc/etcd/tls/etcd-1.key node-04:/etc/rancher/k3s/etcd/client.key
```

Fix permissions:

```bash
sudo chown root:root /etc/rancher/k3s/etcd/*
sudo chmod 600 /etc/rancher/k3s/etcd/client.key
```

---

## 5. Ensure Required Ports Are Open (or Disable Firewall)

Ports used by K3s:

|Port|Purpose|
|---|---|
|6443/tcp|Kubernetes API|
|9345/tcp|K3s Supervisor|
|10250|Kubelet|
|2379|Etcd Client API|
|2380|Etcd Peer API|

Recommended for homelab:

```bash
sudo ufw disable
```

---

## 6. Validate Node Resources (Node-04)

Suggested:

- 2+ vCPUs
    
- 4GB RAM minimum
    
- 20GB disk
    

Check quickly:

```bash
htop
df -h
```

---

**If all checks are green, proceed to Artifact #2 — K3s Server Install Command.**

```

---

When you're ready, say:  
### **“Next artifact”**  
and I’ll send:

# **Artifact #2 — K3s Server Install Command (fully customized)**
```