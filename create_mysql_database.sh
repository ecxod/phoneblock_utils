#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root."
  exit 1
fi

# Load environment variables
source /raid/home/blocklist/virtual/.env

mysql -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"
mysql -e "CREATE USER '$MYSQL_USER'@'$MYSQL_HOST' IDENTIFIED BY '$MYSQL_PASSWORD';"
mysql -e "GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'$MYSQL_HOST';"
mysql -e "FLUSH PRIVILEGES;"
