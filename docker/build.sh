#!/bin/sh

# Build the SSHD docker container
cd sshd/
docker build . -t a2p2v/ssh
cd ../

# Build the PLC emulator container
cd plc_emulator/
docker build . -t a2p2v/plc
cd ../

# Build the Flask HMI container
cd flaskhmi/
docker build . -t a2p2v/flaskhmi
cd ../
