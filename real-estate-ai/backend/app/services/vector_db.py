import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings

class VectorManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_fn = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
            api_key=settings.GEMINI_API_KEY,
            model_name="models/text-embedding-004"
        )
        self.collection = self.client.get_or_create_collection(
            name="lease_documents",
            embedding_function=self.embedding_fn
        )

    def add_document(self, text_chunks: list, doc_id: str):
        self.collection.add(
            documents=text_chunks,
            ids=[f"{doc_id}_{i}" for i in range(len(text_chunks))],
            metadatas=[{"source": doc_id}] * len(text_chunks)
        )

    def query(self, query_text: str, n_results=3):
        return self.collection.query(query_texts=[query_text], n_results=n_results)