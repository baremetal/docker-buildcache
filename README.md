Docker Build Cache
------------------

This utility breaks apart the Dockerfile into multiple, sub-Dockerfiles whenever
an `ADD` command is found.  Each `ADD` command is run as its own `Dockerfile` with
its `FROM` image being the image the previous sub-Dockerfile generated.

A hash of the file being `ADD`ed is generated to create a unique image tag name
in the form of `{{ last image id }}-{{ ADD file hash }}`.

If an image with this tag already exists, the image does not need to be rebuilt
and the existing image's ID is used for the next sub-Dockerfile.

Installation
============

```
pip install -e git://github.com/baremetal/docker-buildcache@master#egg=docker-buildcache
```

Example
=======

Consider the following `Dockerfile`:

```
FROM ubuntu:quantal
MAINTAINER Roberto Aguilar roberto@baremetal.io


# Add the Datastax APT repostiory and key
ADD files/etc/apt/sources.list.d/cassandra.list /etc/apt/sources.list.d/cassandra.list
ADD files/var/cache/baremetal/cassandra_repo_key /var/cache/baremetal/cassandra_repo_key
RUN cat /var/cache/baremetal/cassandra_repo_key | apt-key add -
RUN apt-get update

# Install Cassandra
RUN apt-get install -y dsc12 cassandra=1.2.11
```

Because of the line that adds the APT source, the `apt-get` command would always have to
be re-run.  By building with `docker-buildcache` subsequent builds look like this:

```
(dockman)baremetal@baremetal:~/Projects/baremetal/containers/cassandra$ docker-buildcache -t cassandra .
Building image with tag cassandra
Dockerfile content:
FROM ubuntu:quantal
MAINTAINER Roberto Aguilar roberto@baremetal.io

Building with command: docker build -t cassandra .
Uploading context 93542400 bytes
Step 1 : FROM ubuntu:quantal
 ---> b750fe79269d
Step 2 : MAINTAINER Roberto Aguilar roberto@baremetal.io
 ---> Using cache
 ---> 6042cc630923
Successfully built 6042cc630923
Image ID: 6042cc630923
ADD filename=files/etc/apt/sources.list.d/cassandra.list, file_hash=75a4df75e0cc
  looking for buildcache_tag=buildcache-6042cc630923-75a4df75e0cc
  found cache with id 42319f831d2d, skipping build!
ADD filename=files/var/cache/baremetal/cassandra_repo_key, file_hash=ea32a1e7e2b9
  looking for buildcache_tag=buildcache-42319f831d2d-ea32a1e7e2b9
  found cache with id a684f5110bb0, skipping build!
Building image FROM a684f5110bb0 with tag cassandra
Dockerfile content:
FROM a684f5110bb0
RUN cat /var/cache/baremetal/cassandra_repo_key | apt-key add -
RUN apt-get update
RUN apt-get install -y dsc12 cassandra=1.2.11

Building with command: docker build -t cassandra .
Uploading context 93542400 bytes
Step 1 : FROM a684f5110bb0
 ---> a684f5110bb0
Step 2 : RUN cat /var/cache/baremetal/cassandra_repo_key | apt-key add -
 ---> Using cache
 ---> fd90edb767ce
Step 3 : RUN apt-get update
 ---> Using cache
 ---> 4b17f6cb5a3c
Step 4 : RUN apt-get install -y dsc12 cassandra=1.2.11
 ---> Using cache
 ---> ac28959e749d
Successfully built ac28959e749d
Image ID: ac28959e749d
```

On your system you would see images similar to:

```
(dockman)baremetal@baremetal:~/Projects/baremetal/containers/cassandra$ docker images
[...]
buildcache-42319f831d2d-ea32a1e7e2b9                                                  latest              a684f5110bb0        49 minutes ago      2.941 kB (virtual 175.8 MB)
buildcache-6042cc630923-75a4df75e0cc                                                  latest              42319f831d2d        49 minutes ago      72 B (virtual 175.8 MB)
```

Cleaning up the buildcache can be done by running:

```
docker rmi $(docker images | grep '^buildcache' | awk '{print $3}')
```
