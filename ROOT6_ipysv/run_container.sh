#!/bin/bash
IMAGE_NAME="dockerroot6_ipysv"
PORT=52190

MyIP=`ifconfig | grep "inet 192.168" | awk '{print $2}'`
sed 's/%%SV_IP%%/'${MyIP}'/' jupyter_notebook_config.template > jupyter_notebook_config.py

# prefer in tmux
docker run --rm --net host -v $PWD/jupyter_notebook_config.py:/root/jupyter_notebook_config.py -v $PWD/WK:/root/IPyNB/WK --name ${USER}_ROOT6_IPY -it ${IMAGE_NAME}
