#!/bin/sh

docker build -f Dockerfile-tipboard -t system-checker-tipboard:dev . && \
docker run --rm \
       -v $(pwd)/src:/src \
       -p 0.0.0.0:8080:8080 \
       system-checker-tipboard:dev
