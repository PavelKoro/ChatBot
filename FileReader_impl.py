from langchain_community.document_loaders import TextLoader  # Для чтения файла

class FileReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_document(self):
        loader = TextLoader(self.file_path)
        document = loader.load()
        return document