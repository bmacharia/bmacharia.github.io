[[Ephemeral Kubernetes Environments]]
### End to End Testing with k3d and Python

In a previous post [[Ephemeral Kubernetes Environments]] I explained a method for creating ephemeral Kubernetes Environments. Now it is time to see what kind of cool stuff we can do with our clusters.

Lets say we want to do some end to end testing. For example, say we want to define a bunch of test cases, when an application is running in Kubernetes. An example of that is to `curl`  a health end point to see if a container is actually running and not having any problems.



