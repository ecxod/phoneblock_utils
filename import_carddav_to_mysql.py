import requests
import xmltodict
import mysql.connector
from mysql.connector import Error

# CardDAV server details
url = 'https://phoneblock.net/phoneblock/contacts/'
username = '88289e81-9b63-432e-a6a3-61608298db45'
password = 'dgB7YSzoEE5TGXSaFZEb'

# MySQL database details
db_host = 'localhost'
db_database = 'phoneblock'
db_user = 'phoneblock'
db_password = 'phoneblock'

def fetch_carddav_data(url, username, password):
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        return response.text
    else:
        return None

def save_to_mysql(data, db_details):
    try:
        connection = mysql.connector.connect(host=db_details['host'],
                                             database=db_details['database'],
                                             user=db_details['user'],
                                             password=db_details['password'])
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS addressbook (id INT AUTO_INCREMENT PRIMARY KEY, content LONGTEXT)")
            cursor.execute("INSERT INTO addressbook (content) VALUES (%s)", (data,))
            connection.commit()
            cursor.close()
            connection.close()
    except Error as e:
        print("Error while connecting to MySQL", e)

def main():
    carddav_data = fetch_carddav_data(url, username, password)
    if carddav_data:
        xml_data = xmltodict.unparse(xmltodict.parse(carddav_data))
        db_details = {'host': db_host, 'database': db_database, 'user': db_user, 'password': db_password}
        save_to_mysql(xml_data, db_details)
    else:
        print("Failed to fetch data from CardDAV server")

if __name__ == "__main__":
    main()
