

## Pivoting from CI/CD to Kubernetes with k3d

Lately, I’ve been deep in the world of GitHub Actions and CI/CD pipelines—automating releases, building images, and wiring up deployments. But every now and then, you need to remind yourself why the container orchestration layer exists in the first place. Enter **k3d**, a lightweight wrapper around Rancher’s minimal Kubernetes distribution, k3s. In this post, I’ll walk through setting up k3d locally, reflect on why it matters, and outline how I’m using it for both development and future CI/CD tests.

---

### What Is k3d?

At its core, k3d spins up full Kubernetes clusters inside Docker containers. You get the real deal—API server, controllers, CoreDNS, and all—without the resource overhead of a VM-based cluster.

> _Reflection:_ I love that k3d blurs the line between “works on my machine” and “works in production.” It’s the closest you can get to a real cluster while still coding on your laptop.

---

### Installing k3d

I install k3d through [mise](https://mise.jdx.dev/about.html), my go-to tool for managing local dev utilities. Of course, you could also grab binaries or use Homebrew—refer to the [official docs](https://k3d.io/stable/#releases) for alternatives.

```shell
# Install k3d in one command
mise use k3d
```

> _Reflection:_ When I first started, I manually downloaded every binary and set PATHs. Mise simplifies that—and it’s one less obstacle between me and a fresh cluster.

---

### Creating a Tiny Cluster

With k3d in place, spinning up a single-node cluster is as simple as:

```shell
k3d cluster create
```

You’ll see output like this:

```
INFO[0000] Prep: Network                                
INFO[0000] Created network 'k3d-mycluster'
...
INFO[0037] Cluster 'mycluster' created successfully!    
INFO[0037] You can now use it like this:
kubectl cluster-info
```

> Watching those log lines scroll by reminds me how much Kubernetes “plumbing” k3d manages behind the scenes—network setup, image volumes, load-balancer, CoreDNS tweaks. It’s magic I don’t take for granted.

---

### Interacting with Your k3d Cluster

You’ll need `kubectl` to talk to k3d’s API. I again lean on mise:

```shell
mise use kubectl
```

Then, verify the system pods:

```shell
kubectl get pods -A
```

```
NAMESPACE     NAME                                      READY   STATUS      RESTARTS   AGE
kube-system   coredns-ccb96694c-2zwc9                   1/1     Running     0          8m11s
kube-system   local-path-provisioner-5cf85fd84d-s8zbb   1/1     Running     0          8m11s
kube-system   metrics-server-5985cbc9d7-rjcnt           1/1     Running     0          8m11s
...
```

> Seeing those pods transition to “Running” in seconds always gives me a little thrill. It’s a stark contrast to the fifteen-minute VM spin-up I’m used to in cloud labs.

---

### Running Inside a Devcontainer

Full disclosure: my entire dev environment—including Docker daemon and this k3d cluster—lives inside a VS Code Devcontainer using Docker-in-Docker. This meta-container approach means:

1. **Isolation**: My host remains pristine.
    
2. **Reproducibility**: Anyone can clone the repo, launch the same container, and get an identical k3d environment.
    
3. **CI/CD Parity**: The same Devcontainer config can power local and pipeline tests.
    

> Initially, juggling Docker-in-Docker felt risky, but the payoff in consistency has been huge. No more “it works locally” excuses when builds break on CI.

---

### Why k3d for CI/CD?

- **Speed**: Clusters spin up in seconds versus minutes.
    
- **Resource Efficiency**: Tiny memory and CPU footprint.
    
- **Parity**: Tests run against a real API server rather than mocks.
    

My next step is to wire these k3d clusters into GitHub Actions jobs—deploying manifests, running integration tests, and tearing them down automatically. But that story belongs to another post.

---

By embracing k3d, I’ve gained a nimble playground for Kubernetes experimentation that scales into my CI/CD pipelines. It’s a reminder that sometimes the best innovation comes from simplifying the tools we already know.

---