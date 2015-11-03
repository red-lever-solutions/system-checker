#!/bin/sh

mkdir -p config status logs

docker build -f Dockerfile-checker -t system-checker:dev . && \
docker run --rm \
       -v $(pwd)/src:/src \
       -v $(pwd)/config:/config \
       -v $(pwd)/status:/status \
       -v $(pwd)/logs:/logs \
       -e PYTHONUNBUFFERED="1" \
       system-checker:dev
