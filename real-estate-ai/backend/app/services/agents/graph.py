# from typing import TypedDict, List
# from langgraph.graph import StateGraph, END

# class AgentState(TypedDict):
#     raw_text: str
#     retrieved_context: List[str]
#     analysis: str
#     risk_score: int

# def retrieve_node(state: AgentState):
#     # এখানে VectorManager থেকে প্রাসঙ্গিক তথ্য খুঁজে বের করবে (RAG)
#     return {"retrieved_context": ["Context from Vector DB..."]}

# def analysis_node(state: AgentState):
#     # এখানে জেমিনি বা ক্লড এনালাইসিস করবে
#     return {"analysis": "Professional Lease Report based on RAG"}

# # গ্রাফ বিল্ড করা
# workflow = StateGraph(AgentState)
# workflow.add_node("retrieve", retrieve_node)
# workflow.add_node("analyze", analysis_node)
# workflow.set_entry_point("retrieve")
# workflow.add_edge("retrieve", "analyze")
# workflow.add_edge("analyze", END)
# app_graph = workflow.compile()
# from typing import TypedDict, List
# from langgraph.graph import StateGraph, END
# import google.generativeai as genai
# from app.core.config import settings

# # ১. স্টেট ডেফিনিশন
# class AgentState(TypedDict):
#     raw_text: str
#     retrieved_context: List[str]
#     analysis: str
#     risk_score: int

# # ২. রিট্রিভ নোড (এখানে আমরা শুধু ডাটা পাস করছি)
# def retrieve_node(state: AgentState):
#     # আপনার ভেক্টর ডিবি থেকে আসা কনটেক্সট এখানে থাকবে
#     return {"retrieved_context": state.get("retrieved_context", [])}

# # ৩. এনালাইসিস নোড (আসল জাদুর কাজ এখানেই)
# def analysis_node(state: AgentState):
#     print("--- 🤖 Step 2: Running ACTUAL Gemini Analysis ---")
    
#     # এপিআই কী সেটআপ
#     genai.configure(api_key=settings.GEMINI_API_KEY)
#     model = genai.GenerativeModel('gemini-1.5-flash')
    
#     # জেমিনিকে দেওয়ার জন্য আসল প্রম্পট (RUET Special)
#     prompt = f"""
#     You are an expert Real Estate Lawyer. Based on the lease agreement text provided below, 
#     generate a highly detailed report including:
    
#     1. **Key Financials**: Exact Rent, Security Deposit, and Due Dates.
#     2. **Tenancy Terms**: Lease Start/End dates and Renewal conditions.
#     3. **Legal Clauses**: Notice Period, Late Fees, and Maintenance rules.
#     4. **Risk Assessment**: Any hidden or unfair clauses for the tenant.

#     USE THIS CONTEXT FROM PDF:
#     {state['raw_text'][:8000]}  # আপনার পিডিএফ-এর টেক্সট এখানে পাঠানো হচ্ছে
#     """
    
#     try:
#         response = model.generate_content(prompt)
#         report = response.text
#         return {"analysis": report}
#     except Exception as e:
#         print(f"❌ Gemini Error: {str(e)}")
#         return {"analysis": "Error generating detailed report. Please check API Key."}

# # ৪. গ্রাফ বিল্ড করা
# workflow = StateGraph(AgentState)
# workflow.add_node("retrieve", retrieve_node)
# workflow.add_node("analyze", analysis_node)

# workflow.set_entry_point("retrieve")
# workflow.add_edge("retrieve", "analyze")
# workflow.add_edge("analyze", END)

# app_graph = workflow.compile()

import os
from typing import TypedDict, List
import httpx
from dotenv import load_dotenv
from app.core.config import settings
from langgraph.graph import StateGraph, END
load_dotenv()

# --- ১. এটিই সেই AgentState যা ডিফাইন করা ছিল না ---
class AgentState(TypedDict):
    raw_text: str
    retrieved_context: List[str]
    analysis: str
    risk_score: int

# --- ২. এবার আপনার এনালাইসিস নোড (যা সরাসরি API কল করবে) ---
from google import genai
from app.core.config import settings

def analysis_node(state: AgentState):
    print("--- 🤖 Step 2: Running Gemini 3 Flash Analysis ---")
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file!")
        return {"analysis": "API Key configuration error."}

    # ক্লায়েন্ট সেটআপ
    client = genai.Client(api_key=api_key)
    # আপনার সেই কাজ করা এপিআই কী এবং ক্লায়েন্ট
    #client = genai.Client(api_key="AIzaSyDeRqACHyiGTy6EfEMdyVDy9l5Wd_M7TtQ")
    
    # জেমিনিকে দেওয়ার জন্য লিজ এগ্রিমেন্টের টেক্সটসহ প্রম্পট
    prompt_text = f"""
    Analyze this lease agreement and provide a DETAILED structured report:
    1. Rent Amount & Due Date
    2. Security Deposit amount and conditions
    3. Notice Period and Termination clauses
    4. Maintenance & Repair responsibilities
    5. Key Legal Risks for the tenant
    
    CONTEXT FROM PDF:
    {state.get('raw_text', '')[:15000]}
    """

    try:
        # আপনি যে মডেলটি টেস্ট করে সাকসেস হয়েছেন সেটিই ব্যবহার করছি
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=prompt_text
        )
        
        if response and response.text:
            print("✅ Analysis Successful! Report generated.")
            return {"analysis": response.text}
        else:
            return {"analysis": "Error: Gemini returned empty content."}
            
    except Exception as e:
        print(f"❌ Gemini Error: {str(e)}")
        return {"analysis": f"Critical Error in Analysis: {str(e)}"}

# --- ৩. বাকি নোড এবং গ্রাফ সেটআপ ---
def retrieve_node(state: AgentState):
    return {"retrieved_context": state.get("retrieved_context", [])}

workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("analyze", analysis_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "analyze")
workflow.add_edge("analyze", END)

app_graph = workflow.compile()