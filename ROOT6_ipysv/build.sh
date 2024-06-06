#!/bin/bash
IMAGE_NAME="dockerroot6_ipysv"


docker build -t ${IMAGE_NAME} .




#HARBOR_SITE="harbor.mysite.notfound"
#IMAGE_NAME="${HARBOR_SITE}/"dockerroot6_ipysv":latest"
#
#
#docker login ${HARBOR_SITE}
#docker build -t ${IMAGE_NAME} .
#docker push ${IMAGE_NAME}

