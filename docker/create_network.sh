#!/bin/sh

docker network create testbed10 --subnet 172.10.0.0/24
docker network create testbed20 --subnet 172.20.0.0/24
docker network create testbed30 --subnet 172.30.0.0/24
