#!/bin/bash

IPstr=`hostname -I | awk '{print $1}'`
echo $IPstr
root --notebook --allow-root --config /root/jupyter_notebook_config.py

