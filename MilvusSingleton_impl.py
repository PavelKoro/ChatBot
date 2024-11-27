from pymilvus import connections, db, utility, FieldSchema, DataType, Collection, CollectionSchema
from TextEncoder_impl import TextEmbedding
import json

class MilvusSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MilvusSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize_connection()
            cls._instance.model = TextEmbedding().model_emb()
        return cls._instance

    def _initialize_connection(self):
        try:
            connections.connect(alias="default", host="localhost", port="19530")
            print("[INFO]: Connected to Milvus")
        except Exception as e:
            print(f"[ERROR]: Failed to connect to Milvus: {e}")
            raise e
            
############################################################## Подключение к БД
    ## Настраивает базу данных с указанным именем
    def setup_database(self, db_name):
        existing_databases = db.list_database()
        if db_name not in existing_databases:
            db.create_database(db_name)
        db.using_database(db_name)
        print(f"[INFO]: Using database '{db_name}'")

############################################################## Насчтройка схемы   
    ## Создадим схему коллекции
    def create_schema(self, size_vec):
        id_field = FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=False)
        source_field = FieldSchema(name='source', dtype=DataType.VARCHAR, max_length=255, is_primary=False)
        embedding_field = FieldSchema(name='embeddings', dtype=DataType.FLOAT_VECTOR, dim=size_vec)
        content_field = FieldSchema(name='content', dtype=DataType.VARCHAR, max_length=2048)

        schema = CollectionSchema(fields=[id_field, source_field, embedding_field, content_field])
        return schema
    
    ## Создадим коллекцию в БД
    def create_collection(self, collection_name, size_vec):
        schema = self.create_schema(size_vec)
        self.delete_collection(collection_name)
        collection = Collection(name=collection_name, schema=schema)
        print(f"[INFO]: Create collection '{collection_name}'")
        self.create_index_load(collection_name)

    ## Удаление коллекции
    def delete_collection(self, collection_name):
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
            print(f"[INFO]: Collection '{collection_name}' existed and was deleted.")
        else:
            print(f"[INFO]: Collection '{collection_name}' does not exist.")

    ## Получение коллекции по имени
    def get_collection(self, collection_name):
        return Collection(name=collection_name)
    
############################################################## Настройка индекса поиска и загрузка данных
    ## Прописываем нужные параметры индекса
    def create_index_params(self):
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "COSINE",
            "params": {
                "nlist": 5
            }
        }
        return index_params
    
    ## Загружаем наш индекс поиска в коллекцию
    def create_index_load(self, collection_name):
        collection = self.get_collection(collection_name)
        index_params = self.create_index_params()
        collection.create_index(field_name="embeddings", index_params=index_params)
        collection.load()
        print(f"[INFO]: Create index in '{collection_name}'")

    ## Вставка данных в коллекцию
    def insert_data(self, collection_name, data): 
        data_milv = {
            'id': data['id'],
            'source': data['source'],
            'emb': [self.model.encode(data['content'][i]) for i in range(len(data['content']))],
            'content': data['content']
        }

        collection = self.get_collection(collection_name)
        collection.insert([data_milv['id'], data_milv['source'], data_milv['emb'], data_milv['content']])
        print(f"[INFO]: Inserted data into {collection_name}")

############################################################## Поиск по коллекции
    ## Поиск данных в коллекции
    def search_milvus(self, query, collection_name, limit=10):
        query_embedding = self.model.encode(query)
        search_params = self.create_index_params()
        collection = self.get_collection(collection_name)

        results = collection.search(
            data = [query_embedding],
            anns_field = 'embeddings',
            param = search_params,
            limit = limit,
            output_fields = ['source', 'content']
        )
        Data_results = self.filter_results(results)
        return Data_results
    
    ## Обработка результата
    def filter_results(self, results):
        data = {}
        ids = []
        distances = []
        sources = []
        contents = []

        for result in results[0]:
            id = result.id
            distance = result.distance
            source = result.entity.get('source')
            content = result.entity.get('content')

            ids.append(id)
            distances.append(distance)
            sources.append(source)
            contents.append(content)
        
        data['id'] = ids
        data['distance'] = distances
        data['source'] = sources
        data['content'] = contents

        return data