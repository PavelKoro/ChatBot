import psycopg2
from TextRankBm25_impl import TextRankBm25  # Убедитесь, что этот импорт корректен

def process_data(name_db, query):
    conn = psycopg2.connect(
        host='localhost', 
        dbname='postgres', 
        user='postgres', 
        password='qwerty', 
        port=5432
    )
    cur = conn.cursor()

    # Чтение данных из таблицы
    cur.execute(f"SELECT id, source, content FROM {name_db}")
    rows = cur.fetchall()

    data_postgres = {
        'id': [row[0] for row in rows],
        'source': [row[1] for row in rows],
        'content': [row[2] for row in rows]
    }
    # print(data_postgres)

    # Обработка данных с использованием TextRankBm25
    bm25 = TextRankBm25(data_postgres)
    scores = bm25.bm25_search(query)
    postgres_res_id = bm25.choice_not_zero(scores)
    bm25.bubble_sorting(postgres_res_id)
    # bm25.res_output(postgres_res_id)

    cur.close()
    conn.close()
    print("[INFO]: Data processed successfully.")
    return postgres_res_id

# if __name__ == "__main__":
#     name_db = 'file_data'
#     query = 'Кто был президентом США в середине 20-го века?'  # Пример запроса
#     postgres = process_data(name_db, query)
#     print(postgres['id'])
