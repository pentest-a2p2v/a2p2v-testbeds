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

## Setup

To build the sshd and plc_emulator testbed1 images:

    cd docker/
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

## Testcases

Test cases:

1. [x] current_host=HOST2, ssh_login
2. [ ] current_host=HOST1, exploit/unix/ftp/vsftpd_234_backdoor

## Test case 2 error:

An error occurs when attempting to upgrade from a shell to meterpreter session:

```
[*] Command shell session 5 opened (0.0.0.0:0 -> 172.10.0.101:6200) at 2021-10-05 12:50:37 +0000

msf6 exploit(unix/ftp/vsftpd_234_backdoor) > sessions -u 5
Usage: sessions <id>

Interact with a different session Id.
This command only accepts one positive numeric argument.
This works the same as calling this from the MSF shell: sessions -i <session id>
```

The relevant function calls in *a2p2v/organizer.py*:

```
    def _parse_read_results(self, results):
...
        if re.search(r"Command shell session \d+ opened", data):
            logger.debug("***Found Command shell session opened!***")
            return self._command_shell_opened(data)
...
    def _command_shell_opened(self, data):
        if not self._do_upgrade():
...
    def _do_upgrade(self):
        return self._send_command('sessions -u $session')
```

Next steps:

- Try to run manually using msfconsole (I think this works)
- Try modifying organizer to use "run -j" (I think this causes problems with both test cases)

