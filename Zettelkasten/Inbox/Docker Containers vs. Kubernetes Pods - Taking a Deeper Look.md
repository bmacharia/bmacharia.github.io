

First of all I need to be thinking of abstractions

The container abstraction and the Kubernetes Pod abstraction

In Kubernetes the smallest deployable unit is a group of cohesive containers called a `Pod`


- Each Pod is assigned a unique IP address and a hostname
- Containers within a Pod can communicate with each other via localhost
- Each container in a POD gets an isolated file-system
- Cannot see processes of other containers of the same Pod

 I need to understand how Kubernetes Pods are implemented, what is the difference between a Pod and a container, and finally what would it take to create a Pod using standard Docker commands


First get a container up and running

```bash

docker run --name foo --rm -d --memory='512MB' --cpus='0.5' nginx:alpine


```


Resources and verbs, the Kubernetes API is RESTful

Keep in mind that a resource is a certain kind of object from a resource that is an instance of some kind of object, in the real world RESTful endpoints are called resources

There are different kinds of resources, types of kubernetes resources

resource types are organized into groups and each resource is versioned independently of each other


What is kind? In kubernetes a kind is a data structure it is an object schema.  A compositon of attributes and properties