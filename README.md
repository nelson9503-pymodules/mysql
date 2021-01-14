# mysqloo - Object-oriented MySQL

## Prerequisite

mysqloo is built on [PyMySQL](https://pypi.org/project/PyMySQL/).

```bash
pip install PyMySQL
```

## Quick Start

Here is an simple example to create a database and a table.

```python
import mysqloo

# connect to the mysql server.
conn = mysqloo.NewConnection(
    user="username",
    password="123456",
    host="127.0.0.1", # this is local host
    port=3305
)

dbName = "maindb"
# check if database not in server, create new one.
if not dbName in conn.listDatabase():
    conn.createDatabase(dbName)
# connect to database
db = conn.Database(dbName)

tbName = "employee"
# check if table not in database, create new one.
if not tbName in db.listTable():
    db.createTable(
        tbName,
        "staffid", # key column
        "INT" # key data type
    )
tb = conn.Dataabse(tbName)

# create the column we need
if not "name" in tb.listColumn():
    tb.addColumn("name", "CHAR(30)")
if not "age" in tb.listColumn():
    tb.addColumn("age", "INT")

# this is the data we need update to the table
dataToUpdate = {
    0: {"staffid": 0, "name": "Tom", "age": 28},
    1: {"staffid": 1, "name": "Peter", "age": 45},
    2: {"staffid": 2, "name": "Tony", "age": 32}
}
# update the data
tb.update(dataToUpdate)

# don't forget to commit the changes
conn.commit()
# and don't forget disconnect to the sql server
conn.close()
```


## Methods Discovery

**func |** NewConnection ( user: str, password: str, host: str, port: int )

**class |** Connection

* **var |** user: `str`
* **var |** password: `str`
* **var |** host: `str`
* **var |** port: `int`
* **func |** connect ( )
* **func |** commit ( )
* **func |** close ( )
* **func |** exec ( quote: `str` ) **->** result: `dict`
* **func |** list_database ( ) **->** result: `list`
* **func |** count_database ( ) **->** result: `int`
* **func |** create_database ( name: `str` )
* **func |** Database ( name: `str` ) **->** Database: `Database Object`

**class |** Database

* **func |** drop ( )
* **func |** list_table ( ) **->** result: `list`
* **func |** count_table ( ) **->** result: `int`
* **func |** create_table ( name: `str`, spec: `dict` )
* **func |** Table ( name: `str` ) **->** Table: `Table Object`

**class |** Table

* **func |** drop ( )
* **func |** clear ( )
* **func |** keyCol ( )
* **func |** list_column ( ) **->** result: `list`
* **func |** map_column ( ) **->** result: `dict`
* **func |** count_column ( ) **->** result: `int`
* **func |** add_column ( name: `str`, spec: `str` )
* **func |** drop_column ( name: `str` )
* **func |** alter_column ( name: `str`, spec: `str` )
* **func |** count_row ( ) **->** result: `int`
* **func |** drop_row ( keyVal: *any* )
* **func |** query ( column: `str`, condiction: `str` ) **->** result: `dict`
* **func |** update ( data: `list`+`dict` )