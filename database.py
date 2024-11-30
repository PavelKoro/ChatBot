import psycopg2
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'qwerty',
    'port': 5432
}

def create_users_table():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        """)
        conn.commit()
        print("Таблица 'users' успешно создана.")
    except psycopg2.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_user(email: str, password: str):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        insert_query = "INSERT INTO users (email, password) VALUES (%s, %s) RETURNING id"
        cursor.execute(insert_query, (email, password))
        id_user = cursor.fetchone()
        conn.commit()
        return id_user[0]
    except psycopg2.Error as e:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def authenticate_user(email, password):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT id FROM users WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        id_user = cursor.fetchone()
        return id_user[0]
    except psycopg2.Error as e:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_user_id_name(nickname):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT id FROM users WHERE nickname = %s"
        cursor.execute(query, (nickname))
        id_user = cursor.fetchone()
        return id_user[0]
    except psycopg2.Error as e:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()