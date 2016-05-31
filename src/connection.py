from threading import Thread
from tkinter import *
from tkinter import messagebox
import socket


class Connection:

    def __init__(self):
        self.root = Tk()
        self.connection_type = str
        self.port = 5000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_socket = socket.socket
        self.is_set = False

        # First initializations
        self.frame = Frame(self.root, height=80, width=30)
        self.label = Label(self.frame, text="Ip address: ")
        self.ip_text = Text(self.frame, height=1, width=30)
        self.connect_button = Button(self.frame, text="Connect")
        self.server_button = Button(self.frame, text="Host")

        # Detail setters
        self._init_gui_details()
        self._init_event_listeners()

        self.root.mainloop()

    def _init_gui_details(self):
        self.frame.config(height=80, width=30)
        self.frame.pack_propagate(0)
        self.frame.pack()

        self.label.grid(row=0, column=0)

        self.ip_text.insert(INSERT, socket.gethostbyname(socket.getfqdn()))
        self.ip_text.grid(row=0, column=1)
        self.ip_text.focus()

        self.connect_button.grid(row=1, column=1)
        self.server_button.grid(row=1, column=0)

    def _init_event_listeners(self):
        self.connect_button.bind("<Button-1>", lambda e: Thread(target=self.connect, args=(e,)).start())
        self.server_button.bind("<Button-1>", lambda e: Thread(target=self.host, args=(e,)).start())

    def _close(self):
        """ Closes the window.

        I had to use .after instead of just destroying immediately because of some
        sort of non descriptive error being thrown most likely related destroying
        widgets. """

        self.root.after(200, self.root.destroy)

    def establish_connection(self):
        if self.connection_type == "client":
            self.connection_socket = self.socket

        elif self.connection_type == "server":
            self.connection_socket, address = self.socket.accept()

        self.is_set = True
        self._close()

    def host(self, e: Event):
        connect_host = self.ip_text.get("1.0", 'end-1c').strip()

        try:
            self.socket.bind((connect_host, self.port))
            self.connection_type = "server"
            self.socket.listen(1)
            Thread(target=self.establish_connection).start()

        except OSError as e:
            if e.errno == 10048:
                messagebox.showerror("Client error", "You already have a host client open.")

    def connect(self, e: Event):
        connect_host = self.ip_text.get("1.0", 'end-1c').strip()

        try:
            self.socket.connect((connect_host, self.port))
            self.connection_type = "client"
            Thread(target=self.establish_connection).start()

        except WindowsError as e:
            if e.errno == 10061:
                messagebox.showerror("Server error", "IP Address is not accepting connections.")


if __name__ == '__main__':
    Connection()
