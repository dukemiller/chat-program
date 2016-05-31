import threading
from connection import Connection
from time import sleep
from tkinter import messagebox
from tkinter import *


class Client:

    TEXTBOX_CHARACTER_LENGTH = 50

    def __init__(self, connection: Connection):
        self.root = Tk()
        self.connection_socket = connection.connection_socket
        self.root.wm_title(connection.connection_type)

        # Widgets
        self.frame = Frame(self.root, height=200, width=200)
        self.chat_text = Text(height=10, width=50)
        self.message_text = Text(height=1, width=50)

        # Details & Initializations
        self._init_gui_details()
        self._init_event_listeners()
        self._init_chat_thread()

        self.root.mainloop()

    def _init_gui_details(self):
        self.chat_text.config(state=DISABLED)
        self.chat_text.pack()
        self.message_text.pack()

    def _init_event_listeners(self):
        self.message_text.bind("<Return>", self._send_message)

    def _init_chat_thread(self):
        self.chat = threading.Thread(target=self._receive_message_loop)
        self.chat.daemon = True
        self.chat.start()

    def _clear_message_text(self):
        self.message_text.delete('1.0', END)

    def _receive_message_loop(self):
        """ Continually read and add messages to the chat. """

        while True:
            try:
                message = self.connection_socket.recv(4096)
                if len(message) > 0:
                    self.add_message_to_chat(message.decode('utf-8'))
                sleep(0.2)

            except ConnectionResetError:
                # messagebox.showerror("Client dropped", "The other person has dropped from the connection.")
                self.root.destroy()

    def _send_message(self, e: Event):
        """ Sends the message over the socket and also adds it to the chat. """

        message = self.message_text.get("1.0", 'end-1c').replace('\n', "")

        if len(message) > 0:
            self.add_message_to_chat('you: ' + message)
            self._clear_message_text()
            self.connection_socket.send(bytes('them: ' + message, 'utf-8'))

    def add_message_to_chat(self, message: str):
        """ Adds a message to the chat and scrolls down. """

        scroll_length = (len(message) // Client.TEXTBOX_CHARACTER_LENGTH) + 1
        self.chat_text.config(state=NORMAL)
        self.chat_text.insert(END, message + '\n')
        self.chat_text.yview_scroll(scroll_length, "units")
        self.chat_text.config(state=DISABLED)
