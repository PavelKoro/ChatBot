import psycopg2
import difflib

# Параметры подключения к базе данных
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'qwerty',
    'port': 5432
}

def create_file_list_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files_user (
                id SERIAL PRIMARY KEY,
                user_id  INTEGER NOT NULL,      
                filename TEXT NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        ''')
        conn.commit()
        cursor.close()
        print(f"[INFO]: Table files_user create successfully.")
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    finally:
        if conn:
            conn.close()

def insert_file_list(user_id, filename, content):
    print(f"insert_file_list {user_id}")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        if user_id == 0:
            return 400, "Нужно зарегистрироваться"

        print(f"USER_ID: {user_id}")

        # Проверка, существует ли такой файл в базе данных
        cursor.execute('SELECT COUNT(*) FROM files_user WHERE filename = %s AND user_id = %s', (filename, user_id))
        count = cursor.fetchone()[0]

        if count > 0:
            return 400, f"Файл '{filename}' с таким названием уже существует."
        # Проверка на подобие содержимого
        cursor.execute('SELECT filename, content FROM files_user WHERE user_id = %s', (user_id,))
        existing_files = cursor.fetchall()

        for existing_filename, existing_content in existing_files:
            similarity = difflib.SequenceMatcher(None, content, existing_content).ratio()
            if similarity >= 0.95:  # 95% совпадение
                return 401, f"Файл '{existing_filename}' с таким содержанием уже существует"

        # После проверки загружаем файл в базу данных
        cursor.execute('INSERT INTO files_user (filename, content, user_id) VALUES (%s, %s, %s)', (filename, content, user_id))
        conn.commit()

        return 200, f"Файл '{filename}' успешно загружен."
    except psycopg2.Error as e:
        return 500, f"Ошибка при работе с базой данных: {e}"
    finally:
        if conn:
            cursor.close()
            conn.close()

def delete_file_list_db(user_id, filename):
    try:
        if user_id == 0:
            return None, f"Ошибка при отображении файлов из бд. Необходимо зарегистрироваться!"
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM files_user WHERE user_id = %s AND filename = %s', (user_id, filename))
        conn.commit()

        if cursor.rowcount == 0:
            return False, f"Файл '{filename}' не найден в базе данных."
        
        return True, f"Файл '{filename}' удален из базы данных."
    except Exception as e:
        return False, f"Ошибка при удалении файла из базы данных: {e}"
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_file_list(user_id):
    print(f"get_file_list {user_id}")
    try:
        if user_id == 0:
            return None, "Ошибка при отображении файлов из бд. Необходимо зарегистрироваться!"
        
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('SELECT filename FROM files_user WHERE user_id = %s', (user_id,))
        files = cursor.fetchall()
        
        return [file[0] for file in files], None
    except Exception as e:
        return None, f"Ошибка при отображении файлов из базы данных: {e}"
    finally:
        if conn:
            cursor.close()
            conn.close()