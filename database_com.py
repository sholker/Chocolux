# The packkge databse_com is imported in app.py for mangement of database connection
import mysql.connector as ms # import package for mysql connector DB

DATABASE_NAME = "chocolateStore" # name of the database

class DatabaseConnection: # class for database connection
    # constructor function for database connection class
    def __init__(self, host="localhost", user="root", passwd="admin"):
        self.database_name = DATABASE_NAME # name of the database
        self.host = host # host of the database, default is localhost
        self.user = user # user of the database, default is root
        self.passwd = passwd # password of the database, default is admin
        self.connection = None # connection object for the database
        self.cursor = None # cursor object for the database
        self.create_database() # create database if not exists

    def connect(self): # connect to the database
        try:
            # create connection object
            conn = ms.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database_name)
            if conn.is_connected(): # check if connection is established
                return conn # return connection object
        except ms.Error as e: # if error occurs
            print(f"Error: {e}")

    def open_connection(self): # open connection to the database
        # if connection is not established, create connection object
        if not self.connection or not self.connection.is_connected():
            # create connection object
            self.connection = self.connect()
        # create cursor object
        self.cursor = self.connection.cursor(buffered=True)

    def close_connection(self): # close connection to the database
        if self.cursor: # if cursor object exists
            self.cursor.close() # close cursor object
            self.cursor = None # set cursor object to None
        if self.connection and self.connection.is_connected(): # if connection object exists
            self.connection.close() # close connection object

    def check_database_existence(self): # check if database exists
        self.open_connection() # open connection to the database
        try:
            # execute query
            self.cursor.execute(f"SHOW DATABASES LIKE '{self.database_name}'")
            # fetch result by one row
            result = self.cursor.fetchone()
            return result is not None # True if database exists False otherwise
        except ms.Error as e: # if error occurs
            print(f"Error: {e}")
        finally: # close connection to the database, in any cases
            self.close_connection() # close connection to the database

    def create_database(self): # create database if not exists
        self.open_connection() # open connection to the database
        try:
            # execute query
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")
        except ms.Error as e:
            print(f"Error: {e}")
        finally:
            # close connection to the database, in any cases
            self.close_connection()

    def table_exists(self, table_name): # check if table exists
        self.open_connection() # open connection to the database
        try:
            # execute query
            self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            # fetch result by one row
            result = self.cursor.fetchone()
            return result is not None # True if table exists False otherwise
        except ms.Error as e:
            print(f"Error: {e}")
        finally:
            # close connection to the database, in any cases
            self.close_connection()

    def create_table(self, table_name, **fields): # create table if not exists
        '''
        create a new table if not exists by passing the table name and fields,
        :param table_name: the name of the table
        :param fields: the fields of the table, each field is a
        dictionary with the following keys: primary_key, foreign_key, reference_table, unique, type
        :return: true if table is created successfully, false otherwise
        '''
        try:
            # Constructing the CREATE TABLE query dynamically
            query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, "

            # Adding fields to the query
            for field_name, field_info in fields.items(): # for each field
                field_type = field_info['type'] # get field type, True if field is primary key, False otherwise
                is_primary_key = field_info.get('primary_key', False) # get primary key, True if field is primary key, False otherwise
                is_foreign_key = field_info.get('foreign_key', False) # get foreign key,
                reference_table = field_info.get('reference_table', None) # get reference table, None if field is not foreign key
                is_unique = field_info.get('unique', False) # get unique, True if field is unique, False otherwise

                # Adding the field with its type to the query
                query += f"{field_name} {field_type}" # add field name and type, for example: name VARCHAR(255)

                # Adding primary key constraint
                if is_primary_key: # when there is a primary key constraint
                    query += " PRIMARY KEY" # add primary key constraint, for example: PRIMARY KEY(id)

                # Adding unique constraint
                if is_unique: # when there is a unique constraint
                    query += " UNIQUE" # add unique constraint, for example: UNIQUE(name)

                # Adding foreign key constraint
                if is_foreign_key and reference_table: # when there is a foreign key constraint and reference table is specified
                    # add foreign key constraint, for example: FOREIGN KEY(name) REFERENCES users(id)
                    query += f", FOREIGN KEY ({field_name}) REFERENCES {reference_table}(id)"
                # Adding trailing comma
                query += ", "
            # end of for loop, working in each field

            # Removing the trailing comma and closing the query
            # fixed the query we built above, and removed the trailing comma and closing the query
            # for example:
            # CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255),
            # email VARCHAR(255), <- fixed
            query = query.rstrip(', ') + ")"  #
            print(f'query: {query}')

            # Open, execute, and close the connection
            self.open_connection()
            self.cursor.execute(query) # execute query
        except ms.Error as e: # if error occurs, mysql error
            return e
        finally:
            # Close the connection, in any cases
            self.close_connection()

    def insert_into_table(self, table_name, **values):
        '''
        insert into a table if not exists by passing the table name and values,
        values is a dictionary with the following keys: id, name, email, etc.
        :param table_name: the name of the table
        :param values: the values of the table, each value is a dictionary with the following keys: id, name, email, etc.
        :return: True/False - if the insert was successful, the id of the newly inserted record
        '''
        try:
            # Construct the SQL query for insertion
            print(f"Values: {values}")
            fields = ', '.join(values.keys()) # get the fields
            # join the values with commas, for looping on all the values and adding between them a comma.
            values_data = ', '.join(
                [self.format_value(v) for v in values.values()])
            print(f"Values data: {values_data}")
            # build the query by string formatting, and adding the table name and the values
            query = f"INSERT INTO {table_name} ({fields}) VALUES ({values_data})"

            # Execute the query with the provided values
            self.open_connection() # open connection to the database
            print(f"Adding into table query: {query}")
            self.cursor.execute(query) # execute query

            # Commit the changes to the database
            self.connection.commit()

            # Return the ID of the newly inserted record
            print(f"Returning lastrowid: {self.cursor.lastrowid}")
            return True, self.cursor.lastrowid # return True and the id of the newly inserted record
        except ms.Error as e:
            return False, e # return False and the error
        finally:
            # Close the connection, in any cases
            self.close_connection()

    def format_value(self, value):
        '''
        Format the value to be used in the query, for example:
        - if the value is a string, wrap it with single quotes
        :param value:
        :return:
        '''
        if isinstance(value, str): # check if the value is a string type
            return f"'{value}'" # wrap the value with single quotes
        elif isinstance(value, bool): # check if the value is a boolean type
            return str(value).upper()  # Convert boolean to uppercase string ('True' or 'False')
        else: # all other types
            return str(value) # costing the value to string


    def search_in_table_by_fields(self, table_name, get_one=True, **fields): #{'name': 'Ori', 'age': 20}
        '''
        Search in a table by fields, if get_one is True, return the first result, if get_one is False, return all results
        :param table_name: the name of the table
        :param get_one: True/False - if True, return the first result, if False, return all results. default is True
        :param fields: dictionary with the fields and values to search in the table
        :return: True/False - if the search was successful, the result
        '''
        try:
            if self.table_exists(table_name): # check if the table exists
                print(f"search_in_table_by_fields fields: {fields}")
                # for loop on each field and value and join them with AND, for example: 'name = 'Ori' AND age = 20'
                conditions = ' AND '.join([f"{k} = '{v}' " for k, v in fields.items()]) # 'name = 'Ori' AND age = 20'
                # build the query by string formatting, and adding the table name and the conditions
                query = f"SELECT * FROM {table_name} WHERE {conditions}"
                print(f"search_in_table_by_fields query: {query}")
                # open the DB connection
                self.open_connection()
                # execute the query
                self.cursor.execute(query)
                # if get_one is True, return the first result, if get_one is False, return all results
                if get_one:
                    result = self.cursor.fetchone()
                else: # get_one is False, return all results
                    result = self.cursor.fetchall() # fetch all results

                if result: # if result is not empty
                    print(f"found, result: {result}")
                    return True, result # return True and the result
                else: # if result is empty
                    print(f"No matching rows found.")
                    # return False and the error
                    return False, "No matching rows found."
            else: # if the table does not exist
                print(f"Table {table_name} does not exist")
                # return False and the error
                return False, f"Table {table_name} does not exist"
        except ms.Error as e:
            # return False and the error
            return False, str(e)
        finally:
            # Close the connection, in any cases
            self.close_connection()

    def select_all_from_table(self, table_name):
        '''
        Select all from a table, no filtering
        :param table_name: the name of the table
        :return: True/False - if the search was successful, the result
        '''
        try:
            # check if the table exists
            if self.table_exists(table_name):
                # build the query by string formatting, and adding the table name
                query = f"SELECT * FROM {table_name}"
                print(f"select_all_from_table query: {query}")
                # open the DB connection
                self.open_connection()
                # execute the query
                self.cursor.execute(query)
                # for loop on each row, and return the headers and the rows
                headers = [description[0] for description in self.cursor.description]
                # fetch all results all tbale data values
                rows = self.cursor.fetchall()
                # return the headers and the rows
                return headers, rows
        except ms.Error as e:
            # return False and the error
            return False, str(e)
        finally:
            # Close the connection, in any cases
            self.close_connection()

    def update_table_by_fields(self, table_name,id, **fields): #{'name': 'Ori', 'age': 20}
        '''
        Update a table by fields, the id is required
        :param table_name: table name
        :param id: the id of the row to update
        :param fields: the fields to update
        :return: true/False - if the update was successful, error message
        '''
        try:
            # for loop on each field and value and join them with AND, for example: 'name = 'Ori' AND age = 20'
            update_field = ', '.join([f"{k} = '{v}'" for k, v in fields.items()]) # join the fields with their values for sql formatting
            # build the query by string formatting, and adding the table name and the conditions
            query = f"UPDATE {table_name} SET {update_field} WHERE id = {id}"
            print(f'Update query: {query}')
            # open the DB connection
            self.open_connection()
            # execute the query
            self.cursor.execute(query)
            # commit the changes
            self.connection.commit()
            # when successful, return True and None
            return True, None
        except ms.Error as e:
            # return False and the error
            print(f"Error in delete_row: {e}")
            return False, str(e)
        finally:
            # Close the connection, in any cases
            self.close_connection()

    def delete_row(self, table_name, **fields): #{'user_ID': 1}
        '''
        Delete a row from a table by fields name and value
        :param table_name: the name of the table
        :param fields: dictionary with the fields and values to search in the table, like {'user_ID': 1}
        :return: true/False - if the delete was successful, error message
        '''
        try:
            # for loop on each field and value and join them with AND, for example: 'ID = 1 AND age = 20
            fields = ', '.join([f"{k} = '{v}'" for k, v in fields.items()]) # join the fields with their values
            # build the query by string formatting, and adding the table name and the conditions
            query = f"DELETE FROM {table_name} WHERE {fields}"
            print(f"delete_row query: {query}")
            # open the DB connection
            self.open_connection()
            # execute the query
            self.cursor.execute(query)
            # commit the changes
            self.connection.commit()
            # when successful, return True and None
            return True, None
        except ms.Error as e:
            # return False and the error
            print(f"Error in delete_row: {e}")
            return False, str(e)
        finally:
            # Close the connection, in any cases
            self.close_connection()

    def create_view_4_cart_details(self):
        '''
        Create a view with all the cart details for a user
        :return: true/False - if the view was created, error message
        '''
        try:
            # build the query for the sopping cat details view
            query = '''CREATE VIEW shopping_cart_details AS
            select u.id as user_ID,
                   sc.id as cart_ID,
                   i.ItemName as Item_name,
                   i.image_path as image_path,
                   i.price as price,
                   sc.quantity as item_quantity,
                   (i.price * sc.quantity) AS total_price
                from ((chocolatestore.shopping_cart sc join chocolatestore.users u
                     on ((sc.user_Id = u.id))) join chocolatestore.items i on ((sc.item_Id = i.id)))
                where ((u.id = sc.user_Id) and (sc.item_Id = i.id));'''

            # open the DB connection
            self.open_connection()
            # execute the query
            self.cursor.execute(query)
            # commit the changes
            self.connection.commit()
            # when successful, return True and None
            return True, None

        except ms.Error as e:
            # return False and the error
            print(f"Error in delete_row: {e}")
            return False, str(e)
        finally:
            # Close the connection, in any cases
            self.close_connection()
            
    def create_view_4_admin_report(self):
        '''
        Create a view reporting the total orders and the total amount of orders for each user
        :return: true/False - if the view was created, error message
        '''
        try:
            # build the query for the report view
            query = '''CREATE VIEW user_order_totals AS
                        SELECT u.id AS user_ID,
                               u.username AS username,
                               u.firstname AS firstname,
                               u.lastname AS lastname,
                               COUNT(o.id) AS count_orders,
                               SUM(o.total) AS total_orders
                        FROM users u
                        LEFT JOIN orders o ON u.id = o.user_ID
                        GROUP BY u.id HAVING COUNT(o.id) > 0
                        ORDER BY total_orders DESC;'''
            print(f"query: {query}")
            # open the DB connection
            self.open_connection()
            # execute the query
            self.cursor.execute(query)
            # commit the changes
            self.connection.commit()
            # when successful, return True and None
            return True, None

        except ms.Error as e:
            # return False and the error
            print(f"Error in delete_row: {e}")
            return False, str(e)
        finally:
            # Close the connection, in any cases
            self.close_connection()