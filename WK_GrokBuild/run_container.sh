#!/bin/bash

SCFULLNAME=`realpath $0`
SCPATH=`dirname $SCFULLNAME`
USERNAME=$(id -u -n)

cd $SCPATH

echo "CHECK \`grok update\` in container"

podman run \
 --rm \
 --net host \
 --userns=keep-id \
 -e HOME=/work-dir \
 -e GROK_SESSIONS_DIR=/work-dir/.grok \
 -w "/work-dir" \
 -v ${PWD}/workspace:/work-dir \
 --name=wk_grokbuild_${USERNAME} \
 -it wk_grokbuild \
 /bin/bash



