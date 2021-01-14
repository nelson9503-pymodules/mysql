import pymysql


class Table:

    def __init__(self):
        self.table = ""
        self.database = ""
        self.conn = None

    def drop(self):
        """
        Table drop itself from the database.
        """
        sql = "DROP TABLE `{}`.`{}`;".format(self.database, self.table)
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def clear(self):
        """
        Remove all data in table.
        The specification of columns will be kept.
        """
        sql = "TRUNCATE `{}`.`{}`".format(self.database, self.table)
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def keyCol(self) -> str:
        """
        Return the name of key column.
        If not found, return False.
        """
        sql = "SHOW COLUMNS FROM `{}`.`{}`;".format(self.database, self.table)
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            if row["Key"] == "PRI":
                return row["Field"]
        return False

    def list_column(self) -> list:
        """
        List out columns in table.
        """
        sql = "SHOW COLUMNS FROM `{}`.`{}`;".format(self.database, self.table)
        cols = []
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            cols.append(row["Field"])
        return cols

    def map_column(self) -> dict:
        """
        Return the map of columns with specification. 

        Format like this:
        {
            "key":"int",
            "name":"char(30)",
            "age":"int"
        }
        """
        sql = "SHOW COLUMNS FROM `{}`.`{}`;".format(self.database, self.table)
        colmap = {}
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            colmap[row["Field"]] = row["Type"]
        return colmap

    def count_column(self) -> int:
        """
        Count the number of columns in table.
        """
        sql = "SHOW COLUMNS FROM `{}`.`{}`;".format(self.database, self.table)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        return len(results)

    def add_column(self, name: str, spec: str):
        """
        Add a new column to table. 

        Arguments like this:
        name = "key", spec = "INT NOT NULL PRIMARY KEY"
        """
        sql = "ALTER TABLE `{}`.`{}` ADD `{}` {};".format(
            self.database, self.table, name, spec)
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def drop_column(self, name: str):
        """
        Drop a column in table.
        """
        sql = "ALTER TABLE `{}`.`{}` DROP `{}`;".format(
            self.database, self.table, name)
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def alter_column(self, name: str, spec: str):
        """
        Change the specification of the existed column.

        Arguments like this:
        name = "key", spec = "INT NOT NULL PRIMARY KEY"
        """
        sql = "ALTER TABLE `{}`.`{}` MODIFY `{}` {};".format(
            self.database, self.table, name, spec)
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def count_row(self) -> int:
        """
        Count the number of rows in table.
        """
        sql = "SELECT COUNT(*) FROM `{}`.`{}`;".format(self.database, self.table)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        return results[0][0]

    def drop_row(self, keyVal: any):
        """
        Drop a row by passing a key value.
        """
        keyCol = self.keyCol()
        if keyCol == False:
            raise AttributeError("Cannot control a table without key column.")
        sql = "DELETE FROM `{}`.`{}` WHERE `{}`={};".format(
            self.database, self.table, keyCol, keyVal)
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def query(self, column="*", condition="") -> dict:
        """
        Return the query list of dictionary.

        Here is the example from 2 rows query of data:
        {
            0:{"key":0, "Name":"Joe", "Age":36},
            1:{"key":1, "Name":"Eric", "Age":40}
        }
        ---
        By default argument, this function will execute a sql quote like this:
            SELECT * FROM `database`.`table`;
        ---
        User can pass different arguments to modify the quote.
        For example, we call this method like this:
            data = tb.query("Name, Age", "WHERE Age > 30")
        The sql quote will be executed would be like this:
            SELECT Name, Age FROM `database`.`table` WHERE Age > 30;
        """
        sql = "SELECT {} FROM `{}`.`{}`".format(
            column, self.database, self.table)
        if not condition == "":
            sql += " " + condition
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        records = cursor.fetchall()
        results = {}
        for i in range(len(records)):
            results[i] = records[i]
        return results

    def update(self, data: "dict"):
        """
        update the data to the table.
        user should pass data like this:
        {
            0:{"key":0, "Name":"Joe", "Age":36},
            1:{"key":1, "Name":"Eric", "Age":40}
        }
        ---
        WARMING:
            1. The data MUST contains key Field.
            2. All rows MUST in same size and contains same fields.
        """
        if len(data) == 0:
            return False
        # part 1
        columns = data[0].keys()
        part1 = "("
        for column in columns:
            part1 += "`" + column + "`,"
        if part1[-1] == ',':
            part1 = part1[:-1]
        part1 += ")"
        # part 2
        part2 = ""
        for key in data:
            row = data[key]
            part2 += "("
            for column in columns:
                val = row[column]
                if type(val) == str:
                    val = "'" + val + "'"
                part2 += str(val) + ","
            if part2[-1] == ',':
                part2 = part2[:-1]
            part2 += "),"
        if part2[-1] == ',':
            part2 = part2[:-1]
        # part 3
        key = self.keyCol()
        if key == False:
            raise AttributeError("Cannot control a table without key column.")
        part3 = ""
        for column in columns:
            if column == key:
                part3 += "`" + column + "` = VALUES(`" + column + "`),"
        if part3[-1] == ',':
            part3 = part3[:-1]
        # group parts
        sql = "INSERT INTO `{}`.`{}` ".format(self.database, self.table)
        sql += part1 + " VALUES "
        sql += part2 + " ON DUPLICATE KEY UPDATE "
        sql += part3 + ";"
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
