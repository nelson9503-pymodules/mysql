import pymysql
from .obj_database import Database


class Connection:

    def __init__(self):
        self.user = ""
        self.password = ""
        self.host = ""
        self.port = ""
        self.conn = None

    def connect(self):
        """
        The login information was stored in class during creating new connection.
        User can simply use this function to connect server again after disconnected.
        """
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password
        )

    def commit(self):
        """
        Commit changes to the sql server.

        - any changes should be commited to affact server.
        - frequently commit will slow down the process.
        """
        self.conn.commit()

    def close(self):
        """
        Close the connection to sql server.

        - If connection did not be closed after use, it will stay in the server until time out.
        - Too many connection in server may cause "too many connection" error.
        """
        if self.conn != None:
            self.conn.commit()
            self.conn.close()

    def exec(self, quote: str) -> dict:
        """
        Execute the mysql quotes directly.
        """
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(quote)
        results = cursor.fetchall()
        return results

    def list_database(self) -> list:
        """
        List out all databases in sql server.
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

    def count_database(self) -> int:
        """
        Count the number of databases in sql server.
        """
        sql = "SELECT COUNT(schema_name) FROM information_schema.schemata;"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        return results[0][0]

    def create_database(self, name: str):
        """
        Create a new database.
        """
        sql = "CREATE DATABASE {};".format(name)
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def Database(self, name: str) -> Database:
        """
        Database connect to a database and return database object.
        """
        db = Database()
        db.database = name
        db.conn = self.conn
        return db
