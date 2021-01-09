from .obj_table import Table


class Database:

    def __init__(self):
        self.conn = None
        self.database = ""

    def drop(self):
        """
        Database drop itself from sql server.
        """
        sql = "DROP DATABASE {};".format(self.database)
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def list_table(self) -> list:
        """
        List out tables in database.
        """
        sql = "SHOW TABLES FROM `{}`".format(self.database)
        tbs = []
        cursor = self.conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for val in row:
                tbs.append(val)
        return tbs

    def count_table(self):
        """
        Count number of tables in database.
        """
        sql = "SHOW TABLES FROM `{}`".format(self.database)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        return len(results)

    def create_table(self, name, spec):
        """
        Create a new table to the database.

        The specification of columns is passing by spec.
        Example:
        spec = {
            "key":"INT NOT NULL PRIMARY KEY",
            "name":"CHAR(30)",
            "age":"INT"
        }
        """
        sql = "CREATE TABLE `{}`.`{}` (".format(self.database, name)
        for column in spec.keys():
            sql += "`{}` {},".format(column, spec[column])
        if sql[-1] == ',':
            sql = sql[:-1]
        sql += ")"
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def Table(self, name: str) -> Table:
        """
        Connect a table and return the table object.
        """
        tb = Table()
        tb.database = self.database
        tb.table = name
        tb.conn = self.conn
        return tb
