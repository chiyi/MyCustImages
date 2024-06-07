#!/bin/bash

USERNAME=$(id -u -n)
USER_GROUP=$(id -g -n)
GID=$(id -g)
IMAGE_NAME="gcloud_sdk_client"

docker build \
  --build-arg USERNAME=$USERNAME \
  --build-arg USER_GROUP=$USER_GROUP \
  --build-arg UID=$UID \
  --build-arg GID=$GID \
  -t ${IMAGE_NAME} .
