# Phoneblock Utils

These are some scripts related to https://github.com/haumacher/phoneblock that help you use other tools except AVM Fritzbox, Apple and Google Devices, such as XML, LDAP and Broadsoft on SIP phones. 
You need to register and get a user and a password there, in order to use this scripts.

## Create a user blocklist first

```bash
apt install git python3-pip
adduser --system --disabled-password --shell=/bin/bash --home /raid/home/blocklist --group blocklist
su - blocklist
```
### as user blocklist create a virtual environment

```bash 
python3 -m venv virtual
source virtual/bin/activate
```

### install all dependencies

```bash
python3 -m pip install --upgrade pip
python3 -m pip install requests
python3 -m pip install mysql-connector-python
python3 -m pip install xmltodict
python3 -m pip install vobject
python3 -m pip install python-dotenv
```
### clone this repository in your virtual environment

```bash
cd ~/virtual/
git clone https://github.com/ecxod/phoneblock_utils.git
```

### Get yourself a Blocklist user and password

Get yourself credentials by registering https://phoneblock.net/ and copy this file to `.env`

```env
CARDDAV_URL=https://phoneblock.net/phoneblock/api/blocklist?format=json
CARDDAV_USERNAME=phoneblock_username
CARDDAV_PASSWORD=phoneblock_password
MYSQL_HOST=localhost
MYSQL_DATABASE=your_database
MYSQL_USER=your_db_user
MYSQL_PASSWORD=your_db_password
```

### create the mysql database (as root) if you haven't done it yet

```bash
sudo chmod +x /raid/home/blocklist/virtual/create_mysql_database.sh
sudo /usr/bin/bash /raid/home/blocklist/virtual/create_mysql_database.sh
```

### Set up a crontab to fetch the bad boys every day at 7 AM

```bash
crontab -e -u blocklist
```

```cron
0 7 * * * /usr/bin/python3 /raid/home/blocklist/virtual/import_carddav_to_mysql.py
```

### Create the Django project

```bash
python3 -m pip install django
python3 -m pip install django-admin
python3 -m pip install django-bootstrap5

mkdir ~/virtual/blocklist
cd ~/virtual/blocklist
django-admin startproject blocklist
cd blocklist
```

### This is how your project must look like at this moment

```txt
blocklist/                          # Root directory of your Django project
├── blocklist/                      # Django project directory (configuration and settings)
│   ├── __init__.py                 # Makes Python treat this directory as a Python package
│   ├── asgi.py                     # Entry-point for ASGI-compatible web servers
│   ├── settings.py                 # Settings/configuration for this Django project
│   ├── urls.py                     # The URL declarations for this Django project
│   └── wsgi.py                     # Entry-point for WSGI-compatible web servers
├── searchapp/                      # Your Django app
│   ├── migrations/                 # Directory for database migrations files
│   │   └── __init__.py             # Makes Python treat the migrations directory as a Python package
│   ├── templates/                  # Directory for storing your app's templates
│   │   ├── search.html             # Template for the search form
│   │   └── results.html            # Template for displaying search results
│   ├── __init__.py                 # Makes Python treat this directory as a Python package
│   ├── admin.py                    # Configuration for the Django admin interface
│   ├── apps.py                     # Configuration for the app itself
│   ├── models.py                   # Database models
│   ├── tests.py                    # Test cases for the app
│   ├── urls.py                     # URL declarations for this app
│   └── views.py                    # Views for handling requests and returning responses
├── db.sqlite3                      # Default database file (SQLite)
├── manage.py                       # Command-line utility for administrative tasks
└── requirements.txt                # File for listing project dependencies
```