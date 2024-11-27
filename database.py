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
                nickname VARCHAR(50) NOT NULL,
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

def insert_user(person):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        insert_query = "INSERT INTO users (nickname, email, password) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (person.nickname, person.email, person.password))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def authenticate_user(nickname, password):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE nickname = %s AND password = %s"
        cursor.execute(query, (nickname, password))
        return cursor.fetchone()
    except psycopg2.Error as e:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
