from client import Client
from login import Login

login = Login()
if login.is_set:
    client = Client(login)
