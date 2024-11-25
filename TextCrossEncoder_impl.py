from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class TextCrossEncoder:
    def __init__(self, model_name='amberoad/bert-multilingual-passage-reranking-msmarco'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()  # Установка модели в режим оценки

    def calculate_relevance(self, query, Data_db, data_id):
        # Data_size = self.Data_Size(query, Data_db, data_id)
        Data_size = {
            'query': [query for _ in range(len(data_id))],
            'content': [Data_db['content'][id-1] for id in data_id],
            'id': data_id
        }
        pairs = self.Data_pairs(Data_size)
        scores = self.analysis(pairs)
        sorted_pairs = self.sorted_res(Data_size, scores)
        return sorted_pairs
    
    # def Data_Size(self, query, Data_db, data_id):

    #     return Data_size

    def Data_pairs(self, data_size):
        pairs = [[data_size['query'][i], data_size['content'][i]] for i in range(len(data_size['id']))]
        return pairs
    
    def analysis(self, pairs):
        with torch.no_grad():
            inputs = self.tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
            scores = self.model(**inputs, return_dict=True).logits[:, 0].view(-1).float()
        return scores

    def sorted_res(self, data_size, scores):
        sorted_pairs = [[(i, score.item()), data_size['id'][i]] for i, score in enumerate(scores)]
        n = len(sorted_pairs)
        for i in range(n):
            for j in range(0, n-i-1):
                if sorted_pairs[j][0][1] > sorted_pairs[j+1][0][1]:
                    sorted_pairs[j], sorted_pairs[j+1] = sorted_pairs[j+1], sorted_pairs[j]
        result_id = [pair[1] for pair in sorted_pairs]
        return result_id

# Пример использования
# query = "Ваш запрос"
# data_db = {'content': ["текст документа 1", "текст документа 2", "текст документа 3"]}
# data_id = [1, 2, 3]
# cross_encoder = TextCrossEncoder()
# sorted_pairs = cross_encoder.calculate_relevance(query, data_db, data_id)
# result_id = cross_encoder.sort_results(sorted_pairs)
# print(result_id)
