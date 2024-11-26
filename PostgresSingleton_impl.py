import psycopg2

class PostgresSingleton:
    _instance = None
    _connection = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PostgresSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize_connection()
        return cls._instance

    def _initialize_connection(self):
        self._connection = psycopg2.connect(host = 'localhost', dbname = 'postgres', user = 'postgres', password='qwerty', port=5432)
        print("[INFO]: Connected to PostgreSQL")

    def get_cursor(self):
        if self._connection:
            return self._connection.cursor()
        else:
            raise Exception("Connection not established")

    def commit(self):
        if self._connection:
            self._connection.commit()

    
    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            print("[INFO]: PostgreSQL connection closed")

    def execute_query(self, query, data=None):
        cur = self.get_cursor()
        try:
            if data:
                cur.executemany(query, data)
            else:
                cur.execute(query)
            self.commit()
        except Exception as e:
            print(f"[ERROR]: Failed to execute query: {e}")
        finally:
            cur.close()

    ## Создание таблицы
    def create_table(self, table_name):
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT PRIMARY KEY,
            source VARCHAR(255),
            content VARCHAR(2048)
        );
        """
        self.execute_query(create_table_query)
        print(f"[INFO]: Table '{table_name}' is ready.")
    
    ## Вставка данных в таблицу
    def insert_data(self, table_name, data, j=0):
        data_postgres = [
            (i+1+j, data['source'][i], data['content'][i])
            for i in range(len(data['id']))
        ]
        query = f"INSERT INTO {table_name} (id, source, content) VALUES (%s, %s, %s)"
        self.execute_query(query, data_postgres)
        print(f"[INFO]: Data inserted into table '{table_name}'.")

    ## Чтение дынных таблицы
    def fetch_data(self, table_name):
        query = f"SELECT id, source, content FROM {table_name}"
        cur = self.get_cursor()
        try:
            cur.execute(query)
            rows = cur.fetchall()
            data = {
                'id': [row[0] for row in rows],
                'source': [row[1] for row in rows],
                'content': [row[2] for row in rows]
            }
            return data
        except Exception as e:
            print(f"[ERROR]: Failed to fetch data: {e}")
            return None
        finally:
            cur.close()
    
    ## Удаление таблицы
    def drop_table(self, table_name):
        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
        self.execute_query(drop_table_query)
        print(f"[INFO]: Table '{table_name}' has been dropped.")

# # Usage example
# name_db = 'file_data'
# postgres = PostgresSingleton()

# # Create table if not exists
# postgres.create_table(name_db)

# # Insert data
# data_postgres = [
#     (7, 'source1', 'content1'),
# ]

# postgres.insert_data(name_db, data_postgres)

# # Fetch data
# fetched_data = postgres.fetch_data(name_db)
# if fetched_data:
#     print(fetched_data)

# # Drop table
# # postgres.drop_table(name_db)

# postgres.close()