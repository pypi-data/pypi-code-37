import json
import requests
import sqlite3
import os

api_key = os.environ['api_key']
latitude = os.environ['latitude']
longitude = os.environ['longitude']
db = os.environ['db_path']

def get_current_temperature():
    response = requests.get(
            'https://api.darksky.net/forecast/' +
            api_key + '/' +
            latitude + ',' + longitude
    )
    return {
            'query_time': response.json()['currently']['time'],
            'temperature': response.json()['currently']['temperature']
    }

def check_stored_temperature():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""SELECT id
             FROM temperatures
             WHERE query_time >= strftime('%s', 'now', '-5 minutes');""")
    id = c.fetchone()
    conn.close
    if id is not None:
        return id[0]
    else:
        return False

def get_stored_temperature(id):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("""SELECT query_time, temperature
             FROM temperatures WHERE id = %s;""" % id)
    conn.close
    temperature = c.fetchone()
    return {
            'query_time': temperature[0],
            'temperature': temperature[1]
    }

def store_temperature(temperature):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    values = [temperature['temperature'], temperature['query_time']]
    c.execute("""INSERT INTO temperatures (
                 temperature,
                 query_time
             ) VALUES (?, ?);""", values)
    conn.commit()
    conn.close

def initialize_db():
     conn = sqlite3.connect(db)
     c = conn.cursor()
     values = [temperature['temperature'], temperature['query_time']]
     c.execute("""CREATE TABLE IF NOT EXISTS temperatures (
                 id INTEGER PRIMARY KEY,
                 query_time INTEGER NOT NULL,
                 temperature REAL NOT NULL
             );""")
     conn.commit()
     conn.close


def get_temperature():
    id = check_stored_temperature()
    if id is False:
        temperature =  get_current_temperature()
        store_temperature(temperature)
        return temperature
    else:
        temperature = get_stored_temperature(id)
        return temperature

