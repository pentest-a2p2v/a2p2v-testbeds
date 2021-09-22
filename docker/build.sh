#!/bin/sh

# Build the SSHD docker container
cd sshd/
docker build . -t a2p2v/ssh
cd ../

# Build the PLC emulator container
cd plc_emulator/
docker build . -t a2p2v/plc
