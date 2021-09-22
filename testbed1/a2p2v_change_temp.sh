#!/bin/sh

VULN_FILE=config/testbed1.common
NET_FILE=config/testbed1_network.xml

a2p2v --plan \
    -f ${VULN_FILE} \
    -nx ${NET_FILE} \
    --goal-name change_temp \
    --goal-current-status change_temp \
    --lhost 172.17.0.1 \
    --sleep 0.2 \
    --execute
