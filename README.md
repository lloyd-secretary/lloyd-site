# lloyd.caltech.edu
Lloyd House Website

# Installation instructions

## Initial Environment Setup

### Windows

I wouldn't recommend trying to get this set up on Windows, since mysql-python on Windows has really bad support. Instead, download VMWare/Virtualbox and create an Ubuntu 18 VM from an iso file (the server runs Ubuntu 14, but it was too hard for me to get that running because all of its default packages are so far out of support).

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

Install mysql.

```
sudo apt-get install libmysqlclient-dev
sudo apt install mysql-server-5.7 # or whatever version is default 
```

### Mac

Install git, python 2.7 and python pip.

```
git clone https://github.com/lloyd-secretary/lloyd-site
cd lloyd-site/
```

Then create a virtual environment and activate it. We need a virtual environment so if you have other installations they don't affect each other.

```
pip install -r requirements.txt 
```

Then you can just do `deactivate` when you're done working on the virtual environment.

## All Systems (DB setup)

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
