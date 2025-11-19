

isolated view of the of the filesystem from inside the container

build a container only using stock Linux tools

`unshare`, `mount`, and `pivot_root` the `mount namescape` is the bedrock of container isolation, while the other namespaces such as **PID**, **cgroup**, **UTS**, and **network**

So the goal is to spin up docker containers using nothing but standard Linux commands

So there is a the host that Docker is running 


namespaces overview of Linux namespaces

-- A namespace wraps a global system resource in an abstraction  that makes it appear to the processes withing that namespace that they have their own isolated instance of the global resource

--unshare() allows a process to disassociate parts of its execution context that are currently being shared with other processes


The main use of `unshare()` is allow a process to control its shared execution context without creating a new process



## Preparing container rootfs

```bash

sudo mkdir -p /opt/container-1/rootfs
```

### Mount Namespcae

`mnt` it provides the process with an isolated view of the filesystem, it can be used so that a process does not interfere with the files of another process that is currently using them. The mount namespace a new set of mounts is provided for the process instead of the default

### PID Namespace

PID namespace allows a process to have an isolated view of other processes running on the host. PID namespcae is used so that the contained process can see and affet processes that are part of the contained application. The command `nsenter` shows a list f processes running inside the container


### Network namespace

This namespace is responsible for providing a process's network environment(interface, routing). It is useful for ensuring container processe can bind the ports they need without interfering with each other

### Cgroup namepsace

Control groups are designed to help control a process's resources usage on a Linux system. They are used to reduce the risk of noisy neighbors (containers that use so much of system resources that they degrade the entire performance of other containers on the same host)


### Linux Capabilities

Linux Capabilities split up monolithic root privilege into more granular premissions to processes and files