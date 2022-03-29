# A2P2V Sample Testbeds

This repository contains sample testbeds to use with a2p2v.
The testbeds are built and run using testbed1 and testbed1-compose. 

## Testbed details

Testbed1

- host1: metasploitable2
- host2: sshd
- host3: metasploitable2
- host4: sshd
- host5: plc emulator
- flaskhmi: HMI web application

## Setup

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

Add the following to the $HOME/.config/a2p2v/a2p2v.conf file:

    [INITIAL CONDITIONS]
    initial_condition1 = {"host":"attacker", "type":"state", "key":"initial_host", "value":"attacker"}
    initial_condition2 = {"host":"attacker", "type":"state", "key":"current_role", "value":"admin"}
    initial_condition3 = {"host":"attacker", "type":"state", "key":"current_access", "value":"metasploit"}
    initial_condition4 = {"host":"gw", "type":"credential", "username":"username", "password":"password", "role":"user"}
    initial_condition5 = {"host":"host2", "type":"credential", "username":"test", "password":"test", "role":"user"}
    initial_condition6 = {"host":"host4", "type":"credential", "username":"test", "password":"test", "role":"user"}
    
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

NOTE: Currently we are experiencing issues pivoting between the metasploitable2 machines,
and thus you will encounter issues when using an attack path that includes host1 or host3.

### Flask HMI

Open the flask HMI by navigating to http://localhost:8800

Ensure that the IP address says "host5" and click connect.

The current temperature and temperature setting are displayed.

To change the temperature:

- The "+" raises the temperature by 1C
- The "-" lowers the temperature by 1C

## Testcases

Test cases:

1. [x] current_host=HOST2, ssh_login
2. [x] current_host=HOST1, exploit/unix/ftp/vsftpd_234_backdoor


