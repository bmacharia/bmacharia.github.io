# Lets start with a Simple App


First I will start with a simple Python application, It will be a demo application to play around with, what I want to accomplish or better yet explore are

- Docker Image layers
- The size of the image


To get started I will be utilizing `uv` which is a Python package and project manager. I will use it to quickly get a simple python project setup quickly for demonstration purposes. The link to the `uv` documentation is [uv](https://docs.astral.sh/uv/)

```bash
	# uv init is the command and demo is the name of the project
	uv init demo
```

The following is the output of the `uv` command

![[out-put-of-uv-command.png]]

Now what I want to do is containerize this very important python application, wink, wink!

The first thing to do is create a `Dockerfile` with the following contents

```bash

FROM python:latest

WORKDIR /app

COPY . /app

CMD ["python", "main.py"]
```

With a Dockerfile I can now build a docker image. The command to to build a docker image is `docker build`

In this case the command to build the docker image in this demonstration is

```bash

	docker build -t demo:01 .
```
This command builds a docker image and tags is the the `-t` flag with the name `demo:01`  the `.` means in the current directory

With the docker image built, I can list all the images that I have on my machine with the command `docker image list` 

``` bash
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
demo         01        6b043c05f1a4   46 seconds ago   1.02GB


```

The above is the out of the `docker image list ` command. As I can see the the size of the image is `1.02GB`. What a beefy image!

To run the the containerized application the command to do that is `docker run demo:01`. The app is as simple as it comes, it just prints some statements to the console

```bash
docker run demo:01

Hello from demo!
Lets Build Some Images
Having to Much Fun With Docker
```

## So How do these layers look like?

To inspect the image layers, I can use the `docker image inspect` command. The output of this command is tremendous, so I will not include here, but take my word for it, it will show all the intimate details of the docker image. In my opinion the most interesting info outputted from the docker command is the `Layers` section. To inspect the layers section, to get a better look at the contents of each layer, I can use the command `docker history demo:01`. The output of this command is below

```shell
IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
6b043c05f1a4   15 minutes ago   CMD ["python" "main.py"]                        0B        buildkit.dockerfile.v0
<missing>      15 minutes ago   COPY . /app # buildkit                          34.9kB    buildkit.dockerfile.v0
<missing>      15 minutes ago   WORKDIR /app                                    0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      CMD ["python3"]                                 0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      RUN /bin/sh -c set -eux;  for src in idle3 p…   36B       buildkit.dockerfile.v0
<missing>      2 weeks ago      RUN /bin/sh -c set -eux;   wget -O python.ta…   70.7MB    buildkit.dockerfile.v0
<missing>      2 weeks ago      ENV PYTHON_SHA256=40f868bcbdeb8149a3149580bb…   0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      ENV PYTHON_VERSION=3.13.3                       0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      ENV GPG_KEY=7169605F62C751356D054A26A821E680…   0B        buildkit.dockerfile.v0
<missing>      2 weeks ago      RUN /bin/sh -c set -eux;  apt-get update;  a…   17.8MB    buildkit.dockerfile.v0
<missing>      2 weeks ago      ENV PATH=/usr/local/bin:/usr/local/sbin:/usr…   0B        buildkit.dockerfile.v0
<missing>      16 months ago    RUN /bin/sh -c set -ex;  apt-get update;  ap…   588MB     buildkit.dockerfile.v0
<missing>      16 months ago    RUN /bin/sh -c set -eux;  apt-get update;  a…   177MB     buildkit.dockerfile.v0
<missing>      2 years ago      RUN /bin/sh -c set -eux;  apt-get update;  a…   48.4MB    buildkit.dockerfile.v0
<missing>      2 years ago      # debian.sh --arch 'amd64' out/ 'bookworm' '…   117MB     debuerreotype 0.15

```


## Adding Layers

Let us add some more layers, because at over 1GB is size is not big enough.  To add more layers to this docker image, I have to go back to the Dockerfile and add more stuff. Not very technical, I am very aware of that!!


```Dockerfile
FROM python:latest
WORKDIR /app

# Add some silly layers
RUN touch file1.txt
RUN echo "hello" > file2.txt
RUN mkdir -p /app/test

COPY . /app

CMD ["python", "main.py"]

```


With our beautiful new Dockerfile, we build a new image!!

```bash
docker build -t demo:02 .
```


To inspect the new docker image I can use the 

```bash
docker history demo:01 # original image
docker history demo:02 Image with addotional layers
	
```


That is it for now, stay tuned for more because there will be more!