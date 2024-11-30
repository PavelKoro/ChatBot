from melon_search import poisk
from openai import OpenAI

def process_query(user_id, query: str) -> str:
    print(f"USER_ID: {user_id}")
    promt = poisk(user_id, query, name_db = "file_data", collec = "txt_2", size_vec = 1024)
    return promt