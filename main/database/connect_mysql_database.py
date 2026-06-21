import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""      
)

cursor = connection.cursor()

cursor.execute("""
CREATE DATABASE IF NOT EXISTS accidents_germany
""")

print("Database created successfully!")

cursor.close()
connection.close()