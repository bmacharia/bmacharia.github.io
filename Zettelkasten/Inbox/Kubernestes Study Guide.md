
Here’s a quick and structured “cheat sheet” summarizing the provided Kubernetes material. This is designed for rapid review and exam prep, with essential definitions, key properties, and high-yield facts you’ll need for a fundamental understanding before digging further.

---

## Kubernetes Control Plane Components

- **ETCD**: Persistent key-value data store; the only Control Plane component that stores state. Holds all cluster data (like pod manifests). Controllers watch ETCD for changes and take action .
    
- **Scheduler**: Assigns newly created pods (with “pending” status) to nodes, selecting the most suitable node based on resource criteria .
    
- **Controller Manager**: Runs controller loops. Each controller watches the state from ETCD and reconciles it to the desired state (e.g., ensuring correct pod counts, handling deployments, etc.) .
    

## Kubernetes Service

- Provides a stable, cluster-internal endpoint (ClusterIP by default) to access pods, “decoupling” pod lifecycles from connectivity .
    

## Deployments, ReplicaSets, and Pods

|Object|Description|Managed/Created By|
|---|---|---|
|Deployment|Declarative manager for ReplicaSets. Handles rolling updates, scaling, versioning.|User, kubectl|
|ReplicaSet|Ensures a specified number of identical pods are running.|Deployment, directly|
|Pod|One or more containers running on a single node. Not a process, but an execution environment (cannot move nodes, not horizontally scalable itself).|ReplicaSet|

## Lifecycle Example

- `deployment.apps/pingpong` ⇒ creates
    
- `replicaset.apps/pingpong` ⇒ creates
    
- `pod/pingpong-xxxxxxx`
    

## Pod Details

- Runs on a single node.
    
- Cannot be restarted, only replaced.
    
- Phases: Succeeded (all containers exit successfully), Failed (container crashes and not restarted).
    
- Scaling and replacement handled by ReplicaSet/Deployment.
    
- Pod cannot straddle nodes or be moved between nodes .
    

## Replica Set

- Manages a set of pods from a template.
    
- Adds/removes pods to match desired replica count.
    
- Scaling up/down alters pod count .
    

## Deployment

- Used for rolling updates and declarative version control.
    
- On update, creates a new ReplicaSet, scales it up while scaling down the old one (rolling update).
    
- Maintains ReplicaSet count .
    

## Exposing Containers

- Use `kubectl expose deployment ...` to create a service exposing pods via a stable ClusterIP.
    
- ClusterIP: Internal, not externally reachable.
    
- For a public/external endpoint, use Service Type: LoadBalancer. This provisions an external IP .
    

## kubectl logs

- By default, shows logs from a single pod.
    
- Use `kubectl logs -l app=<label>` to view logs from all matching pods.
    
- Streaming logs has a concurrency limit (default: 5 log streams; can increase with `--max-log-requests`) .
    
- Shortcomings: log lines are not labeled by pod, restarts/interrupted log streams if pods replaced, does not include new pods automatically .
    

## Namespaces

- Used to logically organize Kubernetes resources (“folder” for cluster).
    
- Created via `kubectl create namespace` or YAML definition.
    

## YAML as Source of Truth

- For advanced features (multi-container pods, resource limits, healthchecks, DaemonSets, etc.), defining resources in YAML is essential for version control and auditability.
    

## Kubernetes Network Model

- Flat, routable network: any pod/node can reach any other without NAT.
    
- Pods have L3 IP connectivity, independent of hosting node.
    
- Services expose endpoints using L4 (TCP/UDP) .
    
- Security implemented with Network Policies (require CNI support).
    
- kube-proxy handles service traffic, but is not highly performant.
    
- NodePorts and LoadBalancers expose services externally .
    

## Labels and Selectors

- Deployments automatically assign `app=<name>` labels.
    
- Selectors in Services/ReplicaSets/DaemonSets match pod labels for association.
    
- Multiple labels in selector: logical AND (not OR).
    

## Rolling Deployments

- Kubernetes replaces old ReplicaSets/pods with new ones gradually during updates (rolling update), ensuring availability.
    
- Controlled by `maxSurge` (extra pods allowed during update) and `maxUnavailable` (allowed unavailable pods).
    
- Allows rollback to previous version if needed .
    

## Healthchecks

|Probe Type|Purpose|Behavior|
|---|---|---|
|Liveness Probe|Detects deadlocked or unrecoverable containers|Fails => K8s restarts container (should solve by restart only)|
|Readiness Probe|Detects whether container can accept traffic|Not ready => removed from service endpoint|
|Startup Probe|Initial boot check for slow-starting images|Delays liveness/readiness probe activation|

- Probes can be configured with type (`exec`, `httpGet`, `tcpSocket`, `grpc`) and have parameters for intervals, timeouts, thresholds .
    
- Best practice: always use readiness probes; add liveness probes with caution; use startup probe only for slow-starting apps.
    

## Key Kubernetes Commands

- `kubectl apply -f file.yaml`: apply resource definitions from file.
    
- `kubectl get <resource>`: list resources.
    
- `kubectl logs <pod>`: get logs for a pod.
    
- `kubectl logs -l app=<label>`: get logs for all pods matching label.
    

---

## High-Yield Practice Questions

1. What is the only persistent/storing Control Plane component in Kubernetes?
    
2. What is the main difference between a ReplicaSet and a Deployment?
    
3. What happens if you update a Deployment’s Pod template?
    
4. Explain the difference between `livenessProbe` and `readinessProbe`.
    
5. How do pods in a Kubernetes cluster communicate?
    
6. What determines which pods a Service routes to?
    
7. Why is it important to define advanced features in YAML?
    
8. What is the default concurrency limit for streaming logs with `kubectl`?
    

---

## Flashcards

- **ETCD**: _Stores all cluster data as key-value pairs; only Control Plane component with state._
    
- **Scheduler**: _Assigns pending pods to nodes based on best fit criteria._
    
- **Controller Manager**: _Runs various controllers to maintain cluster desired state._
    
- **Deployment**: _Declarative object managing ReplicaSets and rolling updates._
    
- **ReplicaSet**: _Ensures the right number of pod replicas are running._
    
- **Pod**: _Smallest deployable unit, one or more containers, runs on a single node._
    
- **Service (ClusterIP)**: _Stable internal endpoint for pods, not externally accessible._
    
- **Liveness Probe**: _Checks and restarts stuck containers._
    
- **Readiness Probe**: _Removes/adds pod from service endpoints based on readiness._
    
- **Startup Probe**: _Waits for containers that take long to start before activating other probes._
    
- **Namespace**: _Organizational unit like a folder for cluster resources._
    
- **YAML**: _Defines resources declaratively, source of truth for configuration._
    

---

