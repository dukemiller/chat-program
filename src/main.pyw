from client import Client
from connection import Connection

connection = Connection()
if connection.is_set:
    client = Client(connection)
