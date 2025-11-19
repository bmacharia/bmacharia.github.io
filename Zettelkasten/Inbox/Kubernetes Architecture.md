
Kubernetes is an abstraction layer that sits on top of raw comput primitives VM's or bare metal machines. The  VM's are reffered to as nodes and are arrancged into a clustet that represents the platform to deploy containerized applications

Containers are grouped together into a schduling unit knows as a pod

Networking is a service in the world of kubernetes

Deployments allow for the ease of management of 

The POD is the primary scheduling unit in kubernetes, it is the unit of compute. A Pod is a logical grouping of containers. Kubernetes binds the containers together


Remember that a container is an isolated execution environment

encompass the application into a unit fof compute and that unit of compute is scheduled into a container and deployed to the cluster where the application is managed by kubernetes

The POD is wrapped into a higher order object that manages the deployment

When a cluster is created and I have access to the cluster then i can use the kubectl command to interact with the kube-apiserver.

Kubernetes uses declarative configuration, where one declares the state that I want, then that config is submitted to the cluster and kubernetes does its very best to create the desired state 


```bash
## Query the deploymnet, shows curtent status and how many of the pods are ready to serve traffic

kubectl get pods
```

```bash
# to see more details about the pods that form the deployent query the pods themselves

kubectl get pods
```

after the deployment is issued to the cluster, it takes time to provision new compute capacity, when things ate up it will report a status of ready