import psycopg2

def fetch_data_from_postgres(name_db):
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(
            host='localhost', 
            dbname='postgres', 
            user='postgres', 
            password='qwerty', 
            port=5432
        )
        cur = conn.cursor()

        # Запрос для получения данных из таблицы
        query = f"SELECT id, source, content FROM {name_db}"
        cur.execute(query)
        rows = cur.fetchall()

        cur.execute(f"SELECT id FROM {name_db} ORDER BY id DESC LIMIT 1")
        last_id_record = cur.fetchone()
        last_id = last_id_record[0] if last_id_record else 0

        # Формирование словаря с данными
        data = {
            'id': [row[0] for row in rows],
            'source': [row[1] for row in rows],
            'content': [row[2] for row in rows]
        }
        print("[INFO]: Fetch data from postgres successfully.")
        return data

    except psycopg2.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        return None

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()