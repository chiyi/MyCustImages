#!/bin/bash

DIR_MOUNT=${1:-$PWD}
DIR_DATA=${2:-$HOME/data}
GID=`id -g`
inpUID=${3:-$UID}
inpGID=${4:-$GID}

IMAGE_NAME="kaiyi_wk_tensorflow"


docker run -it --rm --runtime=nvidia -u $inpUID:$inpGID -v $DIR_MOUNT:/workspace -v $DIR_DATA:/ext_data ${IMAGE_NAME} /bin/bash

