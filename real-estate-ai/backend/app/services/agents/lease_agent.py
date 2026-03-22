# from langchain_google_genai import ChatGoogleGenerativeAI
# from app.core.config import settings

# class LeaseAgent:
#     def __init__(self):
#         self.llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=settings.GEMINI_API_KEY)

#     async def analyze_lease(self, contract_text: str):
#         prompt = f"Analyze the following lease for financial risks and hidden clauses: {contract_text}"
#         response = await self.llm.ainvoke(prompt)
#         return response.content
# from google import genai
# from app.core.config import settings
# from fastapi import HTTPException

# class LeaseAgent:
#     def __init__(self):
#         # নতুন SDK ব্যবহার করে ক্লায়েন্ট সেটআপ
#         self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

#     async def analyze_lease_text(self, text: str) -> str:
#         try:
#             prompt = f"""
#             You are an expert Real Estate Lawyer. Analyze the following lease agreement text:
            
#             {text}
            
#             Please provide:
#             1. Monthly Rent and Security Deposit.
#             2. Lease Duration (Start and End dates).
#             3. Hidden Risks or unusual clauses (e.g., unexpected fees).
#             4. Maintenance responsibilities.
            
#             Format the response in structured Markdown.
#             """
            
#             # মডেলের নাম 'gemini-2.0-flash' বা 'gemini-1.5-flash' ব্যবহার করুন
#             response = self.client.models.generate_content(
#                 model='gemini-2.0-flash', 
#                 contents=prompt
#             )
#             return response.text
#         except Exception as e:
#             print(f"Gemini Analysis Error: {e}")
#             raise HTTPException(status_code=500, detail="AI Analysis failed")
from google import genai
from app.core.config import settings
from fastapi import HTTPException

class LeaseAgent:
    def __init__(self):
        # API Key ব্যবহার করে ক্লায়েন্ট সেটআপ
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def analyze_lease_text(self, text: str) -> str:
        if not text or len(text.strip()) < 10:
            raise HTTPException(status_code=400, detail="No readable text found in PDF")

        try:
            prompt = f"""
            You are an expert Real Estate Lawyer. Analyze the following lease agreement text:
            
            {text}
            
            Please provide a structured report in Markdown:
            1. **Financial Summary**: Monthly Rent and Security Deposit.
            2. **Timeline**: Lease Duration (Start and End dates).
            3. **Risk Analysis**: Hidden risks or unusual clauses (e.g., unexpected fees, restrictive terms).
            4. **Maintenance**: Who is responsible for what repairs?
            5. **Verdict**: A brief summary of whether the lease is tenant-friendly or not.
            """
            
            # মডেলের নাম 'gemini-2.0-flash' বর্তমানে ফ্রি টিয়ারে সবচেয়ে ভালো কাজ করে
            response = self.client.models.generate_content(
                model='gemini-2.0-flash', 
                contents=prompt
            )
            
            if not response.text:
                raise ValueError("AI returned an empty response")
                
            return response.text

        except Exception as e:
            # টার্মিনালে আসল এরর প্রিন্ট হবে যাতে আপনি ডিবাগ করতে পারেন
            print(f"--- Gemini Analysis Error Details ---")
            print(f"Error Type: {type(e).__name__}")
            print(f"Message: {str(e)}")
            print(f"-------------------------------------")
            raise HTTPException(status_code=500, detail=f"AI Analysis failed: {str(e)}")

# from google import genai
# from app.core.config import settings
# from fastapi import HTTPException

# class LeaseAgent:
#     def __init__(self):
#         self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

#     async def analyze_lease_text(self, text: str) -> str:
#         # কোটা এরর এড়াতে সাময়িকভাবে এই ডামি রিপোর্টটি রিটার্ন করবে
#         mock_report = """
#         # 📄 NeuraLease AI - Mock Analysis Report
        
#         ### 1. Financial Summary
#         * **Monthly Rent**: R Amount (To be filled) [cite: 37]
#         * **Security Deposit**: R Amount (To be filled) [cite: 72]
        
#         ### 2. Timeline
#         * **Lease Start**: Day of Month, 20 Year [cite: 60, 61, 62]
#         * **Lease End**: Day of Month, 20 Year [cite: 63, 64, 65]
        
#         ### 3. Risk Analysis
#         * **Cancellation Penalty**: High risk identified. If cancelled before 50% of the period, a penalty of 3x monthly rent may apply[cite: 222].
#         * **Late Payment**: Surcharge of R250.00 for payments after the 7th day[cite: 42].
        
#         ### 4. Maintenance
#         * **Landlord**: Exterior, roof, gutters, and installations like geysers[cite: 112, 113].
#         * **Tenant**: Interior maintenance, lightbulbs, and professional carpet cleaning before vacating[cite: 122, 130, 169].
        
#         ### 5. Verdict
#         This is a standard residential lease with specific penalty clauses for early termination.
#         """
        
#         # আসল এপিআই কল আপাতত বন্ধ রাখা হলো কোটা সমস্যার কারণে
#         return mock_report