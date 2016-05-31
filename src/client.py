import socket
import threading
from login import Login
from time import sleep
from tkinter import *


class Client:

    def __init__(self, login: Login):
        self.root = Tk()
        self.socket = login.socket
        self.connection_type = login.connection_type
        self.root.wm_title(self.connection_type)

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

        # Chat thread
        self.chat = threading.Thread(target=self.message_loop)
        self.chat.daemon = True
        self.chat.start()

        self.root.after(200, self._get_connection())
        self.root.mainloop()

    def _get_connection(self):
        if self.connection_type == "server":
            self.connection, address = self.socket.accept()
        else:
            self.connection = self.socket

    def _clear_message_text(self):
        self.message_text.delete('1.0', END)

    def message_loop(self):
        while True:
            message = self.connection.recv(1024)
            if len(message) > 0:
                self.add_message_to_chat(message)
            sleep(0.2)

    def add_message_to_chat(self, message):
        self.chat_text.config(state=NORMAL)
        self.chat_text.insert(END, message)
        self.chat_text.yview_scroll(1, "units")
        self.chat_text.config(state=DISABLED)

    def send_message(self, e: Event):
        message = self.message_text.get("1.0", 'end-1c')

        if len(message) > 0:
            self.add_message_to_chat(message)
            self._clear_message_text()
            self.connection.send(bytes(message, 'utf-8'))
