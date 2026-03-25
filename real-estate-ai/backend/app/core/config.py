# from typing import List
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     PROJECT_NAME: str = "NeuraLease"
#     API_V1_STR: str = "/api/v1"
#     SECRET_KEY: str = "neuralease_secret_key_123"
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
#     MONGODB_URL: str
#     DATABASE_NAME: str = "neuralease_db"
    
#     PINECONE_API_KEY: str
#     GEMINI_API_KEY: str
    
#     BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

#     class Config:
#         case_sensitive = True
#         env_file = ".env"

# settings = Settings()
# # import os
# # from pydantic_settings import BaseSettings
# # from pathlib import Path

# # # এটি আপনার backend ফোল্ডারের এক ধাপ পেছনের (real-estate-ai) পাথ বের করবে
# # env_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"

# # class Settings(BaseSettings):
# #     PROJECT_NAME: str = "NeuraLease"
# #     SECRET_KEY: str
# #     MONGODB_URL: str
# #     PINECONE_API_KEY: str
# #     GEMINI_API_KEY: str
# #     API_V1_STR: str = "/api/v1"

# #     class Config:
# #         env_file = str(env_path)
# #         case_sensitive = True

# # settings = Settings()
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NeuraLease"
    API_V1_STR: str = "/api/v1"
    
    # এগুলোকে Optional করার জন্য ডিফল্ট ভ্যালু দেওয়া হলো
    SECRET_KEY: str = "neuralease_secret_key_123" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    MONGODB_URL: str
    DATABASE_NAME: str = "neuralease_db"
    
    # পাইনকোন যেহেতু লাগছে না, তাই খালি স্ট্রিং ডিফল্ট হিসেবে দিলাম
    PINECONE_API_KEY: str = "" 
    GEMINI_API_KEY: str
    
    # লাইভ করার সময় সব অরিজিন এলাউ করা সেফ (আপাতত)
    BACKEND_CORS_ORIGINS: List[str] = ["*"] 

    class Config:
        case_sensitive = True
        env_file = ".env"
        # অতিরিক্ত ভেরিয়েবল থাকলে ইগনোর করবে
        extra = "ignore" 

settings = Settings()