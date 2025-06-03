

## What is Trivy?

Straight off the Trivy website https://trivy.dev/latest/ , Trivy is used to find vulnerabilities  (CVE) & configurations (IaC) across code repositories, binary artifacts, container images, Kubernetes clusters, and more!

### What is a CVE?

Great question! First of all CVE is short for **Common Vulnerabilities and Exposures.** It is a list of publicly disclosed computer security flaws. Each CVE is issued an ID, and in short CVEs help IT professionals coordinate their efforts to prioritize and addressed  these vulnerabilities to make computer systems as secure as possible


## Getting started with Trivy

I will be using Trivy to scan container images for CVEs. Trivy is a command-line application. What trivy will do is pull in a database of CVEs and scan my container images against the database, and tell me everything wrong with my image

The container image that I will be scanning is quite large. Generally speaking the larger the image, the larger the attack surface, and as a result the more CVE vulnerabilities. 

```shell
docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
backend      00        e48cc776d20c   31 minutes ago   1.09GB

```


To scan my container image I will use the following command

```shell
TAG=00 && trivy image --format table --severity CRITICAL,HIGH backend:$TAG
```

Trivy will scan my container image and the out out will be in the form of a table
below is a snippet of the scan result

```shell
Total: 146 (HIGH: 141, CRITICAL: 5)

┌───────────────────┬────────────────┬──────────┬──────────────┬─────────────────────────┬───────────────┬──────────────────────────────────────────────────────────────┐
│      Library      │ Vulnerability  │ Severity │    Status    │    Installed Version    │ Fixed Version │                            Title                             │
├───────────────────┼────────────────┼──────────┼──────────────┼─────────────────────────┼───────────────┼──────────────────────────────────────────────────────────────┤
│ icu-devtools      │ CVE-2025-5222  │ HIGH     │ affected     │ 72.1-3                  │               │ icu: Stack buffer overflow in the SRBRoot::addTag function   │
│                   │                │          │              │                         │               │ https://avd.aquasec.com/nvd/cve-2025-5222                    │
├───────────────────┼────────────────┼──────────┤              ├─────────────────────────┼───────────────┼──────────────────────────────────────────────────────────────┤
│ libaom3           │ CVE-2023-6879  │ CRITICAL │              │ 3.6.0-1+deb12u1         │               │ aom: heap-buffer-overflow on frame size change               │
│                   │                │          │              │                         │               │ https://avd.aquasec.com/nvd/cve-2023-6879                    │
│                   ├────────────────┼──────────┼──────────────┤                         ├───────────────┼──────────────────────────────────────────────────────────────┤
│                   │ CVE-2023-39616 │ HIGH     │ will_not_fix │                         │               │ AOMedia v3.0.0 to v3.5.0 was discovered to contain an        │
│                   │                │          │              │                         │               │ invalid read mem...                                          │
│                   │                │          │              │                         │               │ https://avd.aquasec.com/nvd/cve-2023-39616                   │
├───────────────────┼────────────────┤          ├──────────────┼─────────────────────────┼───────────────┼──────────────────────────────────────────────────────────────┤
│ libbluetooth-dev  │ CVE-2023-44431 │          │ fix_deferred │ 5.66-1+deb12u2          │               │ bluez: AVRCP stack-based buffer overflow remote code         │
│                   │                │          │              │                         │               │ execution vulnerability                                      │
│                   │                │          │              │                         │               │ https://avd.aquasec.com/nvd/cve-2023-44431                   │
│                   ├────────────────┤          │              │                       
```

To recall my current docker image size is over 1GB in size

```shell
docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED             SIZE
backend      00        e48cc776d20c   About an hour ago   1.09GB
```

My current Dockerfile is as follows

```Dockerfile

FROM python:latest
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . /app

RUN uv sync --locked --no-editable

CMD ["uv", "run", "study-tracker-api"]

```

 As of now my Docker image is huge in size and full of CVEs.  The current base image of my Dockerfile is `FROM python:latest` this image contains an almost entire Operating Systems and tons of packages that I do not need. The easiet and quickest way to reduce image size is to use a different base image `python:3.13-slim`

```Dockerfile

# FROM python:latest
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . /app

RUN uv sync --locked --no-editable

CMD ["uv", "run", "study-tracker-api"]

```

With this one change I have reduced the image size by 800MB

```shell
docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
backend      01        ae9b526becd0   13 seconds ago   189MB
backend      00        e48cc776d20c   2 hours ago      1.09GB
```

Now that was simple. A best practice is to always use alpine images.
What is alpine? Alpine linux is a security-oriented, lightweight Linux distribution. To further slim down my container image I will use the `python:3.13-alpine image` 

```Dockerfile

#FROM python:latest
#FROM python:3.13-slim
FROM python:3.13-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . /app

RUN uv sync --locked --no-editable

CMD ["uv", "run", "study-tracker-api"]
```
	
Rebuilding my container image with the alpine image further reduced the size of my container over 70MB

```shell
docker image ls
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
backend      02        a381a5f768d1   3 seconds ago    114MB
backend      01        ae9b526becd0   16 minutes ago   189MB
backend      00        e48cc776d20c   2 hours ago      1.09GB


```


Just by changing the base image, the container image size went from 1.0GB to 114MB with very minimal work. Next I will explore further optimizations like multi-stage builds, and only add to the container image what is needed to run the application