

## Kubernetes Systems Components

`The Control Plane`

Componetes that make up the Control Plane

1. ETCD
	1. What is the function of the ETCD Data Store
		1. Exampe I want to run an nginx Container I write a manifest and that manifest is stored in ETCD, and then there are controllers that noticed that, and they react to that


Keep in mind this is a quick and dirty overview, the  purpose is to get a basic high level of understanding before digging deeper

2. Scheduler
	1. The scheduler decides which node to place the cluster, it is this component of the control plane that makes this decision
3. Controller Manager
	1. Controller loops
		1. Controller manager


The only component on the control plane that is persistent, or store or has state is etcd


## Kubernetes Service

A service is a stable endpoint to connect to something


## Creating a Deployment 


Pods
deployments
replica set
write


Looking at the names of the objects ( that is the name of kubernetes objects)


## From Deployment to Pod

Lets say that on my cluster I have the resource

`deployment.apps/pingpong` This represents the deployment that was created

`replicaset.apps/pingpong` is the replica set that was created by the deployment  

`pod/pingpong-xdxxxxxx` is the pod that was created by the replica set

## Properties of a Kubernetes Pod

- A Pod can have one or more containers
- A pod runs on a single node
- a POD cannot straddle multiple nodes
- Pods cannot be moved from one Pod to another
- Pods cannot scale horizontally


### Pod Details

A Pod is not a process, it is an environment for containers, a container is an execution environment for containers

- A Pod cannot be restarted
- A pod cannot crashes
- Containers in a pod crash
- If call containers exit successfully, the Pod ends in a "Succeeded phase"
- If some containers fail and dont get restarted, the Pods ends in a "failed phase"

### Replica Set

A replica set is a set of identical pods
It is defined by a pod template and number of desired replicas
If there is not enough pods the replica set creates more pods
if there are too many pods the replica set delete some pods
A replica set can be scaled up/down
The replica set created and destroys pods

### Deployment

- replica sets control identical pods
- Deployments are used to roll out different pods (different image, command, enviromnt variables)
- When a deployment is updated with a new Pod definition
	- a new `Replica Set` is progressively scaled up
	- old `Replica set` is scaled down
- This is a rolling update
- When a deployment is scaled up/down, it scaled up/down it s `ReplicaSet`


The `Replica Set` makes sure that we have the right number of Pods
The `Deployment` makes sure the the Replica Set has the right size

## Exposing Containers

```bash
# first I create a deployment
kubectl create deployment blue --image jepatazzo/color
```

```bash
# Now i want to connect to the pod, I will need the ip address
kubectl get pods -o wide
NAME                        READY   STATUS    RESTARTS   AGE     IP           NODE           NOMINATED NODE   READINESS GATES
blue-5c986bd7bf-2z6zs       1/1     Running   0          5m38s   10.42.2.13   picoworker02   <none>           <none>
pingpong-86959f6599-crd5t   1/1     Running   0          18h     10.42.1.17   picoworker01   <none>           <none>
pingpong-86959f6599-pqp7q   1/1     Running   0          17h     10.42.0.16   picomaster     <none>           <none>
pingpong-86959f6599-sjmlt   1/1     Running   0          18h     10.42.2.12   picoworker02   <none>           <none>
pingpong2                   1/1     Running   0          19h     10.42.2.10   picoworker02   <none>           <none>
pingpong3                   1/1     Running   0          19h     10.42.2.11   picoworker02   <none>           <none>


```

Now I am able to get the IP of the pod, and I can send some http requests tothat IP

## A better way to expose Containers

```bash
kubectl expose deployment blue --port 80



```


```bash
k get services 

NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
blue         ClusterIP   10.43.206.131   <none>        80/TCP    10s
kubernetes   ClusterIP   10.43.0.1       <none>        443/TCP   7d18h



```

## Cluster IP

- It is the default service type
- A virtual IP adress allocated for the service
- This IP is only reachable from within the cluster
- Our code can connect to the service using the original port number
- Perfect for internal communication



Is there a way to get an External IP/Public Facing IP

I can use a LoadBalancer Type, Om the cluster there is a controller that created the external IP, to connect to the service from outside the cluster and to make the service public facing


Connect to the LoadBalancer the LoadBalancer connects to the NordPort and the NordPort connects to Pods 

The LoadBalancer can outside the cluster and the NorPort serves as like an interface


## Kubectl logs

In this section I will be highlighting the limits of datadog
 - by default `kubectl logs` shows the output of a single pod

Currently on my cluster i have a deployment named pingpong, that is for demonstration purposed only


```bash
 kubectl logs deployments/pingpong --tail 1 --follow
Found 3 pods, using pod/pingpong-86959f6599-pqp7q
64 bytes from ::1: seq=28093 ttl=64 time=0.068 ms
64 bytes from ::1: seq=28094 ttl=64 time=0.070 ms
64 bytes from ::1: seq=28095 ttl=64 time=0.064 ms
64 bytes from ::1: seq=28096 ttl=64 time=0.071 ms
64 bytes from ::1: seq=28097 ttl=64 time=0.075 ms
64 bytes from ::1: seq=28098 ttl=64 time=0.068 ms
64 bytes from ::1: seq=28099 ttl=64 time=0.069 ms
64 bytes from ::1: seq=28100 ttl=64 time=0.072 ms


```


By default `kubectl logs` only shows us the logs of only one of the pods.
From the output one can see that I have 3 pods, but only getting the output of one of the pods

So what if I want to retrieve the logs of multiple pods

When getting the logs by `deplyment name`, only one single pod's logs are shown

To view the logs of multiple pods use a `selector`
If we check the pods created by the deployment, they all have the label `app=pingpong` this is the default lable that gets addded when using `kubectl create deployment`

```bash
# View the last line of logs from all pods with app=pingpoong label
kubectl logs -l app=pingpong --tail 1
64 bytes from ::1: seq=28467 ttl=64 time=0.080 ms
64 bytes from ::1: seq=28477 ttl=64 time=0.071 ms
64 bytes from ::1: seq=28468 ttl=64 time=0.082 ms

```
The output from this command is the last line of logs from all 3 pods.


Is it possible to stream the logs of all pingpong pods

```bash
# Keep in mind that there are only 3 pinpong pods
kubectl logs -l app=pingpong --tail 1 -f
64 bytes from ::1: seq=28592 ttl=64 time=0.082 ms
64 bytes from ::1: seq=28582 ttl=64 time=0.084 ms
64 bytes from ::1: seq=28582 ttl=64 time=0.084 ms
64 bytes from ::1: seq=28583 ttl=64 time=0.084 ms
64 bytes from ::1: seq=28583 ttl=64 time=0.079 ms
64 bytes from ::1: seq=28593 ttl=64 time=0.070 ms
64 bytes from ::1: seq=28584 ttl=64 time=0.087 ms
64 bytes from ::1: seq=28584 ttl=64 time=0.081 ms
64 bytes from ::1: seq=28594 ttl=64 time=0.067 ms
64 bytes from ::1: seq=28585 ttl=64 time=0.080 ms
64 bytes from ::1: seq=28585 ttl=64 time=0.074 ms
64 bytes from ::1: seq=28595 ttl=64 time=0.073 ms
64 bytes from ::1: seq=28586 ttl=64 time=0.085 ms
64 bytes from ::1: seq=28586 ttl=64 time=0.081 ms



```


Now what happens when we try to stream the logs for more that 5 pods

```bash
# Scale the deployment from 3 to 8 pods
kubectl scale deployment pingpong --replicas=8
deployment.apps/pingpong scaled

```

```bash
# stream the logs
kubectl logs -l app=pingpong --tail 1 -f
error: you are attempting to follow 8 log streams, but maximum allowed concurrency is 5, use --max-log-requests to increase the limit

```

### Why Can't we stream the logs of many pods

`kubectl` open one connection to the API server per pod
for each pod the API server opens an extra connection to the corresponding kubelet on the node

If there are 1000 pods in a deployment that is 1000 inbound + 1000 outbound connections on the API server

This could easily put a lot of stress on the API server

this could be changed with the `--max-log-requests`

### Shortcomings of kubectl logs

- We do not see which pod sent which log line
- if pods are restarted/replaced the log stream stops
- If new pods are added, we do not see their logs
- To stream the logs of multiple pods, we need to write a selector
- there external tools to address these shortcomings




## Namespaces

- A way to organize resources on a Kubernetes cluster
- An organization technique similar to creating folders on a filesystem

### Two technique to create namespaces in kubernetes


```bash

kubuectl create namespace blue
```

### YAML as a source of truth

- do not use `kubectl run`,`kubectl create deployment`,`kubectl expose ...`
- Define everything ion yaml
- `kubectl apply -f ... --prune --all` that YAML
- Keep the `yaml` under version control
- enforce changes to go through that `yaml` (with pull requests)
- Version control system now has a full histroy of what de deploy
- Compares to "Infrastructure as COde", but for application deployments





## What Happens

what happens when we run `kubectl create deployment web --image=nginx`

`kubectl` communicates with the `API server`. 
THE `apiserver` creates the deployment and stores it in etcd, anc communicates back that the deplyment has been created.
Now that we have a deployment has been created, the deplyment controller gets activated for lack of a better word.

The controller manager consits of dozens of controllers grouped together. Each controller has a specific type of responsibility for each kubernetes object. In case of a deployment we have a deployment controller that will handle the deployment for us in a declarative way.
The deployment controller creates the `ReplicaSet` . Now that we have a replica set, the `ReplicaSet` controller wakes up and the number of pods requested is put in a pending state. Next the scheduler assigns pods to nodes, the schduler is contantly looking for pending pods


next is `kubelet` the responsibility of `kubelet` is to register with the control plane. `kubectl` communicates with the control plane and syas that I am creating that POD

These are the steps that happens when creating a deployment


## Authoring Yaml

- We have already generated YAML implicitly, with e.g.:
    
    - `kubectl run`
        
    - `kubectl create deployment` (and a few other `kubectl create` variants)
        
    - `kubectl expose`
        
- When and why do we need to write our own YAML?
    
- How do we write YAML from scratch?


## The limits of generated YAML

- Many advanced (and even not-so-advanced) features require to write YAML:
    
    - pods with multiple containers
        
    - resource limits
        
    - `healthchecks`
        
    - `DaemonSets, StatefulSets`
        
    - and more!
        
- How do we access these features?


## Various ways to write YAML

- Completely from scratch with our favorite editor
    
    (yeah, right)
    
- Dump an existing resource with `kubectl get -o yaml ...`
    
    (it is recommended to clean up the result)
    
- Ask `kubectl` to generate the YAML
    
    (with a `kubectl create --dry-run=client -o yaml`)
    
- Use The Docs, Luke
    
    (the documentation almost always has YAML examples)

```bash
# use kubectl to generated yaml

k create deployment purple --image jpetazzo/color -o yaml --dry-run
W1106 10:05:06.187318 1830055 helpers.go:703] --dry-run is deprecated and can be replaced with --dry-run=client.
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: purple
  name: purple
spec:
  replicas: 1
  selector:
    matchLabels:
      app: purple
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: purple
    spec:
      containers:
      - image: jpetazzo/color
        name: color
        resources: {}
status: {}

```



## Kubernetes network Model

One big flat network


- In detail:
    
    - all nodes must be able to reach each other, without NAT
        
    - all pods must be able to reach each other, without NAT
        
    - pods and nodes must be able to reach each other, without NAT
        
    - each pod is aware of its IP address (no NAT)
        
    - pod IP addresses are assigned by the network implementation
        
- Kubernetes doesn't mandate any particular 

The not so good parts of the Kubernetes network model

## Kubernetes network model: the less good

- Everything can reach everything
    
    - if you want security, you need to add network policies
        
    - the network implementation that you use needs to support them
        
- There are literally dozens of implementations out there
    
    [ContainerNetworking]([https://github.com/containernetworking/cni/](https://github.com/containernetworking/cni/) lists more than 25 plugins)
    
- Pods have level 3 (IP) connectivity, but _services_ are level 4 (TCP or UDP)
    
    (Services map to a single UDP or TCP port; no port ranges or arbitrary IP packets)
    
- `kube-proxy` is on the data path when connecting to a pod or container,  
    and it's not particularly fast (relies on userland proxying or iptables)

The CNI plugin manages the pod to pod network, the communication betweeen nodes and pods, the logical implementation 

Pod to service network --  out of the box this is ClusterIP

In a kubernetes cluster anyone can talk to anyone

Network policies allow to control communication between pods in a cluster

NodePorts exposes the node in the cluster to the public internet

Network Policies for network isolation

Network policies decide which network traffic is allowed to flow and what network traffic is denied




## Scale the app demo

what I want to do is scale my application, In other words I want more instances of the application running  on my cluster

```bash
kubectl get services --all-namespaces --selector app=webui
NAMESPACE   NAME    TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
blue        webui   NodePort   10.43.238.133   <none>        80:31549/TCP   5d14h
default     webui   NodePort   10.43.48.221    <none>        80:31189/TCP   5d12h
green       webui   NodePort   10.43.211.88    <none>        80:31969/TCP   5d1
```



taints on nodes - prevents pods from running on this node (stinky node)
tolerations go on pods

In my case the master node does not have any taints, so therfore contianers can run on my master node, the question is how do I apply a taint to the masters node, and what will that do to pods that acre already running on the master nodes

DaemonSets and deployments can coexist on the same node

how does the daemonset expose itself to the public internet


### Labels and selectors 
the `rng` service is Load Balancing requests to a set of pods
that set of pods is defined by the selector of the rng service

`app=rng` - means all pods having the label (this label)


### Where do labels come from

- When we create a deployment with `kubectl create deployment rng`,  
    this deployment gets the label `app=rng`
    
- The replica sets created by this deployment also get the label `app=rng`
    
- The pods created by these replica sets also get the label `app=rng`
    
- When we created the daemon set from the deployment, we re-used the same spec
    
- Therefore, the pods created by the daemon set get the same labels



## Isolation of replica sets and daemon sets

- Since both the `rng` daemon set and the `rng` replica set use `app=rng` ...
    
    ... Why don't they "find" each other's pods?
    
- _Replica sets_ have a more specific selector, visible with `kubectl describe`
    
    (It looks like `app=rng,pod-template-hash=abcd1234`)
    
- _Daemon sets_ also have a more specific selector, but it's invisible
    
    (It looks like `app=rng,controller-revision-hash=abcd1234`)
    
- As a result, each controller only "sees" the pods it manages


## Removing a pod from the load balancer

- Currently, the `rng` service is defined by the `app=rng` selector
    
- The only way to remove a pod is to remove or change the `app` label
    
- ... But that will cause another pod to be created instead!
    
- What's the solution?

- We need to change the selector of the `rng` service!
    
- Let's add another label to that selector (e.g. `active=yes`)

## Selectors with multiple labels

- If a selector specifies multiple labels, they are understood as a logical _AND_
    
    (in other words: the pods must match all the labels)
    
- We cannot have a logical _OR_
    
    (e.g. `app=api AND (release=prod OR release=preprod)`)
    
- We can, however, apply as many extra labels as we want to our pods:
    
    - use selector `app=api AND prod-or-preprod=yes`
        
    - add `prod-or-preprod=yes` to both sets of pods
        
- We will see later that in other places, we can use more advanced selectors


## Rolling Deployments

Pods are replaced gradually, by scaling down the old ReplicaSet while at the sametime scaling up the _ReplicaSet_ 

- How should we update a running application?
    
- Strategy 1: delete old version, then deploy new version
    
    (not great, because it obviously provokes downtime!)
	    - there will be downtime of the application
    
- Strategy 2: deploy new version, then delete old version
    
    (uses a lot of resources; also how do we shift traffic?)
	    - if a really big application you have to double the footprint to do the update
	    - if a small application there will be less resources needed
- Strategy 3: replace running pods one at a time
	- replace one at a time
	- 1000 pods one by one have to wait for each pod
	- 
    
    (sounds interesting; and good news, Kubernetes does it for us!)


## Rolling updates

- With rolling updates, when a Deployment is updated, it happens progressively
    
- The Deployment controls multiple Replica Sets
    
- Each Replica Set is a group of identical Pods
    
    (with the same image, arguments, parameters ...)
    
- During the rolling update, we have at least two Replica Sets:
    
    - the "new" set (corresponding to the "target" version)
        
    - at least one "old" set
        
- We can have multiple "old" sets
    
    (if we start another update before the first one is done)



The old version of the application scaled to the max
The new version is scaled up and the old version is scaled down

Creates a smooth transition between the two versions


## Update strategy

- Two parameters determine the pace of the rollout: `maxUnavailable` and `maxSurge
	_maxUnavailable_ how many pods are we comfortable being unavailable,
	the default is 25%. I f you do not want to lose any capacity during the update set maxUnavailable to `0`
	_maxSurge_ how much extra resources we can use when doing updates
	If you want your update to be really fast set _maxSurge_ to `100%`
	
    
- They can be specified in absolute number of pods, or percentage of the `replicas` count
    
- At any given time ...
    
    - there will always be at least `replicas`-`maxUnavailable` pods available
        
    - there will never be more than `replicas`+`maxSurge` pods in total
        
    - there will therefore be up to `maxUnavailable`+`maxSurge` pods being updated
        
- We have the possibility of rolling back to the previous version  
    (if the update fails or is unsatisfactory in any way)




## Kubernetes Commands


the `kubectl apply ` command is used for creating objects as well as mkaing changes to existing . to make changes to the pod object simplky edit the yaml file that represents the object


# Healthchecks

- Containers can have _healthchecks_ (also called "probes")
    
- There are three kinds of healthchecks, corresponding to different use-cases:
    
    `startupProbe`, `readinessProbe`, `livenessProbe`
    
- These healthchecks are optional (we can use none, all, or some of them)
    
- Different probes are available:
    
    HTTP GET, TCP connection, arbitrary program execution, GRPC
    
- All these probes have a binary result (success/failure)
    
- Probes that aren't defined will default to a "success" result

## Liveness probes

_This container is dead, we don't know how to fix it, other than restarting it. The goal of the liveness probe is to check if the container is dead and if it is dead, we start a new container
Something does not work, you restart the service and it fixes the problem. The container is dead and we cannot bring it back to life. Start_

- Check if the container is dead or alive
    
- If Kubernetes determines that the container is dead:
    
    - it terminates the container gracefully
        
    - it restarts the container (unless the Pod's `restartPolicy` is `Never`)
        
-  With the default parameters, it takes:
    
    - up to 30 seconds to determine that the container is dead
        
    - up to 30 seconds to terminate it

## When to use a liveness probe

- To detect failures that can't be recovered
    
    - deadlocks (causing all requests to time out)
        
    - internal corruption (causing all requests to error)
        
- Anything where our incident response would be "just restart/reboot it"

## Liveness probes gotchas

_liveness probes should only be used only of the problem will be solved by restarting the container. Service dependencies ex. Web Frontends and a DataBase backend. If the database is down/fails, all the webservers on the cluster will be down, restarting the containers will not fix the problems. A large amount of containers restarting will casuse extra loads. This causes cascading failures_

**Do not** use liveness probes for problems that can't be fixed by a restart

- Otherwise we just restart our pods for no reason, creating useless load

**Do not** depend on other services within a liveness probe

- Otherwise we can experience cascading failures
    
    (example: web server liveness probe that makes a requests to a database)
    

**Make sure** that liveness probes respond quickly
 _L_
- The default probe timeout is 1 second (this can be tuned!)
    
- If the probe takes longer than that, it will eventually cause a restart


## Readiness probes

_Sometimes, my container "needs a break"._

- Check if the container is ready or not
    
- If the container is not ready, its Pod is not ready
    
- If the Pod belongs to a Service, it is removed from its Endpoints
    
    (it stops receiving new connections but existing ones are not affected)
    
- If there is a rolling update in progress, it might pause
    
    (Kubernetes will try to respect the MaxUnavailable parameter)
    
- As soon as the readiness probe suceeds again, everything goes back to normal

### Examples

_Garbage collection creates a huge spike in latency
Instead of letting the garbage collection happen whenever the runtime decides, the garbage collection is triggered by some event
The container stops receiving requests triggers garbage collection
and when done start receiving requests_

_Another Example  say you have a container that is serving data from an in memory cache. And what if you have to reload the cache and that creates service disruption. A Readiness Probe that says wait I am busy send requests to another service container_

_Another Example Serving something from the client to the server , like video conferencing or gaming.
Imagine a service spike, pods are super busy, and some pods that are idle and ready to serve clients. If a pod as a certain number of connections, it marks itself as not ready, removes itself from the loadbalancer so that new connections can be redirected to pods that are ready to accept connections_

## When to use a readiness probe

- To indicate failure due to an external cause
    
    - database is down or unreachable
        
    - mandatory auth or other backend service unavailable
        
- To indicate temporary failure or unavailability
    
    - runtime is busy doing garbage collection or (re)loading data
        
    - application can only service _N_ parallel connections
        
    - new connections will be directed to other Pods

## Startup probes


 
_My container takes a long time to boot before being able to serve traffic._

- After creating a container, Kubernetes runs its startup probe
    
- The container will be considered "unhealthy" until the probe succeeds
    
- As long as the container is "unhealthy", its Pod...:
    
    - is not added to Services' endpoints
        
    - is not considered as "available" for rolling update purposes
        
- Readiness and liveness probes are enabled _after_ startup probe reports success
    
    (if there is no startup probe, readiness and liveness probes are enabled right away

If the length of time the container takes to start up is predicated, then one can add an extra delay

Check it the container finished its bootup process


## When to use a startup probe

- For containers that take a long time to start
    
    (more than 30 seconds)
    
- Especially if that time can vary a lot
    
    (e.g. fast in dev, slow in prod, or the other way around)

## Startup probes gotchas

- When defining a `startupProbe`, we almost always want to adjust its parameters
    
    (specifically, its `failureThreshold` - this is explained in next slide)
    
- Otherwise, if the container fails to start within 30 seconds...
    
    _Kubernetes terminates the container and restarts it!_
    
- Sometimes, it's easier/simpler to use a `readinessProbe` instead
    
    (except when also using a `livenessProbe`)

## Timing and thresholds

- Probes are executed at intervals of `periodSeconds` (default: 10)
    
- The timeout for a probe is set with `timeoutSeconds` (default: 1)
    

If a probe takes longer than that, it is considered as a FAIL

For liveness probes **and startup probes** this terminates and restarts the container

- A probe is considered successful after `successThreshold` successes (default: 1)
    
- A probe is considered failing after `failureThreshold` failures (default: 3)
    
- All these parameters can be set independently for each probe

## initialDelaySeconds`

- A probe can have an `initialDelaySeconds` parameter (default: 0)
    
- Kubernetes will wait that amount of time before running the probe for the first time
    
- It is generally better to use a `startupProbe` instead
    
    (but this parameter did exist before startup probes were implemented)

## `readinessProbe` vs `startupProbe`

- A lot of blog posts / documentations / tutorials recommend readiness probes...
    
- ...even in scenarios where a startup probe would seem more appropriate!
    
- This is because startup probes are relatively recent
    
    (they reached GA status in Kubernetes 1.20)
    
- When there is no `livenessProbe`, using a `readinessProbe` is simpler:
    
    - a `startupProbe` generally requires to change the `failureThreshold`
        
    - a `startupProbe` generally also requires a `readinessProbe`
        
    - a single `readinessProbe` can fulfill both roles

## Different types of probes

- Kubernetes supports the following mechanisms:
    
    - `exec` (arbitrary program execution)
        
    - `httpGet` (HTTP GET request)
        
    - `tcpSocket` (check if a TCP port is accepting connections)
        
    - `grpc` (standard [GRPC Health Checking Protocol](https://grpc.github.io/grpc/core/md_doc_health-checking.html))
        
- All probes give binary results ("it works" or "it doesn't")
    
- Let's see the specific details for each of them!

## `exec`

_Running inside the container, the program that is run needs to be in the Container Image. Keep in mind is that Kubernetes will only look at the status code_


- Runs an arbitrary program _inside_ the container
    
    (like with `kubectl exec` or `docker exec`)
    
- The program must be available in the container image
    
- Kubernetes uses the exit status of the program
    
    (standard UNIX convention: 0 = success, anything else = failure)

## `exec` example

When the worker is ready, it should create `/tmp/ready`.  
The following probe will give it 5 minutes to do so.

```
apiVersion: v1
kind: Pod
metadata:  
	name: queueworker
spec:  
  containers:  
  - name: worker    image: myregistry.../worker:v1.0    
    startupProbe:      
      exec:        
        command:       
        - test        
        - -f        
        - /tmp/ready      
    failureThreshold: 30
```


## httpGet`

- Make an HTTP GET request to the container
    
- The request will be made by Kubelet
    
    (doesn't require extra binaries in the container image)
    
- `port` must be specified
    
- `path` and extra `httpHeaders` can be specified optionally
    
- Kubernetes uses HTTP status code of the response:
    
    - 200-399 = success
        
    - anything else = failure

## `httpGet` example

The following liveness probe restarts the container if it stops responding on `/healthz`:

```
apiVersion: v1
kind: Pod
metadata:  
  name: frontend
spec:  
  containers:  
  - name: frontend    
    image: myregistry.../frontend:v1.0    
    livenessProbe:      
      httpGet:        
        port: 80        
        path: /healthz
```


## `tcpSocket`



- Kubernetes checks if the indicated TCP port accepts connections
    
- There is no additional check
    

It's quite possible for a process to be broken, but still accept TCP connections!


## `grpc`

- Available in beta since Kubernetes 1.24
    
- Leverages standard [GRPC Health Checking Protocol](https://grpc.github.io/grpc/core/md_doc_health-checking.html)


## Best practices for healthchecks

- Readiness probes are almost always beneficial

	_Readiness Probes almost always do not harm the application. _
    
    - don't hesitate to add them early!
        
    - we can even make them _mandatory_
        
- Be more careful with liveness and startup probes

	_get production experience before adding liveness probes_
    - they aren't always necessary
        
    - they can even cause harm

## Readiness probes

- Almost always beneficial
    
- Exceptions:
    
    - web service that doesn't have a dedicated "health" or "ping" route
        
    - ...and all requests are "expensive" (e.g. lots of external calls)


## Liveness probes

- If we're not careful, we end up restarting containers for no reason
    
    (which can cause additional load on the cluster, cascading failures, data loss, etc.)
    
- Suggestion:
    
    - don't add liveness probes immediately
        
    - wait until you have a bit of production experience with that code
        
    - then add narrow-scoped healthchecks to detect specific failure modes
        
- Readiness and liveness probes should be different
    
    (different check _or_ different timeouts _or_ different thresholds)


## Startup probes

- Only beneficial for containers that need a long time to start
    
    (more than 30 seconds)
    
- If there is no liveness probe, it's simpler to just use a readiness probe
    
    (since we probably want to have a readiness probe anyway)
    
- In other words, startup probes are useful in one situation:
    
    _we have a liveness probe, AND the container needs a lot of time to start_
    
- Don't forget to change the `failureThreshold`
    
    (otherwise the container will fail to start and be killed)

## Recap of the gotchas

- The default timeout is 1 second
    
    - if a probe takes longer than 1 second to reply, Kubernetes considers that it fails
        
    - this can be changed by setting the `timeoutSeconds` parameter  
        (or refactoring the probe)
        
- Liveness probes should not be influenced by the state of external services
    
- Liveness probes and readiness probes should have different paramters
    
- For startup probes, remember to increase the `failureThreshold`

## Healthchecks for workers

(In that context, worker = process that doesn't accept connections)

- A relatively easy solution is to use files
    
- For a startup or readiness probe:
    
    - worker creates `/tmp/ready` when it's ready
    - probe checks the existence of `/tmp/ready`
- For a liveness probe:
    
    - worker touches `/tmp/alive` regularly  
        (e.g. just before starting to work on a job)
    - probe checks that the timestamp on `/tmp/alive` is recent
    - if the timestamp is old, it means that the worker is stuck
- Sometimes it can also make sense to embed a web server in the worker


## The Kubernetes dashboard

- Kubernetes resources can also be viewed with a web dashboard
    
- Dashboard users need to authenticate
    
    (typically with a token)
    
- The dashboard should be exposed over HTTPS
    
    (to prevent interception of the aforementioned token)
    
- Ideally, this requires obtaining a proper TLS certificate
    
    (for instance, with Let's Encrypt)

## Three ways to install the dashboard

- Our `k8s` directory has no less than three manifests!
    
- `dashboard-recommended.yaml`
    
    (purely internal dashboard; user must be created manually)
    
- `dashboard-with-token.yaml`
    
    (dashboard exposed with NodePort; creates an admin user for us)
    
- `dashboard-insecure.yaml` aka _YOLO_
    
    (dashboard exposed over HTTP; gives root access to anonymous users)

## dashboard-insecure.yaml

- This will allow anyone to deploy anything on your cluster
    
    (without any authentication whatsoever)
    
- **Do not** use this, except maybe on a local cluster
    
    (or a cluster that you will destroy a few minutes later)
    
- On "normal" clusters, use `dashboard-with-token.yaml` instead!

## What's in the manifest?

- The dashboard itself
    
- An HTTP/HTTPS unwrapper (using `socat`)
    
- The guest/admin account
    

- Create all the dashboard resources, with the following command:
    
    ```
    kubectl apply -f ~/container.training/k8s/dashboard-insecure.yaml
    ```

## Connecting to the dashboard

- Check which port the dashboard is on:
    
    ```
    kubectl get svc dashboard
    ```
    

You'll want the `3xxxx` port.

- Connect to [http://oneofournodes:3xxxx/](http://oneofournodes:3xxxx/)

The dashboard will then ask you which authentication you want to use.


## Dashboard authentication

- We have three authentication options at this point:
    
    - token (associated with a role that has appropriate permissions)
        
    - kubeconfig (e.g. using the `~/.kube/config` file from `node1`)
        
    - "skip" (use the dashboard "service account")
        
- Let's use "skip": we're logged in!

Remember, we just added a backdoor to our Kubernetes cluster!


## Closing the backdoor

- Seriously, don't leave that thing running!

- Remove what we just created:
    
    ```
    kubectl delete -f ~/container.training/k8s/dashboard-insecure.yaml
    ```

## The risks

- The steps that we just showed you are _for educational purposes only!_
    
- If you do that on your production cluster, people [can and will abuse it](https://redlock.io/blog/cryptojacking-tesla)
    
- For an in-depth discussion about securing the dashboard,  
    check [this excellent post on Heptio's blog](https://blog.heptio.com/on-securing-the-kubernetes-dashboard-16b09b1b7aca)

## dashboard-with-token.yaml

- This is a less risky way to deploy the dashboard
    
- It's not completely secure, either:
    
    - we're using a self-signed certificate
        
    - this is subject to eavesdropping attacks
        
- Using `kubectl port-forward` or `kubectl proxy` is even better

## What's in the manifest?

- The dashboard itself (but exposed with a `NodePort`)
    
- A ServiceAccount with `cluster-admin` privileges
    
    (named `kubernetes-dashboard:cluster-admin`)
    

- Create all the dashboard resources, with the following command:
    
    ```
    kubectl apply -f ~/container.training/k8s/dashboard-with-token.yaml
    ```

## Obtaining the token

- The manifest creates a ServiceAccount
    
- Kubernetes will automatically generate a token for that ServiceAccount
    

- Display the token:
    
    ```
    kubectl --namespace=kubernetes-dashboard \  describe secret cluster-admin-token
    ```
    

The token should start with `eyJ...` (it's a JSON Web Token).

Note that the secret name will actually be `cluster-admin-token-xxxxx`.  
(But `kubectl` prefix matches are great!)

## Connecting to the dashboard

- Check which port the dashboard is on:
    
    ```
    kubectl get svc --namespace=kubernetes-dashboard
    ```
    

You'll want the `3xxxx` port.

- Connect to [http://oneofournodes:3xxxx/](http://oneofournodes:3xxxx/)

The dashboard will then ask you which authentication you want to use.

## Dashboard authentication

- Select "token" authentication
    
- Copy paste the token (starting with `eyJ...`) obtained earlier
    
- We're logged in!

## Other dashboards

- [Kube Web View](https://codeberg.org/hjacobs/kube-web-view)
    
    - read-only dashboard
        
    - optimized for "troubleshooting and incident response"
        
    - see [vision and goals](https://kube-web-view.readthedocs.io/en/latest/vision.html#vision) for details
        
- [Kube Ops View](https://codeberg.org/hjacobs/kube-ops-view)
    
    - "provides a common operational picture for multiple Kubernetes clusters"




## Security implications of `kubectl apply`

- When we do `kubectl apply -f <URL>`, we create arbitrary resources
    
- Resources can be evil; imagine a `deployment` that ...
    
    - starts bitcoin miners on the whole cluster
        
    - hides in a non-default namespace
        
    - bind-mounts our nodes' filesystem
        
    - inserts SSH keys in the root account (on the node)
        
    - encrypts our data and ransoms it
        
    - ☠️☠️☠️

## kubectl apply is the new `curl | sh`

- `curl | sh` is convenient
    
- It's safe if you use HTTPS URLs from trusted sources
    
- `kubectl apply -f` is convenient
    
- It's safe if you use HTTPS URLs from trusted sources
    
- Example: the official setup instructions for most pod networks
    
- It introduces new failure modes
    
    (for instance, if you try to apply YAML from a link that's no longer valid)


## k9s


- Somewhere in between CLI and GUI (or web UI), we can find the magic land of TUI
    
    - [Text-based user interfaces](https://en.wikipedia.org/wiki/Text-based_user_interface)
        
    - often using libraries like [curses](https://en.wikipedia.org/wiki/Curses_%28programming_library%29) and its successors
        
- Some folks love them, some folks hate them, some are indifferent ...
    
- But it's nice to have different options!
    
- Let's see one particular TUI for Kubernetes: [k9s](https://k9scli.io/)

## Installing k9s

- If you are using a training cluster or the [shpod](https://github.com/jpetazzo/shpod) image, k9s is pre-installed
    
- Otherwise, it can be installed easily:
    
    - with [various package managers](https://k9scli.io/topics/install/)
        
    - or by fetching a [binary release](https://github.com/derailed/k9s/releases)
        
- We don't need to set up or configure anything
    
    (it will use the same configuration as `kubectl` and other well-behaved clients)
    
- Just run `k9s` to fire it up!

## What kind to we want to see?

- Press `:` to change the type of resource to view
    
- Then type, for instance, `ns` or `namespace` or `nam[TAB]`, then `[ENTER]`
    
- Use the arrows to move down to e.g. `kube-system`, and press `[ENTER]`
    
- Or, type `/kub` or `/sys` to filter the output, and press `[ENTER]` twice
    
    (once to exit the filter, once to enter the namespace)
    
- We now see the pods in `kube-system`!

## Interacting with pods

- `l` to view logs
    
- `d` to describe
    
- `s` to get a shell (won't work if `sh` isn't available in the container image)
    
- `e` to edit
    
- `shift-f` to define port forwarding
    
- `ctrl-k` to kill
    
- `[ESC]` to get out or get back

## Quick navigation between namespaces

- On top of the screen, we should see shortcuts like this:
    
    ```
    <0> all<1> kube-system<2> default
    ```
    
- Pressing the corresponding number switches to that namespace
    
    (or shows resources across all namespaces with `0`)
    
- Locate a namespace with a copy of DockerCoins, and go there!

## Interacting with Deployments

- View Deployments (type `:` `deploy` `[ENTER]`)
    
- Select e.g. `worker`
    
- Scale it with `s`
    
- View its aggregated logs with `l`

## Exit

- Exit at any time with `Ctrl-C`
    
- k9s will "remember" where you were
    
    (and go back there next time you run it)
## Pros

- Very convenient to navigate through resources
    
    (hopping from a deployment, to its pod, to another namespace, etc.)
    
- Very convenient to quickly view logs of e.g. init containers
    
- Very convenient to get a (quasi) realtime view of resources
    
    (if we use `watch kubectl get` a lot, we will probably like k9s)


## Cons

- Doesn't promote automation / scripting
    
    (if you repeat the same things over and over, there is a scripting opportunity)
    
- Not all features are available
    
    (e.g. executing arbitrary commands in containers)

## Tilt

- What does a development workflow look like?
    
    - make changes
        
    - test / see these changes
        
    - repeat!
        
- What does it look like, with containers?
    
    🤔

## Basic Docker workflow

- Preparation
    
    - write Dockerfiles
- Iteration
    
    - edit code
    - `docker build`
    - `docker run`
    - test
    - `docker stop`

Straightforward when we have a single container.


## Docker workflow with volumes

- Preparation
    
    - write Dockerfiles
    - `docker build` + `docker run`
- Iteration
    
    - edit code
    - test

Note: only works with interpreted languages.  
(Compiled languages require extra work.)

## Docker workflow with Compose

- Preparation
    
    - write Dockerfiles + Compose file
    - `docker-compose up`
- Iteration
    
    - edit code
    - test
    - `docker-compose up` (as needed)

Simplifies complex scenarios (multiple containers).  
Facilitates updating images.

## Basic Kubernetes workflow

- Preparation
    
    - write Dockerfiles
    - write Kubernetes YAML
    - set up container registry
- Iteration
    
    - edit code
    - build images
    - push images
    - update Kubernetes resources

Seems simple enough, right?

## Basic Kubernetes workflow

- Preparation
    
    - write Dockerfiles
    - write Kubernetes YAML
    - **set up container registry**
- Iteration
    
    - edit code
    - build images
    - **push images**
    - update Kubernetes resources

Ah, right ...


## We need a registry

- Remember "build, ship, and run"
    
- Registries are involved in the "ship" phase
    
- With Docker, we were building and running on the same node
    
- We didn't need a registry!
    
- With Kubernetes, though ...

## Special case of single node clusters

- If our Kubernetes has only one node ...
    
- ... We can build directly on that node ...
    
- ... We don't need to push images ...
    
- ... We don't need to run a registry!
    
- Examples: Docker Desktop, Minikube ...

## When we have more than one node

- Which registry should we use?
    
    (Docker Hub, Quay, cloud-based, self-hosted ...)
    
- Should we use a single registry, or one per cluster or environment?
    
- Which tags and credentials should we use?
    
    (in particular when using a shared registry!)
    
- How do we provision that registry and its users?
    
- How do we adjust our Kubernetes YAML manifests?
    
    (e.g. to inject image names and tags)

## More questions

- The whole cycle (build+push+update) is expensive
    
- If we have many services, how do we update only the ones we need?
    
- Can we take shortcuts?
    
    (e.g. synchronized files without going through a whole build+push+update cycle)

## Tilt

- Tilt is a tool to address all these questions
    
- There are other similar tools (e.g. Skaffold)
    
- We arbitrarily decided to focus on that one

## Tilt in practice

- The `dockercoins` directory in our repository has a `Tiltfile`
    
- That Tiltfile includes definitions for the DockerCoins app, including:
    
    - building the images for the app
        
    - Kubernetes manifests to deploy the app
        
    - a self-hosted registry to host the app image
        
- Let's try it out!

## Running Tilt locally

_These instructions are valid only if you run Tilt on your local machine._

_If you are running Tilt on a remote machine or in a Pod, see next slide._

- Start Tilt:
    
    ```
    tilt up
    ```
    
- Then press "space" or connect to [http://localhost:10350/](http://localhost:10350/)

## Running Tilt on a remote machine

- If Tilt runs remotely, we can't access `http://localhost:10350`
    
- We'll need to tell Tilt to listen to `0.0.0.0`
    
    (instead of just `localhost`)
    
- If we run Tilt in a Pod, we need to expose port 10350 somehow
    
    (and Tilt needs to listen on `0.0.0.0`, too)

## Telling Tilt to listen in `0.0.0.0`

- This can be done with the `--host` flag:
    
    ```
    tilt --host=0.0.0.0
    ```
    
- Or by setting the `TILT_HOST` environment variable:
    
    ```
    export TILT_HOST=0.0.0.0tilt up
    ```


## Running Tilt in a Pod

If you use `shpod`, you can use the following command:

```
kubectl patch service shpod --namespace shpod -p "
spec:  
  ports:  
  - name: tilt    
    port: 10350    
    targetPort: 10350    
    nodePort: 30150    
    protocol: TCP"
```

Then connect to port 30150 on any of your nodes.

If you use something else than `shpod`, adapt these instructions!


## Kubernetes contexts

- Tilt is designed to run in dev environments
    
- It will try to figure out if we're really in a dev environment:
    
    - if Tilt thinks that are on a local dev cluster, it will start
        
    - otherwise, it will give us a warning and it won't continue
        
- In the latter case, we need to add one line to the Tiltfile
    
    (to tell Tilt "it's okay, you can run safely in this environment!")
    
- If this happens, add the line to the Tiltfile
    
    (Tilt will tell you exactly what to add!)
    
- We don't need to restart Tilt, it will detect the change immediately

## What's in our Tiltfile?

- Kubernetes manifests for a local registry
    
- Kubernetes manifests for DockerCoins
    
- Instructions indicating how to build DockerCoins' images
    
- A tiny bit of sugar
    
    (telling Tilt which registry to use)

## How does it work?

- Tilt keeps track of dependencies between files and resources
    
    (a bit like a `make` that would run continuously)
    
- It automatically alters some resources
    
    (for instance, it updates the images used in our Kubernetes manifests)
    
- That's it!
    

(And of course, it provides a great web UI, lots of libraries, etc.)


## What happens when we edit a file (1/2)

- Let's change e.g. `worker/worker.py`
    
- Thanks to this line,
    
    ```
    docker_build('dockercoins/worker', 'worker')
    ```
    
    ... Tilt watches the `worker` directory and uses it to build `dockercoins/worker`
    
- Thanks to this line,
    
    ```
    default_registry('localhost:30555')
    ```
    
    ... Tilt actually renames `dockercoins/worker` to `localhost:30555/dockercoins_worker`
    
- Tilt will tag the image with something like `tilt-xxxxxxxxxx`

## What happens when we edit a file (2/2)

- Thanks to this line,
    
    ```
    k8s_yaml('../k8s/dockercoins.yaml')
    ```
    
    ... Tilt is aware of our Kubernetes resources
    
- The `worker` Deployment uses `dockercoins/worker`, so it must be updated
    
- `dockercoins/worker` becomes `localhost:30555/dockercoins_worker:tilt-xxx`
    
- The `worker` Deployment gets updated on the Kubernetes cluster
    
- All these operations (and their log output) are visible in the Tilt UI

## Configuration file format

- The Tiltfile is written in [Starlark](https://github.com/bazelbuild/starlark)
    
    (essentially a subset of Python)
    
- Tilt monitors the Tiltfile too
    
    (so it reloads it immediately when we change it)

## Tilt "killer features"

- Dependency engine
    
    (build or run only what's necessary)
    
- Ability to watch resources
    
    (execute actions immediately, without explicitly running a command)
    
- Rich library of function and helpers
    
    (build container images, manipulate YAML manifests...)
    
- Convenient UI (web; TUI also available)
    
    (provides immediate feedback and logs)
    
- Extensibility!

## Exposing HTTP services with Ingress resources




- Service = layer 4 (TCP, UDP, SCTP)
    
    - works with every TCP/UDP/SCTP protocol
        
    - doesn't "see" or interpret HTTP
        
- Ingress = layer 7 (HTTP)
    
    - only for HTTP
        
    - can route requests depending on URI or host header
        
    - can handle TLS

## Why should we use Ingress resources?

A few use-cases:

- URI routing (e.g. for single page apps)
    
    `/api` → service `api:5000`
    
    everything else → service `static:80`
    
- Cost optimization
    
    (because individual `LoadBalancer` services typically cost money)
    
- Automatic handling of TLS certificates

## `LoadBalancer` vs `Ingress`

- Service with `type: LoadBalancer`
    
    - requires a particular controller (e.g. CCM, MetalLB)
    - if TLS is desired, it has to be implemented by the app
    - works for any TCP protocol (not just HTTP)
    - doesn't interpret the HTTP protocol (no fancy routing)
    - costs a bit of money for each service
- Ingress
    
    - requires an ingress controller
    - can implement TLS transparently for the app
    - only supports HTTP
    - can do content-based routing (e.g. per URI)
    - lower cost per service  
        (exact pricing depends on provider's model)

## Ingress resources

- Kubernetes API resource (`kubectl get ingress`/`ingresses`/`ing`)
    
- Designed to expose HTTP services
    
- Requires an _ingress controller_
    
    (otherwise, resources can be created, but nothing happens)
    
- Some ingress controllers are based on existing load balancers
    
    (HAProxy, NGINX...)
    
- Some are standalone, and sometimes designed for Kubernetes
    
    (Contour, Traefik...)
    
- Note: there is no "default" or "official" ingress controller!


## Ingress standard features

- Load balancing
    
- SSL termination
    
- Name-based virtual hosting
    
- URI routing
    
    (e.g. `/api`→`api-service`, `/static`→`assets-service`)

## Ingress extended features

(Not always supported; supported through annotations, CRDs, etc.)

- Routing with other headers or cookies
    
- A/B testing
    
- Canary deployment
    
- etc.

## Principle of operation

- Step 1: deploy an _ingress controller_
    
    (one-time setup)
    
- Step 2: create _Ingress resources_
    
    - maps a domain and/or path to a Kubernetes Service
        
    - the controller watches ingress resources and sets up a LB
        
- Step 3: set up DNS
    
    - associate DNS entries with the load balancer address



# Volumes

- Volumes are special directories that are mounted in containers
    
- Volumes can have many different purposes:
    
    - share files and directories between containers running on the same machine
	    - access logs from a container
        
    - share files and directories between containers and their host
        
    - centralize configuration information in Kubernetes and expose it to containers
	    - 
        
    - manage credentials and secrets and expose them securely to containers
	    - to talk about configuration we need to talk about volumes first
        
    - store persistent data for stateful services
        
    - access storage systems (like Ceph, EBS, NFS, Portworx, and many others)
        

## Volumes not equal to Persistent Volumes

- Volumes and Persistent Volumes are related, but very different!
    
- _Volumes_:
    
    - appear in Pod specifications (we'll see that in a few slides)
        
    - do not exist as API resources (**cannot** do `kubectl get volumes`)
        
- _Persistent Volumes_:
    
    - are API resources (**can** do `kubectl get persistentvolumes`)
        
    - correspond to concrete volumes (e.g. on a SAN, EBS, etc.)
        
    - cannot be associated with a Pod directly; but through a Persistent Volume Claim
        
    - won't be discussed further in this section



Volumes exist in pods, they are not a Kubernetes Resource


Persistent volumes exists in the Kubernetes API


## Adding a volume to a Pod

- We will start with the simplest Pod manifest we can find
    
- We will add a volume to that Pod manifest
    
- We will mount that volume in a container in the Pod
    
- By default, this volume will be an `emptyDir`
    
    (an empty directory)
    
- It will "shadow" the directory where it's mounted


Volumes are special directories