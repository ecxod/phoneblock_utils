#!/usr/bin/env python3
""" Module providing a function to import CardDAV Data from haumacher/phoneblock. """
import json
import os
import mysql.connector
import requests
from dotenv import load_dotenv

def fetch_carddav_data(url, username, password):
    """ Get the CardDAV data with a timeout. """
    try:
        response = requests.get(url, auth=(username, password), timeout=10)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        print(f"Failed to fetch data: {response.status_code}")
        return None
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def sql_execute_from_file(filename, cursor):
    """ execute sql from file """
    with open(filename, 'r', encoding='utf-8') as sql_file:
        sql_script = sql_file.read()
    sql_commands = sql_script.split(';')
    for command in sql_commands:
        cursor.execute(command)

def save_to_mysql(data, db_details):
    """ save the carddav in the mysql database """
    try:
        connection = mysql.connector.connect(
            host=db_details['host'],
            database=db_details['database'],
            user=db_details['user'],
            password=db_details['password']
        )
        if connection.is_connected():
            cursor = connection.cursor()
            sql_execute_from_file('create_table.sql', cursor)
            # Insert or update data
            insert_update_query = """
                INSERT INTO addressbook (phone, rating, votes)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    rating = %s,
                    votes = %s;
            """
            for entry in data['numbers']:
                cursor.execute(
                    insert_update_query,
                    (
                        entry['phone'],
                        entry['rating'],
                        entry['votes'],
                        entry['rating'],
                        entry['votes']
                    )
                )
            connection.commit()
            cursor.close()
            connection.close()
    except mysql.connector.Error as e:
        print("Error while connecting to MySQL ", e)

def main():
    """ read env variables and start the import"""
    load_dotenv()
    carddav_data = fetch_carddav_data(
        os.getenv('CARDDAV_URL'),
        os.getenv('CARDDAV_USERNAME'),
        os.getenv('CARDDAV_PASSWORD')
    )
    if carddav_data:
        db_details = {
            'host': os.getenv('MYSQL_HOST'), 
            'database': os.getenv('MYSQL_DATABASE'), 
            'user': os.getenv('MYSQL_USER'), 
            'password': os.getenv('MYSQL_PASSWORD')
        }
        save_to_mysql(carddav_data, db_details)
    else:
        print("Failed to fetch data from CardDAV server")

if __name__ == "__main__":
    main()
