import psycopg2
from FileReader_impl import FileReader
from TextChunker_impl import TextChunker

def populate_table(name_db, file_path):
    document = FileReader(file_path).load_document()
    chunks = TextChunker().split_text(document)
    data = TextChunker().text_chunk(chunks)

    conn = psycopg2.connect(
        host='localhost', 
        dbname='postgres', 
        user='postgres', 
        password='qwerty', 
        port=5432
    )
    cur = conn.cursor()

    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {name_db} (
            id SERIAL PRIMARY KEY,
            source VARCHAR(255),
            content VARCHAR(2048)            
        );
    """)

    cur.execute(f"SELECT id FROM {name_db} ORDER BY id DESC LIMIT 1")
    last_id_record = cur.fetchone()
    
    # Проверка, что запись найдена
    if last_id_record is not None:
        last_id = last_id_record[0]
    else:
        last_id = 0

    data_postgres = [
        (data['source'][i], data['content'][i])
        for i in range(len(data['source']))
    ]

    cur.executemany(f"INSERT INTO {name_db} (source, content) VALUES (%s, %s)", data_postgres)
    conn.commit()

    cur.close()
    conn.close()
    print("[INFO]: Table populated successfully.")
    return last_id


# if __name__ == "__main__":
#     name_db = 'file_data'
#     file_path = '1.txt' 
#     populate_table(name_db, file_path)


# cur.execute("DROP TABLE file_data;")