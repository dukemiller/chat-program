from bs4 import BeautifulSoup
from pprint import pprint as pprint
from collections import namedtuple
import requests
import os
from tkinter import *


class Client:

    def __init__(self):
        self.root = Tk()

        # Frame
        self.frame = Frame(self.root, height=200, width=200)

        # Conversation window
        self.chat_text = Text(height=10, width=50)
        self.chat_text.config(state=DISABLED)
        self.chat_text.pack()

        # Message window
        self.message_text = Text(height=1, width=50)
        self.message_text.bind("<Return>", self.send_message)
        self.message_text.pack()

        self.root.mainloop()

    def send_message(self, event: Event):
        message = self.message_text.get("1.0", 'end-1c')
        self.chat_text.config(state=NORMAL)
        self.chat_text.insert(INSERT, message)
        self.chat_text.config(state=DISABLED)
        self.message_text.delete('1.0', END)


Client()

