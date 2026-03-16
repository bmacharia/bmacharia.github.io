---
title: Docker Introduction Basics
tags: [docker, containers, devops]
description: An introduction to Docker — what it is, how it runs, and how to build your first image.
publish: true
---

# Docker

Docker is a tool that lets you package software into an image, and then run that image in an isolated environment called a container.

So why is this useful

- A docker image includes all the files you need to run an application
- All the OS system files, C libraries, the correct versions python for example 
- The Docker images know how to start the application
- And on top of that the application will run the exact same way

## How Docker Runs

Docker is a client/server application, the command line tool `docker`
sends commands to a server, `dockerd`


I can use a Docker Image to run a container

```bash
	# the docker run command is used to run a docker container
	docker run httpd:latest
	
```


## Running a container interactively

```bash
docker run --entrypoint=/bib/sh -it httpd:alpinr
```

The `--entrypoint`  argument means `run a different starting command than the default command`
What this argument allows is to have a shell prompt inside the running container.

Docker containers have isolated file systems, isolated processes, and isolated users

## Where does the container file system come from?

When you run a program on a computer you start with an executable files on the file-system, on disk, and use that file to create a process which is basically a running program. Multiple processes can be run from the same executable file.

One can think of a Docker as an executable file on disk, but instead one file, it is a whole file system, with everything needed to run the container. All the libraries, executable, and other files in a Linux file system to run the executable in a self container isolated execution .

A single image can create multiple containers, and each time a container is created, it gets a new complete and separate copy of the image file-system

## Minimal Docker Packaging

For this example I will create a program that i want to run

```bash
mkdir docker-image
cd docker-image
touch hello.py

```

```python
	# the contents of the hello.py file
from cosway import ghostbusters
ghostbusters("Who You Gonna Call")
 
```


```bash
python hello.py
```

To end the suspense this program does not run

```bash
Traceback (most recent call last):
  File "/home/laborant/docker-image/hello.py", line 1, in <module>
    from cosway import ghostbusters
ModuleNotFoundError: No module named 'cosway'
	


```

It fails because I need the library cosway, and this library is not part of the standard Python library.

This library needs to be installed in the Docker image. As stated earlier, a Docker image contains a complete file-system, In order to run `hello.py`, I will need

- A Python Interpreter
- The `cosway` library
- The file `hello.py`


The Docker image also includes instructions on what to do when the container/ application is run.


## The Base Image

to create an image what is needed is a files called a `Dockerfile`. The `Dockerfile` is akin to a recipe used by the `docker build` command

Lets start with a very simple `Dockerfile`

```Dockerfile
FROM python:3.11-slim


```


This command simply means build the Dockerfile in the current directory. The `.` means current directory

```bash

# to build a docker image simply

docker image build .
```


To label a docker image with a name

```bash

docker image build -t hello .
```

To See a list of docker images

```bash
docker image list
```


