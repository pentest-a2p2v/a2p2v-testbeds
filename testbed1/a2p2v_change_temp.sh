#!/bin/sh

VULN_FILE=/home/python/config/testbed1.common
NET_FILE=/home/python/config/testbed1_network.xml
DOCKER_EXEC="docker exec -it a2p2v"

$DOCKER_EXEC a2p2v --plan \
    -f ${VULN_FILE} \
    -nx ${NET_FILE} \
    --goal-name change_temp \
    --goal-current-status change_temp \
    --lhost 172.17.0.1 \
    --sleep 0.7 \
    --execute
