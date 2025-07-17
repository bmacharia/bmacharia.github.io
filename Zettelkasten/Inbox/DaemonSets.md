
What is a DaemonSet in the Kubernetes ecosystem

- it is a watch loop object like a  deployment
- it ensures that when a node is added to a cluster a pod will be created on the cluster
- A deployment makes sure a number of pods are created
- DaemonSet ensures applications are on each node
- this is helpful for things like metrics and logging in large clusters
- if a node is removed from a cluseter the Pods are garbage collected