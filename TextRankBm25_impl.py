from rank_bm25 import BM25Okapi

class TextRankBm25:
    def __init__(self, data):
        self.data = data
        self.tokenized_corpus = [doc.split(' ') for doc in data['content']]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def bm25_search(self, query):
        tokenized_query = query.split(' ')
        scores = self.bm25.get_scores(tokenized_query)
        return scores

    def choice_not_zero(self, scores):
        results = {'id': [], 'evaluation': []}

        for i, score in enumerate(scores):
            if score > 0:
                results['id'].append(i + 1)
                results['evaluation'].append(score)

        return results

    def bubble_sorting(self, results):
        n = len(results['id'])
        for i in range(n):
            for j in range(0, n-i-1):
                if results['evaluation'][j] < results['evaluation'][j+1]:
                    results['evaluation'][j], results['evaluation'][j+1] = results['evaluation'][j+1], results['evaluation'][j]
                    results['id'][j], results['id'][j+1] = results['id'][j+1], results['id'][j]

    def res_output(self, results):
        for i in range(len(results['id'])):
            print(f"{results['id'][i]}: {results['evaluation'][i]}")
            print(f"{self.data['content'][results['id'][i] - 1]}")
            print("------------------------------------------------\n")
