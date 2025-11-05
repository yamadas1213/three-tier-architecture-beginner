from flask import g
import mysql.connector
from mysql.connector import Error
import os

def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST', 'localhost'),
                user=os.environ.get('MYSQL_USER', 'admin'),
                password=os.environ.get('MYSQL_PASSWORD', ''),
                database=os.environ.get('MYSQL_DATABASE', 'tododb')
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
