#!/bin/bash

IMAGE_NAME="gcloud_sdk_client"

docker run --net host --rm -it $IMAGE_NAME /bin/bash
