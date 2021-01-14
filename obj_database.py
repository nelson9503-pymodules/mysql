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

    def create_table(self, tableName, keyColumnName, keyColumnSpec):
        """
        Create a new table to the database.
        Table should contain a key column so that it can be read and written.
        """
        sql = "CREATE TABLE `{}`.`{}` ".format(self.database, tableName)
        sql += "(`{}` {})".format(keyColumnName,
                                  keyColumnSpec+" NOT NULL PRIMARY KEY")
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
