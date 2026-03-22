from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

class LeaseAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=settings.GEMINI_API_KEY)

    async def analyze_lease(self, contract_text: str):
        prompt = f"Analyze the following lease for financial risks and hidden clauses: {contract_text}"
        response = await self.llm.ainvoke(prompt)
        return response.content