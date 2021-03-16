
""" ServerConnector connects to the MySQL Server and
    return the connection object.

    If here is no login information or failed to connect with existed information,
    ServerConnector will ask user for login information via a tkinter GUI.

    The login information can be return for further processing.
"""

import pymysql
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class ServerConnector:

    def __init__(self):
        self.loginGUI = LoginGUI()

    def set_loginInfo(self, hostname: str, port: int, username: str, password: str):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def get_loginInfo(self) -> dict:
        j = {
            "host": self.hostname,
            "port": self.port,
            "user": self.username,
            "password": self.password
        }
        return j

    def connect_to_MySQLServer(self) -> object:
        while True:
            try:
                conn = pymysql.connect(
                    host=self.hostname,
                    port=self.port,
                    user=self.username,
                    password=self.password
                )
                break
            except:
                self.loginGUI.get_loginInfo()
                self.hostname = self.loginGUI.host
                self.port = self.loginGUI.port
                self.username = self.loginGUI.user
                self.password = self.loginGUI.password
        return conn


class LoginGUI:

    def __init__(self):
        # initialize outputs
        self.host = ""
        self.port = 0
        self.user = ""
        self.password = ""
        # setup main window
        self.root = tk.Tk()
        self.root.title("MySQL Server Login")
        # setup labels
        lblTexts = ["Host Name:", "Port:", "Username:", "Password:"]
        for i in range(len(lblTexts)):
            lbl = ttk.Label(self.root, text=lblTexts[i], font=(12))
            lbl.grid(row=i, column=0)
        # setup entries
        self.entries = []
        for i in range(3):
            entry = ttk.Entry(self.root, font=12)
            entry.grid(row=i, column=1)
            self.entries.append(entry)
        entry = ttk.Entry(self.root, font=12, show="*")
        entry.grid(row=3, column=1)
        self.entries.append(entry)
        # setup login button
        btn = ttk.Button(self.root, text="Login", command=self.__get_inputs)
        btn.grid(row=4, column=0, columnspan=2)

    def get_loginInfo(self):
        self.root.mainloop()

    def __get_inputs(self):
        self.host = self.entries[0].get()
        try:
            self.port = int(self.entries[1].get())
        except:
            messagebox.showerror("Type Error", "port must be Interger")
            return
        self.user = self.entries[2].get()
        self.password = self.entries[3].get()
        self.root.destroy()
