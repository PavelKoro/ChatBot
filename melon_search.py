from TextCrossEncoder_impl import TextCrossEncoder
from MilvusSingleton_impl import MilvusSingleton
from TextRankBm25_impl import TextRankBm25  
from TextChunker_impl import TextChunker
from TextPromt_impl import TextPrompt

import psycopg2

def poisk(user_id, query, name_db = "file_data", collec = "txt_2", size_vec = 1024):
    data_row = get_data(user_id)
    data_postg = TextChunker().сhunk_format(data_row)
    postgres_res_id = parse_data(data_postg, query)
    print("[INFO]: Search results postgres:", postgres_res_id['id'])

    milvus = MilvusSingleton()
    milvus.setup_database(name_db)
    milvus.create_collection(collec, size_vec)
    milvus.insert_data(collec, data_postg)
    milv_id = milvus.search_milvus(query, collec, limit=15)
    while not milv_id['id']:
        print("[INFO]: Milvus no results found, retrying...")
        milv_id = milvus.search_milvus(query, collec, limit=10)
    print("[INFO]: Search results milvus:", milv_id['id'])

    data_milv = milv_id['id']
    data_postgres = postgres_res_id['id']
    
    data_id = TextPrompt().checking_match(data_milv, data_postgres)
    print("[INFO]: Relevant chunks found:", data_id)

    cross_encoder = TextCrossEncoder().calculate_relevance(query, data_postg, data_id)
    if len(cross_encoder) > 25:
        cross_encoder_new = cross_encoder[:25]
        print("[INFO]: Sorted relevant chunks:", cross_encoder_new)
    else:
        cross_encoder_new = cross_encoder[:]
        print("[INFO]: Sorted relevant chunks:", cross_encoder_new)

    promt = TextPrompt().generate_prompt(query, cross_encoder_new, data_postg)
    print("[INFO]: Promt successfully:\n", promt)
    return promt

def get_data(user_id):
    conn = psycopg2.connect(
        host='localhost', 
        dbname='postgres', 
        user='postgres', 
        password='qwerty', 
        port=5432
    )
    cur = conn.cursor()

    # Чтение данных из таблицы с фильтрацией по user_id
    cur.execute(f"SELECT id, filename, content FROM files_user WHERE user_id = %s", (user_id,))
    rows = cur.fetchall()

    data_postgres = {
        'source': [row[1] for row in rows],
        'content': [row[2] for row in rows]
    }

    cur.close()
    conn.close()
    print("[INFO]: Data processed successfully.")
    return data_postgres


def parse_data(data_postgres, query):
    # Обработка данных с использованием TextRankBm25
    bm25 = TextRankBm25(data_postgres)
    scores = bm25.bm25_search(query)
    postgres_res_id = bm25.choice_not_zero(scores)
    bm25.bubble_sorting(postgres_res_id)
    # bm25.res_output(postgres_res_id)
    return postgres_res_id