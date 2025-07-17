
## What is Kubernetes

Running a container on a laptop is relatively simple. But, connecting containers across multiple hosts, scaling them, deploying applications without downtime, and service discovery among several aspects can be difficult. 

Kubernetes addresses those challenges from start with a set of primitives open and extensible API. The ability to add new objects and controllers allows easy customization for various needs.

According the the [kubernetes.io](https://kubernetes.io/) website, Kubernetes is:

*"an open source software for automating deployment, scaling, and management of containerized applications"*


## Monolithic vs Many Small Applications

In a traditional/legacy environment, an application (such as a webserver) would be placed on a dedicated server. As the webserver traffic increases, the application would be tuned, and perhaps moved to a different machine with larger and more powerful hardware. As time passes, a lot of cutomization may have been done in order to meet the current web traffic needs.

In contrast Kubernetes approached the same issue by deploying many small applications, or mircoservices. Each mircoservice should be written such that to expect many possible agents available to respond to a request.  It is also important that each microservice expects others to die and eventually be replaced, leading to a transient sever deployment. For, example instead of a large Apache web server responding to page requests, multiple Nginx servers would respond to page requests with a different microservice handing authentication
	
## Challenges

Containers provide a great way to package, ship, and run applications - that is the Docker motto.

The developer experience has been boosted tremendously thanks to containers. Containers have empowered developers with ease of building container images, simplicity of sharing images via registries, and providing a powerful user experience to manage containers.

However, managing containers at scale and designing a secure distributed application based on microservices' principles may be challenging.

A smart early step is deciding on a continuous integration/continuous delivery (CI/CD) pipeline to build, test and verify container images. Tools such as Spinnaker, Jenkins and Helm can be helpful to use, among other possible tools. This will help with the challenges of a dynamic environment and ensure containers meet minimum requirements.

Then, you need a cluster of machines on which to run your containers. You also need a system to launch your containers, and watch over them when things fail and replace as required. Rolling updates and easy rollbacks of containers is an important feature, and eventually tear down the resource when no longer needed.

All of these actions require flexible, scalable, and easy-to-use network and storage.​ As containers are launched on any worker node, the network must connect the resource to other containers, while still keeping the traffic secure from others. We also need a storage structure which provides and keeps or recycles storage in a seamless manner.

When Kubernetes answers these concerns, one of the biggest challenges to adoption is the applications themselves, running inside the container. They need to be written, or re-written, to be truly transient, decoupled microservices. A good question to ponder: If you were to deploy Chaos Monkey, which could terminate any containers at any time, would your customers

## Kubernetes Architecture

![[Pasted image K8s Architecture.png]]

In its simplest form, Kubernetes is made of one or three control plane nodes (aka **cp** nodes) and many worker nodes. The **cp** runs an API server, a scheduler, various operators and a storage system to keep the persistent state of the cluster, container settings, and the networking configuration.

Kubernetes exposes an API via the API server. You can communicate with the API using a local client called **kubectl** or you can write your own client and use curl commands. The **kube-scheduler** is forwarded the pod spec for running containers coming to the API and finds a suitable node to run those containers. Each node in the cluster runs two processes: a **kubelet**, which is often a `systemd` process, not a container, and **kube-proxy. The **kubelet** receives the **podSpec** to run the containers, manages and downloads any resources necessary, and works with the local container engine to manage them on the local node. The local container engine could be **containerd** or some other.

The **kube-proxy** works with the network plugin to create and manage networking rules which may expose the container on the network to other containers inside the cluster or the outside world.

## Terminology

Now that we have seen some basic architecture, it may be helpful to cover some terminology. We will work with these objects in the course, but hearing about them now may help us absorb how they fit in the larger environment.

We have learned that Kubernetes is an orchestration system to deploy and manage containers. Containers are not managed individually; instead, they are tracked as an object called a Pod. A Pod consists of one or more containers which share an IP address, access to storage and namespace. Typically, one container in a Pod runs an application; if there are other containers, they support the primary application.

Kubernetes uses namespaces to keep objects distinct from each other, for resource control and multi-tenant considerations. Some objects are cluster-scoped, others are scoped to one namespace at a time. As the namespace is a segregation of resources, pods would need to leverage services to communicate to other namespaces.

Orchestration is managed through a series of watch-loops, or operators. Each operator interrogates the kube-apiserver for a particular object state and spec. If the state and spec don't match, the operator will act until the declared state matches the current state. Several controllers are compiled into the kube-controller-manager, but others can be added using Custom Resource Definitions (CRDs). The default and feature-filled operator for containers is a Deployment. A Deployment does not directly work with pods. Instead it manages ReplicaSets. The ReplicaSet is an operator which will create or terminate pods according to a podSpec. The podSpec is sent to the kubelet, which then interacts with the container engine to download and make available the required resources, then spawn or terminate containers until the status matches the spec.

The service operator requests existing IP addresses and information from the endpoint operator, and will manage the network connectivity based on labels. A service is used to communicate between pods, namespaces, and outside the cluster.

To easily manage thousands of Pods across hundreds of nodes could be difficult. To make management easier, we can use labels, arbitrary strings which become part of the object metadata. These can then be used when checking or changing the state of objects without having to know individual names or UIDs. Nodes can have taints to discourage Pod assignments, unless the Pod has a toleration in its metadata.

## Main Components of Kubernetes

Kubernetes has the following main components:

- Control plane(s) and worker node(s)
- Operators
- Services
- Pods of containers
- Namespaces and quotas
- Network and policies
- Storage


A Kubernetes cluster is made of one or more **control plane** node and a set of **worker nodes**. The cluster is all driven via API calls to operators. A network plugin helps handle both interior as well as exterior traffic. We will take a closer look at these components next.

Most of the processes are executed inside a container. There are some differences, depending on the vendor and the tool used to build the cluster.

When upgrading a cluster, be aware that each of these components are developed to work together by multiple teams. Care should be taken to ensure a proper match of versions. The kubeadm upgrade plan command is useful to discover this information.

## Control Plane Node

Control Plane Node
The Kubernetes cp runs various server and manager processes for the cluster. As the software has matured, new components have been created to handle dedicated needs, such as the cloud-controller-manager; it handles tasks once handled by the kube-controller-manager to interact with other tools, such as Rancher or DigitalOcean for third-party cluster management and reporting.

There are several add-ons which have become essential to a typical production cluster, such as DNS services. Others are third-party solutions where Kubernetes has not yet developed a local component, such as cluster-level logging and resource monitoring.

As a concept, the various pods responsible for ensuring the current state of the cluster matches the desired state are called the control plane.

When building a cluster using kubeadm, the kubelet process is managed by systemd. Once running, it will start every pod found in /etc/kubernetes/manifests/.

Components of the Control Plane

### kube-apiserver


The **kube-apiserver** is central to the operation of the Kubernetes cluster. All calls, both internal and external traffic, are handled via this agent. All actions are accepted and validated by this agent, and it is the only connection to the etcd database. It validates and configures data for API objects, and services REST operations. As a result, it acts as a cp process for the entire cluster, and acts as a frontend of the cluster's shared state.

Starting as a beta feature in v1.18, the Konnectivity service provides the ability to separate user-initiated traffic from server-initiated traffic. Until these features are developed, most network plugins commingle the traffic, which has performance, capacity, and security ramifications.

### kube-scheduler

The **kube-scheduler** uses an algorithm to determine which node will host a Pod of containers. The scheduler will try to view available resources (such as volumes) to bind, and then try and retry to deploy the Pod based on availability and success. There are several ways you can affect the algorithm, or a custom scheduler could be used instead. You can also bind a Pod to a particular node, though the Pod may remain in a pending state due to other settings. One of the first settings referenced is if the Pod can be deployed within the current quota restrictions. If so, then the taints and tolerations, and labels of the Pods are used along with the metadata of the nodes to determine the proper placement.

### etcd Database

The state of the cluster, networking, and other persistent information is kept in an etcd database, or, more accurately, a b+tree key-value store. Rather than finding and changing an entry, values are always appended to the end. Previous copies of the data are then marked for future removal by a compaction process. It works with curl and other HTTP libraries, and provides reliable watch queries.

Simultaneous requests to update a value all travel via the kube-apiserver, which then passes along the request to etcd in a series. The first request would update the database. The second request would no longer have the same version number, in which case the kube-apiserver would reply with an error 409 to the requester. There is no logic past that response on the server side, meaning the client needs to expect this and act upon the denial to update. 

There is a Leader database along with possible followers, or non-voting Learners who are in the process of joining the cluster. They communicate with each other on an ongoing basis to determine which will be the Leader, and determine another in the event of failure. While very fast and potentially durable, there have been some hiccups with new tools, such as kubeadm, and features like whole cluster upgrades.

While most Kubernetes objects are designed to be decoupled, a transient microservice which can be terminated without much concern etcd is the exception. As it is, the persistent state of the entire cluster must be protected and secured. Before upgrades or maintenance, you should plan on backing up etcd. The etcdctl command allows for snapshot save and snapshot restore.

### Other Agents


The kube-controller-manager is a core control loop daemon which interacts with the kube-apiserver to determine the state of the cluster. If the state does not match, the manager will contact the necessary controller to match the desired state. There are several operators in use, such as endpoints, namespace, and replication. The full list has expanded as Kubernetes has matured.

Remaining in beta since v1.11, the cloud-controller-manager (ccm) interacts with agents outside of the cloud. It handles tasks once handled by kube-controller-manager. This allows faster changes without altering the core Kubernetes control process. Each kubelet must use the --cloud-provider-external settings passed to the binary. You can also develop your own ccm, which can be deployed as a daemonset as an in-tree deployment or as a free-standing out-of-tree installation. The cloud-controller-manager is an optional agent which takes a few steps to enable. You can learn more about the cloud-controller-manager online.

Depending on which network plugin has been chosen, there may be various pods to control network traffic. To handle DNS queries, Kubernetes service discovery, and other functions, the CoreDNS server has replaced kube-dns. Using chains of plugins, one of many provided or custom written, the server is easily extensible.


## Worker Nodes


All nodes run the kubelet and kube-proxy, as well as the container engine, such as containerd or cri-o, among several options. Other management daemons are deployed to watch these agents or provide services not yet included with Kubernetes.

The kubelet interacts with the underlying container engine also installed on all the nodes, and makes sure that the containers that need to run are actually running. The kube-proxy is in charge of managing the network connectivity to the containers. It does so through the use of iptables entries. It also has the userspace mode, in which it monitors Services and Endpoints using a random port to proxy traffic via ipvs. A network plugin pod, such as cilium-xxxxx, may be found depending on the plugin in use.

Each node could run in a different engine. It is likely that Kubernetes will support additional container runtime engines.

Kubernetes does not have cluster-wide logging yet. Instead, another CNCF project is used, called Fluentd. When implemented, it provides a unified logging layer for the cluster, which filters, buffers, and routes messages.

Cluster-wide metrics is another area with limited functionality. The metrics-server SIG provides basic node and pod CPU and memory utilization. For more metrics, many use the Prometheus project.

## Kubelet

The kubelet systemd process is the heavy lifter for changes and configuration on worker nodes. It accepts the API calls for Pod specifications (a PodSpec is a JSON or YAML file that describes a pod). It will work to configure the local node until the specification has been met.

Should a Pod require access to storage, Secrets or ConfigMaps, the kubelet will ensure access or creation. It also sends back status to the kube-apiserver for eventual persistence. ​

- Uses PodSpec
- Mounts volumes to Pod
- Downloads secrets
- Passes request to local container engine
- Reports status of Pods and node to cluster

Kubelet calls other components such as the Topology Manager, which uses hints from other components to configure topology-aware resource NUMA assignments such as for CPU and hardware accelerators. As an alpha feature, it is not enabled by default.

## Operators 

An important concept for orchestration is the use of operators, otherwise known as controllers or watch-loops. Various operators ship with Kubernetes, and you can create your own, as well. A simplified view of an operator is an agent, or Informer, and a downstream store. Using a DeltaFIFO queue, the source and downstream are compared. A loop process receives an obj or object, which is an array of deltas from the FIFO queue. As long as the delta is not of the type Deleted, the logic of the operator is used to create or modify some object until it matches the specification.

The Informer which uses the API server as a source requests the state of an object via an API call. The data is cached to minimize API server transactions. A similar agent is the SharedInformer; objects are often used by multiple other objects. It creates a shared cache of the state for multiple requests.

A Workqueue uses a key to hand out tasks to various workers. The standard Go work queues of rate limiting, delayed, and time queue are typically used. 

The endpoints, namespace, and serviceaccounts operators each manage the eponymous resources for Pods. Deployments manage replicaSets, which manage Pods running the same podSpec, or replicas.

## Service Operator

With every object and agent decoupled we need a flexible and scalable agent which connects resources together and will reconnect, should something die and a replacement is spawned. A service is an operator which listens to the endpoint operator to provide a persistent IP for Pods. Pods have ephemeral IP addresses chosen from a pool. 

Then the service operator sends messages via the kube-apiserver which forwards settings to kube-proxy on every node, as well as the network plugin such as cilium-agent.

A service also handles access policies for inbound requests, useful for resource control, as well as for security.

- Connect Pods together
- Expose Pods to Internet
- Decouple settings
- Define Pod access policy

## Pods

The whole point of Kubernetes is to orchestrate the lifecycle of a container. We do not interact with particular containers. Instead, the smallest unit we can work with is a Pod. Some would say a pod of whales or peas-in-a-pod. Due to shared resources, the design of a Pod typically follows a one-process-per-container architecture.

Containers in a Pod are started in parallel. As a result, there is no way to determine which container becomes available first inside a pod. The use of InitContainers can order startup, to some extent. To support a single process running in a container, you may need logging, a proxy, or special adapter. These tasks are often handled by other containers in the same pod.

There is only one IP address per Pod, for almost every network plugin. If there is more than one container in a pod, they must share the IP. To communicate with each other, they can either use IPC, the loopback interface, or a shared filesystem.

While Pods are often deployed with one application container in each, a common reason to have multiple containers in a Pod is for logging. You may find the term sidecar for a container dedicated to performing a helper task, like handling logs and responding to requests, as the primary application container may not have this ability. The term sidecar, like ambassador and adapter, does not have a special setting, but refers to the concept of what secondary pods are included to do.

## Containers


While Kubernetes orchestration does not allow direct manipulation on a container level, we can manage the resources containers are allowed to consume. 

In the resources section of the PodSpec you can pass parameters which will be passed to the container runtime on the scheduled node: 

```yaml

resources:
  limits: 
    cpu: "1"
    memory: "4Gi" 
  requests:
    cpu: "0.5"
    memory: "500Mi"

```


Another way to manage resource usage of the containers is by creating a **ResourceQuota** object, which allows hard and soft limits to be set in a namespace. The quotas allow management of more resources than just CPU and memory and allows limiting several objects. 


The **scopeSelector** field in the quota spec is used to run a pod at a specific priority if it has the appropriate **priorityClassName** in its pod spec.

## Init Containers

Not all containers are the same. Standard containers are sent to the container engine at the same time, and may start in any order. LivenessProbes, ReadinessProbes, and StatefulSets can be used to determine the order, but can add complexity. Another option can be an Init container, which must complete before app containers will be started. Should the init container fail, it will be restarted until completion, without the app container running.

The init container can have a different view of the storage and security settings, which allows utilities and commands to be used, which the application would not be allowed to use. Init containers can contain code or utilities that are not in an app. It also has an independent security from app containers.

The code below will run the init container until the ls command succeeds; then the database container will start.


```yaml

spec:
  containers:
  - name: main-app
    image: databaseD 
  initContainers:
  - name: wait-database
    image: busybox
    command: ['sh', '-c', 'until ls /db/dir ; do sleep 5; done; '] 


```



## Component Review

Now that we have seen some of the components, let's take another look with some of the connections shown. Not all connections are shown in the diagram below. Note that all of the components are communicating with kube-apiserver. Only kube-apiserver communicates with the etcd database.


![[Pasted image K8s Architecture Review.png]]


We also see some commands, which we may need to install separately to work with various components. There is an **etcdctl** command to interrogate the database and **cilium** to view more of how the network is configured