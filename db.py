import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Killer_9704",
        database="veriden"
    )
