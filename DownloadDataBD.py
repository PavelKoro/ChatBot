from MilvusSingleton_impl import MilvusSingleton
from postgres_table import populate_table
from fetch_postgress import fetch_data_from_postgres
from del_postgres import delete_table

def upload_database(file_path, name_db, collec, size_vec):
    delete_table(name_db)
    populate_table(name_db, file_path)
    data = fetch_data_from_postgres(name_db)
    milvus = MilvusSingleton()
    milvus.setup_database(name_db)
    milvus.create_collection(collec, size_vec)
    milvus.insert_data(collec, data)