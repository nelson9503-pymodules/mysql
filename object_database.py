import os
import json
import pymysql
from tkinter import messagebox, simpledialog
from .object_table import TB


class DB:

    def __init__(self, db_name: str):
        """
        Connect to a database.
        """
        self.db_name = db_name
        self.__connect_to_server()
        self.__check_db_exists()

    def close(self):
        """
        Close connection.
        """
        self.conn.close()
    
    def commit(self):
        self.conn.commit()

    def drop(self):
        """
        Drop database from server.
        """
        sql = "DROP DATABASE {};".format(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def list_db(self) -> list:
        """
        List out all databases in mysql server.
        """
        sql = "SELECT schema_name FROM information_schema.schemata;"
        dbs = []
        cursor = self.conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
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
        cursor = self.conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for val in row:
                tbs.append(val)
        return tbs

    def add_tb(self, tb_name: str, key_col_name: str, key_data_type: str) -> object:
        sql = "CREATE TABLE `{}`.`{}` ".format(self.db_name, tb_name)
        sql += "(`{}` {})".format(key_col_name,
                                  key_data_type+" NOT NULL PRIMARY KEY")
        cursor = self.conn.cursor()
        cursor.execute(sql)
        tb = TB(tb_name, self)
        return tb

    def TB(self, tb_name: str) -> object:
        tb = TB(tb_name, self)
        return tb

    def execute(self, sql_quote: str) -> dict:
        """
        Execute the sql quote.
        """
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql_quote)
        results = cursor.fetchall()
        return results

    def __check_db_exists(self):
        if not self.db_name in self.list_db():
            sql = "CREATE DATABASE {};".format(self.db_name)
            cursor = self.conn.cursor()
            cursor.execute(sql)

    def __connect_to_server(self):
        while True:
            try:
                self.__get_configs()
                self.conn = pymysql.connect(
                    host=self.config["host"],
                    port=self.config["port"],
                    user=self.config["user"],
                    password=self.config["password"]
                )
                break
            except:
                messagebox.showerror(
                    title="MySQL Login Failed",
                    message="Failed to login MySQL.\nPlease reconfig login information."
                )
                host = simpledialog.askstring(
                    "MySQL Configuration", "Host Name:")
                port = simpledialog.askinteger("MySQL Configuration", "Port:")
                user = simpledialog.askstring(
                    "MySQL Configuration", "User Name:")
                password = simpledialog.askstring(
                    "MySQL Configuration", "Password:", show="*")
                with open(self.config_path, 'w') as f:
                    j = {
                        "host": host,
                        "port": port,
                        "user": user,
                        "password": password
                    }
                    with open(self.config_path, 'w') as f:
                        f.write(json.dumps(j, indent=4))

    def __get_configs(self) -> dict:
        self.config_path = "./mysql_config.json"
        if not os.path.exists(self.config_path):
            j = {
                "host": None,
                "port": None,
                "user": None,
                "password": None
            }
            with open(self.config_path, 'w') as f:
                f.write(json.dumps(j, indent=4))
        with open(self.config_path, 'r') as f:
            self.config = json.loads(f.read())
