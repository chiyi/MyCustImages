#!/bin/bash

SCFULLNAME=`realpath $0`
SCPATH=`dirname $SCFULLNAME`
USERNAME=$(id -u -n)

cd $SCPATH

podman run \
 --rm \
 --net host \
 --user root \
 -e HOME=/work-dir \
 -e GROK_SESSIONS_DIR=/work-dir/.grok \
 -w "/work-dir" \
 -v ${PWD}/workspace:/work-dir \
 --name=wk_grokbuild_${USERNAME} \
 -it wk_grokbuild \
 /bin/bash



