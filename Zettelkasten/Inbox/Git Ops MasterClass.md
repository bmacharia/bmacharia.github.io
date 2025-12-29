777Deploy an application to a kubernetes cluster using flux and gitOps principles 


As of now the only thing that i have in my pico-cluster repo is the flux manifests

How yo go about deploying my application

Best practices for organizing my repo


```bash

└── staging
    └── flux-system
        ├── gotk-components.yaml
        ├── gotk-sync.yaml
        └── kustomization.yaml # this kustomization file is where eveything stems from here
        
 ```       


There is a flux-system directory with a kustomization.yaml, it is a way of templating and reading other files into a file


The name of my cluster is staging cluster, the name of the cluster was configure in the the flux bootstrap command 

in the `pico-cluster/clusters/staging/apps.yaml`

In the staging directory i will have an `apps.yaml` file

```yaml

# this file is a kustomizaton kustom resource
apiVersion: kustomize.config.k8s.io/v1
kind: Kustomization
metadata:
	name: apps
	namespace: flux-system
spec:
 interval: 10m0s
 retryInterval: 1m
 timeout: 5m
 sourceRef:
	kind: GitRepository
	name: flux-system
 path: ./apps/staging
 prune: true
```

The `apps.yaml` is referencing a git repo that is already living on the cluster. Kubernetes Custom Resource Definition, the yaml file is an object description.

Everything added to the `clusters/staging` directory will be picked up by the flux cd kustomization

I am applying a mono repo structure to the repository

.
├── apps
│   └── staging
├── clusters
│   └── staging
│       ├── apps.yaml
│       └── flux-system
│           ├── gotk-components.yaml
│           ├── gotk-sync.yaml
│           └── kustomization.yaml



I have a directory with `apps`, and within the apps directory I have a `staging`  directory

I have a clusters directory, that hold configuration for my clusters, and in that directory i have a directory named `staging` which is the name of the cluster, and in that directory I have an `apps.yaml` file


I will be soon putting a `base` directory in the `apps` directory. The `base` directory will hold applications that I will be running on the cluster


The whole point is to take a base object as a template and use a patch to configure the base object into a production object. This is done in a `kustomization.yaml` file that points to resources and reads those resources and applies it to the base to `kustomize` it


Kustomize as a layering mechanism for clusters. With patches we can replace things in the `kustomization.yaml` file

In the `aps.yaml` it is pointing at the `./apps/staging` directory. So what is in `./apps/staging`. In the `./apps/staging` there is a directory named `linkding` which is the name of the application that is being deployed to the cluster, and it that directory there is a file named `kustomization.yaml` that points the the `base` directory of the `linkding`

so far I have an `apps` directory, and a `clusters` directory. The `apps` directory is for the applications that will be deployed and, and the `clusters` directory will be the `clusters` name `staging, base, production`


The `kustomization.yaml` is in the `apps/staging`, in the `apps/staging` directory there is a `kustomization.yaml` file, that points to the `apps/base/linkding` directory, and in this directory are the resources, in the form of `yaml` files that define the objects and definitions of the application that will be deployed to the cluster

```text

I will leave off at the 42:42 min. mark of the video GitOps Masterclass
I left off at creating the resouces of the linkding application that I am deploying in the GitOps way, I created the files, but I have not put any contents in the files  BM 10/16/2025 17.02pm

```


`kustomization` files are like maps as they specify where to look and what to do

to check the status of `flux` I can use the command

`flux get kustmizations`