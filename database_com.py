import mysql.connector as ms

DATABASE_NAME = "chocolateStore"

class DatabaseConnection:
    def __init__(self, host="localhost", user="root", passwd="admin"):
        self.database_name = DATABASE_NAME
        self.host = host
        self.user = user
        self.passwd = passwd
        self.connection = None
        self.cursor = None
        self.create_database()

    def connect(self):
        try:
            conn = ms.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database_name)
            if conn.is_connected():
                return conn
        except ms.Error as e:
            print(f"Error: {e}")

    def open_connection(self):
        if not self.connection or not self.connection.is_connected():
            self.connection = self.connect()

        self.cursor = self.connection.cursor(buffered=True)

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection and self.connection.is_connected():
            # self.connection.commit()  # Commit any pending changes
            self.connection.close()

    def check_database_existence(self):
        self.open_connection()
        try:
            self.cursor.execute(f"SHOW DATABASES LIKE '{self.database_name}'")
            result = self.cursor.fetchone()
            return result is not None
        except ms.Error as e:
            print(f"Error: {e}")
        finally:
            self.close_connection()

    def create_database(self):
        self.open_connection()
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")
        except ms.Error as e:
            print(f"Error: {e}")
        finally:
            self.close_connection()

    def table_exists(self, table_name):
        self.open_connection()
        try:
            self.cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = self.cursor.fetchone()
            return result is not None # True if table exists False otherwise
        except ms.Error as e:
            print(f"Error: {e}")
        finally:
            self.close_connection()

    def create_table(self, table_name, **fields):

        try:
            # Constructing the CREATE TABLE query dynamically
            query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, "

            # Adding fields to the query
            for field_name, field_info in fields.items():
                field_type = field_info['type']
                is_primary_key = field_info.get('primary_key', False)
                is_foreign_key = field_info.get('foreign_key', False)
                reference_table = field_info.get('reference_table', None)
                is_unique = field_info.get('unique', False)

                # Adding the field with its type to the query
                query += f"{field_name} {field_type}"

                # Adding primary key constraint
                if is_primary_key:
                    query += " PRIMARY KEY"

                # Adding unique constraint
                if is_unique:
                    query += " UNIQUE"

                # Adding foreign key constraint
                if is_foreign_key and reference_table:
                    query += f" REFERENCES {reference_table}(id)"

                query += ", "

            # Removing the trailing comma and closing the query
            query = query.rstrip(', ') + ")"
            print(f'query: {query}')
            self.open_connection()
            self.cursor.execute(query)
        except ms.Error as e:
            return e
        finally:
            self.close_connection()

    def insert_into_table(self, table_name, **values):
        try:
            # Construct the SQL query for insertion
            print(f"Values: {values}")
            fields = ', '.join(values.keys())
            values_data = ', '.join(
                [self.format_value(v) for v in values.values()])
            print(f"Values data: {values_data}")
            query = f"INSERT INTO {table_name} ({fields}) VALUES ({values_data})"

            # Execute the query with the provided values
            self.open_connection()
            print(f"Adding into table query: {query}")
            self.cursor.execute(query)

            # Commit the changes to the database
            self.connection.commit()

            # Return the ID of the newly inserted record
            print(f"Returning lastrowid: {self.cursor.lastrowid}")
            return True, self.cursor.lastrowid
        except ms.Error as e:
            return False, e
        finally:
            self.close_connection()

    def format_value(self, value):
        if isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, bool):
            return str(value).upper()  # Convert boolean to uppercase string ('True' or 'False')
        else:
            return str(value)

    def search_in_table_by_id(self,table_name,id):
        try:
            print(f"query => SELECT * FROM {table_name} WHERE id = {id}")
            self.open_connection()
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = {id}")
            return self.cursor.fetchone()
        except ms.Error as e:
            return e
        finally:
            self.close_connection()

    def search_in_table_by_fields(self, table_name, **fields): #{'name': 'Ori', 'age': 20}
        try:
            if self.table_exists(table_name):
                print(f"search_in_table_by_fields fields: {fields}")
                conditions = ' AND '.join([f"{k} = '{v}' " for k, v in fields.items()]) # 'name = 'Ori' AND age = 20'
                query = f"SELECT * FROM {table_name} WHERE {conditions}"
                print(f"search_in_table_by_fields query: {query}")

                self.open_connection()
                self.cursor.execute(query)
                result = self.cursor.fetchone()

                if result:
                    print(f"found, result: {result}")
                    return True, result
                else:
                    print(f"No matching rows found.")
                    return False, "No matching rows found."
            else:
                print(f"Table {table_name} does not exist")
                return False, f"Table {table_name} does not exist"
        except ms.Error as e:
            return False, str(e)
        finally:
            self.close_connection()

    def select_all_from_table(self, table_name):
        try:
            if self.table_exists(table_name):
                query = f"SELECT * FROM {table_name}"
                print(f"select_all_from_table query: {query}")
                self.open_connection()
                self.cursor.execute(query)
                headers = [description[0] for description in self.cursor.description]
                rows = self.cursor.fetchall()
                return headers, rows
        except ms.Error as e:
            return False, str(e)
        finally:
            self.close_connection()


if __name__ == "__main__":
    DB = DatabaseConnection()
    a = DB.search_in_table_by_fields("users",username = 'daredevil',password = '123')

    if a:
        print(f"not found,{a[1]}")
    else:
        print("found")