# mysqloo - Methods

**func |** `NewConnection` `(` `user`: *str*, `password`: *str*, `host`: *str*, `port`: *int* `)`

**class |** `Connection`

* **var |** `user`: *str*
* **var |** `password`: *str*
* **var |** `host`: *str*
* **var |** `port`: *int*
* **func |** `connect` `(` `)`
* **func |** `commit` `(` `)`
* **func |** `close` `(` `)`
* **func |** `exec` `(` `quote`: *str* `)` `->` `result`: *dict*
* **func |** `list_database` `(` `)` `->` `result`: *list*
* **func |** `count_database` `(` `)` `->` `result`: *int*
* **func |** `create_database` `(` `name`: *str* `)`
* **func |** `Database` `(` `name`: *str* `)` `->` `Database`: *Database Object*

**class |** `Database`

* **func |** `drop` `(` `)`
* **func |** `list_table` `(` `)` `->` `result`: *list*
* **func |** `count_table` `(` `)` `->` `result`: *int*
* **func |** `create_table` `(` `name`: *str*, `spec`: *dict* `)`
* **func |** `Table` `(` `name`: *str* `)` `->` `Table`: *Table Object*

**class |** `Table`

* **func |** `drop` `(` `)`
* **func |** `clear` `(` `)`
* **func |** `keyCol` `(` `)`
* **func |** `list_column` `(` `)` `->` `result`: *list*
* **func |** `map_column` `(` `)` `->` `result`: *dict*
* **func |** `count_column` `(` `)` `->` `result`: *int*
* **func |** `add_column` `(` `name`: *str*, `spec`: *str* `)`
* **func |** `drop_column` `(` `name`: *str* `)`
* **func |** `alter_column` `(` `name`: *str*, `spec`: *str* `)`
* **func |** `count_row` `(` `)` `->` `result`: *int*
* **func |** `drop_row` `(` `keyVal`: *any* `)`
* **func |** `query` `(` `column`: *str*, `condiction`: *str* `)` `->` `result`: *dict*
* **func |** `update` `(` `data`: *list*+*dict* `)`