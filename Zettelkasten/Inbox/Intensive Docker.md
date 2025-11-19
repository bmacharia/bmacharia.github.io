## First Containers

A Dockerfile is a recipe for building Docker images

Container Networking, how to expose containers and connect to them form the outside world

### Day 1


```bash
# -i IO input/output -t terminal
docker run -it ubuntu
```

treat containers as if they are programs running on the machine

the processes in the container are the processes running on that machine

```bash
# this command kills all the docker containers running on the machine
# do not do this on a production machine kiss your app goodbye
docker kill $(docker ps- q)
```

`docker ps -a`
 this command lists all docker containers on the machine
`docker rm` this command removes a docker container on the machine


## Understanding Docker Images


Images = files + metadata
these form the file-system of the the container

Metadata

- author of the image
- the command to execute in the container when starting it
- environment variables
- etc 

From a conceptual standpoint containers images are layers


### The read-write layers

can only write on the layers on top, the layers below, there ate only read only

Instead of writing on the original, you are writing on a copy

A new image is created by stacking a layer on the old image

DAEMON - Disk Asynchronous Execution MOn

docker run -d

On unix systems to stop a program there are two ways to stop a program

Graceful shutdown where we the program is allowed to finish a tasks, then shutdown, then there is the kill/stop the program immediately like right now, i do not care what you are doing

```bash
	# is a graceful shutdown, finihs what you are doinig and than stop 
docker stop
```

```bash
SIGTERM / KILL SIGKILL
```

```bash
# to list the last container that is running
docker ps -l
```

Change the signal that gets sent to the container, install custom handler in the container

- Kubernetes, pre stop hooks, programs to run before stopping the pod

View only the IDS of the containers

```bash
q = ("Quiet, Quick) no columns or headers in the output of the command
docker ps -q
```


If a program can run in a machine, then it can run in a container it is as simple as that, there will be differences in behavior


## Building Images Interactively

To understand to see how things work and to see more advanced docker commands


```bash
# docker diff shows the difference between the image and the container
docker diff eab # firs 3 letters of the sha of the image

```

### # uses cases of docker diff

- install something with a script and it installs something for you, run the script in the container and run the script and it shows you what was installed
- Security - take over the machine, run arbitrary code on a machine that has been hacked, it is a two step process, the bad person trying to get into the system

```bash
#the command docker commit turns a container into an image that can be used to create new containers from

docker commit
```


## Build a Docker Image

Use a Docker file, write a dockerfile and run the command

```bash
# the dot is the current directory of the dockerfile
docker build . -t figlet:dockerfile
```

```bash

--no-cache - build the image all over from scratch
--pull - this flag tries to update the base image
```

`CMD` the CMD directive in a docker file lets us define what should run when a container is started.

`ENTRYPOINT` defines a base command and its parameters for the container


## Copying files during the build

`COPY` when can copy files form the `build context` the directory of where the `Dockerfile` is located `hello.c`

```c
int main() {
	puts("hello, World!")
	return 0;
}
```


Create a directory and put a write a file named hello.c in the directory, the code needs to be compiled in the container

```Dockerfile
FROM ubuntu

# install C compiler
RUN apt-get update
RUN apt-get install build-essential

# copy hello.c to the container
COPY hello.c .

# compile hello..c to an executable
RUN gcc -o hello hello.c
# run the program 
CMD ./hello
```


the Docker builder in a non-interactive process, if the file has changed docker will invalidate the cache


Instead of putting everything with the system files, out the program files in their own directory

`.dockerignore` in a nutshell what if we want o copy eveyfile except some files we can use `.dockerignore` to prevent files that we do not want copied to end up in the container

in the `DOCKERFILE` the directive `WORKDIR` creates the directory inside the working container


### Dockerize the below applicatioin

# Let's containerize the wordsmith project!


The wordsmith project is split into 3 parts:

- web: frontend web server written in Go
- words: REST API written in Java, to query the DB
- db: PostgreSQL database containing the words to display

Our goal is to containerize this application.


## Exercise 1: Writing Dockerfiles

Our goal is to write Dockerfiles for the 3 containers.

First, `git clone` this repository. We need to create one
Dockerfile for each service. Pro tip: place each Dockerfile
in the corresponding directory (web, words, db).

The following paragraphs describe the installation instructions
for each service.

Note: in this first exercise, we only want to build the images
and check that they start correctly (`web` and `words` should display
a short message to indicate that they're running), but we're not
trying to run the whole application or to connect to the services.
This will come later.


### web

This is a web server written in Go. To compile Go code, we can
use the `golang` official image, or install Go packages in
any of the official base images.

The entire code is in a single
source file (`dispatcher.go`), and should be compiled like this:

```
go build dispatcher.go
```

This creates an executable named `dispatcher`, which should be
launched like this:

```
./dispatcher
Listening on port 80
```

The web server needs to access the `static` directory. This directory
must be a subdirectory of the current working directory when the
server is started.

Additional information:

- the server listens on port 80
- the Go compiler is only useful to build the server (not to run it)


### words

This is a REST API backend written in Java. It should be built with maven.

On a Debian or Ubuntu distribution, we can install Java and maven like this:

```
apt-get install maven
```

To build the program, we can invoke maven like this:

```
mvn verify
```

The result is a file named `words.jar`, located in the `target` directory.

The server should be started by running the following command,
in the directory where `words.jar` is located:

```
java -Xmx8m -Xms8m -jar words.jar
```

Additional information:

- the server listens on port 8080
- compilation requires `maven` (on most distributions, this will automatically install a JDK, which includes a Java compiler)
- execution doesn't require `maven` or a Java compiler; only the JRE (Java Runtime Environment) is necessary, and in Debian and Ubuntu it can be provided by the `default-jre` package


### db

This is a PostgreSQL database.

The database must be initialized with the schema (database and tables)
and the data (used by the application).

The file `words.sql` contains all the SQL commands necessary to create
the schema and load the data.

```
# cat words.sql
CREATE TABLE nouns (word TEXT NOT NULL);
CREATE TABLE verbs (word TEXT NOT NULL);
CREATE TABLE adjectives (word TEXT NOT NULL);

INSERT INTO nouns(word) VALUES
  ('cloud'),
  ('elephant'),
  ('gø language'),
  ('laptøp'),
  ('cøntainer'),
  ('micrø-service'),
  ('turtle'),
  ('whale'),
  ('gøpher'),
  ('møby døck'),
  ('server'),
  ('bicycle'),
  ('viking'),
  ('mermaid'),
  ('fjørd'),
  ('legø'),
  ('flødebolle'),
  ('smørrebrød');

INSERT INTO verbs(word) VALUES
  ('will drink'),
  ('smashes'),
  ('smøkes'),
  ('eats'),
  ('walks tøwards'),
  ('løves'),
  ('helps'),
  ('pushes'),
  ('debugs'),
  ('invites'),
  ('hides'),
  ('will ship');

INSERT INTO adjectives(word) VALUES
  ('the exquisite'),
  ('a pink'),
  ('the røtten'),
  ('a red'),
  ('the serverless'),
  ('a brøken'),
  ('a shiny'),
  ('the pretty'),
  ('the impressive'),
  ('an awesøme'),
  ('the famøus'),
  ('a gigantic'),
  ('the gløriøus'),
  ('the nørdic'),
  ('the welcøming'),
  ('the deliciøus');
```

Additional information:

- we strongly suggest using the official PostgreSQL image that can
  be found on the Docker Hub (it's called `postgres`)
- if we check the [page of that official image](https://hub.docker.com/_/postgres) on the Docker Hub, we
  will find a lot of documentation; the section "Initialization scripts"
  is particularly useful to understand how to load `words.sql`
- it is advised to set up password authentication for the database; but in this case, to make our lives easier, we will simply authorize all connections (by setting environment variable `POSTGRES_HOST_AUTH_METHOD=trust`)


## Exercise 2: Optimizing image size

Now, we want to optimize image size.

We can use multi-stage builds, or leverage images based on Alpine.

Here are some targets:

- for `web`, 100 MB is a good result, andd 10 MB is a very good result;
- for `words`, 200 MB is a good result, and 50 MB is a very good result;
- for `db`, 300 MB is a good result.


## Exercise 3: Optimizing build time

We want to ensure that for `web` and `words`, build time remains short when we edit the code. To test code changes, even if you don't know Go or Java, you can update the message that is printed when the server starts.

Our target is to make sure that image build time remains below 10 seconds.


## Exercise 4: Writing a Compose file

When the 3 images build correctly, we can move on and write the Compose
file. We suggest placing the Compose file at the root of the repository.

At this point, we want to make sure that services can communicate
together, and that we can connect to `web`.

Note: the `web` service should be exposed.


## Exercise 5: Compose in dev mode

We want to tweak the Compose file so that it's possible to edit HTML and CSS files in `web` (in the `static` directory) without having to rebuild and restart the container after each change.


## Exercise 6: Deploying multiple stacks with Compose

Now we want to deploy the wordsmith app multiple times side-by-side on the same machine, with minimal effort. Specifically, deploying a new instance of the app should only require to create a new file of a few lines, and a standard `docker compose up` invocation.


## Exercise 7: Kubernetes

We want to deploy wordsmith on Kubernetes, and connect to the web interface from the outside.

We will need to use images hosted on a registry. For our convenience, the images are available on:

- jpetazzo/wordsmith-db:latest
- jpetazzo/wordsmith-words:latest
- jpetazzo/wordsmith-web:latest

Useful reminders for this exercise:

- service `web` is listening on port 80, and we want it to be reachable
  from outside the cluster
- service `words` is listening on port 8080
- service `db` is listening on port 5432


In docker parsing of the command line is off shored to the shell

## Container Network Model

A set of concepts when manipulating a group of containers

- Create a private network for a group of containers
- Use container naming to connect services together 
- Dynamically connect and disconnect containers to networks
- Set IP address of a container


In docker new networks can be created with the command

`docker network create` 

Docker has networks and to list those networks use the command

```bash
# list docker networks

docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
a341a3831980   bridge    bridge    local
12dee0812088   dev       bridge    local
6f1254b39f89   host      host      local
dd6cd40acc83   none      null      local
954182ed87ad   prod      bridge    local
```


a bridge network is a virtual switch in the computer and use this virtual switch to connect containers together

On each docker network we have a different subnet a different subnet in each address



### Service Discovery


it is not a good idea to hardcode the database ip address

```bash
# tell docker to run the image connect it to the network with a network alias name
docker run --net my_little_network_ --net-alias db my-data-base-image
```

in the docker engine there is a dynamic DNS server

DNS is the thing that maps names to ip addresses

```bash
docker run --net dev --net-alias api -d nginx
```

The network alias is local to the network

names ---> addresses

in kubernetes names ----> Cluster IP (kind of like a load balancer)


Service discovery based on DNS

To find the IP address of a container run the command

```bash
docker inspect --format '{{. Networksettings.IPAddress }}' <yourContainerID>
```


Say you have one linux machine running docker, you can have multiple docker networks each isolated from one another, there is no direct connection between containers belonging to different networks, Containers must use published ports. Containers can be connected to multiple networks if needed

User and programs running on the machine can access containers using internal IP addresses even if ports are not published


### CNM vs. CNI


In Kuberenetes you have on big network and all the containers are on the same network. You can add isolation by providing Netowrking policies


In Docker we have network isolation by default


## Compose for development stacks

Dockerfile = great to build one container image


## Tips for effiecient Dockerfiles

- Reduce the number of layers
- Leverage the build cache so that builds can be faster
- embed unit testing in the build process



### Reducing the number of Layers

- Each  line in a Dockerfile create a new layer
- Build `Dockerfile` to take advatage of DOcker's caching system
- Combine commands by using `&&` to continue commands and `\` to wrap lines

