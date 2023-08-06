# PyQRP: A Simple QRP File interpreter in Python

## Description

PyQRP is a simple 

## Install

### From PIP

```
pip3 install sshepherd
```

### From Source
```
git clone https://github.com/drpresq/sshepherd.git
pip3 install ./sshepherd
```

## Usage

```
usage: sshepherd [-h] [-a {list-users,add-users,run-command}]
                [-t TARGETS [TARGETS ...]] [-p PATH]
                [-c COMMAND [COMMAND ...]]

SSHepherd - herd your flock of ssh hosts

optional arguments:
  -h, --help            show this help message and exit
  -a {list-users,add-users,run-command}, --action {list-users,add-users,run-command}
                        
                        Action to be carried out on targets
                        
  -t TARGETS [TARGETS ...], --targets TARGETS [TARGETS ...]
                        
                        List of ip addresses/hostnames to perform action upon
                        
  -p PATH, --path PATH  
                        Path to New User SSH Public Keys. SSH Key names must conform to the following formats:
				<username>.pub or <username>_somethingelse.pub
                        
  -c COMMAND [COMMAND ...], --command COMMAND [COMMAND ...]
                        
                        Commands to be run on host separated by semicolons
                        

    Common Usage:
	sshepherd -a list-users -t 192.168.1.1 192.168.1.2				Returns a list of users by IP
	sshepherd -a add-users -t 192.168.1.1 -p /home/user/pub-keys			Add users to each target based on key name
	sshepherd -a run-command -t 192.168.1.1 -c sudo whoami; cat /etc/passwd		Runs the two commands on each target
```

