import mysql.connector

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     port="8889",
#     database="db_inventaris2"
# )
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        port='3306',
        database='db_inventaris'
    )
