from google import genai
import os

# আপনার এপিআই কী সরাসরি এখানে বসিয়ে দিন টেস্ট করার জন্য
API_KEY = "AIzaSyDeRqACHyiGTy6EfEMdyVDy9l5Wd_M7TtQ"
from google import genai

client = genai.Client(api_key="AIzaSyDeRqACHyiGTy6EfEMdyVDy9l5Wd_M7TtQ")

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
)
print(response.text)