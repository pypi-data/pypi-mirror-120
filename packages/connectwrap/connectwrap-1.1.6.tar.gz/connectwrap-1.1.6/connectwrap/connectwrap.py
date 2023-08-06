#!/usr/bin/env python3

import sqlite3, os
from connectwrap import utils

class db:

    # Constructor
    def __init__(self, db_filepath, db_table = None):
        if (type(db_filepath) is not str):
            raise TypeError("The path to the db_filepath isn't a string!")

        if (os.path.exists(db_filepath) == False):
            raise FileNotFoundError("The file that the db_filepath argument represents doesn't exist!")

        if (os.path.isfile(db_filepath) == False):
            raise ValueError("The db_filepath argument isn't a file!")

        if (utils.isdb(db_filepath) == False):
            raise ValueError("The db_filepath argument doesn't have the correct extension! Use .db, .sqlite, or .sqlite3!")

        if (db_table is not None):
            if (type(db_table) is not str):
                raise TypeError("The db_table attribute isn't a string!")
            
        self.db_filepath = str(db_filepath)
        self.db_table = db_table
        self.connection = sqlite3.connect(self.db_filepath)
        self.connection_cursor = self.connection.cursor()
        self.connection_status = bool(True)

    # Custom exception to raise when the Database is open.
    class DatabaseOpenError(Exception):
        pass

    # Custom exception to raise when the Database is not open.
    class DatabaseNotOpenError(Exception):
        pass

    # Custom exception to raise when an argument table doesn't exist in a database. 
    class TableNotFoundError(Exception):
        pass

    # Custom exception to raise when an argument table already exists in a database. 
    class TableExistsError(Exception):
        pass

    # Execute a custom query.
    def execute(self, query):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(query) is not str):
            raise TypeError("The query argument isn't a string!")

        return self.connection_cursor.execute(query)

    # Commit a query held in the connection cursor. 
    def commit(self):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        self.connection.commit()

    # Close database connection.
    def close_db(self):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        self.connection.close()
        self.connection_status = bool(False)

    # Open database connection. Reset the cursor. 
    def open_db(self):
        if (self.connection_status != False):
            raise db.DatabaseOpenError("Database is not closed! The connection status attribute is not set to False!")

        self.connection = sqlite3.connect(self.db_filepath)
        self.connection_cursor = self.connection.cursor()
        self.connection_status = bool(True)

    # Change the db_filepath attribute value. 
    def set_db_filepath(self, db_filepath):
        if (type(db_filepath) is not str):
            raise TypeError("The path to the db_filepath isn't a string!")

        if (os.path.exists(db_filepath) == False):
            raise FileNotFoundError("The file that the db_filepath argument represents doesn't exist!")

        if (os.path.isfile(db_filepath) == False):
            raise ValueError("The db_filepath argument isn't a file!")

        if (utils.isdb(db_filepath) == False):
            raise ValueError("The db_filepath argument doesn't have the correct extension! Use .db, .sqlite, or .sqlite3!")
        
        if (self.connection_status == True): 
            db.close_db(self)
            self.db_filepath = str(db_filepath)
            db.open_db(self)
        else: 
            self.db_filepath = str(db_filepath)
            db.open_db(self)

    # Change the db_table attribute value.
    def set_db_table(self, db_table):
        if (type(db_table) is not str):
            raise TypeError("The db_table argument isn't a string!")

        if (db.table_exists(self, db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        self.db_table = db_table

    # Return the connection_status attribute representing whether the Database connection is open or closed. 
    # Opened = True; Closed = False
    def get_connection_status(self):
        return self.connection_status

    # Return the db_filepath attribute value representing the database file path.
    def get_db_filepath(self):
        return self.db_filepath

    # Return the db_table attribute value.
    def get_db_table(self):
        return self.db_table

    # Select and return the table names within a database as strings in a list. 
    def get_tablenames(self):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        table_names = list([])
        query = "SELECT name FROM sqlite_master WHERE type='table'"

        for name in db.execute(self, query):
            name = str(name).strip("(,')")
            table_names.append(name)

        return table_names

    # Select and return the key names within the db_table attribute table as strings in a list. 
    def get_keys(self):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!") 
        
        connection = sqlite3.connect(self.db_filepath)
        connection.row_factory = sqlite3.Row
        connection_cursor = connection.cursor()
        query = str(f"SELECT * FROM {self.db_table}")
        connection_cursor.execute(query)
        row = connection_cursor.fetchone()
        connection.close()
        return list(row.keys())

    # Select and return a list of the values in a column within the db_table attribute table based on the key from that column.
    def get_column(self, key):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(key) is not str):
            raise TypeError("The key argument isn't a string!")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        if (db.key_exists(self, key) == False):
            raise KeyError("The key argument doesn't exist within the db_table attribute table!")

        column_values = list([])
        query = str(f"SELECT {key} FROM {self.db_table}")

        for column in db.execute(self, query):
            column = str(column).strip("(,')")

            if (column.isdigit() == True):
                column = int(column)
            elif (utils.isfloat(column) == True):
                column = float(column)
            elif (utils.ishex(column) == True):
                column = bytes.fromhex(column)
            elif (column == "None"):
                column = None
            else:
                column = str(column)
                
            column_values.append(column)
            
        return column_values

    # Select and return a dictionary representing a row in the db_table attribute table where the key and value arguments match a row column key and value pair. 
    # Only returns the first row with the occurance of the key/value argument pair.
    # Returns None if there's no occurance of the key/value argument in any row in the table.
    # The key argument must be a string and a key within the table.
    # The value argument must be one of the following types - int, float, str, bytes, None.  
    def get_row(self, key, value):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(key) is not str):
            raise TypeError("The key argument isn't a string!")

        if (type(value) is not int and type(value) is not float and type(value) is not str and type(value) is not bytes and value != None):
            raise TypeError("The value argument must be one of the following types - int, float, str, bytes, None")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        if (db.key_exists(self, key) == False):
            raise KeyError("The key argument doesn't exist within the db_table attribute table!")

        table = list(db.get_table(self))
        i = int(0)

        while(i < len(table)):
            row = dict(table[i])
                
            for row_key in row:
                if (key == row_key and value == row[row_key]):
                    return row
                
            i += 1
            
        return None

    # Select and return a list of dictionaries with each dictionary representing a row in the db_table attribute table.
    def get_table(self):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        table = list([])
        keys = list(db.get_keys(self))
        query = str(f"SELECT * FROM {self.db_table}")

        for row in db.execute(self, query):
            row_dict = dict.fromkeys(keys)
            row_factor = list([])
            i = int(0)

            for column in row:
                column = str(column).strip("(,')") 
                            
                if (column.isdigit() == True):
                    column = int(column)
                elif (utils.isfloat(column) == True):
                    column = float(column)   
                elif (utils.ishex(column) == True):
                    column = bytes.fromhex(column)    
                elif (column == "None"):
                    column = None
                else:
                    column = str(column)
                
                row_factor.append(column)

            for key in row_dict:
                row_dict[key] = row_factor[i]
                i += 1
                
            table.append(row_dict)

        return table 

    # Select and return a list of dictionaries representing rows in the db_table attribute table limited to the number designated in the 'total' argument.
    def get_top(self, total):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        if (type(total) is not int):
            raise TypeError("The total argument isn't an int!")

        table = list([])
        keys = list(db.get_keys(self))
        query = str(f"SELECT * FROM {self.db_table} LIMIT {total}")

        for row in db.execute(self, query):
            row_dict = dict.fromkeys(keys)
            row_factor = list([])
            i = int(0)

            for column in row:
                column = str(column).strip("(,')") 
                            
                if (column.isdigit() == True):
                    column = int(column)
                elif (utils.isfloat(column) == True):
                    column = float(column)   
                elif (utils.ishex(column) == True):
                    column = bytes.fromhex(column)    
                elif (column == "None"):
                    column = None
                else:
                    column = str(column)
                
                row_factor.append(column)

            for key in row_dict:
                row_dict[key] = row_factor[i]
                i += 1
                
            table.append(row_dict)

        return table

    # Rename db_table attribute table. 
    def rename_table(self, table):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(table) is not str):
            raise TypeError("The tablename argument isn't a string!")

        if (db.table_exists(self, table) == True):
            raise db.TableExistsError("The tablename argument table already exists within the database!")

        query = str(f"ALTER TABLE {self.db_table} RENAME TO {table}")
        db.execute(self, query)
        db.commit(self)
        self.db_table = table
    
    # Drop/delete table in the database. 
    def drop_table(self, table):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(table) is not str):
            raise TypeError("The table argument isn't a string!")

        if (db.table_exists(self, table) == False):
            raise db.TableNotFoundError("The table doesn't exist within the database!")
        
        query = str(f"DROP TABLE {table}")
        db.execute(self, query)
        db.commit(self)

    # Drop/delete rows within the db_table attribute table with matching key & value. 
    # The key argument must be a string and a key within the table. 
    # The value argument must be one of the following types - int, float, str, bytes, None.
    def drop_row(self, key, value):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(key) is not str):
            raise TypeError("The key argument isn't a string!")

        if (type(value) is not int and type(value) is not float and type(value) is not str and type(value) is not bytes and value != None):
            raise TypeError("The value argument must be one of the following types - int, float, str, bytes, None")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        if (db.key_exists(self, key) == False):
            raise KeyError("The key argument doesn't exist within the db_table attribute table!")

        if (value == None):
            value = str("'None'")
            
        if (type(value) is bytes):
            value = str("'" + value.hex() + "'").lower()
            
        if (type(value) is str):
            value = str("'" + value + "'")

        query = str(f"DELETE FROM {self.db_table} WHERE {key}={value}")
        db.execute(self, query)
        db.commit(self)

    # Create table within the file database.
    # The key in each kwargs entry denotes the key name of a column. 
    # The value in each kwargs entry denotes the data type of a column. 
    # The value in each kwargs entry must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'.     
    def create_table(self, table, **kwargs):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(table) is not str):
            raise TypeError("The table argument isn't a string!")

        if (db.table_exists(self, table) == True):
            raise db.TableExistsError("The table already exists within the database!")

        record = str("")
        count = int(0)
    
        for kwarg in kwargs:
            if (type(kwargs[kwarg]) is not str):
                raise TypeError("The value in kwargs must be a string!")

            if (kwargs[kwarg].lower() != "int" and kwargs[kwarg].lower() != "float" and kwargs[kwarg].lower() != "str" and kwargs[kwarg].lower() != "bytes" and kwargs[kwarg].lower().title() != "None"):
                raise ValueError("The value in kwargs must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'")

            if (kwargs[kwarg].lower() == "int"):
                kwargs[kwarg] = "INTEGER"
            elif (kwargs[kwarg].lower() == "float"):
                kwargs[kwarg] = "REAL"
            elif (kwargs[kwarg].lower() == "str"):
                kwargs[kwarg] = "TEXT"
            elif (kwargs[kwarg].lower() == "bytes"):
                kwargs[kwarg] = "BLOB"
            else:
                kwargs[kwarg] = "NULL"

            if (count < len(kwargs) - 1):
                record += (kwarg + " " + kwargs[kwarg] + ",")
            else:
                record += (kwarg + " " + kwargs[kwarg])

            count += 1
        
        query = str(f"CREATE TABLE {table} ({record})") 
        db.execute(self, query)
        db.commit(self)

    # Create a new column within the db_table attribute table.
    # The datatype argument must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'.
    def create_column(self, column, datatype):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(column) is not str):
            raise TypeError("The column argument isn't a string!")

        if (type(datatype) is not str):
            raise TypeError("The datatype argument isn't a string!")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        if (db.key_exists(self, column) == True):
            raise KeyError("The column already exists within the db_table attribute table!")

        if (datatype.lower() != "int" and datatype.lower() != "float" and datatype.lower() != "str" and datatype.lower() != "bytes" and datatype.lower().title() != "None"):
            raise ValueError("The datatype argument must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'")

        if (datatype.lower() == "int"):
            datatype = "INTEGER"
        elif (datatype.lower() == "float"):
            datatype = "REAL"
        elif (datatype.lower() == "str"):
            datatype = "TEXT"
        elif (datatype.lower() == "bytes"):
            datatype = "BLOB"
        else:
            datatype = "NULL"

        query = str(f"ALTER TABLE {self.db_table} ADD {column} {datatype}")
        db.execute(self, query)
        db.commit(self)

    # Select and output to terminal the table names within a database. 
    def select_tablenames(self):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        for name in db.get_tablenames(self):
            print("Table Name:", name)

    # Select and output to terminal the rows from the db_table attribute table.
    def select_table(self):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        for row in db.get_table(self):
            print(self.db_table, "Row:", row)

    # Select and output to terminal the rows from the db_table attribute table limited to the number designated in the 'total' argument.
    def select_top(self, total):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        if (type(total) is not int):
            raise TypeError("The total argument isn't an int!")

        for row in db.get_top(self, total):
            print(self.db_table, "Row:", row)
       
    # Select and output to terminal the values from keys within the db_table attribute table. 
    # Each arg in *args arguments must be strings containing key names within the table.
    def select_column(self, *args):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        for arg in args:
            if (type(arg) is not str):
                raise TypeError("An argument in args isn't a string!")

            print(self.db_table, "Column", arg + ":", db.get_column(self, arg), sep=" ")
            
    # Select and output to terminal the key names within the db_table attribute table. 
    def select_keys(self):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        print(self.db_table, "Keys:", db.get_keys(self))
    
    # Select and output to terminal a row in the db_table attribute table.  
    # Only outputs the first row with the occurance of the key/value argument pair.
    # Outputs None if there's no occurance of the key/value argument in any row in the table.
    # The key argument must be a string and a key within the table. 
    # The value argument must be one of the following types - int, float, str, bytes, None.
    def select_row(self, key, value):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (type(key) is not str):
            raise TypeError("The key argument isn't a string!")

        if (type(value) is not int and type(value) is not float and type(value) is not str and type(value) is not bytes and value != None):
            raise TypeError("The value argument must be one of the following types - int, float, str, bytes, None")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        if (db.key_exists(self, key) == False):
            raise KeyError("The key argument doesn't exist within the db_table attribute table!")

        print(self.db_table, "Row:", db.get_row(self, key, value))

    # Insert a row of data into the db_table attribute table.
    # Each arg in *args must be one of the following types - int, float, str, bytes, None.
    def insert_row(self, *args):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        record = str("")
        count = int(0)

        for arg in args:
            if (type(arg) is not int and type(arg) is not float and type(arg) is not str and type(arg) is not bytes and arg != None):
                raise TypeError("The argument must be one of the following types - int, float, str, bytes, None")

            if (count < len(args) - 1):
                if (type(arg) is str):
                    record += "'" + arg + "'" + ","
                elif (type(arg) is bytes):
                    arg = arg.hex()
                    record += "'" + str(arg).lower() + "'" + ","
                elif (arg == None):
                    record += "'None'" + "," 
                else:
                    record += str(arg) + ","
            else: 
                if (type(arg) is str):
                    record += "'" + arg + "'"
                elif (type(arg) is bytes):
                    arg = arg.hex()
                    record += "'" + str(arg).lower() + "'"
                elif (arg == None):
                    record += "'None'"
                else:
                    record += str(arg)

            count += 1

        query = str(f"INSERT INTO {self.db_table} VALUES ({record})")
        db.execute(self, query)
        db.commit(self)

    # Update/change row column values within the db_table attribute table.
    # The key arguments must be strings and keys within the table. 
    # The value arguments must be one of the following types - int, float, str, bytes, None.
    def update_row(self, change_key, change_value, check_key, check_value):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")
        
        if (type(change_key) is not str):
            raise TypeError("The key argument isn't a string!")

        if (type(check_key) is not str):
            raise TypeError("The key argument isn't a string!")

        if (type(change_value) is not int and type(change_value) is not float and type(change_value) is not str and type(change_value) is not bytes and change_value != None):
            raise TypeError("The change_value argument must be one of the following types - int, float, str, bytes, None")

        if (type(check_value) is not int and type(check_value) is not float and type(check_value) is not str and type(check_value) is not bytes and check_value != None):
            raise TypeError("The check_value argument must be one of the following types - int, float, str, bytes, None")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        if (db.key_exists(self, change_key) == False):
            raise KeyError("The change_key argument doesn't exist within the db_table attribute table!")

        if (db.key_exists(self, check_key) == False):
            raise KeyError("The check_key argument doesn't exist within the db_table attribute table!")

        if (change_value == None):
            change_value = str("'None'")
            
        if (check_value == None):
            check_value = str("'None'")

        if (type(change_value) is bytes):
             change_value = str("'" + change_value.hex() + "'").lower()
            
        if (type(check_value) is bytes):
            check_value == str("'" + check_value.hex() + "'").lower()

        if (type(change_value) is str):
            change_value = str("'" + change_value + "'")

        if (type(check_value) is str):
            check_value = str("'" + check_value + "'")

        query = str(f"UPDATE {self.db_table} SET {change_key}={change_value} WHERE {check_key}={check_value}")
        db.execute(self, query)
        db.commit(self)

    # Return True if the key argument exists in the db_table attribute table. 
    def key_exists(self, key):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")

        if (db.table_exists(self, self.db_table) == False):
            raise db.TableNotFoundError("The db_table attribute table doesn't exist within the database!")

        if (type(key) is not str):
            raise TypeError("The key argument isn't a string!")

        for element in db.get_keys(self):
            if (key == element):
                return True
        
        return False

    # Return True if the table argument is a table name within the database. 
    def table_exists(self, table):
        if (self.connection_status != True):
            raise db.DatabaseNotOpenError("Database is not open! The connection status attribute is not set to True!")
        
        if (type(table) is not str and table is not None):
            raise TypeError("The table argument isn't a string!")

        for name in db.get_tablenames(self):
            if (name == table):
                return True
        
        return False