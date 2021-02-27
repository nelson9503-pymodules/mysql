import pymysql


class TB:

    def __init__(self, table_name: str, DB: object):
        self.DB = DB
        self.tb_name = table_name
        self.key_col_name = self.__get_key_col_name()

    def drop(self):
        """
        Drop table from the database.
        """
        sql = "DROP TABLE `{}`.`{}`;".format(self.DB.db_name, self.tb_name)
        cursor = self.DB.conn.cursor()
        cursor.execute(sql)

    def rename(self, new_tb_name: str):
        """
        Rename table name.
        """
        cursor = self.DB.conn.cursor()
        cursor.execute(
            "ALTER TABLE `{db}`.`{tb}` RENAME `{db}`.`{new_tb}`;".format(
                db=self.DB.db_name,
                tb=self.tb_name,
                new_tb=new_tb_name
            )
        )
        self.tb_name = new_tb_name

    def list_col(self) -> list:
        """
        List out columns in the table.
        """
        sql = "SHOW COLUMNS FROM `{}`.`{}`;".format(
            self.DB.db_name, self.tb_name)
        cols = []
        cursor = self.DB.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            cols.append(row["Field"])
        return cols

    def add_col(self, col_name: str, data_type: str):
        """
        Add a new column to the table.
        """
        sql = "ALTER TABLE `{}`.`{}` ADD `{}` {};".format(
            self.DB.db_name, self.tb_name, col_name, data_type)
        cursor = self.DB.conn.cursor()
        cursor.execute(sql)

    def drop_col(self, col_name: str):
        """
        Drop the column from the table.
        """
        sql = "ALTER TABLE `{}`.`{}` DROP `{}`;".format(
            self.DB.db_name, self.tb_name, col_name)
        cursor = self.DB.conn.cursor()
        cursor.execute(sql)

    def drop_data(self, key_value: any):
        """
        Drop a row of data by using key.
        """
        sql = "DELETE FROM `{}`.`{}` WHERE `{}`={};".format(
            self.DB.db_name, self.tb_name, self.key_col_name, key_value)
        cursor = self.DB.conn.cursor()
        cursor.execute(sql)

    def query(self, column: str = "*", condition="") -> dict:
        """
        Query the table and return results in dictionary.
        """
        sql = "SELECT {} FROM `{}`.`{}`".format(
            column, self.DB.db_name, self.tb_name)
        if not condition == "":
            sql += " " + condition
        cursor = self.DB.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        records = cursor.fetchall()
        results = {}
        for i in range(len(records)):
            results[i] = records[i]
        return results

    def update(self, data: dict):
        """
        Insert data for data with new keys.
        Update data for data with existed keys.
        """
        if len(data) == 0:
            return False
        # part 1
        columns = list(data[list(data.keys())[0]].keys())
        part1 = "(`" + self.key_col_name + "`,"
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
            keyval = key
            if type(keyval) == str:
                keyval = "'" + keyval + "'"
            part2 += str(keyval) + ","
            for column in columns:
                if not column in row:
                    raise AttributeError("Update method cannot process unbalance dictionary.")
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
        key = self.key_col_name
        if key == False:
            raise AttributeError("Cannot control a table without key column.")
        part3 = "`" + self.key_col_name + "` = VALUES(`" + self.key_col_name + "`)"
        # group parts
        sql = "INSERT INTO `{}`.`{}` ".format(self.DB.db_name, self.tb_name)
        sql += part1 + " VALUES "
        sql += part2 + " ON DUPLICATE KEY UPDATE "
        sql += part3 + ";"
        cursor = self.DB.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)

    def __get_key_col_name(self) -> str:
        sql = "SHOW COLUMNS FROM `{}`.`{}`;".format(
            self.DB.db_name, self.tb_name)
        cursor = self.DB.conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            if row["Key"] == "PRI":
                return row["Field"]
        return False
