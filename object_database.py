import os
import json
import pymysql
import tkinter as tk
from tkinter import messagebox, simpledialog
from .object_table import TB

# There are two main object in this mysql package: Database and Table.
# Database object responsible for connection between sql server and management of tables.
# Table object responsible for updating and deleting on data in sql table.
# These two objects generate most of sql quotes, so users can do most CRUD without writing sql quotes.


class DB:

    # When initialize the database object,
    # Object will establish a connection to the sql server.
    # Then, it create a database to sql server if it was not exists.
    def __init__(self, db_name: str):
        """
        Connect to a database.
        """
        self.db_name = db_name
        self.__connect_to_server()
        self.__check_db_exists()

    # close the connection to prevent "too many connection" error
    def close(self):
        """
        Close connection.
        If user dose not close the connection,
            it will be kept in server until timeout.
        If too many connection in the server,
            it may cause request error for further connection.
        """
        self.conn.close()

    def commit(self):
        """
        Commit the changes to the server.
        Any changes via this package would not affect the server 
            until user commit the chanages.
        """
        self.conn.commit()

    def drop(self):
        """
        Drop database from server.
        """
        sql = "DROP DATABASE {};".format(self.db_name)
        self.execute(sql)

    def list_db(self) -> list:
        """
        List out all databases in mysql server.
        """
        sql = "SELECT schema_name FROM information_schema.schemata;"
        dbs = []
        results = self.execute(sql)
        for row in results:
            for val in row:
                dbs.append(val)
        return dbs

    def list_tb(self) -> list:
        """
        List out all tables in the database.
        """
        sql = "SHOW TABLES FROM `{}`".format(self.db_name)
        tbs = []
        results = self.execute(sql)
        for row in results:
            for val in row:
                tbs.append(val)
        return tbs

    def add_tb(self, tb_name: str, key_col_name: str, key_data_type: str) -> object:
        """
        Add/Create a new table to the sql server.
        Users should define the key column name and its data type(e.g. CHAR(10)).
        To expand the table, please use Table.add_col to increase number of columns.
        This method will return the Table object for created table.
        """
        tb_name = tb_name.lower()  # the table name in mysql must be lower case
        sql = "CREATE TABLE `{}`.`{}` ".format(self.db_name, tb_name)
        sql += "(`{}` {})".format(key_col_name,
                                  key_data_type+" NOT NULL PRIMARY KEY")
        self.execute(sql)
        tb = TB(tb_name, self)
        return tb

    def TB(self, tb_name: str) -> object:
        """
        Obtain table object by using table name.
        If user try to control a table not exists, error will be rasied.
        (You should create the table before you control it.)
        """
        tb_name = tb_name.lower()  # the table name in mysql must be lower case
        tb = TB(tb_name, self)
        return tb

    def execute(self, sql_quote: str, return_dict: bool = False) -> any:
        """
        Execute the sql quote.
        Some execution may not return a result,
            user can simply do not catch it.

        If return dict is True,
            returning result will be dictionary instead of tuple.
        """
        if return_dict == True:
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        else:
            cursor = self.conn.cursor()
        cursor.execute(sql_quote)
        results = cursor.fetchall()
        return results

    # Check if the database is in the server
    # If not, create a new database.
    def __check_db_exists(self):
        if not self.db_name in self.list_db():
            sql = "CREATE DATABASE {};".format(self.db_name)
            self.execute(sql)

    # Keep trying to connect the sql server until success.
    def __connect_to_server(self):
        while True:
            try:
                self.__get_sql_config()
                self.conn = pymysql.connect(
                    host=self.config["host"],
                    port=self.config["port"],
                    user=self.config["user"],
                    password=self.config["password"]
                )
                break
            except:
                self.__ask_sql_config_by_gui()

    # Ask user for the sql server configurations.
    # The configurations will be stored in json.
    def __ask_sql_config_by_gui(self):
        root = tk.Tk()
        messagebox.showerror(
            title="MySQL Login",
            message="Failed. Please reconfigure the login information."
        )
        host = simpledialog.askstring("MySQL Configuration", "Host Name:")
        port = simpledialog.askinteger("MySQL Configuration", "Port:")
        user = simpledialog.askstring("MySQL Configuration", "User Name:")
        password = simpledialog.askstring(
            "MySQL Configuration", "Password:", show="*")
        root.destroy()
        # save configurations into json
        with open(self.config_path, 'w') as f:
            j = {
                "host": host,
                "port": port,
                "user": user,
                "password": password
            }
            f.write(json.dumps(j, indent=4))

    # Get the sql configurations.
    # If the config file not exists, ask user for config details by gui.
    def __get_sql_config(self):
        self.config_path = "./mysql_config.json"
        if not os.path.exists(self.config_path):
            self.__ask_sql_config_by_gui()
        with open(self.config_path, 'r') as f:
            self.config = json.loads(f.read())
