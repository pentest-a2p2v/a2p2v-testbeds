#!/bin/sh

VULN_FILE=/home/python/config/testbed/testbed1.common
NET_FILE=/home/python/config/testbed/testbed1_network.xml
DOCKER_EXEC="docker exec -it a2p2v"

if [ $# != 1 ]
then
    echo Usage $0 hostname
    exit
fi

HOSTNAME=$1

$DOCKER_EXEC a2p2v --plan \
    -f ${VULN_FILE} \
    -nx ${NET_FILE} \
    --goal-name host \
    --goal-current-host ${HOSTNAME} \
    --lhost 172.17.0.1 \
    --sleep 0.2 \
    --execute
