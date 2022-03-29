#!/bin/sh

# Build the SSHD docker container
cd docker/sshd/
./build.sh
cd ../../

# Build the PLC emulator container
cd docker/plc_emulator/
./build.sh
cd ../../

# Build the Flask HMI container
cd docker/flaskhmi/
./build.sh
cd ../../

# Build the A2P2v container
docker build . -t a2p2v/a2p2v
