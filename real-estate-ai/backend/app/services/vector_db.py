# import chromadb
# from chromadb.utils import embedding_functions
# from app.core.config import settings

# class VectorManager:
#     def __init__(self):
#         self.client = chromadb.PersistentClient(path="./chroma_db")
#         self.embedding_fn = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
#             api_key=settings.GEMINI_API_KEY,
#             model_name="models/text-embedding-004",
#             api_version="v1"
#         )
#         self.collection = self.client.get_or_create_collection(
#             name="lease_documents",
#             embedding_function=self.embedding_fn
#         )

#     def add_document(self, text_chunks: list, doc_id: str):
#         self.collection.add(
#             documents=text_chunks,
#             ids=[f"{doc_id}_{i}" for i in range(len(text_chunks))],
#             metadatas=[{"source": doc_id}] * len(text_chunks)
#         )

#     def query(self, query_text: str, n_results=3):
#         return self.collection.query(query_texts=[query_text], n_results=n_results)
# import numpy as np
# from app.core.config import settings
# import google.generativeai as genai

# class VectorManager:
#     def __init__(self):
#         genai.configure(api_key=settings.GEMINI_API_KEY)
#         self.documents = []
#         self.embeddings = []

#     def add_document(self, text_chunks: list, doc_id: str):
#         self.documents = text_chunks
        
#         response = genai.embed_content(
#             model="models/text-embedding-004",
#             content=text_chunks,
#             task_type="retrieval_document"
#         )
#         self.embeddings = np.array(response['embedding'])

#     def query(self, query_text: str, n_results=3):
#         # কুয়েরি টেক্সটকেও এমবেডিং করতে হবে
#         query_embedding = np.array(genai.embed_content(
#             model="models/text-embedding-004",
#             content=query_text,
#             task_type="retrieval_query"
#         )['embedding'])

#         # কোসাইন সিমিলারিটি দিয়ে সবচেয়ে কাছের চাঙ্কগুলো খুঁজে বের করা (সলিড RAG লজিক)
#         similarities = np.dot(self.embeddings, query_embedding)
#         top_indices = np.argsort(similarities)[-n_results:][::-1]
        
#         results = [self.documents[i] for i in top_indices]
#         return {"documents": [results]}
import numpy as np
from app.core.config import settings
import google.generativeai as genai
# এই ইমপোর্টটি v1 নিশ্চিত করার জন্য খুব জরুরি
from google.api_core import client_options

class VectorManager:
    def __init__(self):
        # সনু ভাই, এখানে আমরা সরাসরি v1 এন্ডপয়েন্ট সেট করে দিচ্ছি
        options = client_options.ClientOptions(api_endpoint="generativelanguage.googleapis.com/v1")
        genai.configure(api_key=settings.GEMINI_API_KEY, client_options=options)
        self.documents = []
        self.embeddings = []

    def add_document(self, text_chunks: list, doc_id: str):
        self.documents = text_chunks
        
        # সনু ভাই, এখন এই কলটি v1 এন্ডপয়েন্ট দিয়ে যাবে
        response = genai.embed_content(
            model="models/text-embedding-004",
            content=text_chunks,
            task_type="retrieval_document"
        )
        self.embeddings = np.array(response['embedding'])

    def query(self, query_text: str, n_results=3):
        query_embedding = np.array(genai.embed_content(
            model="models/text-embedding-004",
            content=query_text,
            task_type="retrieval_query"
        )['embedding'])

        # কোসাইন সিমিলারিটি ক্যালকুলেশন
        similarities = np.dot(self.embeddings, query_embedding)
        top_indices = np.argsort(similarities)[-n_results:][::-1]
        
        results = [self.documents[i] for i in top_indices]
        return {"documents": [results]}