#!/bin/bash

IMAGE_NAME=wk_grokbuild

podman build -t $IMAGE_NAME .
