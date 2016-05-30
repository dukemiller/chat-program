import socket
from tkinter import *


class Login:

    def __init__(self):
        self.root = Tk()

        # First initializations
        self.frame = Frame(self.root, height=80, width=30)
        self.label = Label(self.frame, text="Ip address: ")
        self.ip_text = Text(self.frame, height=1, width=30)
        self.button = Button(self.frame, anchor=W, text="Connect")

        # Detail setters
        self._init_gui_details()
        self._init_event_listeners()

        # Values I need for later
        self.ip_address = str

        self.root.mainloop()

    def _init_gui_details(self):
        self.frame.pack_propagate(0)
        self.frame.pack()

        self.label.grid(row=0, column=0)

        self.ip_text.insert(INSERT, socket.gethostbyname(socket.getfqdn()))
        self.ip_text.grid(row=0, column=1)
        self.ip_text.focus()

        self.button.grid(row=1, column=1)

    def _init_event_listeners(self):
        self.button.bind("<Button-1>", self.ip)

    def _close(self):
        """ Closes the window.

        I had to use .after instead of just destroying immediately because of some
         sort of non descriptive error being thrown most likely related destroying
         widgets. """

        self.root.after(200, self.root.destroy)

    def ip(self, e: Event):
        self.ip_address = self.ip_text.get("1.0", 'end-1c')
        self._close()

    def connection(self):
        pass

if __name__ == '__main__':
    Login()
