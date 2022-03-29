# A2P2V Sample Testbeds

This repository contains sample testbeds to use with a2p2v.
The testbeds are built and run using docker and docker-compose. 

## Testbed details

Testbed1

- host1: metasploitable2
- host2: sshd
- host3: metasploitable2
- host4: sshd
- host5: plc emulator
- a2p2v: a2p2v and gui
- msfrpc: Metasploit RPC server
- flaskhmi: HMI web application

## Setup

Clone this repository using submodules:

    git clone --recurse-submodules

If you forgot to include the "--recurse-submodules" flag, you can run the following commands:

    git submodule init
    git submodule update --remote

To build the sshd, plc_emulator, flaskhmi, and a2p2v testbed1 images:

    ./build.sh

To create the testbed1 network:

    cd docker/
    ./create_network.sh

The above steps need to be performed only once.

## Testbed startup

Change to the directory of the desired testbed and start docker compose.
For example, to start testbed1:

    cd testbed1/
    docker-compose up

## Testbed1 examples

Obtain a shell on host2:

    cd testbed1/
    ./a2p2v_host.sh host2

Obtain a shell on host4:

    cd testbed1/
    ./a2p2v_host.sh host4

then choose attack path "HOST2(1)>HOST4(1)".

Change the temperature on the PLC:

    cd testbed1/
    ./a2p2v_change_temp.sh

then choose the attack path "HOST2(1)>HOST4(1)>HOST5(1)"

### Flask HMI

Open the flask HMI by navigating to http://localhost:8800

Ensure that the IP address says "host5" and click connect.

The current temperature and temperature setting are displayed.

To change the temperature:

- The "+" raises the temperature by 1C
- The "-" lowers the temperature by 1C
