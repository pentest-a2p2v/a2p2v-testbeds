# A2P2V Sample Testbeds

This repository contains a sample testbed to use with a2p2v.
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

Build the sshd, plc_emulator, flaskhmi, and a2p2v testbed1 images:

    ./build.sh

Create the testbed1 network:

    cd docker/
    ./create_network.sh

If using chrome:

- Install [Markdown Viewer plugin](https://chrome.google.com/webstore/detail/markdown-viewer) and configure to view markdown for http://localhost:3000 to view reports
- Configure to allow pop-ups from localhost

The above steps need to be performed only once.

## Testbed startup

Run the following script to start the testbed via docker compose:

    ./run.sh

## A2P2V GUI

Launch the GUI by navigating to http://localhost:3000

On the main page:

1. For "Network configuration file" use the File selector to choose "config/testbed/testbed1_network.xml"
2. For "Scan result file" use the File selector to choose "config/testbed/testbed1.common"
3. Click "import"
4. In the "target state" box, enter "change_temp".
5. Click "Search Attack Path"
6. Click "Execute"

## Flask HMI

Open the flask HMI by navigating to http://localhost:8800

Ensure that the IP address says "host5" and click connect.

The current temperature and temperature setting are displayed.

To change the temperature:

- The "+" raises the temperature by 1C
- The "-" lowers the temperature by 1C

## Command line examples

Obtain a shell on host2:

    scripts/a2p2v_host.sh host2

Obtain a shell on host4:

    scripts/a2p2v_host.sh host4

then choose attack path "HOST2(1)>HOST4(1)".

Change the temperature on the PLC:

    scripts/a2p2v_change_temp.sh

then choose the attack path "HOST2(1)>HOST4(1)>HOST5(1)"

## Troubleshooting

If upgrading from a previous version of the testbed, you may encounter such as:

    ERROR: for a2p2v  Cannot create container for service a2p2v: Conflict. The container name "/a2p2v" is already in use by container "cfb04c1b4c7de2f3dec4859c6104c94c174ef61bc378ca484337ae93d67c272d". You have to remove (or rename) that container to be able to reuse that name.

To fix this, remove the previous docker containers, then try again:

    docker rm host5 host4 host3 host2 host1 attacker flaskhmi a2p2v msfrpc
