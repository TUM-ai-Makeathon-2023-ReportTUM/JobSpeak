#!/bin/bash

sudo docker run -it --rm  \
    --net=host  \
    --privileged \
    --runtime=nvidia \
    -v $XSOCK:$XSOCK \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v `pwd`/../:/usr/src/app \
    --shm-size 8G \
    reportum "$@"