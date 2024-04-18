# Phoneblock Utils

These are some scripts related to https://github.com/haumacher/phoneblock that help you use other tools ecxept AVM Fritzbox, Apple and Google Devices, such as XML, LDAP and Broadsoft on SIP phones. 
You need to register and get a user and a password there, in irder to use this scripts.

## Create a virtual user first

```bash
$ apt install python3-pip
$ adduser --system --disabled-password --shell=/bin/bash --home /raid/home/blocklist --group blocklist
$ su - blocklist
```
### as user blocklist
```bash 
$ python3 -m venv virtual
$ source virtual/bin/activate
$ python3 -m pip install --upgrade pip
$ python3 -m pip install requests
$ python3 -m pip install mysql-connector-python
$ python3 -m pip install xmltodict
$ python3 -m pip install vobject

```


## Set uo a crontab to fetch the bad boys every day at 7 AM

```bash
$ crontab -e -u blocklist
```

```cron
0 7 * * * /usr/bin/python3 /raid/home/blocklist/virtual/import_carddav_to_mysql.py
```