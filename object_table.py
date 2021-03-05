import pymysql

# Table object manage the data in the table.


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
        self.DB.execute(sql)

    def rename(self, new_tb_name: str):
        """
        Rename table name.
        """
        sql = "ALTER TABLE `{db}`.`{tb}` RENAME `{db}`.`{new_tb}`;".format(
            db=self.DB.db_name,
            tb=self.tb_name,
            new_tb=new_tb_name
        )
        self.DB.execute(sql)
        self.tb_name = new_tb_name

    def list_col(self) -> list:
        """
        List out columns in the table.
        """
        sql = "SHOW COLUMNS FROM `{}`.`{}`;".format(
            self.DB.db_name, self.tb_name)
        cols = []
        results = self.DB.execute(sql, True)
        for row in results:
            cols.append(row["Field"])  # "Field" is column of column names.
        return cols

    def add_col(self, col_name: str, data_type: str):
        """
        Add a new column to the table.
        """
        sql = "ALTER TABLE `{}`.`{}` ADD `{}` {};".format(
            self.DB.db_name, self.tb_name, col_name, data_type)
        self.DB.execute(sql)

    def drop_col(self, col_name: str):
        """
        Drop the column from the table.
        """
        sql = "ALTER TABLE `{}`.`{}` DROP `{}`;".format(
            self.DB.db_name, self.tb_name, col_name)
        self.DB.execute(sql)

    def drop_data(self, key_value: any):
        """
        Drop a row of data by using key.
        """
        sql = "DELETE FROM `{}`.`{}` WHERE `{}`={};".format(
            self.DB.db_name, self.tb_name, self.key_col_name, key_value)
        self.DB.execute(sql)

    def query(self, column: str = "*", condition="") -> dict:
        """
        Query the table and return results in dictionary.
        Users can edit the sql quote via the arguments:
            SELECT {column} from db.tb [WHERE] {condition};
        """
        sql = "SELECT {} FROM `{}`.`{}`".format(
            column, self.DB.db_name, self.tb_name)
        # if user has been set condition,
        if not condition == "":
            sql += " " + condition
        records = self.DB.execute(sql, True)
        # The records returned is a list of dictionary, ([{row data}, {row data}, ...])
        # We need a complete dictionary so that the users will not be surprised.
        results = {}
        for i in range(len(records)):
            results[i] = records[i]
        return results

    def update(self, data: dict):
        """
        Insert data for data with new keys.
        Update data for data with existed keys.
        """
        if len(data) == 0:  # skip update for empty dictionary
            return
        part1 = self.__generate_update_quote_part1(data)
        part2 = self.__generate_update_quote_part2(data)
        part3 = self.__generate_update_quote_part3(data)
        # group different parts of sql quotes
        sql = "INSERT INTO `{db}`.`{tb}` {part1} VALUES {part2} ON DUPLICATE KEY UPDATE {part3};".format(
            db=self.DB.db_name,
            tb=self.tb_name,
            part1=part1,
            part2=part2,
            part3=part3
        )
        self.DB.execute(sql)

    # This part generate the part1 of update sql quote.
    # The output is like this: (column, column, column, column)
    def __generate_update_quote_part1(self, data: dict) -> str:
        first_key_of_data = list(data.keys())[0]  # get the first key value
        # get the column names from first row of data
        columns = list(data[first_key_of_data].keys())
        # write column key as first column -> (`key column name`,
        part1 = "(`{}`,".format(self.key_col_name)
        # write the rest column names to part1 -> (`key column name`,`column name`,`column name`...
        for column in columns:
            part1 += "`{}`,".format(column)
        # remove the last "," and add )
        if part1[-1] == ',':
            part1 = part1[:-1]
        part1 += ")"
        return part1

    # This part generate the part2 of update sql quote.
    # The output is like this: (val, val, val, val), (val, val, val, val), ...
    def __generate_update_quote_part2(self, data: dict) -> str:
        first_key_of_data = list(data.keys())[0]  # get the first key value
        # get the column names from first row of data
        columns = list(data[first_key_of_data].keys())
        part2 = ""
        for key in data:
            row = data[key]
            part2 += "("
            # insert value of key column first
            if type(key) == str:
                key = "'{}'".format(key)
            part2 += str(key) + ","
            # insert the rest of values of columns
            for column in columns:
                if not column in row:
                    raise KeyError("Rows contains different columns.")
                val = row[column]
                # in case value is string
                if type(val) == str:
                    val = "'{}'".format(val)
                # in case value is None
                if val == None:
                    val = "null"
                part2 += str(val) + ","
            # remove the last , and add ),
            if part2[-1] == ',':
                part2 = part2[:-1]
            part2 += "),"
        # remove the last ,
        if part2[-1] == ',':
            part2 = part2[:-1]
        return part2

    # This part generate the part3 of update sql quote.
    def __generate_update_quote_part3(self, data: dict) -> str:
        key = self.key_col_name
        if key == False:
            raise AttributeError("Cannot control a table without key column.")
        part3 = "`{key_col_name}` = VALUES(`{key_col_name}`)".format(
            key_col_name = self.key_col_name
        )
        return part3

    # We ask sql server for the details of columns of table.
    # And then we get the primary key column from it.
    def __get_key_col_name(self) -> str:
        sql = "SHOW COLUMNS FROM `{}`.`{}`;".format(
            self.DB.db_name, self.tb_name)
        results = self.DB.execute(sql, True)
        for row in results:
            if row["Key"] == "PRI":  # only key column fit this condition
                return row["Field"]  # "Field" is the column of column names
        # If no primary key column can be found, return False.
        # This case is unexpected because sql server cannot
        # control a table without primary key.
        return False
