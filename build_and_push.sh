#!/bin/bash -e

ORIGWD="$(pwd)"
TMPWD="$(mktemp -d)"

BUILD_TAG="$1"
if [ -z "$BUILD_TAG" ]; then
    echo "No git tag supplied" >&2
    exit 1
fi

cd $TMPWD
git clone "$ORIGWD"
git checkout tags/"$BUILD_TAG"

docker build -t tutum.co/fuechsl/system-checker:"$BUILD_TAG" -f Dockerfile-checker .
docker build -t tutum.co/fuechsl/system-checker-dashboard:"$BUILD_TAG" -f Dockerfile-tipboard .

export TUTUM_USER="fuechsl"
docker login tutum.co
docker push tutum.co/fuechsl/system-checker:"$BUILD_TAG"
docker push tutum.co/fuechsl/system-checker-dashboard:"$BUILD_TAG"

cd "$ORIGWD"
rm -r $TMPWD
