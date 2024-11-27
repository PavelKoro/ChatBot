from DownloadDataBD import upload_database
from melon_search import poisk

file_path = 'DataTXT/1.txt'
name_db = 'file_data'
size_vec = 1024
collec = 'txt_2'

upload_database(file_path, name_db, collec, size_vec)

def process_query(query: str) -> str:
    promt = poisk(query, name_db, collec)
    return promt