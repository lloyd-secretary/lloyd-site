# lloyd.caltech.edu
Lloyd House Website

# Installation instructions

## Initial Environment Setup

### Windows

I wouldn't recommend trying to get this set up on Windows, since mysql-python on Windows has really bad support. Instead, download VMWare/Virtualbox and create an Ubuntu 18 VM from an iso file (the server runs Ubuntu 14, but it was too hard for me to get that running because all of its default packages are so far out of support).

### Mac

You'll need a virtual machine for Mac as well.

```zsh
brew install --cask multipass
```

Then, create a VM named virtmach:
```zsh
multipass launch --name virtmach "18.04"
```

Then start a shell for the VM:
```zsh
multipass shell virtmach
```

Then you have an Ubuntu 18.04 VM, and follow the instructions for Linux.

### Linux (Ubuntu 18)

Install Python 2.7

```bash
sudo apt install python2.7
sudo apt install python-pip
sudo apt install git
git clone https://github.com/lloyd-secretary/lloyd-site
cd lloyd-site/
pip install -r requirements.txt 
```

If you have any errors, here are some things you might need to download (on a multipass VM):
```
sudo apt-get install python-dev
sudo apt-get install libffi-dev
```

Install mysql:

```
sudo apt-get install libmysqlclient-dev
sudo apt install mysql-server-5.7 # or whatever version is default 
```

## All Systems (DB setup)

You need MySQL 5.5 probably, but it seems like mysql 5.7 works for Ubuntu 18.

You can enter mysql for the first time with:

```bash
sudo mysql -u root
```

Now from inside of

```mysql
CREATE DATABASE lloyd;
use lloyd;
source test-lloyd.sql;

CREATE DATABASE rotation;
use rotation;
source test-rotation.sql;

CREATE USER web@localhost;

GRANT ALL PRIVILEGES ON lloyd.* TO web@localhost;
GRANT ALL PRIVILEGES ON rotation.* TO web@localhost;

\q
```

## Run web server

Set `production = False` in `app/__init__.py` (please don't commit changes with this file having production = False, pull requests will be rejected).

The previous change will make it so that when you change a template file or something, it will automatically reload the file when you reload, which makes testing frontend really easy!

```bash
python run.py
```

## Editing files

You can always edit files directly from nano or vim, or gedit, but those might get annoying and it might be slow to edit directly from the virtual machine at all.

Instead, we will:
1. Set up SSH on the VM
2. Use VS code on your host (main computer not VM)
3. Connect to the codebase via SSH
4. Use port forwarding to forward port 5000 to your main computer
5. Now if you do `python run.py` from a terminal in VS code, then you should be able to access localhost:5000 in your browser window on your normal browser (not in VM).

Remember, to do any of this your VM must be on to accept the SSH connection.

Here's a reference for connecting to SSH on VS code (and forwarding a port): https://code.visualstudio.com/docs/remote/ssh

### Windows VMWare

In VMWare (windows):
```sh
sudo apt-get install openssh-server
sudo ufw allow 22
```

Then make sure your VM is in Bridged mode (in VMWare settings, go to player > manage > virtual machine settings and your networking should be bridged). If not, change this and restart your laptop.

Find your IP address for your VM:
```sh
sudo apt-get install net-tools
ifconfig
```

After inet is the ipaddress to connect to. You can verify the ssh is working by doing `ssh user@IP` or something like `ssh user@10.0.0.60`.

### Mac (multipass)

In your multipass shell:
```sh
sudo apt-get install openssh-server
sudo ufw allow 22
```

Again in your multipass shell, find your IP address for your VM (it's an IP4 address after inet, and not 127.0.0.1):
```sh
sudo apt-get install net-tools
ifconfig
```

Now, from your Mac terminal, you want to get a public key from your .ssh directory (ls ~/.ssh) and choose a .pub file. Then do `cat ~/.ssh/whateveritscalled.pub`

Finally, in the multipass shell, do:
```sh
sudo echo "ssh-something .... FULL PUBLIC KEY... ubuntu@virtmach" > ~/.ssh/authorized_keys
sudo chmod 700 ~/.ssh
sudo chmod 600 ~/.ssh/authorized_keys
```

This makes it so that your Mac is authorized to connect to your virtual machine.

Finally, let's find the IP address for your VM (it's an IP4 address after inet, and not 127.0.0.1):
```sh
sudo apt-get install net-tools
ifconfig
```
