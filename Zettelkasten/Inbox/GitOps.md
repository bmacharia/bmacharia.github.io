

The delivery process?  Delivery entail that something is being delivered, it is going from one place to a final destination? Code is being delivered from staging to production, staging is an environment that code changes are located and stored before it is moved into production, which is forward facing,meaning that it is in front of customers.

In GitOps infrastructure which is the the physical/virtual environment that the forward facing application is available to its intended users.

In terms if Kubernetes, one can think of Kubernetes as a platform to deploy containerized applications.

GitOps the source of truth is the repository where the code is located


on the cluster flux will be installed as a controller on the cluster, and it will be constantly looking at the repo for changes, if there are changes, this is the event that will cause the Flux to put the cluster into the state that is defined in the repo, Flux will implement the change of the cluster to the desired state defined in the GitHub repo. This is all done decoratively. the code delivery process is defined in git. And with this we will need access to the repo. I am managing the repo in code stored in the repo


Reconcile with git to the cluster

Merge a pull request, flux detects the change in the repo and updates the kubernetes cluster to the desired state according to the changes in the repo. not interacting with cluster via `kubectl`. the entire code delivery process is controlled via `Github`

Allows for history and collaboration, it allows for security because you no longer need access to the Kubernetes Api server

The Git repo is the source of truth, GitOps controller contantly looks at the repo for changes

### Kustomize

declarative management of kubernetes objects using kustomize


## Steps to Install FluxCD on a Kubernetes Cluster

1. Create a GitHub repo i will be using the github cli

```bash
# this is the command to create a repo from the command line
gh repo create
```

go through the steps to create the cluster
- give the repo a name
- an owner which in this case it is me
- give the repo a description Cluster for home lab 3 node cluster running on arm64 architecture






the repo is the source of truth