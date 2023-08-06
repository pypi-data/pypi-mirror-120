# ***connectwrap***

    Python package made to manage, display & parse data from SQLite file databases. 

    Python version 3.6 is required at a minimum.   

    To install the package with pip enter command in terminal:
        pip install connectwrap

    To uninstall the package with pip enter command in terminal:
        pip uninstall connectwrap

## ***Module db***

<table width="100%">
	<tr>
		<th align="left">
            Attribute/Exception/Method
        </th>
		<th align="left">
            Description
        </th>
	</tr>
	<tr>
		<td>
            <code>db_filepath</code>
        </td>
		<td>
            Attribute of the string type representing the database file path. <br/>
            The file must have a .db, .sqlite, or .sqlite3 extension.
        </td>
	</tr>
    <tr>
		<td>
            <code>db_table</code>
        </td>
		<td>
            Attribute of the string type representing a table within the database.
            Optional, set to None by default without constructor.
        </td>
	</tr>
    <tr>
		<td>
            <code>connection</code>
        </td>
		<td>
            Attribute of the Connection type from the sqlite3 module representing the database connection. Used to commit changes to database.
        </td>
	</tr>
    <tr>
		<td>
            <code>connection_cursor</code>
        </td>
		<td>
            Attribute of the Cursor type from the sqlite3 module representing the database connection cursor. Used to execute queries.
        </td>
	</tr>
    <tr>
		<td>
            <code>connection_status</code>
        </td>
		<td>
            Attribute of the bool type representing whether the Database connection is opened or closed. <br/>
            Set to True upon the creation of a new Database object. <br/>
            Opened = True <br/>
            Closed = False
        </td>
	</tr>
    <tr>
		<td>
            <code>DatabaseOpenError</code>
        </td>
		<td>
            Custom exception to raise when the Database is open.
        </td>
	</tr>
    <tr>
		<td>
            <code>DatabaseNotOpenError</code>
        </td>
		<td>
            Custom exception to raise when the Database is not open.
        </td>
	</tr>
    <tr>
		<td>
            <code>TableNotFoundError</code>
        </td>
		<td>
            Custom exception to raise when an argument table doesn't exist in a database.
        </td>
	</tr>
    <tr>
		<td>
            <code>TableExistsError</code>
        </td>
		<td>
            Custom exception to raise when an argument table already exists in a database.
        </td>
	</tr>
    <tr>
		<td>
            <code>execute(query)</code>
        </td>
		<td>
            Execute a custom query. The query argument must be a string.
        </td>
	</tr>
    <tr>
		<td>
            <code>commit()</code>
        </td>
		<td>
            Commit a query held in the connection cursor.
        </td>
	</tr>
    <tr>
		<td>
            <code>close_db()</code>
        </td>
		<td>
            Close database connection.
        </td>
	</tr>
    <tr>
		<td>
            <code>open_db()</code>
        </td>
		<td>
            Open database connection. Reset the cursor.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_db_filepath(db_filepath)</code>
        </td>
		<td>
            Change the db_filepath attribute value. <br/>
            The file must have a .db, .sqlite, or .sqlite3 extension. <br/>
            This allows you to switch between file databases while only creating one object. <br/>
            Works on open or closed databases. The result of this method will be an open Database using the db_filepath argument as the new Database file path.
        </td>
	</tr>
    <tr>
		<td>
            <code>set_db_table(db_table)</code>
        </td>
		<td>
            Change the db_table attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_connection_status()</code>
        </td>
		<td>
            Return the connection_status attribute representing whether the Database connection is open or closed. <br/>
            Opened = True <br/>
            Closed = False
        </td>
	</tr>
    <tr>
		<td>
            <code>get_db_filepath()</code>
        </td>
		<td>
            Return the db_filepath attribute value representing the database file path.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_db_table()</code>
        </td>
		<td>
            Return the db_table attribute value.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_tablenames()</code>
        </td>
		<td>
            Select and return the table names within a database as strings in a list.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_keys()</code>
        </td>
		<td>
            Select and return the key names within the db_table attribute table as strings in a list.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_column(key)</code>
        </td>
		<td>
            Select and return a list of the values in a column within the db_table attribute table based on the key from that column.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_row(key, value)</code>
        </td>
		<td>
            Select and return a dictionary representing a row in the db_table attribute table where the key and value arguments match a row column key and value pair. <br/>
            Only returns the first row with the occurance of the key/value argument pair. <br/>
            Returns None if there's no occurance of the key/value argument in any row in the table. <br/>
            The key argument must be a string and a key within the table. <br/>
            The value argument must be one of the following types - int, float, str, bytes, None.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_table()</code>
        </td>
		<td>
           Select and return a list of dictionaries with each dictionary representing a row in the db_table attribute table.
        </td>
	</tr>
    <tr>
		<td>
            <code>get_top(total)</code>
        </td>
		<td>
           Select and return a list of dictionaries representing rows in the db_table attribute table limited to the number designated in the 'total' argument.
        </td>
	</tr>
    <tr>
		<td>
            <code>rename_table(tablename)</code>
        </td>
		<td>
            Rename db_table attribute table.
        </td>
	</tr>
    <tr>
		<td>
            <code>drop_table(table)</code>
        </td>
		<td>
            Drop/delete table in the file database.
        </td>
	</tr>
    <tr>
		<td>
            <code>drop_row(key, value)</code>
        </td>
		<td>
            Drop/delete rows within the db_table attribute table with matching key & value. <br/>
            The key argument must be a string and a key within the table. <br/>
            The value argument must be one of the following types - int, float, str, bytes, None.
        </td>
	</tr>
    <tr>
		<td>
            <code>create_table(table, **kwargs)</code>
        </td>
		<td>
            Create table within the file database. <br/>
            The key in each kwargs entry denotes the key name of a column. <br/>
            The value in each kwargs entry denotes the data type of a column. <br/> 
            The value in each kwargs entry must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'.
        </td>
	</tr>
    <tr>
		<td>
            <code>create_column(column, datatype)</code>
        </td>
		<td>
            Create a new column within the db_table attribute table. <br/>
            The datatype argument must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'.
        </td>
	</tr>
    <tr>
		<td>
            <code>select_tablenames()</code>
        </td>
		<td>
            Select and output to terminal the table names within a database.
        </td>
	</tr>
    <tr>
		<td>
            <code>select_table()</code>
        </td>
		<td>
            Select and output to terminal the rows from the db_table attribute table.
        </td>
	</tr>
    <tr>
		<td>
            <code>select_top(total)</code>
        </td>
		<td>
            Select and output to terminal the rows from the db_table attribute table limited to the number designated in the 'total' argument.
        </td>
	</tr>
    <tr>
		<td>
            <code>select_column(*args)</code>
        </td>
		<td>
             Select and output to terminal the values from keys within the db_table attribute table. <br/> Each arg in *args arguments must be strings containing key names within the table.
        </td>
	</tr>
    <tr>
		<td>
            <code>select_keys()</code>
        </td>
		<td>
            Select and output to terminal the key names within the db_table attribute table.
        </td>
	</tr>
    <tr>
		<td>
            <code>select_row(key, value)</code>
        </td>
		<td>
            Select and output to terminal a row in the db_table attribute table. <br/>  
            Only outputs the first row with the occurance of the key/value argument pair. <br/>
            Outputs None if there's no occurance of the key/value argument in any row in the table. <br/>
            The key argument must be a string and a key within the table. <br/>
            The value argument must be one of the following types - int, float, str, bytes, None.
        </td>
	</tr>
    <tr>
		<td>
            <code>insert_row(*args)</code>
        </td>
		<td>
            Insert a row of data into the db_table attribute table. <br/>
            Each arg in *args must be one of the following types - int, float, str, bytes, None.
        </td>
	</tr>
    <tr>
		<td>
            <code>update_row(change_key, change_value, check_key, check_value)</code>
        </td>
		<td>
            Update/change row column values within the db_table attribute table. <br/>
            The key arguments must be strings and keys within the table. <br/>
            The value arguments must be one of the following types - int, float, str, bytes, None.
        </td>
	</tr>
    <tr>
		<td>
            <code>key_exists(key)</code>
        </td>
		<td>
            Return True if the key argument exists in the db_table attribute table.
        </td>
	</tr>
    <tr>
		<td>
            <code>table_exists(table)</code>
        </td>
		<td>
            Return True if the table argument is a table name within the database.
        </td>
	</tr>
</table>

## ***Module utils***

<table width="100%">
	<tr>
		<th align="left">
            Method
        </th>
		<th align="left">
            Description
        </th>
	</tr>
    <tr>
		<td>
            <code>drop_database(db_filepath)</code>
        </td>
		<td>
            Drop/delete .db, .sqlite, or .sqlite3 file database.
        </td>
	</tr>
    <tr>
		<td>
            <code>create_database(db_filepath)</code>
        </td>
		<td>
            Create .db, .sqlite, or .sqlite3 file database.
        </td>
	</tr>
    <tr>
		<td>
            <code>ishex(arg)</code>
        </td>
		<td>
            Return True if all characters in arg string are hexadecimal.
        </td>
	</tr>
    <tr>
		<td>
            <code>isfloat(arg)</code>
        </td>
		<td>
            Return True if arg string characters constitute a float.
        </td>
	</tr>
    <tr>
		<td>
            <code>isdb(db_filepath)</code>
        </td>
		<td>
            Return True if db_filepath argument has one of the follow extensions: .db, .sqlite, or .sqlite3
        </td>
	</tr>
</table>

[Back to Top](#connectwrap)

---
