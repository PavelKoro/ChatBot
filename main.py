from FileReader_impl import FileReader
from TextChunker_impl import TextChunker
from TextEncoder_impl import TextEmbedding
from TextRankBm25_impl import TextRankBm25
from TextCrossEncoder_impl import TextCrossEncoder
from TextPromt_impl import TextPrompt
from MilvusSingleton_impl import MilvusSingleton
from PostgresSingleton_impl import PostgresSingleton
from openai import OpenAI

query = 'Кто был президентом США в середине 20-го века?'
document = FileReader('1.txt').load_document()
chunks = TextChunker().split_text(document)
data = TextEmbedding().vectorize_text(chunks)

postgres = PostgresSingleton()
name_db = 'file_data_19'
postgres.create_table(name_db)
postgres.insert_data(name_db, data)
data_postgres = postgres.fetch_data(name_db)
postgres.close()

bm25 = TextRankBm25(data_postgres)
scores = bm25.bm25_search(query)
postgres_res_id = bm25.choice_not_zero(scores)
bm25.bubble_sorting(postgres_res_id)

milvus = MilvusSingleton()
baza = 'TEST_777'
size_vec = 1024
col_data = 'txt_2'
milvus.setup_database(baza)
milvus.create_collection(col_data, size_vec)
milvus.insert_data(col_data, data)
milv_id = milvus.search_milvus(query, col_data, limit=10)

data_milv = milv_id['id']
data_postgres = postgres_res_id['id']
data_id = TextPrompt().checking_match(data_milv, data_postgres)
cross_encoder = TextCrossEncoder().calculate_relevance(query, data, data_id)
promt = TextPrompt().generate_prompt(query, cross_encoder, data)

print(promt)