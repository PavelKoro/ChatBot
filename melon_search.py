from data_postgres import process_data
from fetch_postgress import fetch_data_from_postgres
from MilvusSingleton_impl import MilvusSingleton
from TextPromt_impl import TextPrompt
from TextCrossEncoder_impl import TextCrossEncoder

def poisk(query, name_db, collec):
    postgres_res_id = process_data(name_db, query)
    print("[INFO]: Search results postgres:", postgres_res_id['id'])
    data = fetch_data_from_postgres(name_db)

    milvus = MilvusSingleton()
    milv_id = milvus.search_milvus(query, collec, limit=10)
    while not milv_id['id']:
        print("[INFO]: Milvus no results found, retrying...")
        milv_id = milvus.search_milvus(query, collec, limit=10)
    print("[INFO]: Search results milvus:", milv_id['id'])

    data_milv = milv_id['id']
    data_postgres = postgres_res_id['id']
    
    data_id = TextPrompt().checking_match(data_milv, data_postgres)
    print("[INFO]: Relevant chunks found:", data_id)

    cross_encoder = TextCrossEncoder().calculate_relevance(query, data, data_id)
    print("[INFO]: Sorted relevant chunks:", cross_encoder)

    promt = TextPrompt().generate_prompt(query, cross_encoder, data)
    print("[INFO]: Promt successfully:\n", promt)
    return promt