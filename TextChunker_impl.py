from langchain.text_splitter import RecursiveCharacterTextSplitter  # Для разбивки текста на чанки
import re

class TextChunker:
    def __init__(self, chunk_size: int = 200, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def clean_text(self,text):
        cleaned_text = re.sub(r'[\r\n]+', ' ', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text

    def split_text(self,text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        text_res = self.clean_text(text)
        chunks = text_splitter.split_text(text_res)
        return chunks
    
    def сhunk_format(self, data_row):
        size = len(data_row['source'])
        sources = []
        contents = []
        for i in range(size):
            chunks = self.split_text(data_row['content'][i])
            for chunk in chunks:
                contents.append(chunk)
                sources.append(data_row['source'][i])

        data = {
            'id': [i for i in range(1, len(contents)+1)],
            'source': sources,
            'content': contents
        }
        return data